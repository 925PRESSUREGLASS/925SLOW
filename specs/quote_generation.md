# Quote Generation Spec – v0.1

| Rule ID | Description                                                    |
|---------|----------------------------------------------------------------|
| Q-1     | Response **must start** with a Markdown block-quote symbol `>` |
| Q-2     | First line **must include** a currency value (e.g. `$123.45`)  |
| Q-3     | First line **must include** the suburb/location                |
| Q-4     | Second line **must be** an em-dash attribution: `— QuoteGPT, YYYY` |
| Q-5     | A *Rationale* paragraph (≤ 2 sentences) **must follow**        |

These rules are enforced by *SpecGuard*. Violations drop the compliance score.
