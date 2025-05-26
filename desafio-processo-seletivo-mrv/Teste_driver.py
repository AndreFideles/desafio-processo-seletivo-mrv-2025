from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service("C:\\WebDrivers\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.google.com")
print("✅ Teste concluído com sucesso:", driver.title)
driver.quit()
