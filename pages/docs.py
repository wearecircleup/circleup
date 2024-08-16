import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from classes.utils_class import CategoryUtils
import pandas as pd
from menu import menu
from classes.research_es import main_es
from classes.research_en import main_en

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)



# if __name__ == "__main__":
# try:

menu()

tab1, tab2 = st.tabs([ "Inglés (EN)", "Español (ES)"])

with tab1:
    main_en()  

with tab2:
    main_es()


st.divider()
st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
    st.switch_page('app.py')
    # except:
    #     st.switch_page('app.py')