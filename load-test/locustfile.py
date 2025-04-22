from locust import HttpUser, task, between
import json
import time

class StatusUser(HttpUser):
    # Tiempo de espera entre peticiones (entre 1 y 5 segundos)
    wait_time = between(1, 5)
    
    # URL base - asegúrate de incluir el protocolo http:// o https://
    host = "http://192.168.1.205:3000"
    
    @task
    def check_status(self):
        # Hacemos una petición GET al endpoint /status
        with self.client.get("/status", name="Status Check", catch_response=True) as response:
            # Verificamos que la respuesta sea exitosa (código 200)
            if response.status_code == 200:
                # Intentamos parsear la respuesta como JSON
                try:
                    data = response.json()
                    
                    # Verificamos que contenga los campos esperados
                    if all(key in data for key in ["status", "database", "redis", "timestamp"]):
                        # Si todo está bien, marcamos la petición como exitosa
                        response.success()
                    else:
                        # Si faltan campos, marcamos la petición como fallida
                        response.failure(f"Respuesta incompleta: {data}")
                        
                except json.JSONDecodeError:
                    # Si no es un JSON válido, marcamos la petición como fallida
                    response.failure("Respuesta no es un JSON válido")
            else:
                # Si el código de estado no es 200, marcamos la petición como fallida
                response.failure(f"Status code incorrecto: {response.status_code}")
    
    # Método que se ejecuta cuando el usuario inicia
    def on_start(self):
        print("Usuario iniciado")
        
    # Método opcional para probar escenarios de fallos
    @task(2)  # Este task tendrá una menor prioridad (ratio 2:1 respecto al principal)
    def check_status_with_delay(self):
        # Simulamos una carga en el servidor esperando un tiempo antes de hacer la petición
        time.sleep(0.5)
        with self.client.get("/status", name="Status Check (Con Delay)", catch_response=True) as response:
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "active":
                    response.success()
                else:
                    response.failure(f"Estado no activo: {data['status']}")