


window.addEventListener('load', function() {  

    document.getElementById('content').onclick = function() {
        document.getElementById('textbox').focus()
    }

    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:5000');

    class Player {
        constructor() {
            this.hp = 100
            this.weapons = []
            this.potions = []
            this.currentWeapon = "Knife"
        }

        addWeapon(weaponName) {
            this.weapons.push(weaponName)
        }

        addPotion(potionName) {
            this.potions.push(weaponName)
        }

        getHP() { return this.hp; }
        getWeapon() { return this.currentWeapon; }
    }

    player = new Player();

    userNameGiven = false;

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

        if (!userNameGiven){
            userNameGiven = true;
            document.getElementById('name').innerHTML = outgoingMessage + "@dungeon_crawl: ~$&nbsp"
            outgoingMessage = "name," + outgoingMessage;

        }

        // send message to all others in the server
        else if (parsedMessage[0] == "chat") {
            outgoingMessage = "chat," + outgoingMessage.slice(parsedMessage[0].length)
        // move to another room
        } else if (parsedMessage[0] == "move") {
            if (parsedMessage.length <= 1) {
                logInfo(">>> A direction must be given.");
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
                logInfo(">>> Cannot move in that direction.");
                return false;
            }
        // get info on what other players are in the dungeon
        } else if (parsedMessage[0] == "players") {
            outgoingMessage = "players";
        // attack an enemy
        } else if (parsedMessage[0] == "attack") {
            if (parsedMessage.length == 1) {
                outgoingMessage = "attack," + player.getWeapon();
            } else {
                outgoingMessage = "attack," + parsedMessage[1] + "," + player.getWeapon();
            }
        // get an item
        } else if (parsedMessage[0] == "get") {
            if (parsedMessage.length == 1) {
                logInfo(">>> An item name must be given.");
                return false;
            } else {
                outgoingMessage = "get," + parsedMessage[1];
            }
        // if given text is not a recognizable command
        
        // if given text is not a recognizable command
        } else if (parsedMessage[0] == "help") {
            logInfo(">>> Commands available: chat, move, attack, get, players")
        } else {
            logInfo(">>> Command given not recognized.");
            return false;
        }

        socket.send(outgoingMessage);
        return false;
    };

    // message received - show the message in div#messages
    socket.onmessage = function(event) {
        let message = event.data;

        

        let messageElem = document.createElement('div');
        messageElem.textContent = message;
        document.getElementById('messages').prepend(messageElem);
    }

})