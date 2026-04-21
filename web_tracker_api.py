import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Groq 연결
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
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

# ✅ LLM 함수
def ask_llm():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": "한국의 수도는 어디야? 한 단어로 답해."}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

@app.post("/track")
def track(data: RocketState):
    debug_msg = "web_tracker_api.py track() 안으로 들어옴"
    print(debug_msg)

    llm_result = ask_llm()
    print(f"답변: {llm_result}")

    yaw, pitch = calc_angles_to_target(
        data.rocket_x, data.rocket_y, data.rocket_z,
        data.jupiter_x, data.jupiter_y, data.jupiter_z
    )

    return {
        "action": "track_jupiter",
        "yaw": yaw,
        "pitch": pitch,
        "speed": data.speed,
        "debug": debug_msg,
        "llm_result": llm_result
    }
    
