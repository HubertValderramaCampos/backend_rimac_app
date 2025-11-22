"""
Gestor de conexiones Tor para web scraping anónimo
"""
import socket
import socks
import subprocess
import time
import os
from typing import Optional
from pathlib import Path


class TorManager:
    """Administra la conexión a Tor"""

    def __init__(
        self,
        tor_port: int = 9050,
        control_port: int = 9051,
        tor_password: Optional[str] = None
    ):
        """
        Inicializa el gestor de Tor

        Args:
            tor_port: Puerto SOCKS de Tor (default: 9050)
            control_port: Puerto de control de Tor (default: 9051)
            tor_password: Contraseña para el puerto de control
        """
        self.tor_port = tor_port
        self.control_port = control_port
        self.tor_password = tor_password
        self.tor_process = None

    def is_tor_running(self) -> bool:
        """
        Verifica si Tor está corriendo

        Returns:
            True si Tor está corriendo, False en caso contrario
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('127.0.0.1', self.tor_port))
            sock.close()
            return result == 0
        except:
            return False

    def start_tor(self) -> bool:
        """
        Inicia el servicio de Tor si no está corriendo

        Returns:
            True si Tor se inició correctamente o ya estaba corriendo
        """
        if self.is_tor_running():
            print(f"✓ Tor ya está corriendo en el puerto {self.tor_port}")
            return True

        print("Intentando iniciar Tor...")

        # Buscar el ejecutable de Tor en ubicaciones comunes
        tor_paths = [
            r"C:\Program Files\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
            r"C:\Program Files (x86)\Tor Browser\Browser\TorBrowser\Tor\tor.exe",
            r"C:\Users\{}\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe".format(os.getenv('USERNAME')),
            "tor",  # En PATH del sistema
        ]

        tor_exe = None
        for path in tor_paths:
            if os.path.exists(path):
                tor_exe = path
                break

        if not tor_exe:
            # Intentar ejecutar "tor" si está en el PATH
            tor_exe = "tor"

        try:
            # Intentar iniciar Tor
            self.tor_process = subprocess.Popen(
                [tor_exe],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            # Esperar a que Tor se inicie
            print("Esperando a que Tor se inicie...")
            for i in range(30):
                if self.is_tor_running():
                    print(f"✓ Tor iniciado correctamente en el puerto {self.tor_port}")
                    return True
                time.sleep(1)
                print(f"  Esperando... ({i+1}/30)")

            print("✗ Tor no se pudo iniciar en el tiempo esperado")
            return False

        except FileNotFoundError:
            print("✗ No se encontró el ejecutable de Tor")
            print("\nPor favor, instala Tor Browser o el servicio Tor")
            print("Descarga desde: https://www.torproject.org/download/")
            return False
        except Exception as e:
            print(f"✗ Error al iniciar Tor: {str(e)}")
            return False

    def stop_tor(self):
        """Detiene el servicio de Tor si fue iniciado por este manager"""
        if self.tor_process:
            try:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=5)
                print("✓ Tor detenido")
            except:
                self.tor_process.kill()

    def get_new_identity(self) -> bool:
        """
        Solicita una nueva identidad a Tor (cambia la IP)

        Returns:
            True si se obtuvo nueva identidad exitosamente
        """
        try:
            from stem import Signal
            from stem.control import Controller

            with Controller.from_port(port=self.control_port) as controller:
                if self.tor_password:
                    controller.authenticate(password=self.tor_password)
                else:
                    controller.authenticate()

                controller.signal(Signal.NEWNYM)
                print("✓ Nueva identidad de Tor solicitada")
                time.sleep(5)  # Esperar a que se establezca la nueva identidad
                return True

        except Exception as e:
            print(f"⚠ No se pudo obtener nueva identidad: {str(e)}")
            return False

    def test_connection(self) -> bool:
        """
        Prueba la conexión a través de Tor

        Returns:
            True si la conexión funciona correctamente
        """
        try:
            import requests

            # Configurar el proxy SOCKS
            proxies = {
                'http': f'socks5h://127.0.0.1:{self.tor_port}',
                'https': f'socks5h://127.0.0.1:{self.tor_port}'
            }

            # Hacer una petición de prueba para verificar la IP
            response = requests.get(
                'https://check.torproject.org/api/ip',
                proxies=proxies,
                timeout=30
            )

            data = response.json()
            is_tor = data.get('IsTor', False)
            ip = data.get('IP', 'Unknown')

            if is_tor:
                print(f"✓ Conexión Tor verificada - IP: {ip}")
                return True
            else:
                print(f"✗ No se está usando Tor - IP: {ip}")
                return False

        except Exception as e:
            print(f"✗ Error al probar conexión Tor: {str(e)}")
            return False

    def get_chrome_options_with_tor(self):
        """
        Retorna opciones de Chrome configuradas para usar Tor

        Returns:
            ChromeOptions configuradas con proxy Tor
        """
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()

        # Configurar proxy SOCKS5 para Tor
        chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.tor_port}')

        # Opciones adicionales para privacidad
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # User agent más común
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )

        return chrome_options

    def __enter__(self):
        """Context manager entry"""
        self.start_tor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop_tor()
