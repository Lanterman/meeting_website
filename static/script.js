const token = document.getElementById("token").value;

let ws = new WebSocket(`ws://${window.location.host}/ws/notification`);

ws.onmessage = function(event) {};

async function get_users_mathing_search(token) {
    let url = await fetch(`http://127.0.0.1:8000/search`, {method: "get",
        headers: {'Authorization': `Bearer ${token}`}});
    let response = await url.json();
    return response
};

async function setLike(user_id, token) {
    let url = await fetch(`http://127.0.0.1:8000/${user_id}/set_like`, {method: "get",
        headers: {'Authorization': `Bearer ${token}`}});
    let resp = await url.json();
    document.getElementById(`like_${user_id}`).style.color = "red";
    return resp;
};