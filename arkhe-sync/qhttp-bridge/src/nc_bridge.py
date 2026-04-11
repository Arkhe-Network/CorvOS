import json
import hashlib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="QHTTP Bridge - Neural Computer Integration")

class LatentState(BaseModel):
    vector: List[float]
    step: int
    model_hash: str

@app.post("/nc/commit")
async def commit_latent_state(state: LatentState):
    arr = np.array(state.vector)
    norm = np.linalg.norm(arr)
    if abs(norm - 1.0) > 0.05:
        raise HTTPException(status_code=400, detail="Decoerência: norma fora do limite")

    state_bytes = json.dumps(state.vector).encode()
    state_hash = hashlib.sha3_256(state_bytes).hexdigest()

    return {"status": "committed", "state_hash": state_hash, "norm": float(norm)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1338)
