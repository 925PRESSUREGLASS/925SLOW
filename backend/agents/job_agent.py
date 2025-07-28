# SPDX-License-Identifier: MIT


from backend.database import Customer, Job, Quote, get_session



                job: Job | None = sess.get(Job, job_id)
                if job is None:
                    return {"error": "job not found", "id": job_id}

                if payload.get("status"):
                    job.status = payload["status"]
                if payload.get("scheduled_date"):

