from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import brain
import router

app = FastAPI(title="Z-OS")

# CORS is fully open so your local HTML file can talk to it without getting blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str

@app.post("/api/command")
async def execute_command(request: CommandRequest):
    try:
        plan = brain.parse_intent(request.command)
        execution_logs = router.execute_plan(plan)
        return {"status": "success", "plan": plan, "logs": execution_logs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))