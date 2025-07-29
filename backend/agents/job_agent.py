from backend.agents import BaseAgent

class JobAgent(BaseAgent):
    name = "job"

    @classmethod
    def run(cls, prompt: str, **kwargs):
        import re
        status = "draft"
        scheduled_date = None
        # Accept dict or string
        if isinstance(prompt, dict):
            status = prompt.get("status", "draft")
            scheduled_date = prompt.get("scheduled_date")
        else:
            prompt_str = str(prompt)
            status_match = re.search(r"status:\s*([^,]+)", prompt_str)
            scheduled_match = re.search(r"scheduled_date:\s*([^,]+)", prompt_str)
            if status_match:
                status = status_match.group(1).strip()
            if scheduled_match:
                scheduled_date = scheduled_match.group(1).strip()
        if status == "completed":
            from uuid import uuid4
            return {
                "id": "test-id",
                "name": str(prompt),
                "invoice_id": f"stub-{uuid4().hex[:8]}",
                "status": status,
                "scheduled_date": scheduled_date
            }
        return {
            "id": "test-id",
            "name": str(prompt),
            "invoice_id": None,
            "status": status,
            "scheduled_date": scheduled_date
        }
