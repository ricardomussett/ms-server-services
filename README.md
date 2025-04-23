# MS Server Services

Este proyecto implementa un sistema de servicios para el manejo de datos GPS a través de TCP, utilizando una arquitectura moderna con contenedores Docker.

## 🚀 Características

- Base de datos PostgreSQL con PostGIS para almacenamiento geoespacial
- Redis para manejo de colas y caché
- PgBouncer para pooling de conexiones
- Herramientas de administración (pgAdmin y Redis Commander)
- Scripts de prueba y carga

## 🛠️ Requisitos

- Docker
- Docker Compose
- Python 3.x
- Node.js (para pruebas)

## 🏗️ Estructura del Proyecto

```
ms-server-services/
├── data-base/              # Configuración de base de datos
│   └── docker-compose.yml  # Configuración de servicios Docker
├── load-test/              # Scripts de pruebas de carga
│   ├── locustfile.py      # Pruebas de carga HTTP
│   └── locustfiletcp.py   # Pruebas de carga TCP
└── python-send-tcp/        # Scripts de envío de datos
    ├── send_gps_script.py # Script principal de envío GPS
    └── sockect-test.js    # Pruebas de socket
```

## 🔑 Credenciales de Acceso

### PostgreSQL
- **Host**: localhost
- **Puerto**: 5432
- **Base de datos**: msservergpstcp
- **Usuario**: postgres
- **Contraseña**: postgres

### PgBouncer
- **Host**: localhost
- **Puerto**: 6432
- **Base de datos**: msservergpstcp
- **Usuario**: postgres
- **Contraseña**: postgres

### pgAdmin
- **URL**: http://localhost:5433
- **Email**: admin@admin.com
- **Contraseña**: admin

### Redis Commander
- **URL**: http://localhost:8081
- **No requiere autenticación**

### Redis
- **Host**: localhost
- **Puerto**: 6379
- **Bases de datos**:
  - 0: bull
  - 1: truck
- **No requiere autenticación**

## 🚀 Inicio Rápido

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd ms-server-services
```

2. Iniciar los servicios:
```bash
cd data-base
docker-compose up -d
```

3. Acceder a las herramientas de administración:
- pgAdmin: http://localhost:5433
- Redis Commander: http://localhost:8081

## 📊 Servicios Disponibles

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| PostgreSQL | 5432 | Base de datos principal |
| PgBouncer | 6432 | Pool de conexiones |
| Redis | 6379 | Caché y colas |
| pgAdmin | 5433 | Interfaz de administración |
| Redis Commander | 8081 | Monitor de Redis |

## 🧪 Pruebas

### Pruebas de Carga
```bash
cd load-test
locust -f locustfile.py
```

### Envío de Datos GPS
```bash
cd python-send-tcp
python send_gps_script.py
```

## 🔧 Configuración

### Variables de Entorno
- PostgreSQL:
  - DB: msservergpstcp
  - User: postgres
  - Password: postgres

- Redis:
  - Puerto: 6379
  - Bases de datos: 2 (bull, truck)

