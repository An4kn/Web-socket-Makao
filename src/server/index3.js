const ws = new WebSocket('ws://localhost:8082');

ws.onopen = () => {
    console.log('Połączono z serwerem WebSocket.');

    // Wysyłanie ArrayBuffer
    ws.send(arrayBuffer);

    // Wysyłanie Blob (może być potrzebne krótkie opóźnienie po otwarciu połączenia)
    setTimeout(() => {
        ws.send(blob);
    }, 50);
};

ws.onmessage = (event) => {
    if (event.data instanceof ArrayBuffer) {
        const receivedData = new Uint8Array(event.data);
        console.log('Odebrano dane binarne (ArrayBuffer):', receivedData);
    } else if (event.data instanceof Blob) {
        const reader = new FileReader();
        reader.onload = () => {
            const receivedData = new Uint8Array(reader.result);
            console.log('Odebrano dane binarne (Blob):', receivedData);
        };
        reader.readAsArrayBuffer(event.data);
    } else {
        console.log('Odebrano dane:', event.data); // Jeśli serwer wysłał tekst
    }
};

ws.onerror = (error) => {
    console.error('Błąd WebSocket:', error);
};

ws.onclose = () => {
    console.log('Połączenie WebSocket zamknięte.');
};