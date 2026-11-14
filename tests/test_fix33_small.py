#!/usr/bin/env python3
"""Text contracts of the small audit fixes: the audit's fixed severity labels,
its scan of a pasted plan and its feasibility offer."""
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EN = {"Critical", "Serious", "Moderate", "Note"}
TR = {"Kritik", "Ciddi", "Orta", "Not"}


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


class TestAuditSeverityLabels(unittest.TestCase):
    def setUp(self):
        self.skill = read("skills", "ab-test-audit", "SKILL.md")

    def test_every_checklist_item_names_a_fixed_label(self):
        blocks = re.split(r"^(?=\d+\. \*\*)", self.skill.split("## Audit checklist")[1].split("## Output format")[0],
                          flags=re.M)[1:]
        self.assertEqual(len(blocks), 18)
        for block in blocks:
            labels = set(re.findall(r"`\[(\w+)\]`", block))
            number = block.split(".")[0]
            if number == "14":  # a bundled variant takes item 4's label
                self.assertIn("item 4", block)
            self.assertTrue(labels, "item %s has no severity label" % number)
            self.assertLessEqual(labels, EN, "item %s" % number)

    def test_labels_are_defined_once_in_both_languages(self):
        output = self.skill.split("## Output format")[1].split("## Never do")[0]
        for label in EN | TR:
            self.assertEqual(output.count("[%s]" % label), 1, label)

    def test_old_labels_are_gone(self):
        for path in (("skills", "ab-test-audit", "SKILL.md"), ("examples", "audit-example.md"),
                     ("evals", "03-audit.md")):
            text = read(*path)
            for old in ("[Blocking]", "[Improvement]", "[Engelleyici]", "[İyileştirme]"):
                self.assertNotIn(old, text, path[-1])

    def test_example_and_eval_use_only_the_fixed_labels(self):
        example = re.findall(r"^\*\*\[(\w+)\]", read("examples", "audit-example.md"), re.M)
        self.assertGreaterEqual(len(example), 8)
        self.assertLessEqual(set(example), EN)
        order = [sorted(EN, key=["Critical", "Serious", "Moderate", "Note"].index).index(x) for x in example]
        self.assertEqual(order, sorted(order), "findings are listed most severe first")
        self.assertLess(example.count("Serious"), len(example) * 0.6, "severity has to discriminate")
        self.assertLessEqual(set(re.findall(r"`\[(\w+)\]`", read("evals", "03-audit.md"))), TR)


class TestAuditScanAndOffer(unittest.TestCase):
    def setUp(self):
        self.skill = read("skills", "ab-test-audit", "SKILL.md")

    def test_pasted_plan_is_scanned(self):
        self.assertRegex(self.skill, r"pasted into the chat is first written unchanged to a scratch file")

    def test_feasibility_offer_in_both_languages(self):
        self.assertIn("kaba bir ölçülebilirlik aralığı gösterebilirim", self.skill)
        self.assertIn("I can show a rough detectable range", self.skill)
        self.assertIn("I can show a rough detectable range", read("examples", "audit-example.md"))


class TestSuggestContextQuestion(unittest.TestCase):
    def setUp(self):
        self.skill = read("skills", "ab-test-suggest", "SKILL.md")

    def test_context_question_replaces_the_ban(self):
        self.assertNotIn("Context, no questions", self.skill)
        step = [line for line in self.skill.splitlines() if line.startswith("1. **Context.**")][0]
        self.assertIn("multiple choice", step)
        self.assertIn("rule 19", step)
        self.assertIn("never before them", step)  # the question doesn't hold the turn

    def test_generic_picks_line_in_both_languages(self):
        self.assertIn("Bunlar arşivden genel seçimler", self.skill)
        self.assertIn("These are generic archive picks", self.skill)

    def test_rule_19_ranks_the_context_question(self):
        rule = [line for line in read("CLAUDE.md").splitlines() if line.startswith("19. ")][0]
        self.assertIn("with no page shared, what is sold and how", rule)
        self.assertEqual(len(re.findall(r"\((\d)\) ", rule)), 9)  # kinds 7, 8 and 9 keep their numbers


class TestDesignRateQuestion(unittest.TestCase):
    def test_rate_for_a_step_asks_where_inside_it(self):
        step = [line for line in read("skills", "ab-test-design", "SKILL.md").splitlines()
                if line.startswith("1. **Problem first")][0]
        self.assertIn("**A rate given for a step**", step)
        self.assertIn("multiple choice of this step's own parts", step)
        self.assertIn("unless the message says", step)
        self.assertIn("after the scenarios", step)  # delivered first: the question doesn't hold the turn
        rule = [line for line in read("CLAUDE.md").splitlines() if line.startswith("19. ")][0]
        self.assertIn("where inside a step the loss happens", rule)


class TestCriticIdeaQuality(unittest.TestCase):
    def setUp(self):
        self.critic = read("agents", "scenario-critic.md")

    def test_set_level_diversity_check(self):
        section = self.critic.split("## Set-level checks")[1].split("## Verdict")[0]
        self.assertIn("**Idea diversity.**", section)
        self.assertIn("one objection lens", section)
        self.assertIn("impact ranking", section)
        self.assertIn("Explicit asks are exempt", section)

    def test_paste_test_asks_for_an_observed_element(self):
        item = [line for line in self.critic.splitlines() if line.startswith("2. **Problem.**")][0]
        self.assertIn("pasted unchanged onto any page", item)
        self.assertIn("FIX [fixable]: tie the proposal to an element observed on this page", item)

    def test_report_format_is_unchanged(self):
        self.assertIn('1. [blocking|fixable] <check> (rule <n>): "<quoted text>" → <what to write instead>', self.critic)
        self.assertIn("verdict: PASS <fingerprint> | FIX | RET", self.critic)


if __name__ == "__main__":
    unittest.main()
