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
    
    st.title(":material/travel_explore: Explorando el Community-Based Learning")

    
    st.write("""
    Circle Up Community es una iniciativa que busca explorar el potencial del Community-Based Learning (CBL) en conjunto con tecnologías emergentes. Nuestro enfoque se centra en desarrollar un ecosistema de aprendizaje colaborativo, aprovechando el talento local y los recursos comunitarios. Aspiramos a mejorar la educación conectando las experiencias de aprendizaje con las necesidades de la comunidad. A través de nuestra plataforma, trabajamos para facilitar la interacción entre voluntarios, participantes y recursos educativos, con el objetivo de fomentar un ambiente de crecimiento mutuo y desarrollo comunitario sostenible.
    """)

    
    col1, col2 = st.columns(2)

    with col1:
        
        with st.container(border=True):
            st.write("""
            Buscamos contribuir al aprendizaje comunitario desarrollando un modelo adaptable. Nuestro objetivo es optimizar el uso del talento local, fomentar la colaboración entre generaciones y utilizar espacios públicos como centros de aprendizaje. Nos esforzamos por desarrollar habilidades relevantes para el contexto actual, fortalecer los lazos comunitarios y la innovación local a través de una plataforma tecnológica accesible.
            """)

            st.image('./gallery/icons/h_bear.svg', use_column_width=True)
        
        st.info("""
        Circle Up Community se basa en la :blue[**colaboración**], el :blue[**aprendizaje adaptativo**] y la :blue[**innovación responsable**]. Exploramos cómo combinar el voluntariado local con análisis de datos para crear experiencias educativas relevantes y beneficiosas para nuestra comunidad.
        """,icon=":material/self_improvement:")

    with col2:

        st.info("""
        Nuestro método se basa en cuatro áreas :blue[**Voluntariado Académico**], :blue[**Tecnología Educativa**], :blue[**Evaluación de Impacto**] y :blue[**Participación Comunitaria**]. Trabajamos para integrar estos elementos en un ecosistema de aprendizaje en constante evolución.
        """,icon=":material/self_improvement:")
        
        
        with st.container(border=True):
            
            st.image('./gallery/icons/h_leopard.svg', use_column_width=True)
            
            st.write("""
            Estamos desarrollando un sistema que abarca desde la coordinación de voluntarios hasta la creación de contenido educativo. Nuestra plataforma busca facilitar la conexión entre profesionales locales y oportunidades de enseñanza. Uso de tecnología para adaptar y mejorar los programas educativos. Análisis de datos para comprender las  tendencias en la comunidad.
            """)

    st.write("""
    Circle Up Community representa un esfuerzo por unir tecnología, educación y desarrollo comunitario de manera innovadora. Nuestro proyecto aspira no solo a educar, sino también a fortalecer los lazos sociales y fomentar un sentido de pertenencia compartido. Nos comprometemos a basar nuestras decisiones en evidencia, evaluar constantemente nuestro impacto y adaptarnos a las necesidades cambiantes de la comunidad. Invitamos a profesionales, investigadores y entusiastas a explorar con nosotros este camino de aprendizaje colectivo.
    """)

    
    st.title("Preguntas Frecuentes")
    
    
    st.write("""
    Para ayudarte a comprender mejor Circle Up Community y las formas de participación, hemos recopilado algunas preguntas comunes. Si tienes inquietudes adicionales, te invitamos a contactarnos. Estaremos encantados de proporcionarte más información sobre nuestro proyecto y las oportunidades de involucrarte en esta iniciativa comunitaria.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            # st.image('./gallery/icons/h_zebra.svg', use_column_width=True)
            st.info("""
            :blue[**¿Cómo puedo participar como voluntario?**]

            Puedes registrarte en nuestra plataforma, compartiendo tus habilidades e intereses. Trabajamos para conectar voluntarios con oportunidades de enseñanza que se alineen con sus experiencias y las necesidades de la comunidad.
            """,icon=":material/unknown_document:")
            

    with col2:
        with st.container(border=True):
            # st.image('./gallery/icons/h_kids.svg', use_column_width=True)
            st.info("""
            :blue[**¿Qué tipo de actividades educativas se ofrecen?**]

            Exploramos una variedad de temas, desde habilidades prácticas hasta desarrollo personal. El contenido se adapta según las necesidades y las experiencias compartidas por los voluntarios.
            """,icon=":material/unknown_document:")

    with col3:
        with st.container(border=True):
            # st.image('./gallery/icons/h_gorilla.svg', use_column_width=True)
            st.info("""
            :blue[**¿Cómo evalúan el impacto del programa?**]

            Utilizamos diversas herramientas como encuestas y análisis de datos. Buscamos entender tanto el desarrollo de habilidades como los cambios en la cohesión social y el bienestar comunitario a lo largo del tiempo.
            """,icon=":material/unknown_document:")

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