const converter = new showdown.Converter();
let ws;
let response = "";
let conversationStarted = false;
let username = "";
let dontScroll = false;

function signIn(event){
    event.preventDefault();
    usernameInput = document.getElementById("username-input");
    if (usernameInput.value == "") return;
    username = usernameInput.value
    startChat();
}
 
function startChat() {
    document.getElementById("signin-form").classList.add("d-none");
    document.getElementById("chat-form").classList.remove("d-none");
    document.getElementById("messageText").focus();
    connect();
}

function pickBot(bot){
    messageText.value = "!bot " + bot;
    messageText.focus();
    submitMessage();
    messageText.value = "";
    messageText.focus();
    return false;
}

function pickModel(model){
    messageText.value = "!model " + model;
    messageText.focus();
    submitMessage();
    messageText.value = "";
    messageText.focus();
    return false;
}


function setButtons(value, disabled_send, disable_retry) {
    var sendButton = document.getElementById('send');
    sendButton.innerHTML = value;
    sendButton.disabled = disabled_send
    if(disabled_send) {
        sendButton.classList.add("blink_me");
    } else {
        sendButton.classList.remove("blink_me");
    }

    var retryButton = document.getElementById('retry');
    retryButton.disabled = disable_retry;
}

function sendRetry(){
    if (!ws) return;
    dontScroll = false;
    ws.send("###RETRY###");
    setButtons("{{ res.BUTTON_PROCESSING }}", true, true)
}

function localCommandHandled(query) {
    if(query.toLowerCase() === "!clear")
    {
        var messages = document.getElementById('messages');
        messages.innerHTML = "";
        return true;
    }
    return false;
}

function submitMessage(){
    if (!ws) return;

    dontScroll = false;

    var message = document.getElementById('messageText').value;
    if (message === "") return;
    document.getElementById('messageText').value = "";
 
    if (localCommandHandled(message)) return

    ws.send(message);

    setButtons("{{ res.BUTTON_PROCESSING }}", true, true)
}

function sendMessage(event) {
    event.preventDefault();
    submitMessage()
}

function connect() {
    ws = new WebSocket("{{ wsurl }}/chat/" + encodeURI(username));
    ws.onmessage = function (event) {
        var messages = document.getElementById('messages');
        var data = JSON.parse(event.data);
        if (data.sender === "bot") {
            handleResBotResponse(data ,messages)
        } else {
            var senderdiv = document.createElement('div');
            senderdiv.className = 'client-message-sender';
            senderdiv.innerHTML = username;
            messages.appendChild(senderdiv);
            var div = document.createElement('div');
            div.className = 'client-message';
            div.innerHTML = converter.makeHtml(data.message);
            messages.appendChild(div);
        }
        // Scroll to the bottom of the chat
        if (!dontScroll){
            messages.scrollTop = messages.scrollHeight;
        }
    };
    ws.onopen = function() {
        setButtons("{{ res.BUTTON_SEND }}", false, true);
    };

    ws.onclose = function(e) {
        setButtons("{{ res.BUTTON_WAIT }}", true, true);
        console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
        setTimeout(function() {
            connect();
        }, 1000);
    };
}

function handleResBotResponse(data, messages) {
    switch(data.type) {
        case "start":
            response = "";
            var senderdiv = document.createElement('div');
            senderdiv.className = 'server-message-sender';
            senderdiv.innerHTML = "{{ conf.BOT_NAME }}";
            messages.appendChild(senderdiv);
            var div = document.createElement('div');
            div.className = 'server-message';
            messages.appendChild(div);
            response += data.message;
            div.innerHTML = converter.makeHtml(response);
            conversationStarted = true;
            break;

        case "restart":
            response = "";
            var div = messages.lastChild;
            // edge case: if LLM has previously emitted stop
            // token without sending content create bot bubble
            if (!div.classList.contains("server-message"))
            {
                var senderdiv = document.createElement('div');
                senderdiv.className = 'server-message-sender';
                senderdiv.innerHTML = "{{ conf.BOT_NAME }}";
                messages.appendChild(senderdiv);
                div = document.createElement('div');
                div.className = 'server-message';
                messages.appendChild(div);
            }
            response += data.message;
            div.innerHTML = converter.makeHtml(response);
            conversationStarted = true;
            break;

        case "stream":
            setButtons("{{ res.BUTTON_TYPING }}", true, true);
            var div = messages.lastChild;
            response += data.message;
            div.innerHTML = converter.makeHtml(response)
            break;

        case "end":
            // edge case: if LLM has emitted stop token without
            // sending content don't modify lastChild
            if (conversationStarted == true) {
                var div = messages.lastChild;
                div.innerHTML = converter.makeHtml(response);
            }
            conversationStarted = false;
            setButtons("{{ res.BUTTON_SEND }}", false, false);
            break;

        case "info":
            if (data.message=="Configuration changed") {
                window.location.search = '?u=' + username;
            }
            dontScroll = false;
            var div = document.createElement('div');
            div.className = 'info-message';
            div.innerHTML = converter.makeHtml(data.message);
            messages.appendChild(div);
            conversationStarted = false;
            setButtons("{{ res.BUTTON_SEND }}", false, true);
            break;

        case "error":
            var div = document.createElement('div');
            div.className = 'error-message';
            div.innerHTML = converter.makeHtml(data.message);
            messages.appendChild(div);
            conversationStarted = false;
            setButtons("{{ res.BUTTON_SEND }}", false, true);
            break;

    }    
}


document.addEventListener("DOMContentLoaded", function(event) {
    let messages=document.getElementById("messages");
    ['touchmove','mousedown','select','wheel'].forEach((evt) => {
        messages.addEventListener(evt, (e) => {
            if(Math.floor(messages.scrollTop) === Math.floor(messages.scrollHeight - messages.offsetHeight)) {
                dontScroll = false;
            }
            else{
                dontScroll = true;
            }
        });
    });

    const urlParams = new URLSearchParams(window.location.search);
    const qsUser = urlParams.get('u');
    if (qsUser) {
        username = qsUser
        startChat();
    }
});