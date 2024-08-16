import streamlit as st
import pandas as pd


def create_html_table(df):
    html = """
    <style>
    .reference-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 14px;
        border: 0.2px solid #ddd;
        border-radius: 15px;
        overflow: hidden;
    }
    .reference-table th, .reference-table td {
        border: 0.2px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .reference-table th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    .reference-table td {
        color: #2C2C2C;
    }
    .link-button {
        background-color: #9d8ec7;
        color: white !important;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 15px;
        font-size: 14px;
        transition: background-color 0.3s;
        font-weight: bold;
    }
    .link-button:hover {
        background-color: #8a7cb2;
    }
    /* Estilos para bordes redondeados */
    .reference-table tr:first-child th:first-child {
        border-top-left-radius: 15px;
    }
    .reference-table tr:first-child th:last-child {
        border-top-right-radius: 15px;
    }
    .reference-table tr:last-child td:first-child {
        border-bottom-left-radius: 15px;
    }
    .reference-table tr:last-child td:last-child {
        border-bottom-right-radius: 15px;
    }
    </style>
    <table class="reference-table">
    <tr>
        <th>Referencia (APA)</th>
        <th>Enlace</th>
    </tr>
    """
    
    for _, row in df.iterrows():
        html += f'<tr><td>{row["Referencia (APA)"]}</td>'
        if row['Enlace'] != "Sin Referencia":
            html += f'<td><a href="{row["Enlace"]}" target="_blank" class="link-button">Enlace</a></td>'
        else:
            html += '<td>Sin Referencia</td>'
        html += '</tr>'
    
    html += "</table>"
    return html

