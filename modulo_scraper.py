from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import EdgeOptions,Edge
#firefox para compatibilidad con streamlit
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from modulo_main import parse_link

from webdriver_manager.microsoft import EdgeChromiumDriverManager
#para compatibilidad con streamlit
from webdriver_manager.firefox import GeckoDriverManager



class ScrapperBot(object):

    def __init__(self, url):

        self.url=url
        #agregamos las opciones de edge
        #options=EdgeOptions()
        #options.use_chromium=True
        #agregamos las opciones de firefox
        options=Options() #para firefox

        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        #creamos el driver para edge
        #self.driver = Edge(executable_path=EdgeChromiumDriverManager().install(),options=options)
        #creamos el driver para firefox
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=options)
        self.imagenes = []
    
    def login(self):
        pass
    def run(self):
        self.driver.get(self.url)
        #self.driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        #self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #self.driver.implicitly_wait(3)

        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//img[@src]"))
            )

            links=[ element.get_attribute("src") for element in elements]
            print(links)
            self.imagenes=[ parse_link(self.url,link) for link in links]
        except  NoSuchElementException:
            print("[*] SERVER:: No se encontraron elementos <Img>")
            self.imagenes=[]
        
        return self.imagenes
        
    
    def close(self):
        self.driver.stop_client()
        self.driver.close()
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
        del scrapper
    except Exception as e:
        print(e)
    