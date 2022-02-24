from logging import PlaceHolder
import streamlit as st 
from modulo_main import download_file, web_scrapper,imageweb_to_pil,compress_files
from modulo_scraper import ScrapperBot

st.title("Scraping  web archivos multimedia")

resources=[]
#exclusion por problemas de SVG
def filter_files(files,exclude):
    return [file for file in files if file[0].split(".")[-1] not in exclude]

def btn_download(files):
    content=compress_files(files)
    st.download_button(
             label="Download Files",
             data=content,
             file_name="archive.zip",
           )
    


col1,col2,col3=st.columns(3)
url_entry=None
status=0
with col1:
    url_entry=st.text_input(label="",placeholder="Ingresa la URL")
with col2:
    st.write("");st.write("");
    if st.button("BASICO") and url_entry:
        #main(url_entry)
        try:
            resources=web_scrapper(url_entry)
        except Exception as e:
            print("Error interno :",e)
        status=1
        
with col3:
    st.write("");st.write("")
    if st.button("AVANZADO") and url_entry:
        try:
            @st.cache(persist=True)
            def robot(url):
                robot=ScrapperBot(url_entry)
                resources=robot.run()
                robot.close()
                return resources
            resources=robot(url_entry)
        except Exception as e:
            print("Error interno :",e)
        status=2
       

#agregando texto
if status==1:
    st.write("Scraping BASICO ...")
    
elif status==2:
    st.write("Scraping AVANZADO ...")
    

resources=filter_files(resources,["svg"])
st.write("Total de archivos:",len(resources))

if len(resources)>0:
    btn_download([resource[1] for resource in resources])

    for name_img,url_img in resources:
        try:
            img=imageweb_to_pil(url_img,scale=1.0)
            st.image(img.convert("RGB"),caption=name_img)
        except Exception as e:
            print("Error al procesar {0}".format(name_img))
            st.write(e)