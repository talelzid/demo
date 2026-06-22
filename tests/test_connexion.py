import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=chrome_options)
    yield browser
    
    try:
        logout_btn = browser.find_elements(By.CSS_SELECTOR, ".logout")
        if logout_btn:
            logout_btn[0].click()
    except Exception:
        pass
        
    browser.quit()

def test_login(driver):
    # NETTOYAGE SÉCURITÉ : On supprime les chaînes de caractères secrètes en dur.
    # Si les variables ne sont pas trouvées (ex: en local), le test lèvera une erreur claire.
    url = os.environ.get("APP_URL")
    username = os.environ.get("APP_USERNAME")
    password = os.environ.get("APP_PASSWORD")

    # Guard clause : validation que l'environnement fournit bien les accès obligatoires
    if not all([url, username, password]):
        raise ValueError("❌ Erreur de configuration : APP_URL, APP_USERNAME ou APP_PASSWORD est manquant dans l'environnement.")

    url_finale = f"{url.rstrip('/')}/login"
    
    driver.get(url_finale)
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-submit").click()
    
    loggedas = driver.find_element(By.ID, "loggedas")
    assert username in loggedas.text