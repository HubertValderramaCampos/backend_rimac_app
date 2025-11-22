"""
Script para probar la configuración de Tor
"""
import sys
from app.services.tor_manager import TorManager


def main():
    print("\n" + "="*80)
    print("PRUEBA DE CONFIGURACIÓN TOR")
    print("="*80)

    # Crear gestor de Tor
    tor = TorManager(tor_port=9050)

    # Verificar si Tor está corriendo
    print("\n1. Verificando si Tor está corriendo...")
    if tor.is_tor_running():
        print("   ✓ Tor está corriendo")
    else:
        print("   ✗ Tor NO está corriendo")
        print("\n   Intentando iniciar Tor...")
        if tor.start_tor():
            print("   ✓ Tor iniciado correctamente")
        else:
            print("   ✗ No se pudo iniciar Tor")
            print("\n   Por favor, instala Tor:")
            print("   https://www.torproject.org/download/")
            return 1

    # Probar conexión
    print("\n2. Probando conexión a través de Tor...")
    if tor.test_connection():
        print("   ✓ Conexión Tor funciona correctamente")
    else:
        print("   ✗ La conexión Tor falló")
        return 1

    # Mostrar información adicional
    print("\n3. Información adicional:")
    print(f"   Puerto SOCKS: {tor.tor_port}")
    print(f"   Puerto Control: {tor.control_port}")

    # Probar obtener nueva identidad
    print("\n4. Probando renovación de identidad...")
    if tor.get_new_identity():
        print("   ✓ Nueva identidad obtenida")

        # Verificar nueva IP
        print("\n5. Verificando nueva IP...")
        tor.test_connection()
    else:
        print("   ℹ No se pudo renovar identidad (requiere configuración adicional)")

    print("\n" + "="*80)
    print("RESULTADO")
    print("="*80)
    print("\n✓ Tor está configurado correctamente y listo para usar")
    print("\nPara usar Tor con la API, configura en .env:")
    print("   USE_TOR=true")
    print("   TOR_PORT=9050")
    print("\n" + "="*80 + "\n")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nPrueba cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
