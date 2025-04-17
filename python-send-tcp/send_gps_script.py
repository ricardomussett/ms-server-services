import socket
import time
import random
from datetime import datetime
import struct
import binascii




class RopeGpsEmulator:
    def __init__(self, server_ip, server_port, device_id):
        self.server_ip = server_ip
        self.server_port = server_port
        self.device_id = device_id
        self.pseudo_ip = self.generate_pseudo_ip(device_id)
        self.pseudo_ip_str = self.get_pseudo_ip_string()
        self.socket = None
        self.sequence = 1
        
    def connect(self):
        """Establece la conexión TCP con el servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            print(f"Conexión establecida con {self.server_ip}:{self.server_port}")
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False
    
    def generate_pseudo_ip(self, sim_number):
        """Genera la dirección IP pseudo según el algoritmo del protocolo"""
        # Asegurarnos de que tenemos al menos 10 dígitos
        if len(sim_number) == 11:
            sim_number = sim_number[1:]  # Remove first digit if length is 11
        
        # Rellenar con ceros si es necesario para tener 10 dígitos
        sim_number = sim_number.zfill(10)
        
        # Dividir en grupos de 2 dígitos
        groups = [sim_number[i:i+2] for i in range(0, 10, 2)]
        
        # Tomar los últimos 4 grupos (índices 1 a 4)
        last_four = [int(groups[i]) for i in range(1, 5)]
        
        # Procesar el primer grupo
        first_group = int(groups[0]) - 30
        binary_first = format(first_group, '04b')
        
        # Generar los bytes pseudo IP
        pseudo_bytes = []
        for i in range(4):
            last_byte = format(last_four[i], '08b')
            new_byte = binary_first[i] + last_byte[1:]
            pseudo_bytes.append(int(new_byte, 2))
            
        return bytes(pseudo_bytes)
    
    def calculate_xor(self, data):
        """Calcula el checksum XOR para los datos"""
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum
    
    def send_packet(self, packet_type, data=b''):
        """Envía un paquete al servidor"""
        if not self.socket:
            if not self.connect():
                return None

        try:
            # Cabecera básica
            header = b'\x24\x24'
            main_command = packet_type.to_bytes(1, 'big')
            length = len(data).to_bytes(2, 'big')
            
            # Construir paquete completo
            packet = header + main_command + length + self.pseudo_ip + data
            
            # Calcular checksum (desde el byte 2 hasta 9 + length)
            checksum_data = packet[2:9 + len(data)]
            checksum = self.calculate_xor(checksum_data)
            
            # Añadir checksum y footer
            packet += checksum.to_bytes(1, 'big') + b'\x0D'
            
            # Convertir string hexadecimal a bytes
            # hex_packet = "24248000256204c724250416055006010289708665162000000000c04700000000000000000001ff120d"
            # hex_packet = "24248000256204c724000101175125000000000000000000000000004700000000000000000001fffa0d"
            hex_packet = '24248000256204c724250416112036010304868665447000000000c0470000000c0a0000000001ff380d'
            packet = bytes.fromhex(hex_packet)
            
            # Enviar paquete
            self.socket.send(packet)
            print(f"Enviado: {binascii.hexlify(packet).decode('utf-8')}")
            return packet
        except Exception as e:
            print(f"Error al enviar paquete: {e}")
            self.socket = None
            return None
    
    def generate_position_data(self):
        """Genera datos de posición simulados"""
        now = datetime.now()
        
        # Fecha y hora (BCD)
        date_time = bytes([
            (now.year - 2000) // 10 << 4 | (now.year - 2000) % 10,
            now.month // 10 << 4 | now.month % 10,
            now.day // 10 << 4 | now.day % 10,
            now.hour // 10 << 4 | now.hour % 10,
            now.minute // 10 << 4 | now.minute % 10,
            now.second // 10 << 4 | now.second % 10
        ])
        
        # Latitud (30° 37.901' S) - Ejemplo del protocolo
        # Codificación BCD con bit de signo (0 para norte, 1 para sur)
        latitude = bytes([
            0x30,  # Grados (30)
            0x03,  # Primeros dos dígitos de minutos (03)
            0x79,  # Últimos dos dígitos de minutos (79)
            0x01   # Parte fraccional (01)
        ])
        
        # Longitud (130° 45.608' W) - Ejemplo del protocolo
        # Codificación BCD con bit de signo (0 para este, 1 para oeste)
        longitude = bytes([
            0x13,  # Grados (130)
            0x04,  # Primeros dos dígitos de minutos (04)
            0x56,  # Últimos dos dígitos de minutos (56)
            0x08   # Parte fraccional (08)
        ])
        
        # Velocidad (km/h) y ángulo
        # speed = random.randint(0, 120)
        speed = 120  # Ejemplo del protocolo: 120 km/h
        # Codificación BCD para velocidad (ejemplo: 120 km/h -> 0x01, 0x20)
        speed_bcd = bytes([
            0x00,  # Primer byte: 01 (centenas y decenas)
            0x80   # Segundo byte: 20 (unidades y 0)
        ])
        
        # angle = random.randint(0, 359)
        # angle_bcd = bytes([
        #     angle // 100 << 4 | (angle % 100) // 10,
        #     (angle % 10) << 4 | 0x00
        # ])

        angle_bcd = bytes([
            0x01,  # Primer byte: 01 (centenas y decenas)
            0x54   # Segundo byte: 20 (unidades y 0)
        ])
        
        # Estado GPS (localizado, 8 satélites)
        gps_status = 0x80 | 0x08  # Bit 7=1 (localizado), 4 satélites
        
        # Entradas digitales
        digital_inputs = 0x40  # Bit 6=1 (sistema en uso)
        
        # Encendido (random)
        ignition = random.randint(0, 1)
        
        # Resistencia de aceite y voltaje
        oil_resistance = random.randint(100, 500).to_bytes(2, 'big')
        voltage = int((random.uniform(11.5, 14.5) * 100)).to_bytes(2, 'big')
        
        # Kilometraje (metros)
        mileage = random.randint(10000, 10001).to_bytes(4, 'big')
        print(mileage)
        
        # Temperatura (0-40°C)
        # temperature = bytes([0x00, random.randint(0, 40)])
        temperature = bytes([0x00,  0x1E])
        
        # Datos extendidos (opcional)
        extended_data = b''  # Puedes añadir datos extendidos si es necesario
        
        # Construir datos de posición
        position_data = (
            date_time + latitude + longitude + speed_bcd + angle_bcd + 
            bytes([gps_status, digital_inputs, ignition]) + 
            oil_resistance + voltage + mileage + temperature + extended_data
        )
        
        return position_data
    
    def send_heartbeat(self):
        """Envía un paquete de heartbeat"""
        return self.send_packet(0x21, b'\x00')
    
    def send_position(self):
        """Envía datos de posición"""
        position_data = self.generate_position_data()
        return self.send_packet(0x80, position_data)
    
    def send_alarm(self, alarm_type):
        """Envía un paquete de alarma"""
        position_data = self.generate_position_data()
        
        # Tipos de alarma (ver protocolo)
        alarms = {
            'emergency': b'\x01\x01',  # Alarma de emergencia
            'overspeed': b'\x00\x02',  # Exceso de velocidad
            'vibration': b'\x00\x20',  # Alarma de vibración
            'power': b'\x08\x08'       # Problema de potencia
        }
        
        alarm_data = alarms.get(alarm_type, b'\x00\x00')
        return self.send_packet(0x82, position_data + alarm_data)
    
    def send_ibutton_swipe(self, driver_name="Driver1", ibutton_id="000013082D45"):
        """Envía datos de swipe de iButton"""
        status = 0x01  # Modo anti-robo activado
        now = datetime.now()
        
        # Fecha y hora
        date_time = bytes([
            now.year - 2000,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        ])
        
        # Coordenadas (similares a posición)
        latitude = bytes([0x02, 0x41, 0x71, 0x15])
        longitude = bytes([0x05, 0x43, 0x86, 0x88])
        
        # Datos del conductor
        driver_data = f"<{driver_name},{ibutton_id}>".encode('ascii')
        
        # Construir contenido
        content = (
            bytes([status]) + date_time + latitude + longitude + driver_data
        )
        
        return self.send_packet(0x94, bytes([0x0B]) + content)  # 0x0B = Subcomando para swipe
    
    def run(self, interval=30):
        """Ejecuta el emulador con intervalos regulares"""
        try:
            print(f"Emulador GPS iniciado para dispositivo {self.device_id}")
            while True:
                # Enviar heartbeat cada 3 intervalos
                if self.sequence % 3 == 0:
                    self.send_heartbeat()
                
                # Enviar posición regularmente
                self.send_position()
                
                # Enviar alarma ocasionalmente (10% de probabilidad)
                if random.random() < 0.1:
                    alarm_type = random.choice(['emergency', 'overspeed', 'vibration', 'power'])
                    self.send_alarm(alarm_type)
                
                # Enviar swipe de iButton ocasionalmente (5% de probabilidad)
                if random.random() < 0.05:
                    self.send_ibutton_swipe()
                
                time.sleep(interval)
                self.sequence += 1
                
        except KeyboardInterrupt:
            print("\nEmulador detenido")
        finally:
            if self.socket:
                self.socket.close()

    def get_pseudo_ip_string(self):
        """Convierte la pseudo IP en formato string (xxx.xxx.xxx.xxx)"""
        return '.'.join(str(byte) for byte in self.pseudo_ip)

# Configura estos valores según tu entorno
SERVER_IP = 'localhost'  # IP del servidor
SERVER_PORT = 81        # Puerto del servidor
DEVICE_ID = '13512345006'  # Número de SIM del dispositivo

emulator = RopeGpsEmulator(SERVER_IP, SERVER_PORT, DEVICE_ID)
print(emulator.pseudo_ip_str)
emulator.run(3)