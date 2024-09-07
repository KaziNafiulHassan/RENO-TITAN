from PIL import Image
import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="RENO-TITAN",
    page_icon=":radioactive:",
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

img_config = Image.open("images/pic4.jpg")
img_config2 = Image.open("images/germany.png")
img_config3 = Image.open("images/vietnam.png")
radioation = load_lottieurl("https://lottie.host/630b7392-1f8d-43a3-8a11-bc3591e69e5a/UdDPV3Yr3V.json")
mining_animation = load_lottieurl("https://lottie.host/6e9f2ae6-fb3a-450b-a176-e40dcccc5b31/v8sfrmz9IJ.json")


with st.container():
    st.title("RENO-TITAN")
    left_column, right_column = st.columns((3,1))
    with left_column:
        st.header("Overview")
        st.write("RENO-TITAN is an international research project on the development of sustainable disposal methods and possible re-use of naturally radioactive material (NORM) from the extraction and processing of titanium from heavy sand in Vietnam. The project aims to integrate environmental aspects, establish a regulatory framework and investigate technological solutions for the management of radioactive residues in the Vietnamese titanium industry.")
        st.image(img_config)
    with right_column:
        st_lottie(radioation, height=200, key="radiation")
        st_lottie(mining_animation, height=300, key="mining")
    st.sidebar.success("Select a page above.")
    left_column, right_column = st.columns(2)

with st.container():
    st.write("---")
    st.header("Project Partners")
    image_column, image_column2 = st.columns((2,2))
    with image_column:
        st.image(img_config2)
    with image_column2:
        st.image(img_config3)
    st.write("In RENO-TITAN, Vietnamese and German partners, including universities, research institutes, state institutions and companies, are cooperating, with the southern Vietnamese province of Binh Thuan serving as a model region. The project aims to conduct environmental assessments of status quo and alternative solutions, identify economically viable use and disposal options for NORM residues, and develop elements for an integrated waste and radiation protection regulatory framework.")

with st.container():
    st.write("---")
    st.header("Funding")
    st.write("RENO-TITAN is funded by the German Federal Ministry of Education and Research (BMBF) as part of the Client II programme and will run from April 2023 to March 2026 with the aim of making the Vietnamese titanium industry more sustainable and environmentally friendly.")

