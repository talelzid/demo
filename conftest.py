import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # 1. Instanciation des options de configuration pour Chrome
    chrome_options = Options()
    
    # 2. Activation du mode Headless (sans interface graphique)
    chrome_options.add_argument("--headless=new") 
    
    # 3. Arguments de robustesse obligatoires pour les serveurs Linux/Docker
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # Résolution standard simulée

    # 4. Lancement du navigateur avec les configurations injectées
    browser = webdriver.Chrome(options=chrome_options)
    
    # Transmet le driver au test de manière sécurisée
    yield browser
    
    # Teardown : Fermeture propre de la session après le test
    browser.quit()
    