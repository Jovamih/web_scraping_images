import streamlit as st 
from modulo_main import web_scrapper,imageweb_to_pil
from modulo_scraper import ScrapperBot

st.title("Scraping  web archivos multimedia")

url_entry=st.text_input("Ingresa la URL de la pagina a raspar")

if url_entry:
    try:
        resources=web_scrapper(url_entry)
        if len(resources)<=0:
            st.write("No se encontraron recursos multimedia")
            if st.button("PROBAR Scraping avanzado"):
                st.write("Analizando con SELENIUM")
                robot=ScrapperBot(url_entry)
                resources=robot.run()
                robot.close()
        
        st.write("{0} Recursos multimedia disponibles".format(len(resources)))

        for name_img,url_img in resources:
            try:
                img=imageweb_to_pil(url_img,scale=1.0)
                st.image(img.convert("RGB"),caption=name_img)
            except Exception as e:
                print("Error al procesar {0}".format(name_img))
                #st.write(e)
    except Exception as e:
        st.write("Ups!. Hubo un error al procesar una imagen")
        print("Error interno :",e)


    