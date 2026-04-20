import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:8000",
    "https://vercel.com/lee-taegeons-projects/web-unity/CYCUGw7SRTmEupTLJi4RAYibyEwx",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RocketState(BaseModel):
    rocket_x: float
    rocket_y: float
    rocket_z: float
    jupiter_x: float
    jupiter_y: float
    jupiter_z: float
    speed: float = 2.0

def calc_angles_to_target(rx, ry, rz, tx, ty, tz):
    dx = tx - rx
    dy = ty - ry
    dz = tz - rz
    horizontal = math.sqrt(dx * dx + dz * dz)
    yaw = math.degrees(math.atan2(dx, dz))
    pitch = -math.degrees(math.atan2(horizontal, dy))
    return yaw, pitch

@app.get("/")
def root():
    return {"message": "tracking api running"}

@app.post("/track")
def track(data: RocketState):
    yaw, pitch = calc_angles_to_target(
        data.rocket_x, data.rocket_y, data.rocket_z,
        data.jupiter_x, data.jupiter_y, data.jupiter_z
    )
    return {
        "action": "track_jupiter",
        "yaw": yaw,
        "pitch": pitch,
        "speed": data.speed
    }
