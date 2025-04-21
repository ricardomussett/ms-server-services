import websocket
import json

# Función para manejar los mensajes recibidos
def on_message(ws, message):
    data = json.loads(message)
    if data.get('event') == 'gps-data':
        print('Datos recibidos:', data.get('data'))

# Función para manejar errores
def on_error(ws, error):
    print('Error:', error)

# Función para manejar la conexión cerrada
def on_close(ws, close_status_code, close_msg):
    print('Conexión cerrada')

# Función para manejar la conexión abierta
def on_open(ws):
    print('Conexión establecida')
    # Solicitar datos actuales
    ws.send(json.dumps({
        'event': 'request-data'
    }))

# Crear un cliente WebSocket
ws = websocket.WebSocketApp('ws://localhost:3069',
                          on_message=on_message,
                          on_error=on_error,
                          on_close=on_close,
                          on_open=on_open)

# Ejecutar el cliente WebSocket
ws.run_forever()