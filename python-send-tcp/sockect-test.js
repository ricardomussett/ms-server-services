const io = require('socket.io-client');

// Configuration

const SOCKET_URL = 'http://sintrya-demo.pdvsa.app:4000'; // Adjust to your configuration

// Connect to WebSocket server
const socket = io(SOCKET_URL);

// Function to request data with filters
function requestData(filters = {}) {
    const payload = {
        pseudoIPs: filters.pseudoIPs || [], // Now accepts a list of pseudoIPs
    };
    socket.emit('request-data', payload);
}

// handle connection events
socket.on('connect', () => {
    console.log('Connected to WebSocket server');
    
    // Example of using requestData with multiple pseudoIPs
    requestData({
        pseudoIPs: [
            '98.4.201.36',
            '98.4.199.36',
            '98.4.199.37',
            '98.4.199.38',
            '98.4.199.39'
        ],
    });
});

// Listen data-response
socket.on('data-response', (data) => {
    console.log('\nDatos recibidos:');
    console.log(JSON.stringify(data, null, 2));
});

//---------------------------------------------------------------

// Listen Actual Positions
socket.on('positions', (data) => {
    console.log('\nActual Positions:');
    console.log(JSON.stringify(data, null, 2));
});

// Listen Update Positions
socket.on('update-positions', (positions) => {
    console.log('\nUpdate Positions:');
    console.log(JSON.stringify(positions, null, 2));
});

//---------------------------------------------------------------

// handle errors
socket.on('connect_error', (error) => {
    console.error('Error de conexión:', error);
});

socket.on('error', (error) => {
    console.error('Error:', error);
});

// handle disconnect
socket.on('disconnect', (reason) => {
    console.log('Desconectado del servidor:', reason);
});

// keep the process running
process.on('SIGINT', () => {
    console.log('Closing client...');
    socket.disconnect();
    process.exit();
});