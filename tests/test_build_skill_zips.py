#!/usr/bin/env python3
"""build_skill_zips.py için testler (unittest, bağımlılıksız).

Bir claude.ai ZIP'inin bozuk olmasının iki sessiz yolu var: arşivin üst
seviyesi `<skill>/` değilse yükleme skill bulamaz; `${CLAUDE_PLUGIN_ROOT}`
kalırsa ya da işaret ettiği dosya ZIP'e girmemişse skill çalışırken bir
dosyayı okuyamaz. Testler ikisini de gerçek arşivler üzerinden yakalar.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import build_skill_zips as b  # noqa: E402

SKILL_REF = re.compile(r"\$\{SKILL_DIR\}/([A-Za-z0-9_./-]+)")


class TestZips(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = tempfile.mkdtemp()
        cls.zips = {}
        for name in b.skill_names():
            path, _ = b.build_zip(name, cls.out, strict=False)
            cls.zips[name] = path

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.out, ignore_errors=True)

    def test_every_skill_is_built(self):
        self.assertEqual(sorted(self.zips), b.skill_names())
        self.assertEqual(sorted(b.SHORT_DESCRIPTIONS), b.skill_names())

    def test_single_top_level_folder_named_after_the_skill(self):
        for name, path in self.zips.items():
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
            self.assertIn(name + "/SKILL.md", names)
            self.assertEqual({n.split("/", 1)[0] for n in names}, {name}, name)

    def test_front_matter_fits_claude_ai(self):
        for name, path in self.zips.items():
            with zipfile.ZipFile(path) as zf:
                text = zf.read(name + "/SKILL.md").decode("utf-8")
            fm, body = b.split_front_matter(text)
            self.assertEqual(b.field(fm, "name"), name)
            desc = b.field(fm, "description")
            self.assertLessEqual(len(desc), b.MAX_DESCRIPTION, name)
            self.assertTrue(desc)
            self.assertIn("SKILL_DIR=", body.split("\n\n", 1)[0])

    def test_no_plugin_root_left_and_every_reference_resolves(self):
        for name, path in self.zips.items():
            with zipfile.ZipFile(path) as zf:
                names = set(zf.namelist())
                for member in names:
                    if not member.endswith(b.TEXT_EXT):
                        continue
                    text = zf.read(member).decode("utf-8")
                    self.assertNotIn("${CLAUDE_PLUGIN_ROOT}", text, member)
                    for ref in SKILL_REF.findall(text):
                        ref = ref.rstrip(".")
                        target = name + "/" + ref
                        ok = target in names or any(n.startswith(target.rstrip("/") + "/") for n in names)
                        self.assertTrue(ok, "%s -> %s missing" % (member, ref))

    def test_scripts_run_inside_the_unpacked_zip(self):
        tmp = tempfile.mkdtemp()
        try:
            with zipfile.ZipFile(self.zips["ab-test-card"]) as zf:
                zf.extractall(tmp)
            root = os.path.join(tmp, "ab-test-card")
            r = subprocess.run(
                [sys.executable, os.path.join(root, "scripts", "validate_scenario_json.py"),
                 os.path.join(root, "examples", "scenario.json")],
                capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_build_is_reproducible(self):
        other = tempfile.mkdtemp()
        try:
            path, _ = b.build_zip("ab-test", other)
            with open(path, "rb") as a, open(self.zips["ab-test"], "rb") as c:
                self.assertEqual(a.read(), c.read())
        finally:
            shutil.rmtree(other, ignore_errors=True)


class TestGuards(unittest.TestCase):
    def test_short_descriptions_reviewed_against_current_source(self):
        # Fails when a skill's description changes: rewrite its short
        # description in build_skill_zips.py, then update the hash with
        # `python3 scripts/build_skill_zips.py --print-hashes`.
        for name in b.skill_names():
            fm, _ = b.split_front_matter(b.read(os.path.join(b.SKILLS_DIR, name, "SKILL.md")))
            self.assertEqual(b.sha256(b.field(fm, "description")), b.SHORT_DESCRIPTIONS[name][1], name)

    def test_overlong_short_description_is_refused(self):
        saved = b.SHORT_DESCRIPTIONS["ab-test"]
        b.SHORT_DESCRIPTIONS["ab-test"] = ("x" * (b.MAX_DESCRIPTION + 1), saved[1])
        try:
            with self.assertRaises(b.BuildError):
                b.build_zip("ab-test", tempfile.mkdtemp())
        finally:
            b.SHORT_DESCRIPTIONS["ab-test"] = saved

    def test_stale_hash_warns_and_fails_under_strict(self):
        saved = b.SHORT_DESCRIPTIONS["ab-test"]
        b.SHORT_DESCRIPTIONS["ab-test"] = (saved[0], "0" * 64)
        try:
            warnings = []
            b.build_zip("ab-test", tempfile.mkdtemp(), strict=False, warnings=warnings)
            self.assertEqual(len(warnings), 1)
            with self.assertRaises(b.BuildError):
                b.build_zip("ab-test", tempfile.mkdtemp(), strict=True)
        finally:
            b.SHORT_DESCRIPTIONS["ab-test"] = saved

    def test_yaml_quote_escapes(self):
        self.assertEqual(b.yaml_quote('a "b" \\c'), '"a \\"b\\" \\\\c"')


if __name__ == "__main__":
    unittest.main()
