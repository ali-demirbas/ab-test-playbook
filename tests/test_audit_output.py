#!/usr/bin/env python3
"""Text contracts of the audit's output (3.4): the severity table first, the
fixed plan, the card offer, the coverage line, the two measurement items,
item 11's one exception, the on-request pre-start list, the Turkish example
and the eval inputs that test false alarms, an embedded line and a pasted plan."""
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SECTIONS = ["Flagged line", "Table", "Decision", "Details", "Verify line", "Coverage line",
            "Out of scope", "Fixed plan", "Card offer", "At most one question"]
FIXED_PLAN = {
    "en": ("**Fixed plan**", ["Variable", "A", "B", "Hypothesis", "Primary KPI", "Guardrail",
                              "Held constant", "Before you start"]),
    "tr": ("**Düzeltilmiş plan**", ["Değişken", "A", "B", "Hipotez", "Birincil KPI", "Guardrail",
                                    "Sabit kalanlar", "Başlamadan önce"]),
}
EXAMPLES = {"en": "audit-example.md", "tr": "audit-example.tr.md"}


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def flat(text):
    return re.sub(r"\s+", " ", text)


def words(text):
    return [w for w in text.split() if not re.fullmatch(r"[|:\-]+", w)]


class Skill(unittest.TestCase):
    def setUp(self):
        self.skill = read("skills", "ab-test-audit", "SKILL.md")
        self.checklist = self.skill.split("## Audit checklist")[1].split("## Output format")[0]
        self.output = self.skill.split("## Output format")[1].split("## Never do")[0]
        self.items = re.split(r"^(?=\d+\. \*\*)", self.checklist, flags=re.M)[1:]

    def test_output_sections_in_order(self):
        found = re.findall(r"^\d+\. \*\*([^*]+)\*\*", self.output, re.M)
        self.assertEqual(found, SECTIONS)

    def test_table_header_and_fixed_strings_in_both_languages(self):
        for text in ("| Önem | Bulgu | Düzeltme |", "| Severity | Finding | Fix |",
                     "Karar: bu hâliyle başlayamaz; düzeltilmiş planla başlayabilir.",
                     "Doğrulanacaklar:", "To verify:",
                     "İsterseniz düzeltilmiş planı karta çevireyim.",
                     "If you like, I'll turn the fixed plan into a card."):
            self.assertIn(text, self.output)
        self.assertIn('A "needs verifying" item goes in the verify line, never a row', self.output)

    def test_coverage_line_counts_the_checklist(self):
        n = len(self.items)
        self.assertEqual(n, 20)
        self.assertIn("Bakılan %d başlıktan temiz olanlar:" % n, self.output)
        self.assertIn("Of the %d headings checked, clean:" % n, self.output)
        for item in self.items:  # every heading has a Turkish name for that line
            self.assertRegex(item, r"^\d+\. \*\*[^*]+\*\* \([^)]+\)")

    def test_fixed_plan_rules(self):
        block = [line for line in self.output.splitlines() if line.startswith("8. **Fixed plan**")][0]
        self.assertIn("6 to 8 lines", block)
        self.assertIn("one variable", block)
        self.assertIn("never invented", block)
        self.assertIn("nothing item 11 removed comes back", block)
        self.assertIn("none when no runnable single-variable test remains", block)
        for lang in ("en", "tr"):
            for field in FIXED_PLAN[lang][1]:
                self.assertIn(field, block)

    def test_card_offer_goes_through_the_pipeline(self):
        block = [line for line in self.output.splitlines() if line.startswith("9. **Card offer**")][0]
        self.assertIn("never a question", block)
        self.assertIn("`ab-test-design` takes that plan as the named test", block)
        self.assertIn("rule 17", block)
        self.assertIn("none when nothing runnable remains", block)

    def test_two_measurement_items(self):
        scope, exposure = self.items[6], self.items[7]
        self.assertTrue(scope.startswith("7. **Targeting and measurement scope**"))
        self.assertTrue(exposure.startswith("8. **Exposure point**"))
        for item, words_ in ((scope, ("device", "counts everyone assigned", "both arms")),
                             (exposure, ("accordion", "below the first view", "page load", "both arms"))):
            self.assertIn("`[Serious]`", item)
            self.assertIn("`[Note]`", item)
            for w in words_:
                self.assertIn(w, item)

    def test_item_11_has_one_exception(self):
        item = self.items[10]
        self.assertTrue(item.startswith("11. **Ethics, protections and regulation**"))
        self.assertIn("The first three are compliance or ethics findings, never fixed with a gentler variant", item)
        self.assertIn("gets no other finding", item)
        self.assertIn("only the fourth is fixed with a variant, one intermediate method as the variable", item)
        self.assertIn("Sensitive field removed outright", item)

    def test_pre_start_list_only_on_request(self):
        self.assertIn("**On request only:**", self.output)
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/templates/audit-output.md", self.output)
        self.assertIn("never unasked", self.output)
        template = read("templates", "audit-output.md")
        for heading in ("## Test başlamadan önce", "## Before the test starts (English)"):
            body = template.split(heading)[1].split("\n## ")[0]
            self.assertEqual(re.findall(r"^(\d+)\. ", body, re.M), [str(i) for i in range(1, 11)], heading)
        self.assertNotIn("—", template)


