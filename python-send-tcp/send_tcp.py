import socket

def send_gps_data():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 3001))
    
    messages = [
        #"$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A",
        "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
        #"24 24 80 00 25 37 E3 00 A0 13 01 18 07 28 35 02 41 71 15 05 43 86 88 00 00 00 C0 47 00 07 A8 19 28 01 16 A0 1D 00 FF E2 0D"
    ]
    
    for message in messages:
        s.send(message.encode() + b'\r\n')
        print(f"Enviado: {message}")
    
    s.close()

if __name__ == "__main__":
    send_gps_data()