"""
Script de ejemplo para probar la API de búsqueda de medicamentos
"""
import requests
import json


def test_search_medicine():
    """Prueba el endpoint de búsqueda de medicamentos"""

    url = "http://localhost:8000/api/v1/medicines/search"

    # Datos de prueba
    data = {
        "nombre_medicamento": "APRONAX",
        "departamento": "LIMA",
        "provincia": "LIMA",
        "distrito": "PUENTE PIEDRA",
        "limite_resultados": 10
    }

    print("=" * 80)
    print("PRUEBA DE API - BÚSQUEDA DE MEDICAMENTOS EN DIGEMID")
    print("=" * 80)
    print(f"\nURL: {url}")
    print(f"\nDatos de búsqueda:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("\nEnviando petición...")

    try:
        response = requests.post(url, json=data, timeout=60)

        print(f"\nCódigo de estado: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print("\n" + "=" * 80)
            print("RESULTADOS")
            print("=" * 80)
            print(f"\nÉxito: {result['success']}")
            print(f"Mensaje: {result['message']}")
            print(f"Total encontrados: {result['total_encontrados']}")

            if result['resultados']:
                print(f"\nMostrando los primeros {len(result['resultados'])} resultados:\n")

                for i, med in enumerate(result['resultados'], 1):
                    print(f"\n{'─' * 80}")
                    print(f"RESULTADO #{i}")
                    print(f"{'─' * 80}")
                    print(f"Producto: {med['producto']}")
                    print(f"Laboratorio: {med['laboratorio']}")
                    print(f"Farmacia/Botica: {med['farmacia_botica']}")
                    print(f"Precio Unitario: S/ {med['precio_unitario']}")
                    print(f"Tipo: {med['tipo_establecimiento']}")
                    print(f"Actualizado: {med['fecha_actualizacion']}")
            else:
                print("\nNo se encontraron resultados.")

            if result.get('error'):
                print(f"\nError: {result['error']}")

        else:
            print(f"\nError en la petición: {response.status_code}")
            print(response.text)

    except requests.exceptions.Timeout:
        print("\nError: La petición excedió el tiempo de espera")
    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar al servidor. ¿Está corriendo la API?")
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")

    print("\n" + "=" * 80)


def test_health():
    """Prueba el endpoint de health check"""

    url = "http://localhost:8000/api/v1/medicines/health"

    print("\n" + "=" * 80)
    print("PRUEBA DE HEALTH CHECK")
    print("=" * 80)

    try:
        response = requests.get(url)
        print(f"\nEstado: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    # Probar health check
    test_health()

    # Probar búsqueda de medicamentos
    test_search_medicine()
