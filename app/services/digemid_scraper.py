import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class DigemidScraper:
    """Servicio para scraping de la página de DIGEMID"""

    BASE_URL = "https://opm-digemid.minsa.gob.pe/#/consulta-producto"

    # Mapeo de departamentos a códigos
    DEPARTAMENTOS = {
        "AMAZONAS": "01", "ANCASH": "02", "APURIMAC": "03", "AREQUIPA": "04",
        "AYACUCHO": "05", "CAJAMARCA": "06", "CALLAO": "07", "CUSCO": "08",
        "HUANCAVELICA": "09", "HUANUCO": "10", "ICA": "11", "JUNIN": "12",
        "LA LIBERTAD": "13", "LAMBAYEQUE": "14", "LIMA": "15", "LORETO": "16",
        "MADRE DE DIOS": "17", "MOQUEGUA": "18", "PASCO": "19", "PIURA": "20",
        "PUNO": "21", "SAN MARTIN": "22", "TACNA": "23", "TUMBES": "24",
        "UCAYALI": "25"
    }

    # Mapeo de provincias de Lima
    PROVINCIAS_LIMA = {
        "LIMA": "01", "BARRANCA": "02", "CAJATAMBO": "03", "CANTA": "04",
        "CAÑETE": "05", "HUARAL": "06", "HUAROCHIRI": "07", "HUAURA": "08",
        "OYON": "09", "YAUYOS": "10"
    }

    def __init__(self, headless: bool = True, timeout: int = 30, use_tor: bool = False, tor_port: int = 9050):
        """
        Inicializa el scraper

        Args:
            headless: Si debe ejecutarse en modo headless (sin interfaz gráfica)
            timeout: Tiempo máximo de espera en segundos
            use_tor: Si debe usar la red Tor para la conexión
            tor_port: Puerto SOCKS de Tor (default: 9050)
        """
        self.headless = headless
        self.timeout = timeout
        self.use_tor = use_tor
        self.tor_port = tor_port
        self.driver = None
        self.tor_manager = None

    def _setup_driver(self):
        """Configura el driver de Selenium"""
        import os
        from pathlib import Path

        chrome_options = Options()

        # Si se usa Tor, iniciar y configurar
        if self.use_tor:
            from .tor_manager import TorManager

            print("\n🧅 Configurando conexión Tor...")
            self.tor_manager = TorManager(tor_port=self.tor_port)

            # Iniciar Tor si no está corriendo
            if not self.tor_manager.start_tor():
                print("⚠ Advertencia: No se pudo iniciar Tor, continuando sin proxy")
                self.use_tor = False
            else:
                # Probar la conexión
                if self.tor_manager.test_connection():
                    print("✓ Conexión Tor verificada y funcionando")
                    # Configurar Chrome para usar Tor
                    chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.tor_port}')
                else:
                    print("⚠ Advertencia: Tor está corriendo pero la conexión falló")

        if self.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # User agent más común
        if self.use_tor:
            chrome_options.add_argument(
                'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )

        try:
            # Instalar ChromeDriver automáticamente
            driver_path = ChromeDriverManager().install()

            # Corregir la ruta del driver en Windows
            # webdriver-manager a veces devuelve una ruta incorrecta
            if os.name == 'nt' and driver_path:  # Windows
                driver_dir = Path(driver_path).parent
                # Buscar chromedriver.exe en el directorio
                possible_paths = [
                    driver_dir / "chromedriver.exe",
                    driver_dir / "chromedriver-win32" / "chromedriver.exe",
                    driver_dir / "chromedriver-win64" / "chromedriver.exe",
                ]

                for path in possible_paths:
                    if path.exists():
                        driver_path = str(path)
                        break

            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error instalando ChromeDriver automáticamente: {str(e)}")
            print("Intentando usar Chrome sin servicio específico...")
            # Intentar sin especificar el servicio (usa el PATH del sistema)
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                raise Exception(f"No se pudo iniciar ChromeDriver. Error 1: {str(e)}, Error 2: {str(e2)}")

        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def _close_modal(self):
        """Cierra el modal inicial si está presente"""
        try:
            wait = WebDriverWait(self.driver, 10)

            # Esperar a que el modal sea visible
            modal = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ngb-modal-window"))
            )
            print("Modal detectado, esperando botón de cerrar...")
            time.sleep(2)  # Dar tiempo a que el modal se renderice completamente

            # Buscar el botón de cerrar con un selector más específico
            close_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-inverse') and contains(text(), 'Cerrar')]"))
            )

            # Hacer scroll al botón si es necesario
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
            time.sleep(1)

            # Intentar hacer clic con JavaScript si el clic normal falla
            try:
                close_button.click()
            except Exception:
                print("Clic normal falló, usando JavaScript...")
                self.driver.execute_script("arguments[0].click();", close_button)

            print("Modal cerrado exitosamente")

            # Esperar a que el modal desaparezca
            wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "ngb-modal-window")))
            time.sleep(2)  # Dar tiempo extra para que la página se estabilice

        except TimeoutException:
            print("No se detectó modal o ya estaba cerrado")
        except Exception as e:
            print(f"Error al cerrar modal: {str(e)}")

    def _search_medicine(self, nombre_medicamento: str):
        """
        Busca el medicamento en el campo de búsqueda

        Args:
            nombre_medicamento: Nombre del medicamento a buscar
        """
        wait = WebDriverWait(self.driver, self.timeout)

        print(f"Buscando campo de entrada para medicamento...")
        # Buscar el input de búsqueda - Esperar a que esté listo
        search_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][placeholder='']"))
        )

        # Asegurarse de que el input esté visible y clickeable
        time.sleep(1)
        search_input.click()
        time.sleep(0.5)

        # Limpiar y escribir el nombre del medicamento lentamente
        search_input.clear()
        time.sleep(0.5)

        print(f"Escribiendo: {nombre_medicamento}")
        # Escribir carácter por carácter para simular escritura humana
        for char in nombre_medicamento:
            search_input.send_keys(char)
            time.sleep(0.1)

        # Esperar a que aparezcan las sugerencias
        print("Esperando sugerencias...")
        time.sleep(3)

        # Hacer clic en la primera sugerencia
        try:
            suggestions_container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.suggestions-container.is-visible"))
            )
            time.sleep(1)

            first_suggestion = suggestions_container.find_element(By.CSS_SELECTOR, "li.item a")
            print(f"Seleccionando sugerencia: {first_suggestion.text}")

            # Hacer scroll al elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_suggestion)
            time.sleep(0.5)

            first_suggestion.click()
            time.sleep(2)  # Esperar a que se procese la selección
            print("Sugerencia seleccionada")

        except TimeoutException:
            print(f"No se encontraron sugerencias para: {nombre_medicamento}")

    def _select_location(self, departamento: str, provincia: str, distrito: str):
        """
        Selecciona la ubicación (departamento, provincia, distrito)

        Args:
            departamento: Nombre del departamento
            provincia: Nombre de la provincia
            distrito: Nombre del distrito
        """
        from selenium.webdriver.support.ui import Select

        wait = WebDriverWait(self.driver, self.timeout)

        # Seleccionar departamento
        print(f"Seleccionando departamento: {departamento}")
        dept_code = self.DEPARTAMENTOS.get(departamento.upper())
        if dept_code:
            dept_select_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='codigoDepartamento']"))
            )
            dept_select = Select(dept_select_element)
            dept_select.select_by_value(dept_code)
            time.sleep(2)  # Esperar a que se carguen las provincias
            print(f"Departamento seleccionado: {departamento}")

        # Seleccionar provincia
        print(f"Seleccionando provincia: {provincia}")
        prov_code = self.PROVINCIAS_LIMA.get(provincia.upper()) if departamento.upper() == "LIMA" else None
        if prov_code:
            prov_select_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='codigoProvincia']"))
            )
            prov_select = Select(prov_select_element)
            prov_select.select_by_value(prov_code)
            time.sleep(2)  # Esperar a que se carguen los distritos
            print(f"Provincia seleccionada: {provincia}")

        # Seleccionar distrito
        print(f"Seleccionando distrito: {distrito}")
        try:
            dist_select_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='codigoDistrito']"))
            )

            # Esperar a que el select tenga opciones
            time.sleep(2)

            dist_select = Select(dist_select_element)

            # Buscar el distrito por texto visible
            distrito_encontrado = False
            for option in dist_select.options:
                if distrito.upper() in option.text.upper():
                    dist_select.select_by_visible_text(option.text.strip())
                    distrito_encontrado = True
                    print(f"Distrito seleccionado: {option.text.strip()}")
                    break

            if not distrito_encontrado:
                print(f"Advertencia: No se encontró el distrito '{distrito}', usando el primero disponible")
                if len(dist_select.options) > 1:
                    dist_select.select_by_index(1)  # Seleccionar el primer distrito (índice 0 es "--Seleccione--")

            time.sleep(2)  # Esperar después de seleccionar distrito
            print("Distrito configurado")

        except TimeoutException:
            print(f"No se pudo seleccionar el distrito: {distrito}")
        except Exception as e:
            print(f"Error al seleccionar distrito: {str(e)}")

        # Hacer clic en el botón Buscar
        print("\nHaciendo clic en el botón 'Buscar'...")
        try:
            search_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-inverse') and contains(., 'Buscar')]"))
            )

            # Hacer scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
            time.sleep(1)

            # Intentar clic normal
            try:
                search_button.click()
            except Exception:
                print("Clic normal falló, usando JavaScript...")
                self.driver.execute_script("arguments[0].click();", search_button)

            print("✓ Botón 'Buscar' clickeado")
            time.sleep(4)  # Esperar a que se carguen los resultados

        except TimeoutException:
            print("⚠ No se encontró el botón 'Buscar', continuando...")
        except Exception as e:
            print(f"⚠ Error al hacer clic en 'Buscar': {str(e)}")

    def _extract_pharmacy_details(self) -> Dict:
        """
        Extrae los detalles de la farmacia del modal de detalle

        Returns:
            Diccionario con los detalles de la farmacia
        """
        wait = WebDriverWait(self.driver, 10)
        details = {}

        try:
            # Esperar a que el modal esté visible
            time.sleep(2)

            # Extraer nombre comercial
            try:
                nombre_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='nombreComercial']")
                details["nombre_comercial"] = nombre_input.get_attribute("value") or nombre_input.get_attribute("ng-reflect-model") or ""
            except:
                details["nombre_comercial"] = ""

            # Extraer dirección
            try:
                direccion_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='direccion']")
                details["direccion"] = direccion_input.get_attribute("value") or direccion_input.get_attribute("ng-reflect-model") or ""
            except:
                details["direccion"] = ""

            # Extraer teléfono
            try:
                telefono_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='telefono']")
                details["telefono"] = telefono_input.get_attribute("value") or telefono_input.get_attribute("ng-reflect-model") or ""
            except:
                details["telefono"] = ""

            # Extraer departamento
            try:
                dept_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='departamento']")
                details["departamento_farmacia"] = dept_input.get_attribute("value") or dept_input.get_attribute("ng-reflect-model") or ""
            except:
                details["departamento_farmacia"] = ""

            # Extraer provincia
            try:
                prov_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='provincia']")
                details["provincia_farmacia"] = prov_input.get_attribute("value") or prov_input.get_attribute("ng-reflect-model") or ""
            except:
                details["provincia_farmacia"] = ""

            print(f"  Detalles obtenidos: {details['nombre_comercial']} - {details['direccion']}")

        except Exception as e:
            print(f"  Error extrayendo detalles: {str(e)}")

        return details

    def _extract_results(self, limit: int = 10) -> List[Dict]:
        """
        Extrae los resultados de la tabla

        Args:
            limit: Número máximo de resultados a extraer

        Returns:
            Lista de diccionarios con los datos de los medicamentos
        """
        wait = WebDriverWait(self.driver, self.timeout)
        results = []

        try:
            # Esperar a que aparezca la tabla
            table = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.table-striped"))
            )

            # Extraer las filas del tbody
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            print(f"Total de filas encontradas: {len(rows)}")

            for i, row in enumerate(rows[:limit]):
                try:
                    print(f"\nProcesando fila {i+1}/{min(limit, len(rows))}...")

                    cells = row.find_elements(By.TAG_NAME, "td")

                    if len(cells) >= 7:
                        tipo_establecimiento = cells[0].text.strip()
                        fecha_actualizacion = cells[1].text.strip()
                        producto = cells[2].text.strip()
                        laboratorio = cells[3].text.strip()
                        farmacia_botica = cells[4].text.strip()
                        precio_str = cells[5].text.strip()

                        # Convertir precio a float
                        try:
                            precio_unitario = float(precio_str)
                        except ValueError:
                            precio_unitario = 0.0

                        # Hacer clic en "Ver detalle" para obtener información adicional
                        details = {}
                        try:
                            # Buscar el botón de detalle en la última celda
                            detail_link = cells[6].find_element(By.CSS_SELECTOR, "a[title='Ver detalle']")

                            # Hacer scroll al elemento
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", detail_link)
                            time.sleep(0.5)

                            # Hacer clic
                            print(f"  Haciendo clic en 'Ver detalle'...")
                            try:
                                detail_link.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", detail_link)

                            time.sleep(2)  # Esperar a que se abra el modal

                            # Extraer detalles del modal
                            details = self._extract_pharmacy_details()

                            # Cerrar el modal
                            try:
                                close_btn = self.driver.find_element(By.XPATH, "//button[contains(@class, 'close') or contains(text(), 'Cerrar')]")
                                close_btn.click()
                                time.sleep(1)
                            except:
                                # Intentar presionar ESC
                                from selenium.webdriver.common.keys import Keys
                                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                                time.sleep(1)

                        except Exception as e:
                            print(f"  ⚠ No se pudo obtener detalles: {str(e)}")
                            details = {
                                "nombre_comercial": "",
                                "direccion": "",
                                "telefono": "",
                                "departamento_farmacia": "",
                                "provincia_farmacia": ""
                            }

                        # Combinar información básica con detalles
                        result = {
                            "tipo_establecimiento": tipo_establecimiento,
                            "fecha_actualizacion": fecha_actualizacion,
                            "producto": producto,
                            "laboratorio": laboratorio,
                            "farmacia_botica": farmacia_botica,
                            "precio_unitario": precio_unitario,
                            **details  # Agregar detalles de la farmacia
                        }

                        results.append(result)
                        print(f"  ✓ Fila {i+1} procesada")

                except Exception as e:
                    print(f"  ✗ Error extrayendo fila {i+1}: {str(e)}")
                    continue

        except TimeoutException:
            print("No se encontraron resultados en la tabla")

        return results

    def search_medicines(
        self,
        nombre_medicamento: str,
        departamento: str = "LIMA",
        provincia: str = "LIMA",
        distrito: str = "PUENTE PIEDRA",
        limit: int = 10
    ) -> Dict:
        """
        Realiza la búsqueda completa de medicamentos

        Args:
            nombre_medicamento: Nombre del medicamento a buscar
            departamento: Departamento donde buscar
            provincia: Provincia donde buscar
            distrito: Distrito donde buscar
            limit: Número máximo de resultados

        Returns:
            Diccionario con los resultados de la búsqueda
        """
        try:
            print("="*80)
            print(f"Iniciando búsqueda de: {nombre_medicamento}")
            print(f"Ubicación: {departamento} > {provincia} > {distrito}")
            print("="*80)

            # Configurar el driver
            print("\n1. Configurando ChromeDriver...")
            self._setup_driver()

            # Navegar a la página
            print(f"\n2. Navegando a {self.BASE_URL}...")
            self.driver.get(self.BASE_URL)
            print("Página cargada, esperando elementos...")
            time.sleep(5)  # Dar más tiempo para que cargue completamente

            # Cerrar modal inicial
            print("\n3. Cerrando modal inicial (si existe)...")
            self._close_modal()

            # Buscar medicamento
            print("\n4. Buscando medicamento...")
            self._search_medicine(nombre_medicamento)

            # Seleccionar ubicación
            print("\n5. Seleccionando ubicación...")
            self._select_location(departamento, provincia, distrito)

            # Extraer resultados
            print("\n6. Extrayendo resultados...")
            results = self._extract_results(limit)
            print(f"\n✓ Búsqueda completada: {len(results)} resultados encontrados")

            return {
                "success": True,
                "message": "Búsqueda completada exitosamente",
                "total_encontrados": len(results),
                "resultados": results,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "message": "Error durante la búsqueda",
                "total_encontrados": 0,
                "resultados": [],
                "error": str(e)
            }

        finally:
            if self.driver:
                self.driver.quit()

            # Limpiar recursos de Tor
            if self.tor_manager:
                self.tor_manager.stop_tor()
