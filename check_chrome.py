"""
Script para verificar la instalación de Chrome y ChromeDriver
"""
import sys
import subprocess
from pathlib import Path


def check_chrome_installation():
    """Verifica si Chrome está instalado"""
    print("=" * 80)
    print("VERIFICANDO INSTALACIÓN DE GOOGLE CHROME")
    print("=" * 80)

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe"
    ]

    chrome_found = False
    for path in chrome_paths:
        if Path(path).exists():
            print(f"\n✓ Chrome encontrado en: {path}")
            chrome_found = True

            # Intentar obtener la versión
            try:
                result = subprocess.run(
                    [str(path), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.stdout:
                    print(f"  Versión: {result.stdout.strip()}")
            except:
                pass
            break

    if not chrome_found:
        print("\n✗ No se encontró Google Chrome instalado")
        print("\nPor favor, descarga e instala Chrome desde:")
        print("https://www.google.com/chrome/")
        return False

    return True


def test_selenium():
    """Prueba la instalación de Selenium"""
    print("\n" + "=" * 80)
    print("VERIFICANDO INSTALACIÓN DE SELENIUM")
    print("=" * 80)

    try:
        import selenium
        print(f"\n✓ Selenium instalado - Versión: {selenium.__version__}")
        return True
    except ImportError:
        print("\n✗ Selenium no está instalado")
        print("\nInstalar con: pip install selenium")
        return False


def test_webdriver_manager():
    """Prueba la instalación de webdriver-manager"""
    print("\n" + "=" * 80)
    print("VERIFICANDO WEBDRIVER-MANAGER")
    print("=" * 80)

    try:
        import webdriver_manager
        print(f"\n✓ webdriver-manager instalado")
        return True
    except ImportError:
        print("\n✗ webdriver-manager no está instalado")
        print("\nInstalar con: pip install webdriver-manager")
        return False


def test_chrome_driver():
    """Intenta inicializar ChromeDriver"""
    print("\n" + "=" * 80)
    print("PROBANDO CHROMEDRIVER")
    print("=" * 80)

    try:
        import os
        from pathlib import Path
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager

        print("\nInstalando/actualizando ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"✓ ChromeDriver descargado en: {driver_path}")

        # Corregir la ruta del driver en Windows
        if os.name == 'nt' and driver_path:  # Windows
            driver_dir = Path(driver_path).parent
            print(f"\nBuscando chromedriver.exe en: {driver_dir}")

            # Buscar chromedriver.exe en el directorio
            possible_paths = [
                driver_dir / "chromedriver.exe",
                driver_dir / "chromedriver-win32" / "chromedriver.exe",
                driver_dir / "chromedriver-win64" / "chromedriver.exe",
            ]

            for path in possible_paths:
                if path.exists():
                    driver_path = str(path)
                    print(f"✓ ChromeDriver encontrado en: {driver_path}")
                    break
            else:
                print("⚠ No se encontró chromedriver.exe, usando ruta original")

        print("\nIniciando navegador Chrome...")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        print("✓ ChromeDriver iniciado correctamente")

        # Probar navegación
        print("\nProbando navegación...")
        driver.get("https://www.google.com")
        print(f"✓ Navegación exitosa - Título: {driver.title}")

        driver.quit()
        print("✓ ChromeDriver cerrado correctamente")

        return True

    except Exception as e:
        print(f"\n✗ Error al probar ChromeDriver: {str(e)}")
        print("\nDetalles del error:")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "DIAGNÓSTICO DE CHROME Y SELENIUM" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")

    all_ok = True

    # Verificar Chrome
    if not check_chrome_installation():
        all_ok = False

    # Verificar Selenium
    if not test_selenium():
        all_ok = False

    # Verificar webdriver-manager
    if not test_webdriver_manager():
        all_ok = False

    # Probar ChromeDriver
    if all_ok:
        if not test_chrome_driver():
            all_ok = False

    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)

    if all_ok:
        print("\n✓ Todas las verificaciones pasaron exitosamente")
        print("\nEl scraper debería funcionar correctamente.")
        print("Puedes iniciar el servidor con: python run.py")
    else:
        print("\n✗ Algunas verificaciones fallaron")
        print("\nPor favor, corrige los errores indicados arriba.")
        print("\nPasos recomendados:")
        print("1. Instalar Google Chrome si no está instalado")
        print("2. Ejecutar: pip install -r requirements.txt")
        print("3. Volver a ejecutar este script")

    print("\n" + "=" * 80 + "\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
