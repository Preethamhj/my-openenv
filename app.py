import sys
import os

# ✅ CRITICAL FIX — add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from env.environment import CyberEnv 

app = FastAPI()
env = CyberEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()