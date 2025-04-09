import socket

def send_gps_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 3001))
    
    messages = [
        "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A",
        #"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
    ]
    
    for message in messages:
        s.send(message.encode() + b'\r\n')
        print(f"Enviado: {message}")
    
    s.close()

if __name__ == "__main__":
    send_gps_data()