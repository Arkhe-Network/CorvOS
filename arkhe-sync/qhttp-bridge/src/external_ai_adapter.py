from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI(title="External AI Skill Adapter")

class SkillRequest(BaseModel):
    skill_id: str
    input_data: str

@app.post("/execute")
async def execute_external_skill(req: SkillRequest):
    # Mock external API call (e.g. OpenAI)
    output = f"Processed {req.input_data} via {req.skill_id}"
    proof = hashlib.sha256(output.encode()).hexdigest()
    return {"output": output, "proof": proof}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
