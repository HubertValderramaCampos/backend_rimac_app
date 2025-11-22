# DIGEMID Medicine Search API

API REST para buscar medicamentos en el Observatorio de Productos Farmacéuticos de DIGEMID (Perú).

Esta API utiliza web scraping con Selenium para obtener información en tiempo real sobre precios y disponibilidad de medicamentos en farmacias y boticas a nivel nacional.

## Características

- 🔍 Búsqueda de medicamentos por nombre
- 📍 Filtrado por ubicación (departamento, provincia, distrito)
- 💰 Obtención de precios unitarios actualizados
- 🏥 Información de farmacias/boticas y laboratorios
- 🚀 API RESTful con FastAPI
- 📚 Documentación interactiva con Swagger UI
- 🤖 Web scraping automatizado con Selenium
- 🧅 **Soporte para Tor** (anonimato y evitar bloqueos)

## Requisitos Previos

- Python 3.8 o superior
- Google Chrome instalado
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado)**

```bash
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Copiar el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Editar `.env` según tus necesidades:

```env
HOST=0.0.0.0
PORT=8000
HEADLESS_MODE=true
TIMEOUT=30
```

## Uso

### Iniciar el servidor

**Opción 1: Usando el script run.py**

```bash
python run.py
```

**Opción 2: Usando uvicorn directamente**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: `http://localhost:8000`

### Documentación Interactiva

Una vez iniciado el servidor, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### POST /api/v1/medicines/search

Busca medicamentos en DIGEMID.

**Request Body:**

```json
{
  "nombre_medicamento": "APRONAX",
  "departamento": "LIMA",
  "provincia": "LIMA",
  "distrito": "PUENTE PIEDRA",
  "limite_resultados": 10
}
```

**Response:**

```json
{
  "success": true,
  "message": "Búsqueda completada exitosamente",
  "total_encontrados": 10,
  "resultados": [
    {
      "tipo_establecimiento": "Privado",
      "fecha_actualizacion": "23/10/2025 07:44:00 PM",
      "producto": "NAPROXENO SODICO 550 mg Tableta Recubierta x 100 unid.",
      "laboratorio": "MEDROCK CORPORATION SOCIEDAD ANONIMA CERRADA",
      "farmacia_botica": "INKAFARMA",
      "precio_unitario": 0.23
    }
  ],
  "error": null
}
```

### Ejemplos de uso

**Con cURL:**

```bash
curl -X POST "http://localhost:8000/api/v1/medicines/search" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_medicamento": "APRONAX",
    "departamento": "LIMA",
    "provincia": "LIMA",
    "distrito": "PUENTE PIEDRA",
    "limite_resultados": 10
  }'
```

**Con Python (requests):**

```python
import requests

url = "http://localhost:8000/api/v1/medicines/search"
data = {
    "nombre_medicamento": "APRONAX",
    "departamento": "LIMA",
    "provincia": "LIMA",
    "distrito": "PUENTE PIEDRA",
    "limite_resultados": 10
}

response = requests.post(url, json=data)
print(response.json())
```

**Con JavaScript (fetch):**

