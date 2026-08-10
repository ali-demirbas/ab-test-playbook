# Security Policy

## Supported versions

This project is pre-1.0. Only the latest commit on `main` is supported; there are no maintained release branches yet.

## Reporting a vulnerability

Please report security issues privately through [GitHub Security Advisories](https://github.com/ali-demirbas/ab-test-playbook/security/advisories/new) rather than opening a public issue.

Include what you'd include in any report: the affected file(s), how to reproduce, and the impact you think it has.

## Scope

This repo has no server, no hosted service, and collects no user data. It is a Claude Code plugin: mostly prompt/markdown content, plus two small dependency-free Python scripts. The realistic attack surface is:

- `scripts/analyze_results.py` and `scripts/validate_scenarios.py` — both take only numeric/text CLI arguments, run no shell commands, and make no network calls; a bug here would be a wrong calculation or a crash, not code execution.
- `templates/scenario-card.html` — the skill that fills this template is required to HTML-escape any user- or model-supplied text before inserting it into the placeholders; unescaped content reaching the rendered card (e.g. via a crafted scenario title) is in scope.
- Any skill instruction that could be manipulated via crafted page content (a shared screenshot, URL, or scenario text) into producing unsafe output — e.g. a dark-pattern variant, or a card with injected markup.

Issues that only affect a user's own local run (e.g. a malformed CLI argument causing a Python traceback that's already caught and reported as a clean error) are better filed as a normal bug report.

## Response

This is a solo-maintained open-source project. There's no SLA, but reports will be acknowledged and triaged as soon as reasonably possible.
