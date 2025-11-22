import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class UberScraper:
    def __init__(self, headless: bool = True, timeout: int = 30, cookies_file: str = "galleta_uber.json"):
        self.headless = headless
        self.timeout = timeout
        self.cookies_file = cookies_file
        self.driver = None

    def _setup_driver(self):
        """Configura el WebDriver de Chrome"""
        chrome_options = webdriver.ChromeOptions()

        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36')

        driver_path = ChromeDriverManager().install()

        if driver_path:
            driver_dir = Path(driver_path).parent
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
        self.driver.set_page_load_timeout(self.timeout)

    def _load_cookies(self):
        """Carga las cookies desde el archivo JSON"""
        try:
            cookies_path = Path(self.cookies_file)
            if not cookies_path.exists():
                print(f"Archivo de cookies no encontrado: {self.cookies_file}")
                return False

            with open(cookies_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            self.driver.get("https://m.uber.com")
            time.sleep(2)

            for cookie in cookies:
                try:
                    cookie_dict = {
                        'name': cookie.get('name'),
                        'value': cookie.get('value'),
                        'domain': cookie.get('domain', '.uber.com'),
                    }
                    if cookie.get('path'):
                        cookie_dict['path'] = cookie['path']
                    if cookie.get('expirationDate'):
                        cookie_dict['expiry'] = int(cookie['expirationDate'])
                    if 'httpOnly' in cookie:
                        cookie_dict['httpOnly'] = cookie['httpOnly']
                    if 'secure' in cookie:
                        cookie_dict['secure'] = cookie['secure']

                    self.driver.add_cookie(cookie_dict)
                except Exception as e:
                    print(f"Error agregando cookie {cookie.get('name')}: {str(e)}")
                    continue

            return True
        except Exception as e:
            print(f"Error cargando cookies: {str(e)}")
            return False

    def _enter_location(self, test_id: str, location: str):
        """Ingresa una ubicación en el campo de entrada"""
        from selenium.common.exceptions import StaleElementReferenceException

        try:
            wait = WebDriverWait(self.driver, 20)
            selector = f"input[data-testid='{test_id}']"

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            time.sleep(2)

            self.driver.execute_script(f"""
                var input = document.querySelector("{selector}");
                if (input) {{
                    input.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                    input.focus();
                    input.click();
                }}
            """)
            time.sleep(1)

            input_element = self.driver.find_element(By.CSS_SELECTOR, selector)
            for char in location:
                input_element.send_keys(char)
                time.sleep(0.08)

            time.sleep(4)

            try:
                suggestion = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "li[role='option']"))
                )
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", suggestion)
                time.sleep(2)
            except TimeoutException:
                print(f"No se encontraron sugerencias para: {location}")

        except Exception as e:
            print(f"Error ingresando ubicación {test_id}: {str(e)}")
            self.driver.save_screenshot(f"uber_error_{test_id}.png")
            print(f"Screenshot guardado en uber_error_{test_id}.png")
            raise

    def _click_search_button(self):
        """Hace clic en el botón de búsqueda"""
        try:
            wait = WebDriverWait(self.driver, 10)
            search_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Consulta tarifas']"))
            )

            self.driver.execute_script("arguments[0].scrollIntoView(true);", search_button)
            time.sleep(0.5)

            try:
                search_button.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", search_button)

            time.sleep(4)
        except Exception as e:
            print(f"Error haciendo clic en buscar: {str(e)}")
            raise

    def _extract_prices(self) -> List[Dict]:
        """Extrae los precios de los diferentes tipos de viaje"""
        results = []
        try:
            time.sleep(3)
            wait = WebDriverWait(self.driver, 15)

            ride_options = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='button']"))
            )

            for option in ride_options:
                try:
                    ride_info = {}

                    ride_name = option.find_element(By.CSS_SELECTOR, "h3, h4, div[class*='title'], div[class*='name']")
                    ride_info["tipo_viaje"] = ride_name.text.strip() if ride_name else ""

                    price_element = option.find_element(By.CSS_SELECTOR, "p.css-iQlrzm, p[class*='price'], span[class*='price']")
                    price_text = price_element.text.strip() if price_element else ""
                    ride_info["precio"] = price_text

                    try:
                        time_element = option.find_element(By.CSS_SELECTOR, "p[class*='time'], span[class*='time'], div[class*='time']")
                        ride_info["tiempo_espera"] = time_element.text.strip() if time_element else ""
                    except NoSuchElementException:
                        ride_info["tiempo_espera"] = ""

                    if ride_info["tipo_viaje"] and ride_info["precio"]:
                        results.append(ride_info)

                except NoSuchElementException:
                    continue

        except TimeoutException:
            print("No se encontraron opciones de viaje")
        except Exception as e:
            print(f"Error extrayendo precios: {str(e)}")

        return results

    def get_ride_prices(self, pickup_location: str, destination: str) -> Dict:
        """
        Obtiene los precios de viaje de Uber

        Args:
            pickup_location: Ubicación de recogida
            destination: Destino

        Returns:
            Dict con los resultados
        """
        try:
            self._setup_driver()

            if not self._load_cookies():
                return {
                    "success": False,
                    "error": "No se pudieron cargar las cookies",
                    "resultados": []
                }

            self.driver.get("https://m.uber.com")
            time.sleep(5)

            wait = WebDriverWait(self.driver, 20)
            wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            time.sleep(2)

            self._enter_location("dotcom-ui.pickup-destination.input.pickup", pickup_location)
            self._enter_location("dotcom-ui.pickup-destination.input.destination.drop0", destination)

            self._click_search_button()

            prices = self._extract_prices()

            return {
                "success": True,
                "pickup": pickup_location,
                "destination": destination,
                "resultados": prices,
                "total_opciones": len(prices)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Error durante el scraping: {str(e)}",
                "resultados": []
            }
        finally:
            if self.driver:
                self.driver.quit()
