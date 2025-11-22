"""
Script simple para probar el scraper directamente
"""
from app.services.digemid_scraper import DigemidScraper


def test_simple():
    """Prueba simple del scraper"""
    print("\n" + "="*80)
    print("PRUEBA SIMPLE DEL SCRAPER")
    print("="*80)

    # Crear instancia del scraper
    # headless=False para ver qué está pasando
    scraper = DigemidScraper(headless=False, timeout=60)

    # Realizar búsqueda
    resultado = scraper.search_medicines(
        nombre_medicamento="PARACETAMOL",
        departamento="LIMA",
        provincia="LIMA",
        distrito="PUENTE PIEDRA",
        limit=5
    )

    # Mostrar resultados
    print("\n" + "="*80)
    print("RESULTADOS")
    print("="*80)

    if resultado["success"]:
        print(f"\n✓ Búsqueda exitosa")
        print(f"Total encontrados: {resultado['total_encontrados']}")

        if resultado["resultados"]:
            print(f"\nPrimeros {len(resultado['resultados'])} resultados:\n")
            for i, med in enumerate(resultado["resultados"], 1):
                print(f"\n{i}. {med['producto']}")
                print(f"   Farmacia: {med['farmacia_botica']}")
                print(f"   Precio: S/ {med['precio_unitario']}")
                print(f"   Laboratorio: {med['laboratorio']}")
        else:
            print("\nNo se encontraron resultados")
    else:
        print(f"\n✗ Error en la búsqueda")
        print(f"Error: {resultado.get('error', 'Desconocido')}")

    print("\n" + "="*80)


if __name__ == "__main__":
    test_simple()
