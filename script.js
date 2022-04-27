
window.addEventListener('load', function() {


    document.getElementById('content').onclick = function() {
        document.getElementById('textbox').focus()
    }

    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:5000');

    userNameGiven = null;

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

    // Send a msg to the websocket
    const sendMsg = () => {
        socket.send('Hello from Client1!');
    }

    const sendUsrName = () => {
        name = document.getElementById("userName").value
        socket.send('Name,' + name)
    }

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
            userNameGiven = outgoingMessage.replace(/\s/g, "");
            document.getElementById('name').innerHTML = outgoingMessage.replace(/\s/g, "") + "@dungeon_crawl: ~$&nbsp"
            outgoingMessage = "name," + outgoingMessage.replace(/\s/g, "");
        }
        // send message to all others in the server
        else if (parsedMessage[0] == "chat") {
            outgoingMessage = "chat," + outgoingMessage.slice(parsedMessage[0].length)
        // move to another room
        } else if (parsedMessage[0] == "move") {
            if (parsedMessage.length <= 1) {
                logInfo(">>> A direction must be given. You can move north, east, south, or west.");
                return false;
            }
            if (parsedMessage[1] == "north") {
                outgoingMessage = "move,north";
            } else if (parsedMessage[1] == "south") {
                outgoingMessage = "move,south";
            } else if (parsedMessage[1] == "east") {
                outgoingMessage = "move,east";
            } else if (parsedMessage[1] == "west") {
                outgoingMessage = "move,west";
            } else {
                logInfo(">>> Cannot move in that direction. You can move north, east, south, or west.");
                return false;
            }
        // get info on what other players are in the dungeon
        } else if (parsedMessage[0] == "players") {
            outgoingMessage = "players";
        // attack an enemy
        } else if (parsedMessage[0] == "attack") {
            outgoingMessage = "attack"
        // get an item
        } else if (parsedMessage[0] == "get") {
            if (parsedMessage.length == 1) {
                logInfo(">>> An item name must be given. Items include knife, sword, dagger, and potion.");
                return false;
            } else {
                outgoingMessage = "get," + parsedMessage[1];
            }
        // look around room
        } else if (parsedMessage[0] == "look") {
            outgoingMessage = "look"
        // if user wants info on an object
        } else if (parsedMessage[0] == "info") {
            if (parsedMessage.length <= 1) {
                logInfo(">>> An item name must be given. Items include knife, sword, dagger, and potion.");
                return false;
            } else {
                outgoingMessage = "info," + parsedMessage[1][0].toUpperCase() + parsedMessage[1].substring(1)
            }
        // equip weapon
        } else if (parsedMessage[0] == "equip") {
            if (parsedMessage.length <= 1) {
                logInfo(">>> Please choose a weapon to equip.");
                return false;
            } else {
                outgoingMessage = "equip," + parsedMessage[1][0].toUpperCase() + parsedMessage[1].substring(1)
            }
        // info about self
        } else if (parsedMessage[0] == "self") {
            outgoingMessage = "self"
        } else if (parsedMessage[0] == "drink") {
            if (parsedMessage.length <= 1) {
                logInfo(">>> Please choose a potion to drink.");
                return false;
            } else {
                outgoingMessage = "drink," + parsedMessage[1][0].toUpperCase() + parsedMessage[1].substring(1)
            }
        // if given text is not a recognizable command
        } else if (parsedMessage[0] == "help") {
            logInfo(">>> === Available Commands ===")
            logInfo(">>> self : check your HP, equipped weapon, and inventory")
            logInfo(">>> attack : attack an enemy")
            logInfo(">>> drink : drink a potion to heal your HP")
            logInfo(">>> chat [message] : send a message to all the other players")
            logInfo(">>> equip [weapon name] : equip a different weapon")
            logInfo(">>> get [item name] : pick up an item")
            logInfo(">>> info [item name] : learn more about an item")
            logInfo(">>> look: get information about the room you're in")
            logInfo(">>> move [north, east, south, west] : move to another room")
            return false;
        } else {
            logInfo(">>> Command given not recognized. Type help to see commands. ");
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

        } else if (messageParsed[0] == "heal") {
            amount = parseInt(messageParsed[1], 10)
            player.heal(amount)
            logInfo(">>> You healed " + amount + " hp. ")
        }
    }

})
