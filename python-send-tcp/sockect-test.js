const io = require('socket.io-client');
const socket = io('http://localhost:3069');

// Escuchar actualizaciones en tiempo real
socket.on('gps-data', (data) => {
  console.log('Datos recibidos:', data);
});

// Solicitar datos actuales
socket.emit('request-data');