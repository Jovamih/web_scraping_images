from bs4 import BeautifulSoup
import pandas as pd 
import requests 
import time 
import sys 
import re,io, tempfile
from PIL import Image


def save_file(name,content):
    with open(name,mode="wb") as f:
        f.write(content)

def download_file(url,dest):
    response=requests.get(url,allow_redirects=True,verify=False,timeout=30,headers={"User-Agent":"Chrome/50.0.2661.94"}) #deshabilitamos la verificacion SSL
    if response.status_code==200: #se pudo acceder correctamente al discurso
        with open(dest,mode="wb") as file:
            file.write(response.content)
            
def get_dominio(url):
    pattern=r"(https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+~#=]{2,256}\.[a-z]{2,10})"
    match=re.search(pattern,url)
    if match:
        return match.group(1)
    return None

def imageweb_to_pil(url_image,scale=1.0):
    """
    url_image: URL de imagen a procesar
    return: Objeto PIL image
    """
    response=requests.get(url_image,stream=True)

    with tempfile.SpooledTemporaryFile(max_size=1e9) as buffer:
        #downloaded=0
        #filesize=int(response.headers["content-length"])
        for chunk in response.iter_content(chunk_size=1024):
            buffer.write(chunk)
        buffer.seek(0)
        img=Image.open(io.BytesIO(buffer.read()))
    return img.resize((int(img.size[0]*scale),int(img.size[1]*scale)))
    
def web_scrapper(url_victima,path_dest="",filter=""):
    """
    url_victima: URL del sitio web para el raspado
    path_dest  : Ruta donde guardar los datos
    filter     : Extensiones a filtrar de la pagina
    """
    #extraemos el dominio de la pagina
    #dominio=get_dominio(url_victima)
    dominio=get_dominio(url_victima)
    response=requests.get(url_victima)
    if response.status_code==200: #se logro establecer flujo en el servidor
        print("SE ACCEDIO AL SERVIDOR {0} EXITOSAMENTE".format(dominio))
        content=response.content #devuelve un binario del html
        #save_file("scraping_only/saved/page.html",content)
        soup=BeautifulSoup(content,"html.parser")
        
        coincidence_img=soup.find_all("img") #devuelve todas  las coincidencias img (etiquetas que poseen imagenes)
        #print("{0} Imagenes detectadas.".format(len(coincidence_img)))
        #filtramos aquellos que posean HREF
        coincidence_img=[x for x in coincidence_img if x.has_attr("src")]
        list_resources=[]
        for tag_img in coincidence_img:
            image_relative=tag_img.get("src")
            
            if image_relative is None: #si SRC existe pero esta vacio SRC="#"
                continue
            else:
                image_absolute= image_relative if image_relative.startswith("http") or image_relative.startswith("https") else dominio+image_relative
                im_name=image_absolute[image_absolute.rfind("/")+1:]
                list_resources.append((im_name,image_absolute))

            """if image_relative.endswith(".png") or image_relative.endswith(".jpg"):
                image_absolute= image_relative if image_relative.startswith("https") or  else  dominio+image_relative
                im_name=image_absolute[image_absolute.rfind("/")+1:]
                list_resources.append((im_name,image_absolute))
                #download_file(image_absolute,"{0}/{1}".format(path_dest,im_name))
                #print("{0} guardado correctamente en {1}".format(im_name,path_dest))"""
        return list_resources
    
    return []

if __name__=="__main__":
    
    print(sys.argv)
    if len(sys.argv)==3:#si se ingresarom dos argumentos validos se procede a operar
        url=sys.argv[1] #url de la pagina
        path=sys.argv[2] #path de la guardado
        web_scrapper(url,path,"")        