const WebSOcket = require('ws');
const wss = new WebSOcket.Server({ port: 8082 });


wss.on('connection', (ws) => {
    console.log('New client connected!');

    ws.on('message', (data) => {
        const dataString = data.toString();
        console.log('Client has sent us: ${dataString}');

        ws.send(dataString.toUpperCase());
    });

    ws.on('close', (message) => {
        console.log('Client has disconnected!');
    })
});