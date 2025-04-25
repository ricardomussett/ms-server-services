const io = require('socket.io-client');

// Configuración
const SOCKET_URL = 'http://47.243.17.75:4069'; // Ajusta según tu configuración

// Conectar al servidor WebSocket
const socket = io(SOCKET_URL);

// Función para solicitar datos con filtros
function requestData(filters = {}) {
    const payload = {
        pseudoIPs: filters.pseudoIPs || [], // Ahora acepta una lista de pseudoIPs
        startDate: filters.startDate,
        endDate: filters.endDate,
        limit: filters.limit
    };
    socket.emit('request-data', payload);
}

// Manejar eventos de conexión
socket.on('connect', () => {
    console.log('Conectado al servidor WebSocket');
    
    // Ejemplo de uso de requestData con múltiples pseudoIPs
    requestData({
        pseudoIPs: [
            '98.4.199.36',
            '98.4.199.37',
            '98.4.199.38',
            '98.4.199.39'
        ],
        startDate: '2024-04-01',  // Ejemplo de fecha inicio
        endDate: '2026-04-21',    // Ejemplo de fecha fin
        limit: 100                // Ejemplo de límite
    });
});

// Escuchar respuesta de request-data
socket.on('data-response', (data) => {
    console.log('\nDatos recibidos:');
    console.log(JSON.stringify(data, null, 2));
});

// Escuchar actualizaciones de posición individuales
socket.on('position', (data) => {
    console.log('\nNueva actualización de posición:');
    console.log(JSON.stringify(data, null, 2));
});

// Escuchar todas las posiciones
socket.on('all-positions', (positions) => {
    console.log('\nTodas las posiciones actuales:');
    console.log(JSON.stringify(positions, null, 2));
});

// Manejar errores
socket.on('connect_error', (error) => {
    console.error('Error de conexión:', error);
});

socket.on('error', (error) => {
    console.error('Error:', error);
});

// Manejar desconexión
socket.on('disconnect', (reason) => {
    console.log('Desconectado del servidor:', reason);
});

// Mantener el proceso corriendo
process.on('SIGINT', () => {
    console.log('Cerrando cliente...');
    socket.disconnect();
    process.exit();
});