from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

try:
    # Configurações do Chrome
    options = Options()
    # options.add_argument('--headless')  # <- COMENTE ou REMOVA esta linha
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-features=TranslateUI,OptimizationHints,VoiceTrigger,MediaRouter")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")

    # Inicia o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.tenda.com/apartamentos-a-venda")

    # Aguarda carregar ao menos um card
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "card-anuncio"))
    )

    # Scroll para carregar mais cards
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Coleta os cards
    cards = driver.find_elements(By.CLASS_NAME, "card-anuncio")
    dados = []

    for card in cards[:12]:  # Limita para até 12 registros
        try:
            nome = card.find_element(By.CLASS_NAME, "titulo-empreendimento").text
            local = card.find_element(By.CLASS_NAME, "bairro-empreendimento").text
            parcela = card.find_element(By.CLASS_NAME, "valor-box").text
            texto = card.text.lower()

            quartos = "N/A"
            if "dorm" in texto:
                idx = texto.find("dorm")
                quartos = texto[idx - 3:idx].strip()

            vagas = "N/A"
            if "vaga" in texto:
                idx = texto.find("vaga")
                vagas = texto[idx - 3:idx].strip()

            dados.append({
                "Empreendimento": nome,
                "Localização": local,
                "Parcela Inicial": parcela,
                "Quartos": quartos,
                "Vagas": vagas,
                "Resumo do Card": texto
            })
        except Exception as e:
            print("⚠️ Erro ao extrair card:", e)

    # Exporta para Excel
    df = pd.DataFrame(dados)
    df.to_excel("tenda_empreendimentos.xlsx", index=False)
    print(f"✅ Extração concluída com sucesso! {len(df)} empreendimentos salvos.")

except Exception as e:
    print("⛔ Erro crítico durante a execução:", e)

finally:
    try:
        driver.quit()
    except:
        pass
