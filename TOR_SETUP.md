# Guía de Configuración de Tor

## ¿Qué es Tor y por qué usarlo?

**Tor (The Onion Router)** es una red que permite navegar de forma anónima. Al integrar Tor con este scraper:

- 🔒 **Anonimato**: Tu IP real no es visible
- 🌐 **Evita bloqueos**: Cambia de IP cuando sea necesario
- 🚀 **Mejor acceso**: Sortea restricciones geográficas
- 🛡️ **Protección**: Dificulta el rastreo de actividades de scraping

## Instalación de Tor

### Windows

#### Opción 1: Tor Browser (Recomendado para principiantes)

1. **Descargar Tor Browser**
   - Ve a: https://www.torproject.org/download/
   - Descarga la versión para Windows
   - Instala normalmente

2. **Iniciar Tor**
   - Abre Tor Browser
   - Espera a que se conecte
   - Deja el navegador abierto (el servicio Tor correrá en segundo plano)

3. **Verificar el puerto**
   - Por defecto, Tor Browser usa el puerto **9150**
   - Actualiza tu `.env`:
   ```env
   USE_TOR=true
   TOR_PORT=9150
   ```

#### Opción 2: Tor Expert Bundle (Para usuarios avanzados)

1. **Descargar Tor Expert Bundle**
   - Ve a: https://www.torproject.org/download/tor/
   - Descarga "Expert Bundle" para Windows
   - Descomprime en `C:\Tor\`

2. **Crear archivo de configuración**

   Crea `C:\Tor\torrc` con este contenido:
   ```
   SOCKSPort 9050
   ControlPort 9051
   DataDirectory C:\Tor\data
   ```

3. **Iniciar Tor manualmente**
   ```bash
   cd C:\Tor
   tor.exe -f torrc
   ```

4. **Configurar como servicio (opcional)**
   - Ejecuta como Administrador:
   ```bash
   tor.exe --service install -options -f C:\Tor\torrc
   net start tor
   ```

### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tor

# Iniciar servicio
sudo systemctl start tor
sudo systemctl enable tor

# Verificar estado
sudo systemctl status tor
```

### macOS

```bash
# Usando Homebrew
brew install tor

# Iniciar Tor
brew services start tor

# O ejecutar directamente
tor
```

## Configuración del Proyecto

### 1. Instalar dependencias

```bash
pip install stem PySocks
# O simplemente
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Edita el archivo `.env`:

```env
# Habilitar Tor
USE_TOR=true

# Puerto SOCKS de Tor (9050 para servicio, 9150 para Tor Browser)
TOR_PORT=9050

# Puerto de control (opcional, para renovar identidad)
TOR_CONTROL_PORT=9051
```

### 3. Verificar instalación

Ejecuta el script de prueba:

```bash
python test_tor.py
```

Este script verificará:
- ✓ Si Tor está corriendo
- ✓ Si la conexión funciona
- ✓ Tu IP a través de Tor

## Uso

### Opción 1: A través de la API

1. **Iniciar el servidor**:
   ```bash
   python run.py
   ```

2. **Hacer petición** (Tor se usa automáticamente si está habilitado):
   ```bash
   curl -X POST "http://localhost:8000/api/v1/medicines/search" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre_medicamento": "PARACETAMOL",
       "limite_resultados": 5
     }'
   ```

### Opción 2: Directamente en código Python

```python
from app.services.digemid_scraper import DigemidScraper

# Crear scraper con Tor habilitado
scraper = DigemidScraper(
    headless=False,
    timeout=60,
    use_tor=True,      # <-- Habilitar Tor
    tor_port=9050
)

# Realizar búsqueda
resultado = scraper.search_medicines(
    nombre_medicamento="PARACETAMOL",
    departamento="LIMA",
    provincia="LIMA",
    distrito="PUENTE PIEDRA",
    limit=10
)

print(resultado)
```

## Verificación

### Comprobar que Tor está funcionando

```python
import requests

# Sin Tor
response = requests.get('https://api.ipify.org?format=json')
print(f"Tu IP normal: {response.json()['ip']}")

# Con Tor
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}
response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
print(f"Tu IP con Tor: {response.json()['ip']}")
```

### Verificar en navegador

1. Inicia Tor
2. Configura tu navegador para usar proxy SOCKS5 en `127.0.0.1:9050`
3. Ve a: https://check.torproject.org/
4. Deberías ver: "Congratulations. This browser is configured to use Tor."

## Solución de Problemas

### Error: "No se pudo conectar a Tor"

1. **Verificar que Tor esté corriendo**:
   ```bash
   # Windows (PowerShell)
   Get-Process tor

   # Linux/Mac
   ps aux | grep tor
   ```

2. **Verificar el puerto**:
   - Tor Browser usa puerto **9150**
   - Tor Service usa puerto **9050**
   - Actualiza `TOR_PORT` en `.env` según corresponda

3. **Firewall bloqueando**:
   - Agrega excepción para Tor en Windows Firewall
   - O deshabilita temporalmente para probar

### Error: "Connection refused"

El servicio Tor no está corriendo:

```bash
# Windows (si instalaste como servicio)
net start tor

# Linux
sudo systemctl start tor

# O ejecuta Tor Browser
```

### Tor muy lento

1. **Esperar más tiempo**: La red Tor es más lenta que una conexión directa
2. **Aumentar timeout**: En `.env` pon `TIMEOUT=90`
3. **Renovar identidad**: El scraper lo hace automáticamente si es necesario

### No se puede instalar stem o PySocks

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar manualmente
pip install stem==1.8.2
pip install PySocks==1.7.1
```

## Mejores Prácticas

### 1. No abusar de Tor

- Usa Tor solo cuando sea necesario
- Respeta la red (no hagas scraping masivo con Tor)
- Considera donar al Tor Project: https://donate.torproject.org/

### 2. Combinar con delays

```python
# En tu código, agrega delays entre peticiones
import time

scraper = DigemidScraper(use_tor=True)

for medicamento in ["PARACETAMOL", "IBUPROFENO"]:
    resultado = scraper.search_medicines(medicamento)
    print(resultado)
    time.sleep(10)  # Esperar 10 segundos entre búsquedas
```

### 3. Renovar identidad periódicamente

El `TorManager` puede solicitar nuevas identidades:

```python
from app.services.tor_manager import TorManager

tor = TorManager()
tor.start_tor()

# Después de varias peticiones
tor.get_new_identity()  # Cambia la IP
```

## Desactivar Tor

Si quieres volver a conexión normal:

```env
USE_TOR=false
```

O al crear el scraper:

```python
scraper = DigemidScraper(use_tor=False)
```

## Recursos Adicionales

- **Tor Project**: https://www.torproject.org/
- **Documentación Stem**: https://stem.torproject.org/
- **FAQ Tor**: https://support.torproject.org/

## Advertencias Legales

- Usar Tor es legal en la mayoría de países
- El web scraping debe hacerse de forma responsable
- Respeta los términos de servicio de los sitios web
- No uses Tor para actividades ilegales

## Contacto

Para problemas con Tor en este proyecto, revisa:
- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- Issues: https://github.com/tu-repo/issues
