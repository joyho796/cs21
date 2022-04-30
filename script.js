
window.addEventListener('load', function() {


    document.getElementById('content').onclick = function() {
        document.getElementById('textbox').focus()
    }

    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:5000');

    userNameGiven = null;
    alive = true;

    // Connection opened
    socket.addEventListener('open', function (event) {
        console.log('Connected to the WS Server!')
    });

    // Connection closed
    socket.addEventListener('close', function (event) {
        console.log('Disconnected from the WS Server!')
    });

    // Listen for messages
    socket.addEventListener('message', function (event) {
        console.log('Message from server ', event.data);
    });

    // helper function -- log info to user
    function logInfo(message) {
        document.getElementById('messages').insertAdjacentHTML("afterbegin", "<div>" + message +"</div>");
    }

    // send message from the form
    document.getElementById('inputbox').onsubmit = function() {
        let outgoingMessage = this.message.value;
        this.message.value = ''
        parsedMessage = outgoingMessage.toLowerCase().split(" ");

        if (userNameGiven == null) {
            outgoingMessage = "name " + outgoingMessage.replace(/\s/g, "");
        } else if (alive == false) {
            if (parsedMessage[0] == "restart") {
                outgoingMessage = "restart"
            } else {
                return false
            }
        } else if (parsedMessage[0] == "help") {
            logInfo(">>> === Available Commands ===")
            logInfo(">>> self : check your HP, equipped weapon, and inventory")
            logInfo(">>> attack : attack an enemy. ")
            logInfo(">>> attack [player name] : attack a player.")
            logInfo(">>> chat [message] : send a message to all the other players")
            logInfo(">>> drink : drink a potion to heal your HP")
            logInfo(">>> equip [weapon name] : equip a different weapon")
            logInfo(">>> get [item name] : pick up an item")
            logInfo(">>> give [item name] : pick up an item")
            logInfo(">>> info [item name] : learn more about an item")
            logInfo(">>> look: get information about the room you're in")
            logInfo(">>> move [north, east, south, west] : move to another room")
            logInfo(">>> players : get list of players in the dungeon")
            logInfo(">>> restart : restart the game")
            logInfo(">>> ===")
            return false;
        }

        socket.send(outgoingMessage);
        return false;
    };

    // message received - show the message in div#messages
    socket.onmessage = function(event) {
        let message = event.data;

        messageParsed = message.split(" ")

        if (messageParsed[0] == ">>>") {
            let messageElem = document.createElement('div');
            messageElem.textContent = message;
            document.getElementById('messages').prepend(messageElem);
        } else if (messageParsed[0] == "dead") {
            alive = false
        } else if (messageParsed[0] == "nameTaken") {
            userNameGiven = null;
        } else if (messageParsed[0] == "validName") {
            userNameGiven = messageParsed[1];
            document.getElementById('name').innerHTML = messageParsed[1] + "@dungeon_crawl: ~$&nbsp"
        }
    }

})
