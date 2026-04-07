import sys
import os

# ✅ FORCE Python to see /app as root
sys.path.append("/app")

from fastapi import FastAPI
from env.environment import CyberEnv

app = FastAPI()
env = CyberEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()