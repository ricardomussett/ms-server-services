from locust import User, task, between
import socket
import struct
import random
import time

class TcpClient:
    def __init__(self, host, port):
        self.host = "192.168.1.205"
        self.port = 81
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def send_packet(self):
        # Paquete fijo en formato hexadecimal
        hex_packet = '24248000256204c724250416112036010304868665447000000000c0470000000c0a0000000001ff380d'
        packet = bytes.fromhex(hex_packet)
        
        # Enviar paquete
        self.socket.send(packet)
        
        # Recibir respuesta
        response = self.socket.recv(1024)
        return response

class TcpUser(User):
    wait_time = between(28, 32)  # Tiempo de espera entre tareas
    
    def on_start(self):
        self.client = TcpClient("localhost", 81)  # Ajustar host y puerto según necesidad
        self.client.connect()
    
    def on_stop(self):
        self.client.disconnect()
    
    @task
    def send_gps_packet(self):
        start_time = time.time()
        try:
            response = self.client.send_packet()
            self.environment.events.request.fire(
                request_type="TCP",
                name="send_gps_packet",
                response_time=int((time.time() - start_time) * 1000),
                response_length=len(response),
                exception=None
            )
        except Exception as e:
            self.environment.events.request.fire(
                request_type="TCP",
                name="send_gps_packet",
                response_time=int((time.time() - start_time) * 1000),
                response_length=0,
                exception=e
            ) 