#!/usr/bin/env python3
"""examples/*.md içindeki "gerçek script çıktısı" bloklarını motorla karşılaştırır.

Örnek dosyalar her sayının `scripts/analyze_results.py` çıktısı olduğunu söyler. Motor değişip
belgeler değişmezse bu iddia sessizce yanlışlaşır; bu test her `analyze_results.py` komutunu
yeniden çalıştırır ve belgede hemen ardından gelen JSON bloğundaki her alanın çıktıyla aynı
olduğunu doğrular (belgedeki blok kırpılmıştır: alt küme karşılaştırması yapılır).
"""
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SCRIPT = os.path.join(ROOT, "scripts", "analyze_results.py")
FENCE = re.compile(r"```(\w+)\n(.*?)```", re.S)


def blocks(path):
    with open(path, encoding="utf-8") as f:
        return [(m.group(1), m.group(2)) for m in FENCE.finditer(f.read())]


def command_args(bash):
    """Bash bloğundaki tek analyze_results.py komutunun argümanları (yoksa None)."""
    text = bash.replace("\\\n", " ")
    for line in text.splitlines():
        if "analyze_results.py" in line:
            parts = shlex.split(line)
            return parts[[i for i, p in enumerate(parts) if p.endswith("analyze_results.py")][0] + 1:]
    return None


def subset_problems(doc, out, where=""):
    """Belgedeki değer çıktının alt kümesi mi? Uyuşmayan yolların listesi."""
    if isinstance(doc, dict):
        if not isinstance(out, dict):
            return [f"{where}: beklenen nesne"]
        problems = []
        for k, v in doc.items():
            if k not in out:
                problems.append(f"{where}.{k}: çıktıda yok")
            else:
                problems.extend(subset_problems(v, out[k], f"{where}.{k}"))
        return problems
    if isinstance(doc, list) and doc and all(isinstance(x, dict) for x in doc):
        if not isinstance(out, list) or len(out) != len(doc):
            return [f"{where}: liste uzunluğu farklı"]
        return [p for i, (d, o) in enumerate(zip(doc, out)) for p in subset_problems(d, o, f"{where}[{i}]")]
    return [] if doc == out else [f"{where}: belgede {doc!r}, çıktıda {out!r}"]


def run(args, cwd):
    out = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, cwd=cwd)
    return out.returncode, out.stdout


class TestExampleOutputsAreReal(unittest.TestCase):
    def check_file(self, name, min_pairs):
        path = os.path.join(ROOT, "examples", name)
        found = blocks(path)
        checked = 0
        with tempfile.TemporaryDirectory() as d:
            for i, (lang, body) in enumerate(found):
                if lang != "bash":
                    continue
                # Belgedeki veri üreticisi: heredoc içindeki Python aynen çalıştırılır (tohumlu, deterministik).
                gen = re.search(r"python3 - <<'EOF'\n(.*?)\nEOF", body, re.S)
                if gen:
                    subprocess.run([sys.executable, "-c", gen.group(1)], cwd=d, check=True)
                    continue
                args = command_args(body)
                if args is None or i + 1 >= len(found) or found[i + 1][0] != "json":
                    continue
                rc, out = run(args, d)
                self.assertEqual(rc, 0, f"{name}: {' '.join(args)}\n{out}")
                problems = subset_problems(json.loads(found[i + 1][1]), json.loads(out), args[0])
                self.assertEqual(problems, [], f"{name}: {' '.join(args)}")
                checked += 1
        self.assertGreaterEqual(checked, min_pairs, f"{name}: beklenenden az komut/çıktı çifti bulundu")

    def test_results_walkthrough(self):
        self.check_file("results-walkthrough.md", 5)

    def test_audit_example(self):
        self.check_file("audit-example.md", 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
