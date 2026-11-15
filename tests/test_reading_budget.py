#!/usr/bin/env python3
"""The fixed reading of each flow, and that everything a skill points to exists.

Every file a flow reads before it produces anything is re-billed on every model
call of a run, so the always-read set has a ceiling here, and every rule moved
out of it into an on-demand file must still be reachable: each `file → Section`
reference, each methodology section a decision table names, each on-demand file
the triggers name, and each of them inside every skill ZIP.

`python3 tests/test_reading_budget.py --table` prints the bytes per flow.
"""
import os
import re
import shutil
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import build_skill_zips  # noqa: E402
import read_section  # noqa: E402

CORE = ["CLAUDE.md", "skills/ab-test-card/SKILL.md", "templates/record-checklist.md", "knowledge/mockup-style.md"]
# flow -> (files read whole before producing, ceiling in bytes). The ceilings
# leave a little room; raising one is a decision, not a test fix.
FLOWS = {
    "design": (CORE[:1] + ["skills/ab-test-design/SKILL.md"] + CORE[1:], 73000),
    "suggest": (CORE[:1] + ["skills/ab-test-suggest/SKILL.md"] + CORE[1:], 69000),
    "card": (CORE, 53000),
    "audit": (["CLAUDE.md", "skills/ab-test-audit/SKILL.md"], 36000),
    "router (added)": (["skills/ab-test/SKILL.md"], 13500),
    "critic, per round": (["agents/scenario-critic.md", "CLAUDE.md"], 47000),
    "mockup reviewer, per round": (["agents/mockup-reviewer.md", "knowledge/mockup-style.md", "CLAUDE.md"], 50000),
}
ON_DEMAND = ("special-cases", "raw-markup", "fast-mode", "draft-and-final", "render-check")
RUNTIME_DIRS = ("skills", "agents", "knowledge", "templates")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def size(rel):
    return os.path.getsize(os.path.join(ROOT, rel))


def runtime_md():
    """Every Markdown file the plugin reads at runtime."""
    out = ["CLAUDE.md"]
    for top in RUNTIME_DIRS:
        for base, _, files in os.walk(os.path.join(ROOT, top)):
            out.extend(os.path.relpath(os.path.join(base, f), ROOT) for f in sorted(files) if f.endswith(".md"))
    return sorted(out)


def skill_body(rel):
    text = read(rel)
    return text.split("\n---\n", 1)[1] if text.startswith("---\n") else text


# A named reference: `<target>` → Section. The target is a file or a skill name.
REF = re.compile(r"`(?:\$\{CLAUDE_PLUGIN_ROOT\}/)?([A-Za-z0-9_./ -]+?)` → ([A-Za-z][^;:.,()`\n]*)")
SKILLS = {n: "skills/%s/SKILL.md" % n for n in os.listdir(os.path.join(ROOT, "skills"))}


def target_file(name):
    if name in SKILLS:
        return SKILLS[name]
    base = os.path.basename(name)
    for rel in runtime_md():
        if rel == name or rel.endswith("/" + name) or os.path.basename(rel) == base:
            return rel
    return None


def heading_titles(rel):
    lines = read(rel).split("\n")
    return [read_section.norm(t) for _, _, t in read_section.headings(lines)]


def resolves(rel, section):
    s = read_section.norm(section)
    return any(s.startswith(h) or h.startswith(s) for h in heading_titles(rel))


class TestBudget(unittest.TestCase):
    def test_every_flow_stays_under_its_ceiling(self):
        for flow, (files, ceiling) in FLOWS.items():
            total = sum(size(f) for f in files)
            self.assertLessEqual(total, ceiling, "%s reads %d bytes before producing" % (flow, total))

    def test_each_flow_names_what_it_reads(self):
        for flow in ("design", "suggest"):
            body = skill_body("skills/ab-test-%s/SKILL.md" % flow)
            self.assertIn("${CLAUDE_PLUGIN_ROOT}/templates/record-checklist.md", body, flow)
            self.assertIn("`ab-test-card`", body, flow)
        card = skill_body("skills/ab-test-card/SKILL.md")
        for rel in ("templates/record-checklist.md", "knowledge/mockup-style.md", "knowledge/mockup-style/"):
            self.assertIn("${CLAUDE_PLUGIN_ROOT}/" + rel, card)

    def test_the_schema_and_the_worked_example_are_never_read(self):
        for rel in runtime_md():
            text = read(rel)
            for path in ("${CLAUDE_PLUGIN_ROOT}/templates/scenario.schema.json", "${CLAUDE_PLUGIN_ROOT}/examples/"):
                self.assertNotIn(path, text, rel)
        self.assertIn("never read", read("templates/record-checklist.md"))

    def test_no_flow_reads_another_flow_skill(self):
        """A cross-reference into another flow's skill reads that whole file too."""
        for flow, other in (("design", "suggest"), ("suggest", "design")):
            body = skill_body("skills/ab-test-%s/SKILL.md" % flow)
            self.assertNotIn("`ab-test-%s` →" % other, body, flow)
            self.assertNotIn("`ab-test` →", body, flow)


