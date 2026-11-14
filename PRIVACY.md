# Privacy

A/B Test Builder (`ab-test-playbook`) collects no data.

- It runs inside your Claude session and your own working folder. Its scripts use the Python standard library and, for the optional visual check, a local headless browser. None of them makes a network call.
- It reads only what you share in the conversation (a screenshot, a URL's text, a description) and files you point it at.
- Files it writes (scenario records, HTML cards, PNG previews, the optional `.abtest-history.md` and `.abtest-backlog.md`) stay in your working folder. Nothing is sent to the author or to any third party.
- Its rules forbid copying personal values from a screenshot (names, account numbers, balances) into a card; they are masked.
- It reads no API keys, tokens or credentials.

How your conversation itself is handled is governed by your agreement with Anthropic, not by this plugin.

Questions: open an issue at https://github.com/ali-demirbas/ab-test-playbook/issues
