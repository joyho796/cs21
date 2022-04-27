


window.addEventListener('load', function() {

    document.getElementById('content').onclick = function() {
        document.getElementById('textbox').focus()
    }

    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:5000');

    class Player {
        constructor() {
            this.hp = 100
            this.weapons = ["Knife"]
            this.potions = []
            this.currentWeapon = "Knife"
        }

        addWeapon(weaponName) {
            this.weapons.push(weaponName)
        }

        addPotion(potionName) {
            this.potions.push(potionName)
        }

        takeDamge(amount) {
            this.hp -= amount
        }

        heal(amount) {
            this.hp += amount
        }

        getHP() { return this.hp; }
        getWeapon() { return this.currentWeapon; }

        getInventory() {
            var weaponsList = "Weapons: "
            var potionsList = "Potions: "

            for (var i = 0; i < this.weapons.length; i++) {
                weaponsList += this.weapons[i]
            }

            for (var j = 0; j < this.potions.length; j++) {
                potionsList += this.potions[j]
            }

            return [weaponsList, potionsList]
        }

        equip(weaponName) {
            if (this.weapons.includes(weaponName)) {
                this.currentWeapon = weaponName
                return true
            } else {
                return false
            }
        }
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
        // look around room
        } else if (parsedMessage[0] == "look") {
            outgoingMessage = "look"
        // if user wants info on an object
        } else if (parsedMessage[0] == "info") {
            outgoingMessage = "info," + parsedMessage[1][0].toUpperCase() + parsedMessage[1].substring(1)
        // check current inventory
        } else if (parsedMessage[0] == "inventory") {
            inventory = player.getInventory()
            logInfo(">>> " + inventory[0])
            logInfo(">>> " + inventory[1])
        // equip weapon
        } else if (parsedMessage[0] == "equip") {
            weaponName = parsedMessage[1][0].toUpperCase() + parsedMessage[1].substring(1)
            var success = player.equip(weaponName)
            if (success) {
                logInfo(">>> You equipped a " + parsedMessage[1] + ".")
            } else {
                logInfo(">>> You don't have that. ")
            }
        // if given text is not a recognizable command
        } else if (parsedMessage[0] == "help") {
            logInfo(">>> Commands available: attack, chat, equip, get, info, inventory, look, move. ")
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