def main_es():

    st.title("Resumen")

    st.write("""
    Circle Up Community es una iniciativa que combina el voluntariado académico con tecnología para impulsar el desarrollo de habilidades comunitarias. Este proyecto va más allá de ser un programa de voluntariado; es una :blue[**plataforma tecnológica integral**] diseñada para optimizar el uso del capital humano local y fomentar un :blue[**ecosistema de aprendizaje colaborativo y adaptativo**].
    """)

    st.title("Fundamentación Conceptual y Contexto")


    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            st.info("""
            El proyecto se basa en un marco teórico sólido que integra conceptos clave como, :blue[**Community-Based Learning (CBL)**], :blue[**Aprendizaje a lo largo de la vida**] y :blue[**Economía del conocimiento**]
            """, icon=":material/diversity_3:")

        with col2:
            st.success("""
            Circle Up Community responde a las necesidades de la :green[**cuarta revolución industrial**], donde la adaptabilidad y el aprendizaje continuo son cruciales.
            """, icon=":material/charger:")


    st.write("""
    Esta infraestructura tecnológica permite que Circle Up Community sea a la vez estandarizada en su gestión y flexible en su implementación, adaptándose a las necesidades de la comunidad.
    """)

    st.title("Problema Central y Objetivos")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Problema Central y Objetivo General**
            
            1. Subutilización del capital humano local en Tocancipá para el desarrollo de habilidades comunitarias.
            
            2. Optimizar el aprovechamiento del capital humano local para el desarrollo de habilidades comunitarias en Tocancipá.
            """, icon=":material/target:")
    
        with col2:
            st.info("""
            **Objetivos Específicos**
            
            1. :blue[**Implementar un sistema estructurado de voluntariado académico.**]
            
            2. :blue[**Alinear las habilidades locales con las necesidades de la comunidad.**]
            """, icon=":material/self_improvement:")

    st.title("Articulación Institucional")

    st.write("""
    Circle Up Community, como iniciativa de Community-Based Learning (CBL) en Tocancipá, establece una relación significativa con la Secretaría de Desarrollo e Integración Social, particularmente a través del Programa Juventud. Esta colaboración estratégica potencia el impacto de ambas en el desarrollo comunitario y juvenil del municipio.
    """)

    st.write("Aportes de Circle Up al Programa Juventud")

    st.write("""
    1. **Capacidades Juveniles** Capacitar a jóvenes en la construcción de su proyecto de vida. Los cursos y talleres ofrecidos por Circle Up desarrollan habilidades blandas y técnicas esenciales para el futuro personal y profesional de los participantes.
    2. **Participación Comunitaria** Incrementar la participación juvenil en proyectos comunitarios. Esto fortalece el tejido social y promueve el liderazgo juvenil en Tocancipá.
    3. **Conexión con Expertos** Circle Up facilita la interacción entre jóvenes y profesionales experimentados de diversos campos. Esta conexión proporciona orientación valiosa sobre emprendimiento y desarrollo profesional, complementando los esfuerzos del Programa Juventud en la creación de redes de apoyo para los jóvenes.
    """)


    st.title("Plataforma Tecnológica e Innovación")

    st.write("""
    El núcleo de Circle Up Community es una :blue[**plataforma digital**] que ofrece más que la simple gestión de voluntarios.
    """)

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            :blue[**Inteligencia Artificial**]
            
            Algoritmos que colaboran con los voluntarios para desarrollar y adaptar programas educativos personalizados.
            """, icon=":material/rocket:")
        
        with col2:
            st.info("""
            :blue[**Sistema de Automatización de Procesos**]
            
            Mejora la asignación de recursos, la programación de cursos y el seguimiento del progreso de los participantes.
            """, icon=":material/rocket:")
        
        with col3:
            st.info("""
            :blue[**Análisis Predictivo**]
            
            Utiliza datos para identificar tendencias en las necesidades de aprendizaje de la comunidad y anticipar demandas.
            """, icon=":material/rocket:")
        
    
    with st.container(border=True):
        st.success("""
        **Beneficios**

        Esta infraestructura tecnológica permite que Circle Up Community sea a la vez, :green[**Estandarizada en su gestión**], :green[**Flexible en su implementación**]. Adaptándose a las necesidades específicas de la comunidad.
        """, icon=":material/bubble_chart:")

    st.image('./gallery/icons/research.svg',use_column_width=True)

    st.title("Introducción")

    st.write("Tocancipá, un municipio ubicado en la región de Sabana Centro de Colombia, ha experimentado un notable crecimiento industrial y económico en los últimos años. Este desarrollo ha traído consigo una serie de cambios demográficos y sociales que han impactado significativamente el panorama educativo y laboral de la región. El rápido crecimiento poblacional, impulsado en parte por la migración laboral, ha puesto de manifiesto desafíos en términos de desarrollo de habilidades y acceso a oportunidades educativas que se alineen con las demandas del mercado laboral en evolución.")

    st.write("La región enfrenta retos particulares en el desarrollo de habilidades blandas entre su población joven, una situación que puede afectar la empleabilidad y el desarrollo económico a largo plazo. Además, la brecha intergeneracional en términos de habilidades digitales y conocimientos técnicos presenta otro desafío importante para la cohesión social y el desarrollo comunitario.")

    st.info("""
    **Desafíos Clave**
    - Rápido crecimiento poblacional e industrial
    - Desarrollo de habilidades blandas en la población joven
    - Brecha intergeneracional en habilidades digitales y técnicas
    """, icon=":material/pool:")


    st.title("Justificación")

    st.write("""
    El panorama social y educativo en Colombia, particularmente en regiones de rápido crecimiento industrial, presenta una serie de desafíos interconectados que requieren soluciones innovadoras y adaptables. Esta iniciativa surge como respuesta a estas múltiples problemáticas, buscando abordarlas de manera integral y efectiva.

    Uno de los retos más apremiantes es la brecha entre las habilidades demandadas por el mercado laboral y aquellas que posee la fuerza de trabajo actual. En áreas de acelerado desarrollo económico, esta disparidad se acentúa, creando una demanda de competencias específicas que el sistema educativo tradicional no logra satisfacer con la rapidez necesaria. Un enfoque que facilite la transferencia de conocimientos prácticos y actualizados entre profesionales locales y miembros de la comunidad podría contribuir significativamente a reducir esta brecha.
    """)





    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(':blue[**Deserción y Habilidades Blandas**]',icon=':material/kayaking:')
            st.info("""La deserción escolar y universitaria representa otro desafío crítico. Ofrecer formación práctica y relevante podría aumentar la motivación de los estudiantes y mejorar sus perspectivas de empleabilidad. Además, el desarrollo de habilidades blandas, cada vez más valoradas en el ámbito laboral, es otra área donde el sistema educativo tradicional a menudo queda corto.
            """)

        with col2:
            st.info(':blue[**Aprendizaje Continuo y Desempleo Juvenil**]',icon=':material/kayaking:')
            st.info("""La falta de oportunidades de aprendizaje continuo y actualización profesional, especialmente fuera de las grandes ciudades, es otro desafío que requiere atención. El desempleo juvenil y el subempleo son problemas persistentes. Iniciativas que mejoren las habilidades de los jóvenes y creen redes de contactos profesionales podrían abrir nuevas oportunidades laborales.
            """)

        with col3:
            st.info(':blue[**Desigualdad y Envejecimiento**]',icon=':material/kayaking:')
            st.info("""La desigualdad en el acceso a recursos educativos de calidad entre regiones merece atención. Aprovechar el talento local y las tecnologías digitales podría llevar conocimientos especializados a comunidades con acceso limitado. El envejecimiento de la población presenta la necesidad de aprovechar la experiencia de los adultos mayores, fomentando su inclusión social y sentido de propósito.
            """)

    st.write("""
    La falta de espacios para la innovación social a nivel local es otra área de oportunidad. Plataformas de colaboración comunitaria podrían catalizar el surgimiento de soluciones innovadoras a problemas locales. Finalmente, la necesidad de fortalecer el tejido social y el sentido de comunidad, especialmente en áreas de rápido crecimiento demográfico, es un aspecto crucial. Fomentar interacciones significativas entre miembros de la comunidad a través del aprendizaje compartido podría contribuir a la cohesión social y al desarrollo integral de la región.
    """)
    
    st.info("El CBL y la integración de tecnologías emergentes ofrecen un enfoque prometedor para abordar los desafíos educativos y sociales de Tocancipá.", icon=":material/memory:")

    st.title("Marco Conceptual y Metodológico")

    st.write("""
    El fundamento conceptual de Circle Up Community se basa en una convergencia de teorías y prácticas educativas que han evolucionado en respuesta a los desafíos de la sociedad contemporánea. Este marco teórico explora los conceptos clave que sustentan la iniciativa, proporcionando una base para su desarrollo y evaluación crítica.
    """)

    st.title("Community-Based Learning (CBL)")

    st.info("""
    :blue[**Definición de CBL**]: El Community-Based Learning (CBL) es un enfoque pedagógico que 
    integra el aprendizaje académico con el servicio comunitario y la reflexión crítica.
    """, icon=":material/bubble_chart:")

    st.write("""
    Este modelo tiene sus raíces en la filosofía educativa de John Dewey, quien argumentaba que el 
    aprendizaje más efectivo ocurre a través de la experiencia y la reflexión sobre esa experiencia 
    (*Giles & Eyler*, 1994, p. 78). En las últimas décadas, el CBL ha evolucionado para incluir una 
    variedad de prácticas, desde el aprendizaje-servicio hasta la investigación-acción participativa.

    *Bringle y Clayton* (2020) definen el (SL) de "aprendizaje-servicio" (service-learning en inglés) 
    como un enfoque educativo que combina el aprendizaje académico con el servicio comunitario. Los 
    estudiantes aplican lo que aprenden en clase para abordar problemas reales en su comunidad, y a 
    su vez, reflexionan sobre sus experiencias para profundizar su comprensión académica. (p. 47).

    Según *Bringle y Clayton* (2020), este enfoque innovador integra de manera significativa el 
    servicio a la comunidad en el currículo académico de las universidades, otorgando a los estudiantes 
    créditos por el aprendizaje adquirido a través de su compromiso activo en la resolución de problemas 
    del mundo real.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(":green[**Reflexión**]\n\nLa reflexión crítica sobre las experiencias es fundamental en el proceso de aprendizaje-servicio.", icon=":material/emoji_objects:")

    with col2:
        st.success(":green[**Aprendizaje Experiencial**]\n\nLos estudiantes aplican conocimientos teóricos a problemas del mundo real.", icon=":material/experiment:")

    with col3:
        st.success(":green[**Colaboración Comunitaria**]\n\nEstudiantes, académicos y miembros de la comunidad trabajan juntos en proyectos de beneficio mutuo.", icon=":material/handshake:")

    st.write("""
    El aprendizaje-servicio trasciende las aulas universitarias y se extiende a la comunidad en general. 
    Estudiantes, académicos y miembros de la comunidad trabajan de la mano, compartiendo conocimientos, 
    habilidades y perspectivas diversas. Este enfoque colaborativo fomenta la creación de comunidades 
    de aprendizaje donde todos los participantes se convierten en recursos de enseñanza, solucionadores 
    de problemas y socios en la búsqueda de soluciones a los desafíos del mundo real.

    El (SL) ha sido elogiado por su potencial para fomentar el compromiso cívico y el aprendizaje 
    experiencial, uniendo a estudiantes y comunidades en proyectos de beneficio mutuo. Sin embargo, 
    como señala *Stoecker* (2016), el (SL) no está exento de críticas.
    """)

    st.info(""":blue[**Crítica al SL**]: *Stoecker* (2016) argumenta que el (SL) institucionalizado a menudo se centra en los resultados de aprendizaje de los estudiantes, dejando de lado las necesidades y prioridades de la comunidad. Este enfoque puede perpetuar dinámicas de poder desiguales, donde las instituciones educativas dictan los términos del compromiso sin una verdadera colaboración con la comunidad.""", icon=":material/hiking:")

    st.write("""
    Además, existe la crítica de que el (SL) puede caer en el "tokenismo" o práctica de involucrar a 
    miembros de la comunidad de manera superficial o simbólica, utilizando a las comunidades como meros 
    escenarios de aprendizaje para los estudiantes, sin un compromiso genuino con el cambio social.

    Estas críticas no pretenden invalidar el (SL), sino más bien subrayar la importancia de un diseño 
    cuidadoso y una evaluación continua de estos programas. Para que el (SL) sea verdaderamente 
    transformador, debe basarse en relaciones equitativas y respetuosas entre las instituciones 
    educativas y las comunidades. Esto implica reconocer y valorar el conocimiento y la experiencia 
    de los miembros de la comunidad, así como involucrarlos en todas las etapas del proceso, desde 
    la identificación de necesidades hasta la evaluación del impacto.
    """)


    st.title("Aprendizaje a lo largo de la vida")

    st.write("""
    El concepto de aprendizaje a lo largo de la vida ha ganado prominencia en las últimas décadas como 
    respuesta a los rápidos cambios tecnológicos y sociales. La UNESCO ha sido un defensor clave de este 
    enfoque, argumentando que el aprendizaje a lo largo de la vida es esencial para el desarrollo 
    sostenible y la cohesión social (*UNESCO*, 2016, p. 8).
    """)

    st.info("""
    :blue[**Definición de LLL**]: El aprendizaje a lo largo de toda la vida o Life Long Learning por 
    sus siglas en inglés (LLL) abarca toda la gama de aprendizaje que incluye: formal, informal y no formal.

    -- *Laal y Salamati* (2012)
    """, icon=":material/hiking:")

    st.write("""
    Esta perspectiva amplia del aprendizaje reconoce que la educación no se limita a las instituciones 
    formales o a una etapa particular de la vida. Los autores destacan que el LLL ocurre en diversos 
    contextos, incluyendo experiencias cotidianas, el lugar de trabajo y actividades de ocio, y que 
    puede conducir tanto al desarrollo personal como al crecimiento profesional.

    Además, *Laal y Salamati* (2012) señalan que "en el siglo XXI, todos debemos ser aprendices de por 
    vida. Necesitamos mantener continuamente nuestras habilidades actualizadas para tener una ventaja 
    en todo lo que hacemos". Esta afirmación subraya la importancia del aprendizaje continuo en el mundo 
    actual, que cambia rápidamente, y enfatiza que el aprendizaje no es solo un medio para un fin, sino 
    un proceso continuo que abarca toda la vida.
    """)

    st.warning("""
    :orange[**Desafío de equidad**]: Sin embargo, es crucial reconocer que el acceso a oportunidades 
    de aprendizaje a lo largo de la vida no es equitativo (*Desjardins & Ioannidou*, 2020). Factores 
    como el nivel socioeconómico, la ubicación geográfica y las obligaciones familiares pueden limitar 
    la capacidad de las personas para participar en el aprendizaje continuo.
    """, icon=":material/hiking:")

    st.write("""
    Aquellos que ya están mejor educados y aquellos con posiciones profesionales relativamente seguras 
    están expandiendo aún más su ventaja a través de inversiones adicionales en el aprendizaje de adultos, 
    el llamado principio de Mateo o al fenómeno en el que aquellos que ya tienen ventajas, como una mejor 
    educación o posiciones profesionales seguras, continúan acumulando más ventajas a través de la 
    participación en el aprendizaje. Los hallazgos de la investigación hasta la fecha también confirman 
    que, por varias razones, las empresas apoyan a aquellos empleados en su desarrollo de competencias 
    que ya poseen mayores habilidades. Por lo tanto, cualquier iniciativa que busque promover el 
    aprendizaje a lo largo de la vida debe abordar estas barreras de manera proactiva.
    """)

    st.success("""
    :green[**Implicación clave**]: Las iniciativas de aprendizaje a lo largo de la vida deben 
    diseñarse teniendo en cuenta la equidad, abordando proactivamente las barreras que impiden 
    el acceso y la participación de todos los segmentos de la sociedad.
    """, icon=":material/pool:")

    st.title("Economía del conocimiento")

    st.info("""
    :blue[**Definición de Economía del Conocimiento**]: La economía del conocimiento representa un cambio 
    de paradigma en el que la producción y los servicios se basan principalmente en actividades intensivas 
    en conocimiento.
    """, icon=":material/lightbulb:")

    st.write("""
    Este cambio se caracteriza por un mayor énfasis en las capacidades intelectuales que en los insumos 
    físicos o los recursos naturales. *Powell y Snellman* (2004) señalan que la economía del conocimiento 
    se distingue por "una mayor dependencia de las capacidades intelectuales que de los insumos físicos 
    o los recursos naturales" (p. 201). En este sentido, la innovación, la creatividad y la capacidad de 
    adaptación son cruciales para el éxito en este nuevo modelo económico.

    La economía del conocimiento también se caracteriza por un ritmo acelerado de cambio tecnológico y 
    científico. Las nuevas tecnologías y los avances científicos surgen a un ritmo sin precedentes, lo 
    que a su vez conduce a una rápida obsolescencia de los productos y servicios existentes. *Powell y 
    Snellman* (2004) afirman que la economía del conocimiento se caracteriza por "un ritmo acelerado de 
    avance técnico y científico, así como por una obsolescencia igualmente rápida" (p. 199). En este 
    entorno, las empresas y los individuos deben ser capaces de adaptarse rápidamente a los cambios para 
    seguir siendo competitivos.

    Además, la economía del conocimiento está impulsada por la producción y difusión de nuevos 
    conocimientos. Las inversiones en investigación y desarrollo (I+D), educación y tecnología de la 
    información y la comunicación son fundamentales para el crecimiento y el desarrollo. Esto implica 
    que el conocimiento no solo se produce, sino que también se comparte y se aplica de manera efectiva 
    en todos los niveles de la economía.
    """)

    st.title("Habilidades del Siglo XXI")

    st.write("""
    En este contexto, las "habilidades del siglo XXI" han ganado prominencia. *Binkley et al.* (2012) 
    identificaron diez habilidades clave para el siglo XXI, agrupándolas en cuatro categorías:
    """)

    with st.expander("Ver Habilidades del Siglo XXI"):
        st.markdown("""
        - **Formas de pensar:** Creatividad e innovación, pensamiento crítico, resolución de problemas y toma de decisiones, y aprender a aprender y metacognición.
        - **Formas de trabajar:** Comunicación y colaboración (trabajo en equipo).
        - **Herramientas para trabajar:** Alfabetización informacional (que incluye investigación) y alfabetización en TIC.
        - **Vivir en el mundo**: Ciudadanía (local y global), vida y carrera, y responsabilidad personal y social (incluyendo conciencia y competencia cultural) (p. 18-19).
        """)

    st.write("""
    Estas habilidades reflejan la creciente necesidad de que los individuos se adapten a los cambios 
    rápidos en la sociedad y la tecnología. Se enfatiza la importancia de que los estudiantes desarrollen 
    un pensamiento de orden superior, habilidades de resolución de problemas flexibles y colaboración, 
    y habilidades de comunicación para tener éxito en el trabajo y la vida.
    """)

    st.title("Tendencias en el mercado laboral")

    st.write("""
    Un informe del Foro Económico Mundial (2023) sobre el futuro del trabajo revela tendencias 
    significativas en el mercado laboral, especialmente en lo que respecta a la creciente importancia 
    de las habilidades blandas y la adopción de tecnología. El informe, basado en una encuesta a 803 
    empresas en 27 sectores y 45 economías, destaca que más del 85% de las organizaciones encuestadas 
    anticipan que la adopción de tecnologías nuevas y de vanguardia, junto con un mayor acceso digital, 
    impulsará la transformación en sus empresas (Foro Económico Mundial, 2023, p. 10).

    En América Latina, se espera que las empresas adopten principalmente tecnologías como el big data, 
    la computación en la nube y la inteligencia artificial (IA) en los próximos cinco años (Foro 
    Económico Mundial, 2023, pp. 32-33). Aunque se prevé que la mayoría de estas tecnologías tengan un 
    impacto positivo neto en el empleo, las empresas de la región también anticipan una importante 
    disrupción laboral debido a factores como el aumento del costo de vida y la ralentización del 
    crecimiento económico (Foro Económico Mundial, 2023, pp. 20-21).
    """)

    st.success("""
    :green[**Importancia de las habilidades blandas**]: El informe subraya la creciente importancia de 
    las habilidades blandas en el entorno laboral actual. A pesar de los avances en automatización, el 
    pensamiento analítico y creativo siguen siendo las habilidades más valoradas por los empleadores 
    (Foro Económico Mundial, 2023, p. 38). Además, habilidades como la resiliencia, la flexibilidad, 
    la motivación y la autoconciencia son cada vez más esenciales para que los trabajadores se adapten 
    a los cambios constantes en el lugar de trabajo y colaboren eficazmente (Foro Económico Mundial, 2023, p. 38).
    """, icon=":material/scuba_diving:")

    st.warning("""
    Se estima que el 44% de las habilidades actuales de los trabajadores podrían quedar obsoletas en 
    los próximos cinco años (Foro Económico Mundial, 2023, p. 37), lo que subraya la necesidad urgente 
    de invertir en programas de capacitación y actualización.
    """, icon=":material/hiking:")

    st.write("""
    Las empresas de la región reconocen esta necesidad y planean invertir en el aprendizaje y la 
    capacitación en el trabajo como parte de sus estrategias para el futuro (Foro Económico Mundial, 
    2023, p. 50). No obstante, la responsabilidad de cerrar esta brecha de habilidades no recae únicamente 
    en las empresas, sino que requiere un esfuerzo conjunto de los sectores público y privado para 
    garantizar que los trabajadores estén preparados para los desafíos y oportunidades que presenta la 
    economía del conocimiento.
    """)

    st.title("Políticas públicas y prácticas organizacionales")

    st.write("""
    Las políticas públicas y las prácticas organizacionales juegan un papel crucial en la economía del 
    conocimiento al facilitar el desarrollo de habilidades y la adaptabilidad de la fuerza laboral. 
    *Brown et al.* (2020) argumentan que la teoría ortodoxa del capital humano ha llevado a políticas 
    que reducen la productividad humana a "aprender para ganar", lo que limita el potencial de crecimiento 
    y desarrollo de los trabajadores.

    En este sentido, es fundamental que las políticas públicas promuevan un enfoque más holístico de la 
    educación y el desarrollo de habilidades, que vaya más allá de la simple adquisición de credenciales 
    y se centre en el crecimiento personal y el florecimiento humano (*Brown et al.*, 2020, p. 143). 
    Esto implica fomentar habilidades como el pensamiento crítico, la creatividad, la colaboración y la 
    adaptabilidad, que son esenciales en la economía del conocimiento en constante cambio.
    """)

    st.info("""
    :blue[**Prácticas organizacionales**]: Las prácticas organizacionales deben adaptarse para apoyar 
    el desarrollo continuo de los empleados y fomentar una cultura de aprendizaje. Esto puede incluir 
    programas de capacitación y desarrollo, oportunidades de aprendizaje en el trabajo, tutoría y coaching, 
    y sistemas de evaluación del desempeño que reconozcan y recompensen el aprendizaje y el crecimiento 
    (*Brown et al.*, 2020, p. 183).
    """, icon=":material/account_tree:")

    st.write("""
    El aprendizaje-servicio (SL) puede complementar este enfoque al proporcionar oportunidades para 
    que los empleados apliquen sus conocimientos y habilidades en contextos reales y desarrollen un 
    sentido de responsabilidad cívica (*Bringle & Clayton*, 2020). Al participar en proyectos de SL, 
    los empleados pueden adquirir nuevas habilidades, ampliar sus perspectivas y fortalecer su compromiso 
    con el aprendizaje continuo y el crecimiento personal.
    """)


    st.success("""
    :green[**Beneficios del Aprendizaje-Servicio en Organizaciones**]:
    - Aplicación práctica de conocimientos y habilidades
    - Desarrollo de responsabilidad cívica
    - Adquisición de nuevas habilidades
    - Ampliación de perspectivas
    - Fortalecimiento del compromiso con el aprendizaje continuo
    - Fomento del crecimiento personal
    """, icon=":material/potted_plant:")


    st.title("Innovación social")

    st.info("""
    :blue[**Definición de Innovación Social**]: La innovación social representa cambios en las relaciones 
    sociales, sistemas de gobernanza y empoderamiento colectivo que conducen a una mayor inclusión social.

    -- *Moulaert y MacCallum* (2019, p. 13)
    """, icon=":material/self_improvement:")

    st.write("""
    La innovación social ha emergido como un campo de estudio y práctica que busca abordar desafíos 
    sociales complejos a través de soluciones novedosas. Esta definición enfatiza el aspecto transformador 
    de la innovación social, más allá de simplemente proponer nuevas soluciones.

    El concepto de innovación social ha ganado prominencia en las últimas décadas como respuesta a la 
    creciente complejidad de los problemas sociales y a las limitaciones de las soluciones tradicionales 
    basadas en el mercado o la tecnología. *Howaldt et al.* (2018) argumentan que la innovación social 
    representa un cambio de paradigma en cómo abordamos los desafíos sociales, alejándonos de soluciones 
    puramente tecnológicas o de mercado hacia enfoques más participativos y centrados en la comunidad (pág. 16).
    """)

    st.info("""
    :blue[**Definición ampliada**]: La innovación social se define como el desarrollo e implementación 
    de nuevas ideas, productos, servicios y modelos que satisfacen necesidades sociales y crean nuevas 
    relaciones sociales o colaboraciones (*Howaldt et al.*, 2018, pág. 84).
    """, icon=":material/notifications:")

    st.write("""
    A diferencia de la innovación tradicional, que a menudo se centra en el beneficio económico y la 
    ventaja competitiva, la innovación social prioriza el bienestar social y la creación de valor público. 
    Este enfoque reconoce que los problemas sociales complejos, como la pobreza, la desigualdad y el 
    cambio climático, requieren soluciones que vayan más allá de las intervenciones individuales y 
    aborden las causas fundamentales de los problemas.

    *Howaldt et al.* (2018) enfatizan que la innovación social no se limita a un solo sector o disciplina, 
    sino que abarca una amplia gama de actores, incluidos ciudadanos, organizaciones sin fines de lucro, 
    empresas, instituciones gubernamentales e instituciones de investigación (pág. 4). La colaboración 
    entre estos diversos actores es esencial para aprovechar diferentes perspectivas, conocimientos y 
    recursos, lo que permite el desarrollo de soluciones más integrales y sostenibles. Además, la 
    innovación social a menudo implica la participación activa de los ciudadanos y las comunidades 
    afectadas por los problemas sociales, lo que garantiza que las soluciones sean relevantes y respondan 
    a sus necesidades específicas.
    """)

    st.success("""
    :green[**Hallazgo clave**]: *Krlev et al.* (2021) encontraron en su estudio empírico que "las 
    iniciativas de innovación social más exitosas son aquellas que logran crear redes diversas de 
    actores y fomentar la co-creación con la comunidad" (p. 288).
    """, icon=":material/travel_explore:")

    st.write("""
    Este hallazgo subraya la importancia de la participación y el empoderamiento comunitario en los 
    procesos de innovación social. La co-creación, en particular, permite que las soluciones sean 
    diseñadas y desarrolladas en colaboración con aquellos que experimentan los problemas sociales, 
    asegurando así que las innovaciones sean relevantes y respondan a las necesidades reales de la 
    comunidad (p. 259).

    Además, *Krlev et al.* (2021) destacan que la innovación social no se trata solo de crear nuevas 
    ideas o soluciones, sino de institucionalizar nuevas prácticas que aborden las causas fundamentales 
    de los problemas sociales (p. 280). El estudio también revela que el éxito de la innovación social 
    a menudo depende de la capacidad de los actores para movilizar diversos recursos y establecer 
    colaboraciones intersectoriales (p. 281). Esto puede incluir la combinación de recursos financieros, 
    humanos y sociales de diferentes sectores, como el gobierno, las empresas y las organizaciones de 
    la sociedad civil. Al aprovechar las fortalezas y los conocimientos de diversos actores, las 
    iniciativas de innovación social pueden lograr un mayor impacto y abordar los problemas sociales 
    de manera más integral.
    """)

    st.warning("""
    :orange[**Advertencia**]: *Pel et al.* (2020) advierten sobre el riesgo de que "la retórica de la 
    innovación social se utilice para justificar la retirada del estado de la provisión de servicios 
    sociales, sin abordar las causas estructurales de los problemas sociales" (pág. 2).
    """, icon=":material/hiking:")

    st.write("""
    Esta crítica subraya la necesidad de considerar la innovación social en el contexto más amplio de 
    las políticas sociales y las estructuras de poder existentes. No se debe ver como una panacea para 
    todos los problemas sociales, sino como una herramienta que puede ser utilizada de manera efectiva 
    o ineficaz, dependiendo de cómo se implemente y quién la controle.

    *Pel et al.* (2020) también señalan la importancia de comprender la innovación social como un proceso 
    relacional y contextualizado (pág. 3). Las innovaciones sociales no ocurren en el vacío; están 
    profundamente arraigadas en las relaciones sociales existentes y en contextos sociomateriales específicos. 
    Por lo tanto, el análisis de la innovación social debe ir más allá de las iniciativas individuales y 
    considerar las dinámicas de poder, las instituciones y las estructuras sociales que dan forma a estas 
    innovaciones.

    Además, *Pel et al.* (2020) destacan la necesidad de distinguir entre diferentes tipos de innovación 
    social (pág. 5). No todas las innovaciones sociales son iguales en términos de su potencial transformador. 
    Algunas pueden ser incrementales, mientras que otras pueden ser más radicales y desafiar las estructuras 
    de poder existentes. Es crucial, por lo tanto, desarrollar una comprensión más matizada de los diversos 
    tipos de innovación social y sus implicaciones para el cambio social.
    """)

    st.title("Tecnologías emergentes en educación")

    st.write("""
    En el contexto latinoamericano, la adopción de tecnologías emergentes en educación presenta tanto 
    oportunidades como desafíos únicos. La región ha experimentado un crecimiento significativo en el 
    uso de tecnologías educativas en la última década, impulsado por la necesidad de mejorar la calidad 
    y el acceso a la educación en diversos contextos socioeconómicos.
    """)

    st.warning("""
    :orange[**Desafío en la Adopción de Tecnologías**]: *Avello Martínez et al.* (2021) señalan que 
    "las áreas urbanas se han beneficiado más que las rurales" (p. 45) en la integración de tecnologías 
    educativas.
    """, icon=":material/developer_board:")

    st.write("""
    Esta disparidad se debe a varios factores, incluyendo la falta de infraestructura tecnológica en 
    áreas rurales, la insuficiente capacitación docente en el uso de tecnologías emergentes y las 
    limitaciones económicas que impiden a muchas escuelas rurales adquirir y mantener estas tecnologías.
    """)

    st.title("Tecnologías emergentes prometedoras")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        :blue[**Aprendizaje móvil**]: *Crompton y Burke* (2018) argumentan que "el alto índice de 
        penetración de teléfonos móviles en países en desarrollo ofrece una oportunidad única para 
        democratizar el acceso a recursos educativos digitales" (p. 53).
        """, icon=":material/developer_board:")

    with col2:
        st.info("""
        :blue[**Inteligencia Artificial**]: *Zawacki-Richter et al.* (2019) señalan que "la IA en 
        educación tiene el potencial de proporcionar apoyo personalizado a los estudiantes, automatizar 
        tareas administrativas y ofrecer análisis de aprendizaje detallados" (p. 3).
        """, icon=":material/developer_board:")

    st.write("""
    La tendencia del aprendizaje móvil es particularmente relevante en América Latina, donde los 
    teléfonos móviles están ampliamente disponibles incluso en áreas con recursos limitados.

    En cuanto a la IA, los sistemas de tutoría inteligente, por ejemplo, pueden adaptar el ritmo y el 
    contenido de la instrucción a las necesidades individuales de cada estudiante, mejorando 
    significativamente la eficiencia y la eficacia del aprendizaje, especialmente en contextos donde 
    los recursos docentes son limitados.

    Sin embargo, la implementación efectiva de la IA en la educación requiere una cuidadosa adaptación 
    a los contextos educativos locales. *Zawacki-Richter et al.* (2019) enfatizan la importancia de 
    considerar aspectos éticos, como el uso responsable y transparente de los datos de los estudiantes, 
    la protección de su privacidad y la prevención de cualquier tipo de discriminación (p. 21).
    """)

    st.success("""
    :green[**Perspectiva crítica**]: *Lugo y Ithurburu* (2019) advierten que "la implementación de 
    tecnología educativa debe ir más allá de la mera provisión de dispositivos, para enfocarse en el 
    desarrollo de competencias digitales tanto en estudiantes como en docentes" (p. 12).
    """, icon=":material/travel_explore:")

    st.write("""
    Esta visión subraya la importancia de un enfoque holístico que no solo se centre en el acceso a 
    dispositivos y conectividad, sino también en el desarrollo de habilidades para utilizar estas 
    herramientas de manera crítica y creativa.

    En el contexto de Circle Up Community en Tocancipá, Colombia, la integración de tecnologías emergentes ofrece 
    oportunidades para enriquecer el aprendizaje comunitario y ampliar su alcance. Sin embargo, será 
    crucial evaluar críticamente su implementación y su impacto en los resultados de aprendizaje y la 
    equidad educativa, considerando las particularidades del contexto latinoamericano y colombiano.
    """)


    st.title("Aprendizaje Intergeneracional")

    st.write("""
    El aprendizaje intergeneracional, un proceso que fomenta el intercambio de conocimientos y experiencias 
    entre distintas generaciones, se está convirtiendo en un componente cada vez más crucial en las 
    organizaciones modernas. Este enfoque reconoce que tanto los empleados jóvenes como los mayores 
    poseen valiosos conocimientos y experiencias que pueden compartir entre sí, desafiando la visión 
    tradicional de la transferencia de conocimientos unidireccional de los mayores a los jóvenes.
    """)

    st.success("""
    :green[**Estudio de Caso: Aprendizaje Intergeneracional**]

    *Gerpott et al.* (2017) exploraron la dinámica del aprendizaje intergeneracional en un programa de 
    aprendizaje de 18 meses en una empresa automovilística alemana, donde aprendices jóvenes (16-19 años) 
    y experimentados (41-47 años) colaboraron para formarse como fabricantes de herramientas.
    """, icon=":material/experiment:")

    st.write("""
    Este entorno de aprendizaje único permitió a los investigadores observar cómo el conocimiento fluía 
    en ambas direcciones, con aprendices jóvenes y mayores compartiendo sus conocimientos y habilidades 
    únicas. Por ejemplo, los aprendices más jóvenes aportaron sus conocimientos sobre tecnología y 
    métodos de aprendizaje actuales, mientras que los aprendices mayores compartieron su amplia 
    experiencia práctica y conocimientos específicos de la empresa. Este intercambio bidireccional de 
    conocimientos pone de relieve el concepto de "mentoría inversa", en el que los empleados más jóvenes 
    enseñan a los mayores, un fenómeno cada vez más reconocido en el panorama empresarial actual.

    Los hallazgos de *Gerpott et al.* (2017) revelaron que "ambas generaciones poseen distintos 
    conocimientos expertos, prácticos, sociales y metacognitivos, e intercambian diferentes tipos de 
    conocimiento en distintos momentos" (p. 4). El estudio identificó cuatro tipos de conocimiento 
    intercambiados durante el programa.
    """)

    with st.expander("Tipos de Conocimiento en el Aprendizaje Intergeneracional"):
        st.markdown("""
        - **Conocimiento experto:** Información que se puede articular y transmitir fácilmente, como el conocimiento escolar de los aprendices más jóvenes sobre matemáticas o mecánica (p. 20).

        - **Conocimiento práctico:** Conocimiento tácito adquirido a través de la experiencia, relacionado con saber cómo realizar tareas específicas. Los aprendices mayores poseían un amplio conocimiento práctico sobre los procedimientos y movimientos manuales necesarios para crear herramientas (p. 22).

        - **Conocimiento social:** Abarca habilidades como la gestión de relaciones y la interacción eficaz con los demás. Los aprendices mayores a menudo actuaban como modelos a seguir, enseñando a gestionar conflictos y la importancia de la amistad y la integridad en el trabajo (p. 23).

        - **Conocimiento metacognitivo:** Se refiere a la supervisión de los procesos de pensamiento propios. Los aprendices jóvenes enseñaron nuevas estrategias para memorizar información, mientras que los mayores demostraron cómo mantener la concentración y afrontar situaciones estresantes (p. 24).
        """)

    st.write("""
    Si bien el aprendizaje intergeneracional ofrece numerosos beneficios, su implementación exitosa 
    requiere una planificación y consideración cuidadosas. *Findsen y Formosa* (2011) destacan la 
    importancia de abordar los desafíos potenciales que pueden surgir debido a las diferencias 
    generacionales. Los autores señalan que "las diferencias en estilos de aprendizaje, expectativas 
    y experiencias de vida pueden crear barreras para la comunicación efectiva entre generaciones" 
    (p. 168). Por ejemplo, los aprendices mayores pueden preferir métodos de enseñanza tradicionales, 
    mientras que los más jóvenes pueden sentirse más cómodos con enfoques basados en la tecnología. 
    Además, las expectativas sobre los roles y responsabilidades en el aprendizaje pueden variar entre 
    generaciones, lo que puede llevar a malentendidos y conflictos.

    Además de las diferencias en los estilos de aprendizaje y las expectativas, *Findsen y Formosa* (2011) 
    también señalan que los estereotipos negativos sobre el envejecimiento y las capacidades de los 
    adultos mayores pueden ser un obstáculo importante para el aprendizaje intergeneracional. Estos 
    estereotipos pueden llevar a una falta de respeto y comprensión mutua, lo que dificulta la creación 
    de un entorno de aprendizaje positivo e inclusivo.
    """)

    st.info("""
    :blue[**Recomendación clave**]: Para superar estos desafíos, los autores sugieren que el diseño de 
    programas intergeneracionales debe ser intencional y reflexivo. Esto implica reconocer y valorar 
    las diversas perspectivas y experiencias que cada generación aporta al entorno de aprendizaje.
    """, icon=":material/lightbulb:")

    st.write("""
    Los programas deben diseñarse para fomentar el respeto mutuo, la comprensión y la colaboración 
    entre generaciones. La capacitación en comunicación intercultural, la facilitación de grupos y 
    las actividades que promueven la interacción y el intercambio de conocimientos pueden ser 
    herramientas valiosas para lograr estos objetivos. Además, es fundamental abordar los estereotipos 
    negativos a través de la educación y la promoción de interacciones positivas entre generaciones. 
    Al hacerlo, podemos crear programas de aprendizaje intergeneracional más efectivos que aprovechen 
    el poder de la diversidad generacional para beneficio de todos los involucrados.
    """)


    st.title("Conclusión Marco Conceptual")

    st.info("""
    :blue[**Marco Teórico de Circle Up Community**]: Este marco teórico proporciona la base conceptual para Circle Up Community, 
    situando la iniciativa en el contexto de las teorías y prácticas educativas contemporáneas.
    """, icon=":material/hiking:")

    st.write("""
    Al combinar elementos del CBL, el aprendizaje a lo largo de la vida, la innovación social y el uso 
    de tecnologías emergentes, Circle Up Community busca crear un modelo de aprendizaje comunitario que sea relevante 
    y adaptable a las necesidades cambiantes de la sociedad. Solo a través de una consideración cuidadosa 
    de estos factores podremos evaluar verdaderamente el potencial de Circle Up Community para contribuir al 
    aprendizaje y desarrollo comunitario.
    """)

    st.warning("""
    :orange[**Consideración importante**]: Sin embargo, es crucial reconocer que cada uno de estos 
    conceptos presenta sus propios desafíos y limitaciones. La implementación y evaluación de Circle Up Community 
    deberá abordar cuidadosamente estas complejidades, manteniendo un enfoque crítico y reflexivo en 
    todo momento.
    """, icon=":material/hiking:")

    st.title("Conceptos clave del Marco Conceptual")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("Community-Based Learning (CBL)", icon=":material/handshake:")

    with col2:
        st.success("Aprendizaje a lo largo de la vida", icon=":material/self_improvement:")

    with col3:
        st.success("Innovación social", icon=":material/lightbulb:")

    with col4:
        st.success("Tecnologías emergentes en educación", icon=":material/developer_board:")

    st.write("""
    Estos conceptos forman los pilares fundamentales del marco teórico de Circle Up Community. La integración 
    efectiva de estos elementos será crucial para el éxito y la sostenibilidad de la iniciativa en 
    el contexto de Tocancipá, Colombia.
    """)

    st.info("""
    :blue[**Próximos pasos**]: La implementación de Circle Up Community requerirá una cuidadosa consideración de 
    cómo estos conceptos teóricos se traducen en prácticas concretas y medibles. Será esencial desarrollar 
    métricas e indicadores que permitan evaluar el impacto de la iniciativa en términos de aprendizaje 
    comunitario, innovación social y desarrollo sostenible.
    """, icon=":material/rocket:")


    st.title("Marco Metodológico")

    st.write("""
    Este estudio propone un enfoque de investigación cualitativa con un diseño de estudio de caso, 
    centrado en la planificación y el diseño de Circle Up Community en Tocancipá, Colombia. El estudio de caso, 
    como lo define *Yin* (2018), es "una investigación empírica que investiga un fenómeno contemporáneo 
    en profundidad y dentro de su contexto real" (p. 15). Este enfoque permitirá una comprensión profunda 
    de los factores contextuales que influyen en el diseño de Circle Up Community.
    """)

    st.title("Diseño de la investigación")

    st.write("""
    El estudio se estructurará en tres fases principales, adaptadas para maximizar el uso de datos 
    secundarios y análisis cuantitativos, mientras se mantiene la flexibilidad para incorporar elementos 
    cualitativos cuando sea necesario:
    """)

    st.success("""
    :green[**Fases del Diseño de Investigación**]

    1. **Fase de análisis de datos secundarios:**
      - Recopilación y organización de las bases de datos de la Encuesta Multipropósito Bogotá-Cundinamarca y del censo 2018.
      - Análisis exhaustivo de la literatura sobre Community-Based Learning y tecnologías emergentes en educación, con énfasis en estudios basados en datos secundarios.
      - Revisión de políticas educativas locales y regionales relevantes para Circle Up Community, utilizando documentos oficiales y datos públicos.

    2. **Fase de modelado y proyección:**
      - Desarrollo de un marco analítico para Circle Up Community, integrando los hallazgos del análisis de datos secundarios y la revisión de literatura.
      - Elaboración de modelos estadísticos y de proyección para estimar las condiciones actuales en Tocancipá, basados en los datos históricos disponibles.
      - Diseño de escenarios potenciales para la implementación de Circle Up Community, utilizando técnicas de modelado predictivo.

    3. **Fase de validación y refinamiento:**
      - Consulta con expertos en análisis de datos, educación, tecnología educativa y desarrollo comunitario para validar los modelos y proyecciones propuestos.
      - Realización de un análisis de sensibilidad para evaluar la robustez de nuestras estimaciones y proyecciones.
      - Refinamiento de los modelos basado en el feedback de expertos y los resultados del análisis de sensibilidad.
    """, icon=":material/travel_explore:")

    st.info("""
    :blue[**Nota**]: Este diseño de investigación se centra en el análisis riguroso de datos secundarios 
    y la creación de modelos predictivos. Reconocemos las limitaciones inherentes a este enfoque y nos 
    comprometemos a ser transparentes sobre estas limitaciones en todas las fases del estudio.
    """, icon=":material/bubble_chart:")

    st.title("Aspectos clave del diseño")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        1. **Integración de múltiples fuentes de datos:** Combinaremos datos de la Encuesta Multipropósito, 
        el censo 2018 y otras fuentes relevantes para crear una imagen comprehensiva de la situación en Tocancipá.

        2. **Enfoque en la extrapolación y proyección:** Dada la naturaleza dinámica de Tocancipá, 
        desarrollaremos modelos sofisticados para proyectar las tendencias actuales basándonos en los 
        datos históricos disponibles.

        3. **Validación multidisciplinaria:** Buscaremos la validación de expertos en diversos campos 
        para asegurar que nuestras interpretaciones y proyecciones sean robustas y relevantes.
        """)

    with col2:
        st.markdown("""
        4. **Flexibilidad metodológica:** Aunque nos centramos en el análisis cuantitativo, mantendremos 
        la apertura para incorporar insights cualitativos cuando sea necesario para contextualizar 
        nuestros hallazgos.

        5. **Consideración de escenarios:** Desarrollaremos múltiples escenarios para la implementación 
        de Circle Up Community, reconociendo la incertidumbre inherente en las proyecciones a futuro.
        """)

    st.write("""
    Este diseño nos permitirá aprovechar al máximo los datos disponibles, mientras mantenemos un enfoque 
    crítico y reflexivo sobre las limitaciones de nuestro método. El objetivo es proporcionar una base 
    sólida para la toma de decisiones informadas sobre la implementación de Circle Up Community en Tocancipá.
    """)


    st.title("Métodos de recolección de datos propuestos")

    st.write("""
    Para este estudio, hemos optado por un enfoque basado en el análisis de datos secundarios, 
    aprovechando la rica información disponible a través de fuentes oficiales. Nuestra principal 
    fuente de datos será el Departamento Administrativo Nacional de Estadística (DANE) de Colombia, 
    específicamente:
    """)

    st.markdown("""
    1. Utilizaremos más de 5 bases de datos provenientes de la Encuesta Multipropósito Bogotá-Cundinamarca. 
      Esta encuesta ofrece una visión detallada de las condiciones de vida en la región, abarcando temas 
      como vivienda, educación, salud, y empleo.

    2. Realizaremos una extrapolación cuidadosa de los datos presentados en el censo nacional de 2018 
      para obtener estimaciones actualizadas para Tocancipá y la región circundante.
    """)

    st.warning("""
    :orange[**Limitaciones y consideraciones**]
               
    - Las estimaciones basadas en el censo de 2018 y la muestra de 2021 pueden no reflejar con precisión 
      la situación actual, especialmente en áreas de rápido crecimiento como Tocancipá.
    - Es probable que nuestras estimaciones subestimen los valores actuales debido al dinamismo demográfico 
      de la región.
    - Los usuarios de esta información deben considerar un margen de error adicional al interpretar estos 
      resultados.
    - Recomendamos utilizar estas estimaciones como una referencia general y no como valores precisos para 
      la población actual de Tocancipá.
    """, icon=":material/hiking:")

    st.title("Razones para elegir este método")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        1. **Eficiencia en recursos**: El uso de datos secundarios nos permite acceder a una gran cantidad 
          de información sin los costos y el tiempo asociados a la recolección de datos primarios.
        2. **Confiabilidad de la fuente**: El DANE es reconocido por su rigor metodológico y la calidad 
          de sus datos.
        """)

    with col2:
        st.markdown("""
        3. **Amplitud de la información**: Las bases de datos de la Encuesta Multipropósito ofrecen una 
          visión multidimensional que sería difícil de replicar con recursos limitados.
        4. **Continuidad temporal**: Al utilizar datos del censo 2018 y encuestas más recientes, podemos 
          observar tendencias y cambios a lo largo del tiempo.
        """)

    st.title("Mitigación de limitaciones")

    st.markdown("""
    Para mitigar las limitaciones de este enfoque, nos proponemos:

    1. Ser transparentes sobre la metodología y las fuentes de datos utilizadas.
    2. Proporcionar intervalos de confianza o rangos de estimación cuando sea posible.
    3. Complementar, cuando sea factible, con datos cualitativos o de fuentes locales para contextualizar 
      nuestros hallazgos.
    4. Mantener una actitud crítica hacia nuestros propios resultados, reconociendo abiertamente las 
      áreas de incertidumbre.
    """)

    st.title("Análisis de datos propuesto")

    st.write("""
    El análisis de datos para este estudio se basará en un enfoque sistemático y detallado de la 
    información proporcionada por la Encuesta Multipropósito Bogotá-Cundinamarca y los datos del censo 
    2018. Utilizaremos técnicas de análisis estadístico y visualización de datos para extraer insights 
    significativos.
    """)

    st.info("""
    :blue[**Metodología propuesta**]

    1. **Extracción y Preparación de Datos**
    2. **Limpieza y Transformación de Datos**
    3. **Análisis Exploratorio de Datos (EDA)**
    4. **Visualización de Datos**
    5. **Estimación e Inferencia Estadística**
    6. **Análisis Comparativo**
    7. **Manejo de Sesgos y Limitaciones**
    8. **Contextualización de Resultados**
    """, icon=":material/stacked_bar_chart:")


    st.write("""
    Este enfoque metodológico nos permitirá realizar un análisis robusto y detallado de los datos disponibles, siempre teniendo en cuenta las limitaciones inherentes al uso de datos secundarios y la naturaleza dinámica de la región estudiada. Nuestro objetivo es proporcionar insights valiosos mientras mantenemos un alto estándar de rigor metodológico y transparencia en nuestras conclusiones.
    """)

    st.title("Consideraciones Éticas")

    st.write("""
    El diseño de la investigación incluirá la elaboración de protocolos éticos rigurosos, siguiendo 
    las pautas éticas de la Asociación Americana de Investigación Educativa (*AERA*, 2011). Aunque 
    nuestro estudio se basa principalmente en datos secundarios, es fundamental mantener altos 
    estándares éticos en todas las fases de la investigación.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **1. Protección de la privacidad y confidencialidad**
        - Asegurar que ningún individuo pueda ser identificado
        - Implementar técnicas de anonimización adicionales si es necesario
        """, icon=":material/hiking:")

        st.info("""
        **2. Uso responsable de los datos**
        - Utilizar los datos solo para los fines especificados
        - Evitar análisis que puedan estigmatizar a comunidades
        """, icon=":material/hiking:")

        st.info("""
        **3. Transparencia y reproducibilidad**
        - Detallar meticulosamente los métodos y fuentes
        - Poner a disposición los scripts de análisis
        """, icon=":material/hiking:")

    with col2:
        st.info("""
        **4. Consideración de impactos potenciales**
        - Evaluar las consecuencias de los hallazgos
        - Presentar resultados de manera equilibrada
        """, icon=":material/hiking:")

        st.info("""
        **5. Consentimiento informado para datos adicionales**
        - Implementar formularios de consentimiento detallados si se requieren datos adicionales
        """, icon=":material/hiking:")

        st.info("""
        **6. Manejo ético de datos sensibles**
        - Prestar especial atención a datos sensibles
        - Manejar con máximo cuidado y confidencialidad
        """, icon=":material/hiking:")

    st.info("""
    :blue[**Importante**] Es fundamental garantizar la protección de los derechos y el bienestar de 
    todos los participantes indirectos en el estudio, manteniendo altos estándares éticos en todas las 
    fases de la investigación, desde el análisis de datos hasta la difusión de resultados.
    """, icon=":material/hiking:")

    st.title("Limitaciones Potenciales")

    st.warning("""
    :orange[**Advertencia**]: Se reconoce que este estudio estará limitado al contexto específico de 
    Tocancipá, y los resultados pueden no ser directamente generalizables a otros contextos. Además, 
    al ser un estudio basado en datos secundarios y extrapolaciones, las conclusiones sobre la situación 
    actual de Tocancipá y el potencial impacto de Circle Up Community serán tentativas.
    """, icon=":material/hiking:")


    st.title("Limitaciones del Estudio")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(":green[1. **Limitaciones de los datos secundarios:** Posible desactualización y sesgos inherentes.]", icon=":material/tactic:")
        
        st.success(":green[4. **Naturaleza tentativa de las conclusiones:** Especulación sobre el impacto potencial de Circle Up Community.]", icon=":material/tactic:")

        st.success(":green[7. **Desafíos en la integración de datos:** Posibles problemas de compatibilidad entre fuentes.]", icon=":material/tactic:")

    with col2:
        st.success(":green[2. **Desafíos en la extrapolación:** Incertidumbre en las estimaciones debido al rápido desarrollo.]", icon=":material/tactic:")
        
        st.success(":green[5. **Falta de datos primarios actuales:** Limitación en capturar dinámicas muy recientes.]", icon=":material/tactic:")

    with col3:
        st.success(":green[3. **Limitaciones en la generalización:** Hallazgos específicos pueden no ser aplicables a otras regiones.]", icon=":material/tactic:")
        
        st.success(":green[6. **Limitaciones en la captura de aspectos cualitativos:** Posible falta de representación de realidades vividas.]", icon=":material/tactic:")

        st.success("""
        :green[**Estrategias de mitigación**]:

        - Ser transparentes sobre todas las limitaciones en nuestros reportes y publicaciones.
        - Proporcionar rangos de estimación e intervalos de confianza siempre que sea posible.
        - Recomendar cautela en la interpretación y aplicación de nuestros hallazgos.
        """, icon=":material/tactic:")


    st.title("Población")

    st.title("Análisis Demográfico y Socioeconómico de Tocancipá")

    st.write("""
    La segmentación de la población es un pilar fundamental para Circle Up Community en Tocancipá. Para diseñar e 
    implementar programas efectivos, es esencial comprender en profundidad el contexto demográfico y 
    socioeconómico actual del municipio. En este análisis, nos basaremos principalmente en dos fuentes 
    de datos clave: el Censo Nacional de Población y Vivienda (CNPV) de 2018 y la Encuesta Multipropósito 
    de Bogotá-Cundinamarca (EM) de 2021.
    """)

    st.info("""
    :blue[**Nota Metodológica**]: Aunque estos conjuntos de datos tienen algunos años de antigüedad, 
    representan la información más completa y confiable recopilada por el DANE para Tocancipá. Nuestro 
    análisis buscará conciliar y contextualizar las diferencias entre estas fuentes para proporcionar 
    una visión lo más actualizada posible de la situación demográfica del municipio.
    """, icon=":material/bubble_chart:")

    st.title("Crecimiento Poblacional y Estructura Etaria")

    st.success("""
    :green[**Dato importante**]: El CNPV 2018 registró una población total de 39,416 habitantes en 
    Tocancipá, evidenciando un crecimiento poblacional significativo desde los 23,981 habitantes 
    contabilizados en 2005.
    """, icon=":material/stacked_bar_chart:")

    st.write("La estructura etaria de Tocancipá muestra variaciones notables entre el CNPV 2018 y la EM 2021:")

    df_comparacion = pd.DataFrame({
        'Grupo de edad': ['0-14 años', '15-59 años', '60 años o más'],
        'CNPV 2018': ['24.4%', '68.6%', '7.0%'],
        'EM 2021': ['7.5%', '80.5%', '12.0%']
    })

    st.dataframe(df_comparacion, hide_index=True, use_container_width=True)

    st.write("Esta discrepancia en los datos presenta tanto oportunidades como desafíos para Circle Up Community:")

    with st.expander("Implicaciones para Circle Up Community"):
        st.markdown("""
        - **Oportunidades**: La mayor proporción de población entre 15-59 años según la EM 2021 (80.5%) 
          sugiere un amplio pool de potenciales participantes para los programas de voluntariado y mentoría.
        - **Desafíos**: La marcada diferencia en la proporción de menores de 14 años entre ambas fuentes 
          indica la necesidad de un análisis más profundo para entender la verdadera composición demográfica 
          actual, aunque no será necesario dado que la población objetivo esta en mayores de 14 años.
        """)

    st.warning("""
    Las diferencias observadas entre el CNPV 2018 y la EM 2021 podrían indicar un sesgo en la muestra 
    de la EM o cambios demográficos. Es crucial considerar ambas fuentes al diseñar estrategias para 
    Circle Up Community y, posiblemente, realizar ajustes en las estimaciones.
    """, icon=":material/hiking:")

    st.write("""
    La (EM 2021) proporciona una visión detallada y multidimensional de Tocancipá, crucial para el 
    diseño e implementación de Circle Up Community. El enfoque será sobre los datos relevantes para la población 
    mayor de 14 años, que constituye el grupo objetivo de todas las líneas de trabajo de Circle Up Community.
    """)

    with st.expander("Capítulos Seleccionados | Encuesta Multipropósito"):
        st.markdown("""
        1. Identificación
        2. Datos de la vivienda y su entorno
        5. Composición del hogar y demografía
        6. Salud
        8. Educación
        9. Uso de tecnologías de la información (TIC)
        10. Participación en organizaciones y redes sociales
        11. Fuerza de trabajo
        """)

    st.write("""
    Esta estructura integral nos permite analizar diversos aspectos relevantes para Circle Up Community, desde 
    el nivel educativo y el uso de tecnologías hasta la participación comunitaria y las condiciones 
    laborales de la población adulta y joven de Tocancipá.
    """)

    st.success("""
    :green[**Importante para Circle Up Community**]: Esta información es crucial para adaptar cada una de sus 
    líneas de trabajo a las necesidades específicas de la población mayor de 14 años en Tocancipá:

    1. **El Programa de Voluntariado Académico** puede beneficiarse de los datos sobre nivel educativo 
      y fuerza de trabajo para identificar potenciales voluntarios y áreas de conocimiento necesarias.
    2. **El Programa de Mentoría Inversa** puede utilizar la información sobre uso de TIC y composición 
      del hogar para diseñar estrategias efectivas de intercambio intergeneracional.
    3. **El Laboratorio de Innovación Social** puede aprovechar los datos sobre participación en 
      organizaciones para identificar áreas prioritarias de intervención.
    """, icon=":material/pool:")

    st.title("Análisis de Segmentación | Tocancipá")

    st.write("""
    El análisis de segmentación de la población de Tocancipá se basa en dos fuentes principales de 
    información: el Censo Nacional de Población y Vivienda (CNPV) de 2018 y la Encuesta Multipropósito 
    (EM) de Bogotá-Cundinamarca de 2021. Estas fuentes presentan diferencias significativas en la 
    distribución etaria de la población, lo que requiere un análisis cuidadoso y una metodología de 
    extrapolación para obtener estimaciones actualizadas y coherentes.
    """)

    st.title("Comparación de Distribuciones Etarias")

    df_comparacion_revisada = pd.DataFrame({
        'Grupo de edad': ['0-14 años', '15-59 años', '60 años o más'],
        'CNPV 2018': ['24.4%', '68.6%', '7.0%'],
        'EM 2021': ['7.5%', '80.5%', '12.0%'],
        'Diferencia': ['-16.9%', '+11.9%', '+5.0%']
    })

    st.dataframe(df_comparacion_revisada, hide_index=True, use_container_width=True)

    st.write("""
    Las discrepancias observadas entre el CNPV 2018 y la EM 2021 no reflejan necesariamente cambios 
    reales en la población, sino que pueden ser atribuidas a diferencias en las metodologías de 
    recolección de datos y en los tamaños de muestra.
    """)

    st.title("Metodología de Extrapolación")

    st.write("""
    Para abordar estas diferencias y obtener estimaciones actualizadas, se emplea una metodología de 
    extrapolación estadística. Este enfoque se basa en el diseño muestral de la EM 2021, que según el 
    documento metodológico, es "una muestra probabilística, estratificada y de conglomerados" (DANE, 2021, p. 8).
    """)

    st.write("**Proceso de Estimación**")

    with st.expander("Ver detalles del proceso de estimación"):
        st.markdown("""
        1. **Cálculo de la Proporción Muestral**
          
          La proporción muestral se calcula como:
          
          $$p = \\frac{x}{n}$$
          
          Donde $x$ es el número de individuos con la característica de interés y $n$ es el tamaño total de la muestra.
        
        2. **Estimación del Error Estándar**
          
          El error estándar se calcula como:
          
          $$SE = \\sqrt{\\frac{p(1-p)}{n}}$$
          
          Esta fórmula considera el diseño muestral complejo de la EM 2021.
        
        3. **Cálculo del Intervalo de Confianza**
          
          Se utiliza un intervalo de confianza del 95%, calculado como:
          
          $$CI_{95\\%} = p \\pm z \\times SE$$
          
          Donde $z$ es el valor crítico de la distribución normal estándar para un nivel de confianza del 95%, que es aproximadamente 1.96.
        
        4. **Extrapolación a la Población Total**
          
          La estimación para la población total se calcula como:
          
          $$\\hat{N} = p \\times N$$
          
          Donde $N$ es la población total según el CNPV 2018 (39,416 para Tocancipá).
        
        5. **Cálculo del Error Estándar Relativo**
          
          El error estándar relativo se calcula como:
          
          $$RSE = \\frac{SE}{p} \\times 100\\%$$
        """)

    st.write("**Ajuste por Distribución Etaria**")

    st.write("""
    Es importante notar que la muestra de la EM 2021 para Tocancipá (n=2015) debe ser ajustada para 
    reflejar la distribución etaria del CNPV 2018. Este proceso de post-estratificación implica asignar 
    pesos a las observaciones de la EM 2021 para que coincidan con la distribución del censo. Este 
    ajuste es crucial para garantizar que las estimaciones finales sean representativas de la estructura 
    poblacional actual de Tocancipá.
    """)

    st.title("Limitaciones y Consideraciones")

    st.write("""
    1. **Desfase Temporal**: La extrapolación de datos de 2021 a una base poblacional de 2018 puede no 
      capturar completamente los cambios demográficos recientes.
    2. **Tamaño de Muestra**: La EM 2021 se basa en una muestra relativamente pequeña para Tocancipá, 
      lo que puede aumentar el margen de error en las estimaciones.
    3. **Homogeneidad Asumida**: El método asume una distribución similar de características poblacionales 
      entre 2018 y 2021, lo cual puede no ser completamente preciso.
    """)

    st.warning("""
    :orange[**Nota Importante**]: Las estimaciones resultantes deben interpretarse con cautela, 
    considerando estas limitaciones. Se recomienda complementar este análisis con datos locales 
    adicionales cuando sea posible.
    """, icon=":material/hiking:")


    with st.expander("Distribución de Datos Población (VA, 25-44 años)"):

        df_va_gender_age = pd.DataFrame({
            'Genero': ['Hombre', 'Hombre', 'Hombre', 'Hombre', 'Mujer', 'Mujer', 'Mujer', 'Mujer'],
            'Rango de edad': ['25-29', '30-34', '35-39', '40-44', '25-29', '30-34', '35-39', '40-44'],
            'Muestra': [105, 87, 70, 81, 108, 90, 81, 93],
            'Estimación poblacional': ['1,671-2,436', '1,352-2,052', '1,054-1,684', '1,246-1,923', 
                                    '1,725-2,500', '1,405-2,116', '1,246-1,923', '1,458-2,180']
        })

        st.dataframe(df_va_gender_age, hide_index=True, use_container_width=True)

    st.info("""
    :blue[**Nota metodológica**]: Las estimaciones poblacionales se basan en la extrapolación de la 
    muestra de 2,015 personas de la EM 2021 a la población total de 39,416 según el CNPV 2018. Es 
    importante considerar que esta extrapolación asume una distribución proporcional, lo cual puede 
    no reflejar cambios demográficos ocurridos entre 2018 y 2021.
    """, icon=":material/bubble_chart:")

    st.write("""
    El segmento de Voluntarios Académicos (VA), que abarca el rango de edad de 25 a 44 años, presenta 
    una composición demográfica significativa para el programa Circle Up Community. En la muestra, este grupo 
    está compuesto por 343 hombres y 372 mujeres, lo que se traduce en una estimación poblacional de 
    6,715 hombres y 7,284 mujeres en Tocancipá.
    """)

    st.success("""
    :green[**Insight Clave**]: La presencia de un 8.46% más de mujeres que hombres en el segmento VA 
    (372 vs 343 en la muestra) sugiere un potencial de liderazgo femenino en el programa de voluntariado 
    académico de Circle Up Community, reflejando una tendencia de mayor participación femenina en actividades de 
    desarrollo comunitario.
    """, icon=":material/lightbulb:")

    st.title("Distribución por Subgrupos de Edad")

    subgrupos = [
        ("25-29 años", """Este subgrupo muestra una ligera predominancia femenina, con 108 mujeres 
        (estimado 1,725-2,500) frente a 105 hombres (estimado 1,671-2,436). Esta paridad sugiere un 
        equilibrio generacional en los profesionales jóvenes que podrían aportar perspectivas frescas 
        al programa."""),
        ("30-34 años", """Se observa un pequeño desequilibrio a favor de las mujeres, con 90 mujeres 
        (estimado 1,405-2,116) contra 87 hombres (estimado 1,352-2,052). Este subgrupo podría representar 
        profesionales con experiencia emergente, valiosa para el programa."""),
        ("35-39 años", """Aquí se invierte la tendencia, con 81 mujeres (estimado 1,246-1,923) y 70 
        hombres (estimado 1,054-1,684). Este subgrupo podría aportar una experiencia profesional más 
        consolidada al programa."""),
        ("40-44 años", """El subgrupo de mayor edad muestra de nuevo una predominancia femenina, con 
        93 mujeres (estimado 1,458-2,180) frente a 81 hombres (estimado 1,246-1,923). Este segmento 
        podría ofrecer la experiencia más sólida y diversa al programa.""")
    ]

    for grupo, descripcion in subgrupos:
        with st.expander(grupo):
            st.write(descripcion)


    st.title("Implicaciones para Circle Up Community")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(":green[**1. Diversidad de Experiencias**\n\nLa distribución relativamente uniforme entre los subgrupos de edad sugiere que Circle Up Community puede beneficiarse de un amplio espectro de experiencias profesionales y vitales en su programa VA.]", icon=":material/tactic:")

        st.success(":green[**4. Adaptabilidad Generacional**\n\nLa diversidad de edades dentro del grupo VA requiere que Circle Up Community desarrolle estrategias de engagement y retención adaptadas a las diferentes generaciones representadas.]", icon=":material/tactic:")

    with col2:
        st.success(":green[**2. Potencial de Mentorías Internas**\n\nLa presencia de diferentes cohortes de edad dentro del grupo VA ofrece la posibilidad de establecer un sistema de mentorías internas, donde los voluntarios de mayor edad puedan guiar a los más jóvenes.]", icon=":material/tactic:")

        st.success(":green[**5. Potencial de Innovación Intergeneracional**\n\nLa mezcla de diferentes cohortes de edad dentro del grupo VA puede fomentar la innovación a través del intercambio de perspectivas entre generaciones.]", icon=":material/tactic:")

    with col3:
        st.success(":green[**3. Enfoque en Equidad de Género**\n\nAunque hay una ligera predominancia femenina, Circle Up Community debe mantener un enfoque en la equidad de género para asegurar una representación balanceada en todos los niveles del programa.]", icon=":material/tactic:")

    st.write("""
    Este análisis demográfico proporciona una base sólida para el diseño y adaptación del programa de 
    Voluntarios Académicos de Circle Up Community. La diversidad de edad y la ligera predominancia femenina ofrecen 
    oportunidades únicas para crear un programa de voluntariado rico en experiencias y perspectivas, 
    capaz de abordar de manera efectiva los desafíos educativos y sociales de Tocancipá.
    """)

    st.title("Voluntarios Académicos (VA) Panorama Laboral")

    with st.expander("Situación Laboral VA, 25-44 años"):
        df_va_labor = pd.DataFrame({'Genero': ['Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre',
                    'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer'],
            'Situación': ['Buscando trabajo', 'Estudiando', 'Incapacitado(a) permanente para trabajar',
                        'Oficios del hogar', 'Otra actividad', 'Trabajando',
                        'Buscando trabajo', 'Estudiando', 'Incapacitado(a) permanente para trabajar',
                        'Oficios del hogar', 'Otra actividad', 'Trabajando'],
            'Muestra': [49, 127, 2, 16, 5, 375, 43, 101, 7, 114, 6, 300],
            'Estimación poblacional': ['693-1,224', '2,066-2,903', '-15-93', '160-466', '12-183', '6,666-8,005',
                                    '592-1,090', '1,600-2,351', '36-238', '1,832-2,628', '24-211', '5,256-6,481']
        })

        st.dataframe(df_va_labor, hide_index=True, use_container_width=True)

    st.info("""
    :blue[**Nota metodológica**]: Las estimaciones poblacionales asumen una distribución proporcional 
    entre la muestra y la población total, lo cual puede no reflejar cambios recientes en la dinámica 
    laboral de Tocancipá.
    """, icon=":material/bubble_chart:")

    st.write("""
    El análisis de la situación laboral de los potenciales Voluntarios Académicos (VA) revela patrones 
    significativos que impactan directamente en la estrategia de reclutamiento y retención de Circle Up Community:
    """)

    patrones = [
        ("Población Activa", """La mayoría de los VA potenciales están trabajando, con 375 hombres 
        (estimado 6,666-8,005) y 300 mujeres (estimado 5,256-6,481) en esta categoría. Esta preponderancia 
        de individuos empleados sugiere un rico pool de experiencias profesionales, pero también implica 
        la necesidad de diseñar un programa de voluntariado flexible que se adapte a los horarios laborales."""),
        ("Buscadores de Empleo", """Un segmento significativo está buscando trabajo: 49 hombres 
        (estimado 693-1,224) y 43 mujeres (estimado 592-1,090). Este grupo representa una oportunidad 
        única para Circle Up Community, ya que el voluntariado podría servir como plataforma para el desarrollo 
        de habilidades y networking, mejorando sus perspectivas de empleo."""),
        ("Brecha de Género en Oficios del Hogar", """Se observa una marcada diferencia en la categoría 
        de oficios del hogar, con 114 mujeres (estimado 1,832-2,628) frente a solo 16 hombres 
        (estimado 160-466). Esta disparidad refleja patrones culturales que Circle Up Community debe considerar 
        al diseñar estrategias de inclusión y empoderamiento."""),
        ("Población Estudiantil", """Un número considerable de individuos en este grupo etario aún está 
        estudiando: 127 hombres (estimado 2,066-2,903) y 101 mujeres (estimado 1,600-2,351). Este 
        segmento ofrece la oportunidad de integrar el voluntariado con el desarrollo académico y 
        profesional temprano.""")
    ]

    for titulo, descripcion in patrones:
        with st.expander(titulo):
            st.write(descripcion)

    st.success("""
    :green[**Insight Clave**]: La diversidad de situaciones laborales en el grupo VA sugiere la necesidad 
    de un enfoque multifacético en el programa de voluntariado de Circle Up Community. La estrategia debe equilibrar 
    la experiencia de los profesionales activos con las aspiraciones de desarrollo de los buscadores de 
    empleo y estudiantes.
    """, icon=":material/lightbulb:")

    st.title("Implicaciones Laborales para Circle Up Community")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(":blue[**1. Flexibilidad Programática**]\n\nEs crucial desarrollar un programa que ofrezca opciones de voluntariado en diversos horarios para acomodar a los VA empleados.", icon=":material/tactic:")

        st.info(":blue[**4. Mentorías Cruzadas**]\n\nFacilitar interacciones entre VA empleados y aquellos buscando trabajo o estudiando podría enriquecer la experiencia de voluntariado y fortalecer el tejido social de Tocancipá.", icon=":material/tactic:")

    with col2:
        st.info(":blue[**2. Desarrollo de Habilidades**]\n\nIntegrar componentes de desarrollo profesional en el programa de voluntariado podría atraer a buscadores de empleo y estudiantes, creando un ciclo de beneficio mutuo.", icon=":material/tactic:")

        st.info(":blue[**5. Alianzas Estratégicas**]\n\nColaborar con empleadores locales para promover el voluntariado como parte del desarrollo profesional podría aumentar la participación de VA empleados.", icon=":material/tactic:")

    with col3:
        st.info(":blue[**3. Inclusión de Género**]\n\nImplementar estrategias específicas para involucrar a mujeres en oficios del hogar podría diversificar el pool de voluntarios y abordar desigualdades de género.", icon=":material/tactic:")

    st.write("""
    Este análisis revela que la diversidad laboral entre los potenciales Voluntarios Académicos (VA) 
    es tanto un desafío como una oportunidad para Circle Up Community. Al adaptar su programa para satisfacer las 
    necesidades y aprovechar las fortalezas de cada segmento laboral, Circle Up Community puede maximizar su 
    impacto en la comunidad de Tocancipá mientras ofrece experiencias de voluntariado enriquecedoras 
    y relevantes.
    """)

    st.title("Voluntarios Académicos (VA) Perfil Ocupacional")

    with st.expander("Distribución Ocupacional VA, 25-44 años Empleados"):

        df_va_employed = pd.DataFrame({'Genero': ['Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre', 'Hombre',
                    'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer', 'Mujer'],
            'Ocupación': ['Empleado doméstico', 'Jornalero o peón', 'Obrero o empleado de empresa particular',
                        'Obrero o empleado del gobierno', 'Patrón o empleador', 'Profesional independiente',
                        'Trabajador independiente o por cuenta propia',
                        'Empleado doméstico', 'Jornalero o peón', 'Obrero o empleado de empresa particular',
                        'Obrero o empleado del gobierno', 'Patrón o empleador', 'Profesional independiente',
                        'Trabajador independiente o por cuenta propia'],
            'Muestra': [0, 1, 236, 5, 1, 7, 70, 3, 0, 183, 11, 0, 9, 52],
            'Estimación poblacional': ['0-0', '-19-58', '4,063-5,170', '12-183', '-19-58', '36-238', '1,054-1,684',
                                    '-8-125', '0-0', '3,085-4,074', '88-342', '0-0', '61-291', '744-1,290']
        })

        st.dataframe(df_va_employed, hide_index=True, use_container_width=True)

    st.write("""
    El análisis de la distribución ocupacional de los Voluntarios Académicos (VA) empleados revela 
    patrones significativos que tienen implicaciones directas para el programa de Circle Up Community:
    """)

    patrones_ocupacionales = [
        ("Predominancia del Sector Privado", """La mayoría de los VA empleados, tanto hombres (236, 
        estimado 4,063-5,170) como mujeres (183, estimado 3,085-4,074), trabajan en empresas particulares. 
        Este dato sugiere un amplio pool de experiencias en el sector privado que Circle Up Community puede aprovechar 
        para su programa de voluntariado."""),
        ("Brecha de Género en Empleos Gubernamentales", """Aunque la participación en el sector público 
        es baja en general, se observa una mayor presencia femenina (11 mujeres, estimado 88-342) en 
        comparación con los hombres (5, estimado 12-183). Esta diferencia podría indicar un mayor 
        potencial entre las mujeres VA para proyectos relacionados con servicios públicos y administración."""),
        ("Emprendimiento y Trabajo Independiente", """Un número significativo de VA son trabajadores 
        independientes o por cuenta propia, con 70 hombres (estimado 1,054-1,684) y 52 mujeres 
        (estimado 744-1,290). Este grupo podría aportar valiosas habilidades de autogestión y creatividad 
        al programa de voluntariado."""),
        ("Profesionales Independientes", """Aunque en menor número, la presencia de profesionales 
        independientes (7 hombres, estimado 36-238; 9 mujeres, estimado 61-291) sugiere un nicho de 
        expertise especializada que Circle Up Community podría aprovechar para proyectos más técnicos o complejos.""")
    ]

    for titulo, descripcion in patrones_ocupacionales:
        with st.expander(titulo):
            st.write(descripcion)

    st.success("""
    :green[**Insight Clave**]: La diversidad ocupacional entre los VA empleados ofrece a Circle Up Community un 
    rico ecosistema de habilidades y experiencias. Sin embargo, la concentración en el sector privado 
    sugiere la necesidad de estrategias específicas para involucrar a estos profesionales en actividades 
    de voluntariado que complementen sus carreras corporativas.
    """, icon=":material/lightbulb:")


    st.title("Implicaciones Ocupacionales para Circle Up Community")

    st.write("Estas tendencias ocupacionales tienen implicaciones estratégicas para Circle Up Community:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.warning(":orange[**1. Alianzas Corporativas**]\n\nEstablecer alianzas con empresas locales para promover el voluntariado corporativo.", icon=":material/strategy:")

        st.warning(":orange[**4. Mentorías Cruzadas**]\n\nFomentar la colaboración entre VA de diferentes sectores para enriquecer el intercambio de conocimientos.", icon=":material/strategy:")

    with col2:
        st.warning(":orange[**2. Proyectos Especializados**]\n\nLos profesionales independientes podrían liderar proyectos específicos que requieran habilidades especializadas.", icon=":material/strategy:")

        st.warning(":orange[**5. Desarrollo de Habilidades Complementarias**]\n\nOfrecer oportunidades para que los VA desarrollen habilidades fuera de su ámbito profesional habitual.", icon=":material/strategy:")

    with col3:
        st.warning(":orange[**3. Diversificación de Proyectos**]\n\nOfrecer una variedad de proyectos que aprovechen distintas habilidades y experiencias profesionales.", icon=":material/strategy:")


    st.title("Voluntarios Académicos (VA) Perfil Educativo y Migratorio")

    st.info("""
    :blue[**Niveles de Educación**]:
    1. Técnico
    2. Universitaria completa (con título)
    3. Especialización completa (con título)
    4. Universitaria incompleta (sin título)
    5. Tecnológico
    6. Maestría completa (con título)
    """, icon=":material/hiking:")
    
    with st.expander("Distribución Nivel Educativo (VA, 25-44 años) Empleados & Educación"):

        df_va_education = pd.DataFrame({'Genero': ['Hombre', 'Hombre', 'Hombre', 'Mujer', 'Mujer', 'Mujer'] * 6,
            'Ubicacion (5 años)': ['Este municipio', 'Otro municipio', 'Otro país'] * 12,
            'Nivel Educativo': ['Especialización completa (con título)', 'Especialización completa (con título)', 'Especialización completa (con título)',
                                'Especialización completa (con título)', 'Especialización completa (con título)', 'Especialización completa (con título)',
                                'Maestría completa (con título)', 'Maestría completa (con título)', 'Maestría completa (con título)',
                                'Maestría completa (con título)', 'Maestría completa (con título)', 'Maestría completa (con título)',
                                'Tecnológico', 'Tecnológico', 'Tecnológico', 'Tecnológico', 'Tecnológico', 'Tecnológico',
                                'Técnico', 'Técnico', 'Técnico', 'Técnico', 'Técnico', 'Técnico',
                                'Universitaria incompleta (sin título)', 'Universitaria incompleta (sin título)', 'Universitaria incompleta (sin título)',
                                'Universitaria incompleta (sin título)', 'Universitaria incompleta (sin título)', 'Universitaria incompleta (sin título)',
                                'Universitaria completa (con título)', 'Universitaria completa (con título)', 'Universitaria completa (con título)',
                                'Universitaria completa (con título)', 'Universitaria completa (con título)', 'Universitaria completa (con título)'],
            'Muestra': [1, 7, 0, 9, 11, 0, 2, 1, 0, 2, 2, 0, 3, 3, 2, 3, 3, 0, 14, 7, 0, 17, 9, 1, 3, 2, 2, 3, 0, 3, 12, 7, 5, 14, 10, 2],
            'Estimación poblacional': ['-19-58', '36-238', '0-0', '61-291', '88-342', '0-0',
                                    '-15-93', '-19-58', '0-0', '-15-93', '-15-93', '0-0',
                                    '-8-125', '-8-125', '-15-93', '-8-125', '-8-125', '0-0',
                                    '131-417', '36-238', '0-0', '175-490', '61-291', '-19-58',
                                    '-8-125', '-15-93', '-15-93', '-8-125', '0-0', '-8-125',
                                    '102-367', '36-238', '12-183', '131-417', '75-317', '-15-93']
        })

        st.dataframe(df_va_education, hide_index=True, use_container_width=True)

    st.write("""
    El análisis de la distribución del nivel educativo de los Voluntarios Académicos (VA) empleados, 
    considerando su lugar de residencia hace 5 años, revela patrones significativos:
    """)

    patrones_educativos = [
        ("Atracción de Talento Calificado", """Tocancipá está atrayendo profesionales con formación 
        académica superior, especialmente en niveles de especialización y universitaria completa. Este 
        flujo de talento calificado enriquece el pool de potenciales VA para Circle Up Community, aportando 
        diversidad de experiencias y conocimientos."""),
        ("Movilidad Femenina Destacada", """Se observa una mayor presencia de mujeres con niveles 
        educativos superiores que se han trasladado a Tocancipá en los últimos 5 años. Por ejemplo, 
        11 mujeres con especialización completa (estimado 88-342) provienen de otros municipios, en 
        comparación con 7 hombres (estimado 36-238). Esta tendencia subraya el potencial de liderazgo 
        femenino identificado en análisis anteriores."""),
        ("Predominio de Formación Técnica Local", """Entre los residentes de larga data, se destaca una 
        mayor presencia de formación técnica, con 14 hombres (estimado 131-417) y 17 mujeres 
        (estimado 175-490) que residían en Tocancipá hace 5 años. Esto sugiere una base sólida de 
        habilidades prácticas entre los VA locales."""),
        ("Migración Internacional Selectiva", """Aunque en menor número, se observa una presencia de 
        profesionales con títulos universitarios provenientes de otros países, especialmente hombres 
        (5, estimado 12-183). Esto añade una capa adicional de diversidad cultural y experiencia 
        internacional al pool de VA.""")
    ]

    for titulo, descripcion in patrones_educativos:
        with st.expander(titulo):
            st.write(descripcion)

    st.success("""
    :green[**Insight Clave**]: La combinación de talento local con formación técnica y la afluencia de 
    profesionales con educación superior crea un ecosistema diverso de conocimientos y habilidades entre 
    los VA. Circle Up Community tiene la oportunidad de aprovechar esta diversidad para enriquecer sus programas 
    de voluntariado y fomentar la innovación social en Tocancipá.
    """, icon=":material/lightbulb:")

    st.write("Estas tendencias educativas y migratorias tienen implicaciones estratégicas para Circle Up Community:")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(":blue[**1. Programas de Integración**]\n\nDesarrollar iniciativas que faciliten la integración de los nuevos residentes profesionales, especialmente mujeres, en la comunidad de Tocancipá a través del voluntariado.", icon=":material/strategy:")

        st.info(":blue[**4. Desarrollo de Habilidades Complementarias**]\n\nOfrecer oportunidades para que los VA con formación técnica amplíen sus conocimientos teóricos, y para que aquellos con formación universitaria adquieran habilidades prácticas locales.", icon=":material/strategy:")

    with col2:
        st.info(":blue[**2. Mentorías Multidimensionales**]\n\nImplementar un sistema de mentorías que aproveche tanto la experiencia local (formación técnica) como la expertise de los profesionales recién llegados con formación superior.", icon=":material/strategy:")

        st.info(":blue[**5. Networking Profesional**]\n\nFacilitar espacios de networking que promuevan la colaboración entre VA de diferentes backgrounds educativos y orígenes geográficos, potenciando el intercambio de conocimientos y oportunidades.", icon=":material/strategy:")

    with col3:
        st.info(":blue[**3. Proyectos de Innovación Social**]\n\nDiseñar proyectos que combinen el conocimiento práctico local con las perspectivas innovadoras de los profesionales con formación avanzada, fomentando soluciones creativas a desafíos comunitarios.", icon=":material/strategy:")

    st.write("""
    Este análisis educativo y migratorio revela que Circle Up Community tiene acceso a un rico y diverso pool de 
    talentos entre los VA empleados. Al diseñar programas de voluntariado que aprovechen esta diversidad 
    educativa y la dinámica migratoria, Circle Up Community puede no solo maximizar el impacto de sus iniciativas 
    en la comunidad de Tocancipá, sino también contribuir a la integración y desarrollo profesional de 
    sus voluntarios, fortaleciendo así el tejido social y económico del municipio.
    """)


    st.title("Satisfacción Vital de Voluntarios Académicos (VA)")

    st.write("Satisfacción con la Vida (VA, 25-44 años) Empleados & Educación")

    st.write("""
    La distribución de la satisfacción vital entre los VA empleados y con formación académica revela 
    patrones significativos:
    """)

    fig1,fig2,fig3 = st.columns([1,2,1])

    fig2.image("./figures/vida.png", caption="Distribución de Satisfacción Vital en Potenciales Voluntarios Académicos (VA) de Circle Up Community: Empleados de 25-44 años con Formación Superior", use_column_width=True)

    patrones_satisfaccion = [
        ("Concentración en Niveles Altos", """Tanto hombres (34.3%) como mujeres (33.9%) presentan una 
        concentración modal en el nivel 9 de satisfacción, indicando un bienestar subjetivo elevado en 
        este segmento poblacional."""),
        ("Dispersión Asimétrica", """Se observa una asimetría negativa en ambos géneros, con una cola 
        más larga hacia los valores inferiores. Esta distribución sugiere la existencia de subgrupos 
        con niveles de satisfacción divergentes del patrón general."""),
        ("Diferencias de Género Sutiles", """
        - Hombres: Muestran una distribución más uniforme entre los niveles 8, 9 y 10 (24.8%, 34.3%, 25.7% respectivamente).
        - Mujeres: Presentan una concentración más pronunciada en los niveles 8 y 9 (32.2% y 33.9%), con menor representación en el nivel 10 (20.3%).
        """),
        ("Presencia de Casos Atípicos", """La existencia de respuestas en niveles bajos (4-6) en ambos 
        géneros, aunque minoritarias, señala la presencia de individuos con experiencias vitales 
        significativamente diferentes al grueso de la población.""")
    ]

    for titulo, descripcion in patrones_satisfaccion:
        with st.expander(titulo):
            st.write(descripcion)

    st.success("""
    :green[**Insight Clave**]: La alta satisfacción vital general, combinada con la presencia de casos 
    atípicos, sugiere un escenario complejo donde coexisten experiencias diversas. Este panorama ofrece 
    oportunidades para iniciativas de voluntariado que aborden tanto el mantenimiento del bienestar 
    general como la atención a grupos específicos con necesidades particulares.
    """, icon=":material/lightbulb:")

    st.write("Implicaciones para la investigación y el diseño de programas:")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(":blue[**1. Segmentación de Iniciativas**]\n\nDiseñar programas diferenciados que atiendan tanto a la mayoría satisfecha como a los subgrupos con menor bienestar subjetivo.", icon=":material/account_tree:")

        st.info(":blue[**4. Monitoreo Longitudinal**]\n\nEstablecer un sistema de seguimiento temporal de la satisfacción vital.", icon=":material/account_tree:")

    with col2:
        st.info(":blue[**2. Análisis de Factores Contextuales**]\n\nExplorar las variables socioeconómicas, laborales y comunitarias que podrían explicar la distribución observada.", icon=":material/account_tree:")

        st.info(":blue[**5. Exploración de Motivaciones**]\n\nInvestigar la relación entre los niveles de satisfacción y las motivaciones para el voluntariado.", icon=":material/account_tree:")

    with col3:
        st.info(":blue[**3. Enfoque en Equidad de Género**]\n\nInvestigar más profundamente las sutiles diferencias entre géneros y sus implicaciones para la participación en actividades de voluntariado.", icon=":material/account_tree:")

        st.info(":blue[**6. Diseño de Intervenciones Focalizadas**]\n\nDesarrollar programas específicos para abordar las necesidades de los individuos en los extremos inferiores de la escala de satisfacción.", icon=":material/account_tree:")




    st.write("""
    La complejidad de la distribución de satisfacción vital entre los VA subraya la necesidad de un 
    enfoque matizado en el diseño de programas de voluntariado. Si bien la tendencia general hacia altos 
    niveles de satisfacción sugiere un terreno fértil para iniciativas comunitarias, la presencia de 
    variabilidad y casos atípicos demanda una aproximación flexible y adaptativa que reconozca la 
    diversidad de experiencias y necesidades dentro de la población objetivo.
    """)

    st.title("Satisfacción Laboral de Voluntarios Académicos (VA)")

    st.write("""
    La satisfacción laboral de los potenciales VA revela patrones significativos con implicaciones 
    directas para Circle Up Community:
    """)

    fig1,fig2,fig3 = st.columns([1,2,1])

    fig2.image("./figures/trabajo.png", caption="Satisfacción Laboral en la Población (VA)", use_column_width=True)

    patrones_laborales = [
        ("Alta Satisfacción General", """Tanto hombres como mujeres muestran niveles elevados de 
        satisfacción laboral, con una concentración en los niveles 7-9. Esta tendencia sugiere un 
        ambiente laboral propicio en Tocancipá, que podría traducirse en una mayor disposición para 
        el voluntariado."""),
        ("Diferencias de Género Sutiles", """
        - Hombres: Pico en nivel 8 (36.2%), seguido por 9 (17.1%) y 7 (15.2%).
        - Mujeres: Distribución más uniforme entre 9 (22.9%), 8 (21.2%) y 7 (16.1%).
        Esta variación indica posibles diferencias en las expectativas o experiencias laborales entre 
        géneros, requiriendo un enfoque matizado en el reclutamiento de voluntarios."""),
        ("Casos de Baja Satisfacción", """La presencia de un pequeño porcentaje con baja satisfacción 
        (niveles 1-5) en ambos géneros señala la existencia de subgrupos que podrían beneficiarse de 
        iniciativas de desarrollo profesional o apoyo laboral.""")
    ]

    for titulo, descripcion in patrones_laborales:
        with st.expander(titulo):
            st.write(descripcion)



    st.write("Implicaciones para Circle Up Community")

    col1, col2 = st.columns(2)

    with col1:
        st.success(":green[**Implicación 1**]\n\nLa alta satisfacción laboral general sugiere un pool de potenciales voluntarios motivados y con experiencias positivas que pueden transferir al ámbito comunitario.", icon=":material/target:")

        st.success(":green[**Implicación 2**]\n\nLa variabilidad en los niveles de satisfacción ofrece la oportunidad de diseñar programas de voluntariado que aborden diversas necesidades y motivaciones.", icon=":material/target:")

        st.success(":green[**Implicación 3**]\n\nLa correlación entre satisfacción laboral y compromiso comunitario merece una investigación más profunda para optimizar las estrategias de reclutamiento y retención de voluntarios.", icon=":material/target:")

    with col2:
        st.success(":green[**Estrategia 1**]\n\nDesarrollar programas de voluntariado que complementen las experiencias laborales positivas, aprovechando las habilidades y la motivación de los VA altamente satisfechos.", icon=":material/target:")

        st.success(":green[**Estrategia 2**]\n\nImplementar iniciativas específicas para involucrar a aquellos con menor satisfacción laboral, ofreciendo oportunidades de desarrollo personal y profesional a través del voluntariado.", icon=":material/target:")

        st.success(":green[**Estrategia 3**]\n\nEstablecer alianzas con empleadores locales para promover el voluntariado como una extensión del desarrollo profesional, potenciando la satisfacción tanto laboral como personal.", icon=":material/target:")


    st.write("""
    La distribución de satisfacción laboral entre los potenciales VA presenta un panorama favorable 
    para Circle Up Community, con un amplio segmento de profesionales satisfechos y motivados. Sin embargo, la 
    presencia de variabilidad y casos de baja satisfacción subraya la necesidad de un enfoque 
    diversificado en el diseño de programas de voluntariado, que considere tanto el aprovechamiento 
    de las experiencias positivas como la atención a las necesidades de desarrollo y realización 
    personal de todos los segmentos de la población objetivo.
    """)


    st.title("Satisfacción Comunitaria de Voluntarios Académicos (VA)")

    fig1,fig2,fig3 = st.columns([1,2,1])
    fig2.image("./figures/comunidad.png", caption="Satisfacción con la Comunidad en la Población Empleada de 25 a 44 Años con Formación Académica en Tocancipá", use_column_width=True)

    st.write("""
    La figura revela patrones críticos en la satisfacción comunitaria de los potenciales VA, con 
    implicaciones sustanciales para Circle Up Community:
    """)

    patrones_comunitarios = [
        ("Predominio de Alta Satisfacción", """El nivel 8 de satisfacción domina en ambos géneros 
        (42 hombres, est. 719-1,247; 36 mujeres, est. 616-1,067), indicando una base sólida de aprecio 
        comunitario. Esta tendencia sugiere un terreno fértil para iniciativas de voluntariado arraigadas 
        en el orgullo local."""),
        ("Segmento de Excelencia", """Un grupo significativo reporta nivel 9 de satisfacción (22 hombres, 
        26 mujeres), representando potenciales líderes comunitarios y embajadores entusiastas para los 
        programas de Circle Up Community."""),
        ("Diversidad de Experiencias", """Aproximadamente un tercio de los encuestados (36.2% hombres, 
        37.3% mujeres) reporta niveles de satisfacción de 7 o menos, señalando un segmento crítico que 
        percibe oportunidades de mejora comunitaria.""")
    ]

    for titulo, descripcion in patrones_comunitarios:
        with st.expander(titulo):
            st.write(descripcion)

    st.title("Implicaciones Estratégicas para Circle Up Community")

    implicaciones_comunitarias = [
        "La alta satisfacción general proporciona una base de voluntarios potencialmente comprometidos y motivados por el bienestar comunitario.",
        "La presencia de un segmento menos satisfecho ofrece oportunidades para programas de voluntariado enfocados en abordar preocupaciones específicas y mejorar la calidad de vida comunitaria.",
        "La distribución variada de satisfacción sugiere la necesidad de un enfoque diversificado en el reclutamiento y diseño de programas de voluntariado."
    ]

    for implicacion in implicaciones_comunitarias:
        st.markdown(f"- {implicacion}")

    st.title("Recomendaciones Operativas")

    recomendaciones_comunitarias = [
        "Desarrollar programas que capitalicen el orgullo comunitario de los altamente satisfechos, involucrándolos en iniciativas de mejora y preservación.",
        "Implementar proyectos específicos que aborden las preocupaciones del segmento menos satisfecho, utilizando el voluntariado como herramienta de empoderamiento y cambio comunitario.",
        "Establecer un sistema de retroalimentación continua para monitorear cómo las iniciativas de voluntariado impactan la satisfacción comunitaria a lo largo del tiempo."
    ]

    for recomendacion in recomendaciones_comunitarias:
        st.markdown(f"- {recomendacion}")

    st.write("""
    La distribución de satisfacción comunitaria entre los potenciales VA presenta un escenario prometedor 
    para Circle Up Community, con una mayoría satisfecha que puede impulsar iniciativas positivas. Sin embargo, 
    la presencia de un segmento significativo con menor satisfacción subraya la importancia de un 
    enfoque inclusivo y orientado a la mejora continua en el diseño de programas de voluntariado. 
    Esta dualidad ofrece a Circle Up Community la oportunidad única de catalizar el compromiso cívico, aprovechando 
    tanto el entusiasmo de los más satisfechos como la motivación para el cambio de aquellos que 
    perciben áreas de mejora en su comunidad.
    """)

    st.title("Uso de Internet para Educación entre Voluntarios Académicos (VA)")

    df_internet_edu = pd.DataFrame({
        'Genero': ['Hombre', 'Hombre', 'Mujer', 'Mujer'],
        'Uso de Internet': ['No', 'Si', 'No', 'Si'],
        'Muestra': [68, 37, 64, 54],
        'Estimación poblacional': ['1,019-1,641', '493-955', '950-1,554', '778-1,334']
    })

    st.dataframe(df_internet_edu, hide_index=True, use_container_width=True)

    st.write("""
    La tabla revela patrones cruciales en el uso de Internet para educación entre los potenciales VA, 
    con implicaciones profundas para Circle Up Community y el panorama educativo en Tocancipá:
    """)

    patrones_internet = [
        ("Brecha Digital Educativa", """La mayoría de los VA no utiliza Internet para fines educativos 
        (64.8% de hombres y 54.2% de mujeres), evidenciando una subutilización crítica de recursos 
        digitales. Este fenómeno sugiere una desconexión entre la formación académica y la adopción de 
        tecnologías educativas modernas, potencialmente limitando el desarrollo continuo de habilidades 
        en la fuerza laboral local."""),
        ("Disparidad de Género en Adopción Digital", """Las mujeres muestran una mayor propensión al uso 
        educativo de Internet (45.8% vs 35.2% en hombres), indicando una brecha de género en la adaptabilidad 
        tecnológica. Esta tendencia podría reflejar diferencias en estrategias de desarrollo profesional 
        o en la percepción del valor del aprendizaje en línea entre géneros."""),
        ("Oportunidad de Innovación Educativa", """El segmento significativo que sí utiliza Internet para 
        educación (35.2% de hombres y 45.8% de mujeres) representa un núcleo de innovadores educativos 
        potenciales. Este grupo podría actuar como catalizador para la adopción más amplia de recursos 
        digitales de aprendizaje en la comunidad.""")
    ]

    for titulo, descripcion in patrones_internet:
        with st.expander(titulo):
            st.write(descripcion)

    st.title("Implicaciones Estratégicas para Circle Up Community")

    implicaciones_internet = [
        "La baja adopción general de aprendizaje en línea señala una necesidad crítica de programas de alfabetización digital y concientización sobre recursos educativos en línea.",
        "La disparidad de género ofrece la oportunidad de diseñar iniciativas de voluntariado que aprovechen y amplíen la mayor apertura de las mujeres hacia el aprendizaje digital.",
        "El segmento de usuarios activos de Internet para educación representa un recurso valioso para el diseño y liderazgo de programas de voluntariado basados en tecnología."
    ]

    for implicacion in implicaciones_internet:
        st.markdown(f"- {implicacion}")

    st.title("Recomendaciones Estratégicas")

    recomendaciones_internet = [
        "Implementar un programa de **Embajadores Digitales** utilizando el segmento de usuarios activos para promover y enseñar habilidades de aprendizaje en línea a sus pares.",
        "Desarrollar una plataforma de microaprendizaje específica para Circle Up Community, que introduzca gradualmente a los VA al aprendizaje en línea a través de contenido relevante y accesible.",
        "Establecer alianzas con empresas locales para promover y reconocer el desarrollo profesional a través del aprendizaje en línea, incentivando la adopción de estas herramientas.",
        "Crear un programa de mentorías cruzadas que aproveche la mayor adopción femenina del aprendizaje en línea para fomentar la equidad de género en habilidades digitales."
    ]

    for recomendacion in recomendaciones_internet:
        st.markdown(f"- {recomendacion}")

    st.title("Perspectivas de Investigación Futuras")

    perspectivas_futuras = [
        "Explorar las barreras específicas que impiden la adopción del aprendizaje en línea entre los VA, considerando factores como acceso a tecnología, percepciones de utilidad y preferencias de aprendizaje.",
        "Investigar la correlación entre el uso de Internet para educación y la participación en actividades de voluntariado, para informar estrategias de reclutamiento y retención más efectivas."
    ]

    for perspectiva in perspectivas_futuras:
        st.markdown(f"- {perspectiva}")

    st.write("""
    Este análisis revela que Circle Up Community se encuentra en una posición única para catalizar una transformación 
    digital educativa en Tocancipá. Al abordar la brecha en el uso de Internet para educación, Circle Up Community 
    no solo puede mejorar la eficacia de sus programas de voluntariado, sino también contribuir 
    significativamente al desarrollo del capital humano local, preparando a la comunidad para los 
    desafíos de la economía del conocimiento del siglo XXI.
    """)

    with st.expander("Redes Sociales Puente Digital para VA"):

        df_redes_sociales = pd.DataFrame({'Genero': ['Hombre', 'Hombre', 'Mujer', 'Mujer'],
            'Uso de Redes Sociales': ['No', 'Si', 'No', 'Si'],
            'Muestra': [1, 104, 0, 118],
            'Estimación poblacional': ['-19-58', '1,654-2,415', '0-0', '1,904-2,712']
        })

        st.dataframe(df_redes_sociales, hide_index=True, use_container_width=True)

    st.write("""
    La tabla revela una adopción casi universal de redes sociales entre los potenciales VA, con 
    implicaciones cruciales para Circle Up Community:
    """)

    hallazgos_redes = [
        ("Saturación Digital", """La adopción del 100% entre mujeres y 99% entre hombres indica una 
        saturación del espacio social digital, creando un ecosistema virtual omnipresente en la vida 
        de los VA."""),
        ("Brecha de Género Mínima", """La diferencia marginal en adopción (1 hombre no usuario) sugiere 
        una equidad digital de género en el ámbito social, contrastando con la brecha observada en el 
        uso educativo de Internet.""")
    ]

    for titulo, descripcion in hallazgos_redes:
        with st.expander(titulo):
            st.write(descripcion)

    st.title("Estrategia de Redes Sociales para Circle Up Community")

    col1, col2 = st.columns(2)

    with col1:
        st.success(":green[**Implicaciones Estratégicas**]", icon=":material/network_node:")
        st.success(":green[1. Canal de Comunicación Primario: Las redes sociales emergen como el medio más eficaz para la difusión de información y reclutamiento de VA.]", icon=":material/network_node:")
        st.success(":green[2. Plataforma de Engagement: Ofrece un espacio ideal para cultivar comunidades virtuales de voluntarios, facilitando la coordinación y el intercambio de experiencias.]", icon=":material/network_node:")
        st.success(":green[3. Herramienta de Microvoluntariado: Posibilita la implementación de iniciativas de voluntariado digital de bajo compromiso pero alto impacto.]", icon=":material/network_node:")
        st.success(":green[4. Amplificador de Impacto: Proporciona un medio para que los VA compartan sus experiencias, potenciando el efecto multiplicador del voluntariado.]", icon=":material/network_node:")

        st.success(":green[**Recomendaciones Tácticas**]", icon=":material/network_node:")
        st.success(":green[1. Desarrollar una estrategia de contenido multiplataforma que aproveche las características únicas de cada red social.]", icon=":material/network_node:")
        st.success(":green[2. Implementar campañas de storytelling digital para destacar el impacto del voluntariado a través de narrativas personales de los VA.]", icon=":material/network_node:")
        st.success(":green[3. Crear un programa de embajadores digitales que aproveche la influencia social de los VA más activos en redes.]", icon=":material/network_node:")
        st.success(":green[4. Diseñar desafíos virales y campañas de hashtags que promuevan la visibilidad de Circle Up Community y sus iniciativas.]", icon=":material/network_node:")

    with col2:
        st.success(":green[**Consideraciones Críticas**]", icon=":material/network_node:")
        st.success(":green[1. La alta adopción no garantiza engagement activo; es crucial desarrollar contenido que resuene con los intereses y valores de los VA.]", icon=":material/network_node:")
        st.success(":green[2. El uso intensivo de redes sociales puede llevar a la fatiga digital; Circle Up Community debe equilibrar su presencia online con experiencias offline significativas.]", icon=":material/network_node:")
        st.success(":green[3. La privacidad y seguridad de datos deben ser prioritarias en todas las interacciones digitales para mantener la confianza de los VA.]", icon=":material/network_node:")

        st.success(":green[**Oportunidades de Investigación**]", icon=":material/network_node:")
        st.success(":green[1. Analizar los patrones de uso específicos de redes sociales entre los VA para optimizar la estrategia de comunicación.]", icon=":material/network_node:")
        st.success(":green[2. Explorar la correlación entre la actividad en redes sociales y la propensión al voluntariado para informar estrategias de reclutamiento más efectivas.]", icon=":material/network_node:")

    st.write("""
    La omnipresencia de las redes sociales entre los VA ofrece a Circle Up Community un canal poderoso para 
    catalizar el compromiso cívico digital. Al aprovechar estratégicamente este espacio virtual, 
    Circle Up Community puede no solo amplificar su alcance e impacto, sino también redefinir el voluntariado 
    para la era digital, creando un modelo de participación comunitaria que sea tan dinámico y 
    interconectado como la sociedad a la que sirve.
    """)

    st.title("Conclusiones del Análisis Demográfico")

    st.write("""
    El análisis demográfico de Tocancipá revela un ecosistema diverso y dinámico, ideal para la 
    implementación de los programas de Circle Up Community. La población muestra una combinación de residentes 
    de larga data y nuevos migrantes, creando un caldo de cultivo para la innovación y el desarrollo 
    comunitario. Los altos niveles de satisfacción vital y comunitaria, junto con una creciente adopción 
    de tecnologías digitales, proporcionan una base sólida para iniciativas de voluntariado e innovación social.

    La diversidad educativa y ocupacional observada ofrece un amplio espectro de habilidades y 
    perspectivas, crucial para abordar los desafíos multifacéticos de la comunidad. Sin embargo, 
    también se identificaron brechas significativas, particularmente en el uso de internet para 
    educación y en la participación femenina en ciertos sectores, que Circle Up Community puede abordar estratégicamente.
    """)


    st.title("Árboles de Problemas y Objetivos")

    st.write("""
    Este proyecto utiliza árboles de problemas y objetivos para analizar y abordar desafíos en Tocancipá. 
    Se enfoca en tres áreas: voluntariado académico, mentores inversos y un laboratorio de innovación 
    social. El estudio busca identificar problemas clave, proponer soluciones y desarrollar estrategias 
    para potenciar el capital humano local, fomentar la transferencia intergeneracional de conocimientos 
    y promover la innovación comunitaria.
    """)

    def mostrar_arbol(titulo, imagen_url, descripcion, tabla_data, implicaciones):
        st.title(titulo)

        fig1,fig2,fig3 = st.columns([1,2,1])
        fig2.image(imagen_url, use_column_width=True)
        st.write(descripcion)
        
        df = pd.DataFrame(tabla_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        with st.expander("Implicaciones para Circle Up Community"):
            st.write(implicaciones)

    mostrar_arbol("Árbol de Problemas - Voluntariado Académico",
        "https://yuml.me/gocircleup/ap-va.svg",
        """
        El siguiente árbol de problemas analiza la situación actual del voluntariado académico en Tocancipá. 
        Identifica como problema central la subutilización del capital humano local para el desarrollo de 
        habilidades comunitarias. Este análisis revela una serie de causas interconectadas que contribuyen 
        a esta situación, así como los efectos que tiene en la comunidad.
        """,
        {
            "Nivel": ["Efectos Indirectos", "Efectos Directos", "Problema Central", "Causas Directas", "Causas Indirectas"],
            "Descripción": [
                "1. Estancamiento en el desarrollo socioeconómico local.\n2. Disminución de la cohesión social y el sentido de comunidad.",
                "1. Limitado desarrollo de habilidades relevantes para el contexto local.\n2. Desaprovechamiento del potencial de liderazgo en la comunidad.",
                "Subutilización del capital humano local en Tocancipá para el desarrollo de habilidades comunitarias.",
                "1. Ausencia de un sistema estructurado para canalizar el conocimiento de profesionales locales.\n2. Desconexión entre las habilidades existentes en la comunidad y las necesidades locales.",
                "1.1. Falta de mecanismos para identificar y movilizar el talento local.\n1.2. Escasez de incentivos para la participación en actividades de voluntariado académico.\n2.1. Limitada identificación de las necesidades de aprendizaje de la comunidad.\n2.2. Ausencia de un currículo adaptado a las características demográficas locales."
            ]
        },
        """
        Este árbol de problemas sugiere que Circle Up Community debe enfocarse en:
        1. Crear sistemas estructurados para identificar y movilizar el talento local.
        2. Desarrollar incentivos efectivos para el voluntariado.
        3. Diseñar currículos adaptados a las necesidades específicas de Tocancipá.
        4. Implementar mecanismos para identificar las necesidades de aprendizaje de la comunidad.

        Abordar estos aspectos podría conducir a un mejor aprovechamiento del capital humano local y, 
        en consecuencia, a un mayor desarrollo de habilidades comunitarias.
        """
    )

    # Árbol de Objetivos - VA
    mostrar_arbol("Árbol de Objetivos - Voluntariado Académico",
        "https://yuml.me/gocircleup/ao-va.svg",
        """
        El siguiente árbol de objetivos presenta una visión estructurada para optimizar el aprovechamiento 
        del capital humano local en Tocancipá. Este enfoque busca transformar las problemáticas identificadas 
        en el árbol de problemas en objetivos alcanzables y medios concretos para lograrlos.
        """,
        {
            "Nivel": ["Fines Indirectos", "Fines Directos", "Objetivo General", "Objetivos Específicos", "Medios"],
            "Descripción": [
                "1. Mejora en el desarrollo socioeconómico local.\n2. Fortalecimiento de la cohesión social y el sentido de comunidad.",
                "1. Incremento en la adquisición de habilidades relevantes para el contexto local.\n2. Aumento en el número de líderes comunitarios capacitados.",
                "Optimizar el aprovechamiento del capital humano local para el desarrollo de habilidades comunitarias en Tocancipá.",
                "1. Implementar un sistema estructurado de voluntariado académico.\n2. Alinear las habilidades locales con las necesidades de la comunidad.",
                "1.1. Desarrollar una plataforma para la identificación y gestión de voluntarios.\n1.2. Establecer un sistema de reconocimiento para los voluntarios académicos.\n2.1. Realizar un análisis continuo de las necesidades de aprendizaje de la comunidad.\n2.2. Diseñar un currículo flexible basado en las características demográficas locales."
            ]
        },
        """
        Para lograr estos objetivos, Circle Up Community podría considerar las siguientes estrategias:
        1. Desarrollar una plataforma digital para conectar voluntarios con oportunidades de enseñanza.
        2. Implementar un sistema de badges o certificaciones para reconocer el trabajo de los voluntarios.
        3. Conducir encuestas y focus groups regulares para identificar las necesidades de aprendizaje.
        4. Colaborar con expertos locales para diseñar un currículo adaptativo y relevante.

        Estas estrategias buscan crear un ecosistema de voluntariado académico eficiente y alineado con 
        las necesidades de Tocancipá.
        """
    )

    st.title("Referencias")

    st.info("""
    Este capítulo presenta una lista exhaustiva de las referencias utilizadas en este proyecto de 
    investigación. Las fuentes están organizadas en una tabla que incluye la citación en formato APA 
    y un enlace directo al documento original cuando está disponible. Esta compilación refleja la 
    diversidad y profundidad de la literatura consultada, abarcando temas como tecnología educativa, 
    aprendizaje a lo largo de la vida, innovación social y metodologías de investigación.
    """, icon=":material/hiking:")


    referencias = pd.DataFrame([
        {"Referencia (APA)": "Álvarez, M., Gardyn, N., Iardelevsky, A., & Rebello, G. (2020). Segregación Educativa en Tiempos de Pandemia: Balance de las Acciones Iniciales durante el Aislamiento Social por el Covid-19 en Argentina. Revista Internacional de Educación para la Justicia Social, 9(3).", "Enlace": "https://drive.google.com/file/d/15MGMS96FzBvBJIxXRq4ua4VPpv8uJQ9H/view?usp=sharing"},
        {"Referencia (APA)": "American Educational Research Association. (2011). Code of Ethics. Educational Researcher, 40(3), 145-156.", "Enlace": "Sin Referencia"},
        {"Referencia (APA)": "Avello Martínez, R., Lavonen, J., & Zapata-Ros, M. (2022). Emerging Technologies in Education for Innovative Pedagogies and Competence Development. Sustainability, 37(5), 1723.", "Enlace": "https://drive.google.com/file/d/1HMZ_KbCVAg2HA48fPz9olCy6J4P4eMet/view?usp=sharing"},
        {"Referencia (APA)": "Bayne, S. (2015). What's the matter with 'technology-enhanced learning'? Learning, Media and Technology, 40(1), 5-20.", "Enlace": "https://drive.google.com/file/d/1iruNdNa_nDHPV2QDT7mQhPfkKI4C8gHf/view?usp=sharing"},
        {"Referencia (APA)": "Binkley, M., Erstad, O., Herman, J., Raizen, S., Ripley, M., Miller-Ricci, M., & Rumble, M. (2012). Defining twenty-first century skills. In P. Griffin, B. McGaw, & E. Care (Eds.), Assessment and teaching of 21st century skills (pp. 17-66).", "Enlace": "https://drive.google.com/file/d/1f2Di-Mx4HC9dchfucEY4oDdsl04Bzoke/view?usp=sharing"},
        {"Referencia (APA)": "Bond, M., Marín, V. I., Dolch, C., Bedenlier, S., & Zawacki-Richter, O. (2020). Digital transformation in German higher education: student and teacher perceptions and usage of digital media. International Journal of Educational Technology in Higher Education, 17(1), 1-21.", "Enlace": "https://drive.google.com/file/d/1Cw-CINpDMY_RfJjn3t5HEGyOIQDY8gV8/view?usp=sharing"},
        {"Referencia (APA)": "Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. Qualitative Research in Psychology, 3(2), 77-101.", "Enlace": "Sin Referencia"},
        {"Referencia (APA)": "Bringle, R. G., & Clayton, P. H. (2020). Integrating Service Learning and Digital Technologies: Examining the Challenge and the Promise. RIED. Revista Iberoamericana de Educación a Distancia, 23(1), 43-65.", "Enlace": "https://drive.google.com/file/d/1AtW5571ZP7oTF3Cg169BamBBw1T802D4/view?usp=sharing"},
        {"Referencia (APA)": "British Council. (n.d.). [Título del documento].", "Enlace": "https://drive.google.com/file/d/1iZluoOuZHqTov3FzIdtAHA2K7wbzhu4a/view?usp=sharing"},
        {"Referencia (APA)": "Brown, P., Lauder, H., & Cheung, S. Y. (2020). The Death of Human Capital?: Its Failed Promise and How to Renew It in an Age of Disruption. Oxford University Press.", "Enlace": "https://drive.google.com/file/d/15ZXERFpEw9UaAlLKdKw8hSo-gse0ZDUK/view?usp=sharing"},
        {"Referencia (APA)": "Crompton, H., & Burke, D. (2018). The use of mobile learning in higher education: A systematic review. Computers & Education, 123, 53-64.", "Enlace": "https://drive.google.com/file/d/1SAtVNFP28Q7C2q3fjuwaOgKjyTc-DG2D/view?usp=sharing"},
        {"Referencia (APA)": "DANE. (2021). Encuesta Multipropósito Bogotá - Cundinamarca - EM - 2021 Colombia.", "Enlace": "https://microdatos.dane.gov.co/index.php/catalog/743/get-microdata"},
        {"Referencia (APA)": "Desjardins, R. (2019). The political economy of adult learning systems - Some institutional features that promote adult learning participation.", "Enlace": "https://drive.google.com/file/d/1_EeboCgjQvPoJ4rCFST4zWrx_1UT4eVf/view?usp=sharing"},
        {"Referencia (APA)": "Findsen, B., & Formosa, M. (2011). Lifelong learning in later life: A handbook on older adult learning. Sense Publishers.", "Enlace": "https://drive.google.com/file/d/1aQDJGSZ8KcO_Pr3y2eAMTXq8iho-ddNd/view?usp=sharing"},
        {"Referencia (APA)": "Gerpott, F. H., Lehmann-Willenbrock, N., & Voelpel, S. C. (2017). A phase model of intergenerational learning in organizations. Academy of Management Learning & Education, 16(2), 193-216.", "Enlace": "https://drive.google.com/file/d/1QVtNCG5NiArgVDbs0UmjJ9PYJEN73Kmj/view?usp=sharing"},
        {"Referencia (APA)": "Giraudeau, C., & Bailly, N. (2019). Intergenerational programs: What can school-age children and older people expect from them? A systematic review. European Journal of Ageing, 16(3), 363-376.", "Enlace": "https://drive.google.com/file/d/1d2ne4AxNIk7s3sGx0W0KfUsRx1TS4TKy/view?usp=sharing"},
        {"Referencia (APA)": "Howaldt, J., Kaletka, C., Schröder, A., & Zirngiebl, M. (2018). Atlas of Social Innovation: New Practices for a Better Future. Sozialforschungsstelle, TU Dortmund University.", "Enlace": "https://drive.google.com/file/d/1hb1QJAdgbKuD0dBe8VLKwK204Exip1U7/view?usp=sharing"},
        {"Referencia (APA)": "Krlev, G., Anheier, H. K., & Mildenberger, G. (2021). Social Innovation in a Comparative Perspective. Routledge.", "Enlace": "https://drive.google.com/file/d/15vxPkw_sIhMr2HlqwUeT6qUM07VRcrxV/view?usp=sharing"},
        {"Referencia (APA)": "Laal, M., & Salamati, P. (2012). Lifelong learning; why do we need it? Procedia-Social and Behavioral Sciences, 31, 399-403.", "Enlace": "https://drive.google.com/file/d/1GpNnZdehT8Hdo_eVSVPV0Gpzp0WrA7Mr/view?usp=sharing"},
        {"Referencia (APA)": "Lugo, M. T., & Ithurburu, V. (2019). Políticas digitales en América Latina. Tecnologías para fortalecer la educación de calidad. Revista Iberoamericana de Educación, 79(1), 11-31.", "Enlace": "https://drive.google.com/file/d/10lMOy3yw0_lqAXnYu0kskeNDEvtnAsGy/view?usp=sharing"},
        {"Referencia (APA)": "Moulaert, F., & MacCallum, D. (2019). Advanced Introduction to Social Innovation. Edward Elgar Publishing.", "Enlace": "https://drive.google.com/file/d/1SvwHR_sRLyuU4W4CLQlF9_949sza3nCb/view?usp=sharing"},
        {"Referencia (APA)": "Pel, B., Haxeltine, A., Avelino, F., Dumitru, A., Kemp, R., Bauler, T., Kunze, I., Dorland, J., Wittmayer, J., & Jørgensen, M. S. (2020). Towards a theory of transformative social innovation: A relational framework and 12 propositions. Research Policy, 49(8), 104080.", "Enlace": "https://drive.google.com/file/d/12byZo62RW4uZKEdiAY83RDaSf7ftCY8C/view?usp=sharing"},
        {"Referencia (APA)": "Powell, W. W., & Snellman, K. (2004). The knowledge economy. Annual Review of Sociology, 30, 199-220.", "Enlace": "https://drive.google.com/file/d/1ei9ecK9vyy5ZnCrluJyzxNPgmADne7K0/view?usp=sharing"},
        {"Referencia (APA)": "Stoecker, R. (2016). Liberating service learning and the rest of higher education civic engagement. Temple University Press.", "Enlace": "https://drive.google.com/file/d/1ZKX1cdCEkjNZ7j0VxpM5W35RdIFHED0h/view?usp=sharing"},
        {"Referencia (APA)": "van Wijk, J., Zietsma, C., Dorado, S., de Bakker, F. G., & Martí, I. (2019). Social innovation: Integrating micro, meso, and macro level insights from institutional theory. Business & Society, 58(5), 887-918.", "Enlace": "https://drive.google.com/file/d/1hqny6lDE1wvCKxOuTDhVmWxbJeB21qdH/view?usp=sharing"},
        {"Referencia (APA)": "World Economic Forum. (2023). The Future of Jobs Report 2023.", "Enlace": "https://drive.google.com/file/d/1DkS32l0KuXITMWx0XcBsI3dY5sXOt8-d/view?usp=sharing"},
        {"Referencia (APA)": "Yin, R. K. (2018). Case Study Research and Applications: Design and Methods (6th ed.). Sage Publications.", "Enlace": "Sin Referencia"},
        {"Referencia (APA)": "Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education – where are the educators? International Journal of Educational Technology in Higher Education, 16(1), 39.", "Enlace": "https://drive.google.com/file/d/1O0QOlx800iGfgHLguJXKoieFda8XISdf/view?usp=sharing"}
    ])



    # st.dataframe(referencias, hide_index=True, column_config={
    #     "Referencia (APA)": st.column_config.TextColumn("Referencia (APA)"),
    #     "Enlace": st.column_config.LinkColumn("Enlace")
    # })

    html_table = create_html_table(referencias)
    st.markdown(html_table, unsafe_allow_html=True)

    st.info("""
    Algunas referencias no tienen enlaces asociados y se ha indicado **Sin Referencia** en la columna 
    de enlace. Para estas entradas, se recomienda buscar la fuente original o crear una referencia 
    completa basada en la información disponible.
    """, icon=":material/bubble_chart:")

    st.write("""
    Esta lista de referencias proporciona una base sólida para el proyecto de investigación, 
    abarcando una amplia gama de temas relevantes para Circle Up. La diversidad de fuentes 
    consultadas asegura una perspectiva integral y actualizada sobre los desafíos y oportunidades 
    en el ámbito del voluntariado académico, la mentoría inversa y la innovación social.

    Los lectores interesados en profundizar en temas específicos pueden acceder directamente a 
    las fuentes originales a través de los enlaces proporcionados, facilitando así la verificación 
    y expansión de la información presentada en este estudio.
    """)