class Examples(unittest.TestCase):
    def audit(self, lang):
        text = read("examples", EXAMPLES[lang])
        header = "| Severity |" if lang == "en" else "| Önem |"
        self.assertIn(header, text)
        return header + text.split(header, 1)[1]

    def test_table_comes_first_and_decision_follows(self):
        for lang, decision in (("en", "**Decision:"), ("tr", "**Karar:")):
            out = self.audit(lang)
            table_end = max(i for i, line in enumerate(out.splitlines()) if line.startswith("|"))
            after = [line for line in out.splitlines()[table_end + 1:] if line.strip()]
            self.assertTrue(after[0].startswith(decision), lang)

    def test_no_needs_verifying_row(self):
        for lang in EXAMPLES:
            for row in re.findall(r"^\| \[.*$", self.audit(lang), re.M):
                self.assertNotRegex(row.lower(), r"needs verif|to verify|doğrulan", lang)

    def test_fixed_plan_block(self):
        for lang, (title, fields) in FIXED_PLAN.items():
            out = self.audit(lang)
            lines = out.split(title + "\n", 1)[1].split("\n\n")[0].splitlines()
            self.assertTrue(6 <= len(lines) <= 8, lang)
            labels = [re.match(r"^- ([^:]+): ", line).group(1) for line in lines]
            self.assertEqual(labels, [f for f in fields if f in labels], lang)
            self.assertEqual(labels[:6], fields[:6], lang)

    def test_coverage_line_names_real_headings(self):
        skill = read("skills", "ab-test-audit", "SKILL.md")
        en = set(re.findall(r"^\d+\. \*\*([^*]+)\*\*", skill.split("## Audit checklist")[1].split("## Output")[0], re.M))
        tr = set(re.findall(r"^\d+\. \*\*[^*]+\*\* \(([^)]+)\)", skill, re.M))
        for lang, opener, names in (("en", "Of the 20 headings checked, clean: ", en),
                                    ("tr", "Bakılan 20 başlıktan temiz olanlar: ", tr)):
            line = flat(self.audit(lang)).split(opener, 1)[1].split(".")[0]
            listed = line
            for name in sorted(names, key=len, reverse=True):
                listed = listed.replace(name, "")
            self.assertEqual(listed.replace(",", "").strip(), "", "%s: %r" % (lang, listed))

    def test_ends_with_the_card_offer(self):
        self.assertTrue(self.audit("en").rstrip().endswith("If you like, I'll turn the fixed plan into a card."))
        self.assertTrue(self.audit("tr").rstrip().endswith("İsterseniz düzeltilmiş planı karta çevireyim."))

    def test_shorter_than_before(self):
        # 3.3's outputs ran 374-518 words; the example carries more faults than most plans.
        for lang, ceiling in (("en", 460), ("tr", 380)):
            self.assertLessEqual(len(words(self.audit(lang))), ceiling, lang)

    def test_turkish_example(self):
        text = read("examples", "audit-example.tr.md")
        self.assertNotIn("—", text)
        self.assertIn("kaba bir ölçülebilirlik aralığı gösterebilirim", flat(text))
        cells = [c.strip() for row in re.findall(r"^\| \[.*$", text, re.M) for c in row.split("|")[2:4]]
        values = [line.split(": ", 1)[1] for line in
                  text.split("**Düzeltilmiş plan**\n", 1)[1].split("\n\n")[0].splitlines()]
        for value in cells + values:
            self.assertTrue(value[0].isupper() or value[0] in "“\"%", value)


class Eval(unittest.TestCase):
    def setUp(self):
        self.text = read("evals", "03-audit.md")

    def test_inputs_a_to_f(self):
        self.assertEqual(re.findall(r"^\*\*Girdi ([A-Z])", self.text, re.M), list("ABCDEF"))

    def test_sound_plan_expects_no_false_alarm(self):
        d = self.text.split("**Girdi D")[1].split("**Girdi E")[0]
        self.assertIn("“Karar: bu hâliyle başlayabilir.”", d)
        self.assertIn("“İsterseniz bu planı karta çevireyim.”", d)
        self.assertIn("Herhangi bir `[Kritik]` ya da `[Ciddi]` satır.", d)

    def test_embedded_line_and_pasted_plan(self):
        e = self.text.split("**Girdi E")[1].split("**Girdi F")[0]
        self.assertIn("İşaretli satır 8", e)
        self.assertIn("Karar satırın varlığına göre değişmez", e)
        f = self.text.split("**Girdi F")[1]
        self.assertIn("`validate_input.py --stdin`", f)
        self.assertIn("tarama yakalamasa da", f)

    def test_refused_plan_gets_no_fixed_plan(self):
        c = self.text.split("**Girdi C")[1].split("**Girdi D")[0]
        self.assertIn("düzeltilmiş plan ve karta çevirme teklifi yoktur", c)


if __name__ == "__main__":
    unittest.main()
