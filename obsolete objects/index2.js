const http = require('http');
const { WebSocketServer } = require('ws');

const url = require('url');
const uuidv4 = require('uuid').v4;

const server = http.createServer();
const wsServer = new WebSocketServer({ server});
const port = 8000;

const connections = {};
const users = {};

const broadcast = () => {
    Object.keys(connections).forEach((uuid) => {
        const connection = connections[uuid];
        const message = JSON.stringify(users)
        connection.send(message);
        //Tylko wysylac dane dotyczace sesji SessionGameID
    })
}

const handleMessage = (bytes,uuid) => {
    const message = JSON.parse(bytes.toString());
    const user = users[uuid];
    user.state = message;

    broadcast()

    console.log(message);
}
const handleClose = (uuid) => {
    delete connections[uuid]
    delete users[uuid]
    broadcast()
}

wsServer.on('connection', (connection,request) => {
    const{username} = url.parse(request.url, true).query;
    const uuid = uuidv4();
    console.log(username);
    console.log(uuid);

    connections[uuid] = connection;

    users[uuid] = {
        username: username,
        state: {
            x: 0,
            y: 0,
            SessionGameID: 0// mysle zeby sprawidzc czy jest juz ustalony jak nie no to wtedy wpisac
            
        },
    }
    connection.on('message', message => handleMessage(message, uuid))
    connection.on('close', () => handleClose(uuid))
})

server.listen(port, () => {
    console.log(`Server is listening on port ${port}`);
});

