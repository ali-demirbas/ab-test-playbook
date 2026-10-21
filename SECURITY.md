# Security Policy

## Supported versions

Only the latest commit on `main` is supported; there are no maintained release branches.

## Reporting a vulnerability

Please report security issues privately through [GitHub Security Advisories](https://github.com/ali-demirbas/ab-test-playbook/security/advisories/new) rather than opening a public issue.

Include what you'd include in any report: the affected file(s), how to reproduce, and the impact you think it has.

## Scope

This repo has no server, no hosted service, and collects no user data. It is a Claude Code plugin: mostly prompt/markdown content, plus small dependency-free Python scripts (validators, an input scanner and the card builder). The realistic attack surface is:

- `scripts/validate_scenarios.py`, `scripts/validate_scenario_json.py` and `scripts/validate_input.py` — they read local files, run no shell commands, and make no network calls; a bug here would be a wrong check or a crash, not code execution.
- `scripts/build_card.py` and `templates/scenario-card.html` — the builder HTML-escapes every user- or model-supplied text field and passes the mockup markup through an allowlist before filling the template's placeholders; unescaped or non-allowlisted content reaching the rendered card (e.g. via a crafted scenario title or mockup body) is in scope.
- The card builder's refusals: it refuses a mockup containing a value shaped like personal data (an 11-digit national ID, a TR IBAN, a 16-digit card number, an e-mail address, a mobile number; masks and all-zero placeholders pass), and it refuses to write a final card without both review stamps matching the record and the card it would write. A refused build writes nothing and leaves an existing output file untouched. A personal-data value of those shapes that reaches a card, or a final card written without matching stamps, is in scope. The stamps are integrity checks, not signatures: they show the content is unchanged since its review, not who reviewed it, and anyone who can edit the record can write one.
- Any skill instruction that could be manipulated via crafted page content (a shared screenshot, URL, or scenario text) into producing unsafe output — e.g. a dark-pattern variant, or a card with injected markup.

Issues that only affect a user's own local run (e.g. a malformed CLI argument causing a Python traceback that's already caught and reported as a clean error) are better filed as a normal bug report.

## Response

This is a solo-maintained open-source project. There's no SLA, but reports will be acknowledged and triaged as soon as reasonably possible.
