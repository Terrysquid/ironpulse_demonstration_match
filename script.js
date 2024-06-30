let ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onmessage = function(event) {
    let data = JSON.parse(event.data);
    document.getElementById("status").innerText = `Status: ${data.status}`;
    document.getElementById("match_time").innerText = `match_time: ${data.match_time}`;
    document.getElementById("remaining_time").innerText = `remaining_time: ${data.remaining_time}`;
    
    document.getElementById("blue_score").innerText = `蓝队(${data.team_blue}): ${data.score_blue}`;
    document.getElementById("red_score").innerText =  `红队(${data.team_red}): ${data.score_red}`;
};

async function score(team) {
    const response = await fetch(`http://127.0.0.1:8000/score?team=${team}`);
    const data = await response.json();
    console.log(data);
}

async function reset() {
    let team_blue = document.getElementById("team_blue").value;
    let team_red = document.getElementById("team_red").value;
    let time = document.getElementById("time").value;
    const response = await fetch(`http://127.0.0.1:8000/reset?team_blue=${team_blue}&team_red=${team_red}&time=${time}`);
    const data = await response.json();
    console.log(data);
}

async function start() {await fetch(`http://127.0.0.1:8000/start`);}
async function stop() {await fetch(`http://127.0.0.1:8000/stop`);}
async function finish() {await fetch(`http://127.0.0.1:8000/finish`);}