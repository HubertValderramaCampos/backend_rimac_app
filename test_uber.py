import requests
import json

BASE_URL = "http://localhost:8000"

def test_uber_quote():
    url = f"{BASE_URL}/uber/quote"

    payload = {
        "pickup_location": "Plaza de Armas, Lima",
        "destination": "Aeropuerto Jorge Chávez, Lima"
    }

    print(f"\nProbando endpoint: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(url, json=payload, timeout=120)

        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print(f"\n✓ Cotización exitosa")
                print(f"Total de opciones: {data.get('total_opciones')}")
                for option in data.get('resultados', []):
                    print(f"  - {option['tipo_viaje']}: {option['precio']}")
            else:
                print(f"\n✗ Error: {data.get('error')}")
        else:
            print(f"\n✗ Error HTTP {response.status_code}")

    except requests.exceptions.Timeout:
        print("\n✗ Timeout - La petición tardó más de 120 segundos")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")

if __name__ == "__main__":
    print("="*80)
    print("PRUEBA DE ENDPOINT UBER")
    print("="*80)
    print("\nAsegúrate de que el servidor esté corriendo:")
    print("  python run.py")
    print("\nPresiona CTRL+C para cancelar\n")

    test_uber_quote()

    print("\n" + "="*80)
