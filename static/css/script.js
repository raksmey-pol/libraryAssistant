async function sendQuery() {
    const queryText = document.getElementById("queryText").value;
    if (!queryText.trim()) {
        return;
    }

    const chatBox = document.getElementById("chatBox");
    const userMessage = document.createElement("div");
    userMessage.className = "message user-message";
    userMessage.innerHTML = `${queryText}<strong style = "border: 5px solid lightgray;
     border-radius: 10px; background-color:lightgray;
     text-shadow: 2px 0 #fff, -2px 0 #fff, 0 2px #fff, 0 -2px #fff,
             1px 1px #fff, -1px -1px #fff, 1px -1px #fff, -1px 1px #fff;"> :YOU</strong>`;
    chatBox.appendChild(userMessage);

    const response = await fetch("/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query_text: queryText })
    });

    const result = await response.json();
    const botMessage = document.createElement("div");
    botMessage.className = "message bot-message";
    botMessage.innerHTML = `<strong style = "border: 5px solid lightgray;
     border-radius: 10px; background-color:lightgray;
     text-shadow: 2px 0 #fff, -2px 0 #fff, 0 2px #fff, 0 -2px #fff,
             1px 1px #fff, -1px -1px #fff, 1px -1px #fff, -1px 1px #fff;">LA: </strong> ${result.response}`;
    chatBox.appendChild(botMessage);

    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById("queryText").value = '';
}