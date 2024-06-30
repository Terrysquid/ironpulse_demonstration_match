from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import time

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState:
    def __init__(self):
        self.team_blue = 0
        self.team_red = 0
        self.score_blue = 0
        self.score_red = 0
        self.status = "create"
        self.match_time = 0
        self.start_time = 0
        self.remaining_time = 0

    def reset(self, team_blue: str, team_red: str, time: int):
        self.status = "create"
        self.team_blue = team_blue
        self.team_red = team_red
        self.score_blue = 0
        self.score_red = 0
        self.match_time = time
        self.remaining_time = 0

    def start(self):
        if self.status == "create":
            self.status = "started"
            self.start_time = time.time()
            self.remaining_time = self.match_time

    def stop(self):
        self.status = "stopped"
        self.remaining_time = 0

    def finish(self):
        self.status = "finished"
        self.remaining_time = 0
    
    def get_time(self):
        elapsed_time = int(time.time() - self.start_time)
        self.remaining_time = max(min(self.match_time - elapsed_time, self.remaining_time), 0)
        if self.remaining_time == 0 and self.status == "started":
            self.status = "stopped"
        print(self.remaining_time)
        return self.remaining_time

    def score(self, team: str):
        if self.status == "started":
            if team == "blue":
                self.score_blue += 1
            elif team == "red":
                self.score_red += 1
        elif self.status == "stopped":
            if team == "blue":
                self.score_red += 3
            elif team == "red":
                self.score_blue += 3

game_state = GameState()
clients: List[WebSocket] = []

@app.get("/reset")
async def reset(team_blue: str, team_red: str, time: int):
    print(team_blue, team_red, time)
    game_state.reset(team_blue, team_red, time)
    return {"status": game_state.status}

@app.get("/start")
async def start():
    game_state.start()
    return {"status": game_state.status}

@app.get("/stop")
async def stop():
    game_state.stop()
    return {"status": game_state.status}

@app.get("/finish")
async def finish():
    game_state.finish()
    return {"status": game_state.status}

@app.get("/get_time")
async def get_time():
    remaining_time = game_state.get_time()
    return {"remaining_time": remaining_time}

@app.get("/score")
async def score(team: str):
    game_state.score(team)
    return {"team_blue": game_state.score_blue, "team_red": game_state.score_red}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(0.1)
            data = {
                "status": game_state.status,
                "team_blue": game_state.team_blue,
                "team_red": game_state.team_red,
                "score_blue": game_state.score_blue,
                "score_red": game_state.score_red,
                "match_time": game_state.match_time,
                "remaining_time": game_state.get_time()
            }
            for client in clients:
                await client.send_json(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(websocket)
        await websocket.close()
