import sys
import os

# ✅ FIX import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from env.environment import CyberEnv

app = FastAPI()
env = CyberEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()