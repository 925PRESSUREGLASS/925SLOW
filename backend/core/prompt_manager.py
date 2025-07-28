"""Central place to assemble prompts once LLM integration lands."""


def build_quote_prompt(
    raw: str, context_items: list[str] | None = None
) -> str:  # noqa: D401,ANN001
    """Format the LLM prompt.

    If *context_items* supplied, each is prepended as a bullet under a
    `Context:` header so GPT-4 / Ollama can read prior examples.
    """

    if context_items:
        ctx = "\n".join(f"\u2022 {c}" for c in context_items)
        return f"Context:\n{ctx}\n\nUser: {raw}"
    return raw
