"""Central place to assemble prompts once LLM integration lands."""


def build_quote_prompt(raw: str, context: str | None = None) -> str:
    if context:
        return f"Context:\n{context}\n\nUser: {raw}"
    return raw
