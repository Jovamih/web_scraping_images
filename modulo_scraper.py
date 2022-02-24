from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import EdgeOptions,Edge
from modulo_main import parse_link

from webdriver_manager.microsoft import EdgeChromiumDriverManager



class ScrapperBot(object):

    def __init__(self, url):

        self.url=url
        #agregamos las opciones
        options=EdgeOptions()
        options.use_chromium=True
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        #creamos el driver
        self.driver = Edge(executable_path=EdgeChromiumDriverManager().install(),options=options)

        self.imagenes = []
    
    def login(self):
        pass
    def run(self):
        self.driver.get(self.url)
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//img[@src]"))
            )

            links=[ element.get_attribute("src") for element in elements]
            self.imagenes=[ parse_link(self.url,link) for link in links]
        except  NoSuchElementException:
            print("[*] SERVER:: No se encontraron elementos <Img>")
            self.imagenes=[]
        
        return self.imagenes
        
    
    def close(self):
        self.driver.quit()

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Scrapper Bot')
    parser.add_argument('--url', help='URL de la pagina',type=str,required=True)

    args=parser.parse_args()
    try:
        scrapper = ScrapperBot(args.url)
        scrapper.run()
        print(scrapper.imagenes)
        scrapper.close()
    except Exception as e:
        print(e)
    