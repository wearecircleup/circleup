import streamlit as st

st.set_page_config(
    page_title="Circle Up Community",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from classes.utils_class import CategoryUtils
from menu import menu

st.markdown(CategoryUtils.markdown_design(), unsafe_allow_html=True)
st.image('./gallery/WebSvg/main_header.svg', use_column_width=True)

def main():
    st.title("Community-Based Learning (CBL) y Tecnología en Latinoamérica")

    st.write("""
    El Community-Based Learning (CBL) está transformando la educación en Latinoamérica, 
    combinando el aprendizaje académico con experiencias comunitarias reales. En Circle Up Community, 
    reconocemos el potencial del CBL para abordar desafíos sociales y educativos en la región, 
    aprovechando la tecnología para amplificar su impacto.
    """)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.image('./gallery/icons/h_penguin.svg', use_column_width=True)
            st.write("""
            En Latinoamérica, el CBL ofrece una solución a la brecha entre 
            educación y necesidades sociales. Este enfoque permite a los estudiantes 
            aplicar sus conocimientos en proyectos que abordan problemas locales.
            """)

        st.info("""
        La implementación del CBL requiere adaptar los currículos 
        tradicionales, establecer colaboraciones con organizaciones locales y 
        desarrollar métodos de evaluación que valoren tanto el :blue[**aprendizaje académico**] 
        como el :blue[**impacto social**].
        """)

    with col2:
        st.write("""
        La tecnología juega un papel crucial en la expansión y efectividad del CBL 
        en Latinoamérica. Las plataformas digitales facilitan la conexión entre 
        estudiantes y comunidades, superando barreras geográficas y sociales.
        """)

        with st.container(border=True):
            st.image('./gallery/icons/h_monkey.svg', use_column_width=True)
            st.info("""
            El uso de :blue[**análisis de datos**] y :blue[**tecnologías móviles**] en proyectos 
            de CBL permite un seguimiento más preciso del impacto y la adaptación en 
            tiempo real de las intervenciones. Esto es particularmente relevante en 
            Latinoamérica.
            """)

    st.write("""
    El CBL, potenciado por la tecnología, ofrece un camino prometedor para la educación en 
    Latinoamérica. Al combinar el aprendizaje académico con la acción comunitaria y las herramientas 
    digitales, podemos formar una generación de líderes capaces de abordar los desafíos complejos 
    de la región. Circle Up Community se compromete a impulsar esta visión, promoviendo un 
    aprendizaje que sea tanto académicamente riguroso como socialmente impactante.
    """)

    st.title("Preguntas Frecuentes")
    faq1, faq2, faq3 = st.columns(3)
    
    with faq1:
        st.info("""
        :blue[**¿Cómo beneficia el CBL a las comunidades latinoamericanas?**]

        El CBL aporta recursos, conocimientos y energía joven a proyectos comunitarios, 
        fomentando soluciones innovadoras a problemas locales. Este enfoque promueve 
        el desarrollo sostenible y fortalece los lazos entre instituciones educativas 
        y comunidades, creando un impacto duradero en la región.
        """)

    with faq2:
        st.info("""
        :blue[**¿Qué desafíos tecnológicos enfrenta el CBL en la región?**]

        La brecha digital y el acceso desigual a internet son retos significativos 
        para el CBL en Latinoamérica. Sin embargo, el uso creativo de tecnologías 
        móviles y soluciones de bajo ancho de banda están ayudando a superar estas 
        barreras, permitiendo una participación más inclusiva en proyectos de CBL.
        """)

    with faq3:
        st.info("""
        :blue[**¿Cómo se mide el éxito del CBL en contextos latinoamericanos?**]

        El éxito del CBL se evalúa mediante una combinación de indicadores académicos, 
        impacto social medible y desarrollo de habilidades prácticas. La retroalimentación 
        de las comunidades beneficiadas es crucial, así como la capacidad para aplicar conocimientos en contextos reales y diversos de la región.
        """)

if __name__ == "__main__":
    try:
        main()
        menu()
        st.divider()
        st.image('./gallery/WebSvg/main_footer.svg', use_column_width=True)
        if st.button(':material/hiking: Volver al Inicio', type="secondary", help='Volver al menú principal', use_container_width=True):
            st.switch_page('app.py')
    except:
        st.switch_page('app.py')

