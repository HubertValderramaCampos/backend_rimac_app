# Solución al Error: "%1 no es una aplicación Win32 válida"

## 🔍 Descripción del Problema

Este error ocurre cuando ChromeDriver no puede ejecutarse correctamente en Windows. Generalmente se debe a:
- ChromeDriver corrupto o mal descargado
- Incompatibilidad de versiones entre Chrome y ChromeDriver
- Caché de webdriver-manager corrupto

## ✅ Solución Paso a Paso

### Paso 1: Ejecutar el Script de Diagnóstico

```bash
python check_chrome.py
```

Este script te mostrará exactamente qué está mal.

### Paso 2: Limpiar el Caché de ChromeDriver

**Windows:**
1. Presiona `Windows + R`
2. Escribe: `%USERPROFILE%\.wdm`
3. Presiona Enter
4. Elimina toda la carpeta `.wdm`

O desde la terminal:
```bash
rmdir /s /q "%USERPROFILE%\.wdm"
```

### Paso 3: Reinstalar webdriver-manager

```bash
pip uninstall webdriver-manager selenium -y
pip install selenium==4.15.2
pip install webdriver-manager==4.0.1
```

### Paso 4: Verificar la Instalación de Chrome

1. Abre Chrome
2. Ve a: `chrome://version/`
3. Anota la versión (ej: 120.0.6099.109)
4. Asegúrate de que Chrome esté actualizado

### Paso 5: Reiniciar el Servidor

```bash
python run.py
```

## 🔧 Solución Alternativa

Si los pasos anteriores no funcionan, puedes usar la versión sin caché de ChromeDriver:

### Editar el archivo `.env`:

```env
HOST=0.0.0.0
PORT=8000
HEADLESS_MODE=false
TIMEOUT=30
```

Nota: `HEADLESS_MODE=false` te permitirá ver qué está pasando en el navegador.

## 🧪 Verificar que Funciona

### 1. Ejecutar diagnóstico nuevamente:
```bash
python check_chrome.py
```

Deberías ver todos los checks en verde (✓)

### 2. Probar la API:
```bash
python test_api.py
```

### 3. Hacer una petición de prueba:

```bash
curl -X POST "http://localhost:8000/api/v1/medicines/search" -H "Content-Type: application/json" -d "{\"nombre_medicamento\": \"PARACETAMOL\", \"limite_resultados\": 5}"
```

## 📝 Si Aún No Funciona

### Opción A: Instalar ChromeDriver Manualmente

1. **Descargar ChromeDriver:**
   - Ve a: https://chromedriver.chromium.org/downloads
   - Descarga la versión que coincida con tu Chrome
   - Descomprime el archivo

2. **Agregar al PATH:**
   - Copia `chromedriver.exe` a `C:\Windows\System32\`
   - O agrega la carpeta al PATH de Windows

### Opción B: Usar Firefox en lugar de Chrome

Modificar `app/services/digemid_scraper.py` para usar Firefox (GeckoDriver):

1. Instalar Firefox: https://www.mozilla.org/firefox/
2. Modificar requirements.txt:
   ```
   pip install geckodriver-autoinstaller
   ```

## 🆘 Obtener Ayuda

Si ninguna solución funciona:

1. Ejecuta el diagnóstico completo:
   ```bash
   python check_chrome.py > diagnostico.txt 2>&1
   ```

2. Revisa el archivo `diagnostico.txt` para ver los errores

3. Asegúrate de tener:
   - Google Chrome instalado
   - Python 3.8 o superior
   - Conexión a internet

## 💡 Consejos Adicionales

- **Siempre usa un entorno virtual:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

- **Mantén las dependencias actualizadas:**
  ```bash
  pip install -r requirements.txt --upgrade
  ```

- **Verifica la versión de Python:**
  ```bash
  python --version
  ```
  Debe ser 3.8 o superior

## ✅ Checklist Final

- [ ] Chrome está instalado y actualizado
- [ ] Caché de ChromeDriver eliminado
- [ ] webdriver-manager reinstalado
- [ ] Script de diagnóstico pasa todos los tests
- [ ] Servidor inicia sin errores
- [ ] API responde correctamente
