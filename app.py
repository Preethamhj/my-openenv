from fastapi import FastAPI
from env.environment import CyberEnv

app = FastAPI()
env = CyberEnv()

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()