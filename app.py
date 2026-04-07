from fastapi import FastAPI

from env.environment import CyberEnv

app = FastAPI(title="OpenEnv Space")
env = CyberEnv()


@app.post("/reset")
def reset():
    observation = env.reset()
    return observation.model_dump()