```javascript
const url = 'http://localhost:8000/api/v1/medicines/search';
const data = {
  nombre_medicamento: 'APRONAX',
  departamento: 'LIMA',
  provincia: 'LIMA',
  distrito: 'PUENTE PIEDRA',
  limite_resultados: 10
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Estructura del Proyecto

```
backend_rimac/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal FastAPI
│   ├── config.py              # Configuración de la aplicación
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── medicines.py   # Rutas del API
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Modelos Pydantic
│   └── services/
│       ├── __init__.py
│       └── digemid_scraper.py # Servicio de scraping
├── .env                       # Variables de entorno (no incluir en git)
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore               # Archivos ignorados por git
├── requirements.txt         # Dependencias del proyecto
├── run.py                  # Script para ejecutar la aplicación
└── README.md              # Documentación
```

## Parámetros de Búsqueda

### Departamentos disponibles

AMAZONAS, ANCASH, APURIMAC, AREQUIPA, AYACUCHO, CAJAMARCA, CALLAO, CUSCO, HUANCAVELICA, HUANUCO, ICA, JUNIN, LA LIBERTAD, LAMBAYEQUE, LIMA, LORETO, MADRE DE DIOS, MOQUEGUA, PASCO, PIURA, PUNO, SAN MARTIN, TACNA, TUMBES, UCAYALI

### Provincias de Lima

LIMA, BARRANCA, CAJATAMBO, CANTA, CAÑETE, HUARAL, HUAROCHIRI, HUAURA, OYON, YAUYOS

## Configuración Avanzada

### Modo Headless

Por defecto, el navegador se ejecuta en modo headless (sin interfaz gráfica). Para ver el navegador durante la ejecución:

```env
HEADLESS_MODE=false
```

### Timeout

Ajustar el tiempo de espera máximo (en segundos):

```env
TIMEOUT=45
```

### Tor (Anonimato y Evitar Bloqueos)

Esta API incluye soporte completo para la red Tor, permitiendo:
- 🔒 Navegación anónima
- 🌐 Evitar bloqueos por IP
- 🔄 Rotación de identidad automática

**Configuración rápida:**

1. **Instalar Tor**:
   - Windows: Descarga Tor Browser desde https://www.torproject.org/download/
   - Linux: `sudo apt install tor`
   - macOS: `brew install tor`

2. **Habilitar en `.env`**:
   ```env
   USE_TOR=true
   TOR_PORT=9050  # 9150 si usas Tor Browser
   ```

3. **Iniciar Tor**:
   - Tor Browser: Simplemente abre el navegador
   - Servicio Tor: `systemctl start tor` (Linux) o `net start tor` (Windows)

4. **Verificar**:
   ```bash
   python test_tor.py
   ```

**Documentación completa**: Ver [TOR_SETUP.md](TOR_SETUP.md) para instrucciones detalladas.

**Ejemplo de uso en código**:
```python
from app.services.digemid_scraper import DigemidScraper

scraper = DigemidScraper(use_tor=True, tor_port=9050)
resultado = scraper.search_medicines("PARACETAMOL")
```

## Solución de Problemas

### Verificación del Sistema

Antes de reportar un problema, ejecuta el script de diagnóstico:

```bash
python check_chrome.py
```

Este script verificará:
- Instalación de Google Chrome
- Instalación de Selenium
- Funcionamiento de ChromeDriver
- Conectividad del navegador

### Error: "%1 no es una aplicación Win32 válida" (Windows)

Este error ocurre cuando ChromeDriver tiene problemas en Windows. Soluciones:

1. **Ejecutar el script de diagnóstico:**
   ```bash
   python check_chrome.py
   ```

2. **Reinstalar ChromeDriver:**
   ```bash
   pip uninstall webdriver-manager -y
   pip install webdriver-manager --upgrade
   ```

3. **Verificar que Chrome esté instalado:**
   - Descargar desde: https://www.google.com/chrome/
   - Asegurarse de que esté en la ruta predeterminada

4. **Limpiar caché de ChromeDriver:**
   - Windows: Eliminar `C:\Users\{usuario}\.wdm\`
   - Ejecutar nuevamente la aplicación

### Chrome WebDriver no se encuentra

El sistema descarga automáticamente el ChromeDriver usando `webdriver-manager`. Si hay problemas:

1. Verificar que Google Chrome esté instalado
2. Verificar conexión a internet
3. Intentar actualizar webdriver-manager: `pip install --upgrade webdriver-manager`
4. Ejecutar: `python check_chrome.py`

### Error de timeout

Si las búsquedas fallan por timeout:

1. Aumentar el valor de `TIMEOUT` en `.env` (ej: 45 o 60)
2. Verificar la conexión a internet
3. Verificar que la página de DIGEMID esté disponible
4. Desactivar el modo headless temporalmente: `HEADLESS_MODE=false`

### Error de módulo no encontrado

Asegurarse de que todas las dependencias estén instaladas:

```bash
pip install -r requirements.txt --upgrade
```

### La página no carga correctamente

1. Probar con modo headless desactivado:
   ```env
   HEADLESS_MODE=false
   ```
2. Verificar que la URL de DIGEMID esté accesible
3. Revisar los logs del servidor para más detalles

## Consideraciones

- Este proyecto realiza web scraping de un sitio público
- Los tiempos de respuesta dependen de la velocidad de la página de DIGEMID
- Se recomienda implementar rate limiting en producción
- Los selectores CSS pueden cambiar si DIGEMID actualiza su sitio web

## Licencia

MIT License

## Autor

Backend RIMAC

## Contacto

Para consultas o reportar problemas, contactar a: support@example.com
# backend_rimac_app
