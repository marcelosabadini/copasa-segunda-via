import pandas as pd
import re
import time
import sys

from selenium import webdriver

driver = webdriver.Chrome('chromedriver.exe')

df_numeros = pd.DataFrame()
df = pd.read_csv('data.csv', sep=';')

for ndx,i in df.iterrows():
    cpf = '00000000000' + str(df['cpf'][ndx])
    cpf = cpf[len(cpf)-11:]
    # essa URL faz com que os dados já cheguem carregados na página
    url = f'http://www2.copasa.com.br/servicos/2avia2/msginicial.asp?visor={cpf}&Opcao=CPF'
    
    time.sleep(0.2)
    
    driver.get(url)
    
    page = driver.page_source
            
    if 'ATENÇÃO' in page:
        pass
    else:    
        
        # como os dados já estão na página, é soh clicar em pesquisar
        driver.find_element_by_name('BtnSubmit').click()
        
        result_len = len(driver.find_elements_by_xpath('/html/body/center/table/tbody/tr/td/form/table[2]/tbody//tr'))   
                    
        if result_len > 1:
            for i in range(1, result_len):
                ii = i+1
                
                if ii > result_len:
                    break
            
                log       = driver.find_elements_by_xpath(f'/html/body/center/table/tbody/tr/td/form/table[2]/tbody/tr[{ii}]/td[2]')[0].text
                bairro    = driver.find_elements_by_xpath(f'/html/body/center/table/tbody/tr/td/form/table[2]/tbody/tr[{ii}]/td[3]')[0].text
                municipio = driver.find_elements_by_xpath(f'/html/body/center/table/tbody/tr/td/form/table[2]/tbody/tr[{ii}]/td[4]')[0].text
                
                time.sleep(0.1)
                
                # Clica no detalhe da conta para pegar o mes referencia
                driver.find_elements_by_xpath(f'/html/body/center/table/tbody/tr/td/form/table[2]/tbody/tr[{ii}]/td[1]/a')[0].click()
                
                time.sleep(0.1)
                
                page = driver.page_source
                
                if 'ATENÇÃO' in page:
                    print(f"INSERT copasa (cpf, logradouro, bairro, municipio, ref) VALUES ('{cpf}', '{log}', '{bairro}', '{municipio}', '')",)
                else:
                    
                    table = driver.find_element_by_xpath(f'/html/body/div/table/tbody/tr/td[3]/form/table[1]')
                    
                    df_contas = pd.read_html(table.get_attribute('outerHTML'))
                    
                    # para todas faturas abertas pinta o insert na tela
                    for j in df_contas[0].iterrows():
                        ref = j[1][1]
                        if re.match('\d{2}\/\d{4}', str(ref)):
                            print(f"INSERT copasa (cpf, logradouro, bairro, municipio, ref) VALUES ('{cpf}', '{log}', '{bairro}', '{municipio}', '{ref}')",)
                
                driver.execute_script('javascript:window.history.go(-1)')                
                time.sleep(0.5)
            
