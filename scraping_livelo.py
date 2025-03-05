from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# URL da página de promoções
url_promocoes = "https://www.livelo.com.br/ganhe-pontos-compre-e-pontue"

def acessar_pagina():
    """Acessa a página de promoções e aguarda o carregamento."""
    driver.get(url_promocoes)
    time.sleep(5)  # Tempo para carregamento inicial

def extrair_promocoes():
    """Extrai nome da loja e taxa de conversão das promoções e filtra as que têm 5 ou mais pontos."""
    try:
        # Aguarda os elementos de promoções aparecerem
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "parity__card"))
        )

        promocoes = driver.find_elements(By.CLASS_NAME, "parity__card")
        
        dados_promocoes = []

        for promocao in promocoes:
            try:
                # Extrai o nome da loja pelo atributo alt da imagem
                imagem = promocao.find_element(By.TAG_NAME, "img")
                nome_loja = imagem.get_attribute("alt")

                # Extrai a taxa de conversão de pontos
                taxa_element = promocao.find_element(By.CLASS_NAME, "info__value")
                taxa_conversao = taxa_element.text.strip()

                # Captura o número de pontos da conversão (exemplo: "R$ 1 = 6 Pontos Livelo")
                match = re.search(r"(\d+)\s*(?:até\s*)?(\d*)\s*Pontos?", taxa_conversao)
                if match:
                    min_pontos = int(match.group(1))  # Número mínimo de pontos
                    max_pontos = int(match.group(2)) if match.group(2) else min_pontos  # Se houver um intervalo, pega o maior valor

                    # Filtra apenas promoções com 5 ou mais pontos por real
                    if max_pontos >= 5:
                        dados_promocoes.append({
                            "Loja": nome_loja,
                            "Taxa de Conversão": taxa_conversao
                        })

            except Exception as e:
                print(f"Erro ao processar uma promoção: {e}")

        if dados_promocoes:
            print("\n✅ Promoções com 5 ou mais pontos encontradas:")
            for promocao in dados_promocoes:
                print(f"{promocao['Loja']} - {promocao['Taxa de Conversão']}")
        else:
            print("❌ Nenhuma promoção com mais de 5 pontos encontrada.")

    except Exception as e:
        print(f"❌ Erro ao capturar promoções: {e}")

# Fluxo do script
acessar_pagina()
extrair_promocoes()

# Fecha o navegador após a execução
driver.quit()