class TestEveryReferenceResolves(unittest.TestCase):
    def test_named_sections_exist(self):
        checked = 0
        for rel in runtime_md():
            if rel.startswith("knowledge/scenarios/"):
                continue  # archive prose names ideas in Turkish, not headings
            for target, section in REF.findall(read(rel)):
                if "<" in target or target.startswith("."):
                    continue
                path = target_file(target)
                if path is None and resolves("knowledge/methodology.md", target):
                    path = "knowledge/methodology.md"  # `Section` → its subsection
                if path is None:
                    continue  # not a document: a command or a field name before the arrow
                checked += 1
                self.assertTrue(resolves(path, section.strip()), "%s: `%s` → %s" % (rel, target, section.strip()))
        self.assertGreater(checked, 40)

    def test_methodology_tables_name_real_sections(self):
        meth = "knowledge/methodology.md"
        for rel in ("skills/ab-test-design/SKILL.md", "skills/ab-test-suggest/SKILL.md"):
            text = read(rel)
            table = text[text.index("| Decision | Section |"):]
            table = table[:table.index("\n\n")]
            names = re.findall(r"`([^`]+)`", "\n".join(l.rsplit("|", 2)[-2] for l in table.split("\n")[2:]))
            self.assertGreater(len(names), 10, rel)
            for name in names:
                self.assertTrue(resolves(meth, name), "%s names `%s`" % (rel, name))

    def test_read_section_commands_name_real_headings(self):
        cmd = re.compile(r"read_section\.py \$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+) (?:--until )?\"([^\"<]+)\"")
        for rel in runtime_md():
            for path, title in cmd.findall(read(rel)):
                lines = read(path).split("\n")
                self.assertIsNotNone(read_section.find(read_section.headings(lines), title), "%s: %s" % (rel, title))

    def test_every_backticked_document_exists(self):
        name = re.compile(r"`(?:\$\{CLAUDE_PLUGIN_ROOT\}/)?([A-Za-z0-9_/-]+\.md)`")
        for rel in runtime_md():
            for ref in name.findall(read(rel)):
                self.assertIsNotNone(target_file(ref), "%s: `%s`" % (rel, ref))

    def test_the_core_trigger_table_names_every_on_demand_file(self):
        core = read("knowledge/mockup-style.md")
        table = core[:core.index("\n## ")]
        on_disk = sorted(f[:-3] for f in os.listdir(os.path.join(ROOT, "knowledge", "mockup-style")) if f.endswith(".md"))
        self.assertEqual(on_disk, sorted(ON_DEMAND))
        for stem in ON_DEMAND:
            self.assertIn("`%s.md`" % stem, table, stem)
            first = read("knowledge/mockup-style/%s.md" % stem).split("\n\n", 2)[1]
            self.assertTrue(first.startswith("Read ") or first.startswith("Rule 17"), stem)  # each says when it is read


class TestZipsCarryWhatSkillsReference(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = tempfile.mkdtemp()
        cls.members = {}
        for name in build_skill_zips.skill_names():
            path, _ = build_skill_zips.build_zip(name, cls.out)
            with zipfile.ZipFile(path) as zf:
                cls.members[name] = set(zf.namelist())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.out, ignore_errors=True)

    def test_every_zip_carries_the_fixed_and_on_demand_files(self):
        needed = set(CORE[2:]) | {"knowledge/mockup-style/%s.md" % s for s in ON_DEMAND} | {"CLAUDE.md"}
        for name, members in self.members.items():
            for rel in sorted(needed):
                self.assertIn(name + "/" + rel, members, name)

    def test_every_referenced_path_and_script_is_bundled(self):
        ref = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_./-]+)")
        for name, members in self.members.items():
            texts = [read(SKILLS[name])] + [read(rel) for rel in runtime_md() if not rel.startswith("skills/")]
            for text in texts:
                for path in ref.findall(text):
                    path = path.rstrip(".,;:)`")
                    if "<" in path or "*" in path or not os.path.exists(os.path.join(ROOT, path)):
                        continue
                    target = name + "/" + path.rstrip("/")
                    self.assertTrue(target in members or any(m.startswith(target + "/") for m in members),
                                    "%s ZIP lacks %s" % (name, path))


def table():
    rows = []
    for flow, (files, ceiling) in FLOWS.items():
        rows.append("%-28s %7d  (ceiling %d)  %s" % (flow, sum(size(f) for f in files), ceiling, " + ".join(files)))
    return "\n".join(rows)


if __name__ == "__main__":
    if "--table" in sys.argv:
        print(table())
    else:
        unittest.main()
