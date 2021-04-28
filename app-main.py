import streamlit as st 
from modulo_main import web_scrapper,imageweb_to_pil

st.title("Scraping de web archivos multimedia")

url_entry=st.text_input("Ingresa la URL de la pagina a raspar")

if url_entry:
    resources=web_scrapper(url_entry)
    st.write("{0} Recursos multimedia disponibles".format(len(resources)))
    for name_img,url_img in resources:
        img=imageweb_to_pil(url_img,scale=1.0)
        st.image(img,caption=name_img)


    