import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # AJUSTEMENT CLOUD 1 : Mode Headless obligatoire pour GitHub Actions
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=chrome_options)
    yield browser
    
    # AJUSTEMENT CLOUD 2 : Déconnexion sécurisée (uniquement si le bouton est présent)
    try:
        logout_btn = browser.find_elements(By.CSS_SELECTOR, ".logout")
        if logout_btn:
            logout_btn[0].click()
    except Exception:
        pass # Évite de faire planter le teardown si le test a échoué avant
        
    browser.quit()

def test_login(driver):
    # AJUSTEMENT CLOUD 3 : Remplacement par une IP publique ou variable d'environnement
    # Si APP_URL n'est pas fournie par GitHub, on utilise l'IP publique de votre Redmine
    url = os.environ.get("APP_URL", "http://34.123.38.242") 
    username = os.environ.get("APP_USERNAME", "user1")
    password = os.environ.get("APP_PASSWORD", "Hdjsy@1hrts")

    driver.get(url + "/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-submit").click()
    
    # Critère de succès
    loggedas = driver.find_element(By.ID, "loggedas")
    assert username in loggedas.text