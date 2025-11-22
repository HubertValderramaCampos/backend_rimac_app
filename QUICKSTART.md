# Guía de Inicio Rápido

## Instalación en 5 pasos

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar que Chrome esté instalado

Este proyecto usa Google Chrome para el web scraping. Asegúrate de tener Chrome instalado en tu sistema.

### 3. Iniciar el servidor

```bash
python run.py
```

O con uvicorn directamente:

```bash
uvicorn app.main:app --reload
```

### 4. Verificar que el servidor está corriendo

Abre tu navegador y ve a: http://localhost:8000

Deberías ver un mensaje JSON con información de la API.

### 5. Probar la API

#### Opción A: Usando la documentación interactiva

Abre http://localhost:8000/docs en tu navegador y usa la interfaz de Swagger para hacer peticiones.

#### Opción B: Usando el script de prueba

En otra terminal:

```bash
python test_api.py
```

#### Opción C: Usando cURL

```bash
curl -X POST "http://localhost:8000/api/v1/medicines/search" \
  -H "Content-Type: application/json" \
  -d "{\"nombre_medicamento\": \"APRONAX\", \"departamento\": \"LIMA\", \"provincia\": \"LIMA\", \"distrito\": \"PUENTE PIEDRA\", \"limite_resultados\": 10}"
```

## Ejemplo de Respuesta

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

## Parámetros de Búsqueda

- **nombre_medicamento** (requerido): Nombre del medicamento
- **departamento** (opcional): Default "LIMA"
- **provincia** (opcional): Default "LIMA"
- **distrito** (opcional): Default "PUENTE PIEDRA"
- **limite_resultados** (opcional): Default 10, máximo 50

## Solución de Problemas Rápidos

### ⚠️ Primero: Ejecuta el diagnóstico

```bash
python check_chrome.py
```

Este script te dirá exactamente qué está fallando.

### El servidor no inicia

- Verifica que el puerto 8000 no esté en uso
- Cambia el puerto en `.env` si es necesario

### Error: "%1 no es una aplicación Win32 válida"

Este es el error más común en Windows. Soluciones:

1. **Ejecutar diagnóstico:**
   ```bash
   python check_chrome.py
   ```

2. **Reinstalar webdriver-manager:**
   ```bash
   pip uninstall webdriver-manager -y
   pip install webdriver-manager
   ```

3. **Limpiar caché (Windows):**
   - Eliminar la carpeta: `C:\Users\{tu_usuario}\.wdm\`
   - Reiniciar el servidor

### ChromeDriver no se encuentra

- Asegúrate de tener conexión a internet (se descarga automáticamente)
- Verifica que Chrome esté instalado
- Ejecuta `python check_chrome.py`

### Timeout en las búsquedas

- Aumenta el `TIMEOUT` en `.env` (ej: 60)
- Verifica tu conexión a internet
- Desactiva headless: `HEADLESS_MODE=false` para ver qué pasa

### No aparecen resultados

- Verifica que el nombre del medicamento sea correcto
- Prueba con nombres genéricos como "PARACETAMOL" o "IBUPROFENO"
- Verifica que la combinación departamento/provincia/distrito sea válida

## Próximos Pasos

- Lee el [README.md](README.md) completo para más detalles
- Explora la documentación en http://localhost:8000/docs
- Revisa los ejemplos en [test_api.py](test_api.py)
