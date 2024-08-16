from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from typing import List
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_anthropic import ChatAnthropic
from typing import List, Dict


def brainstorming(profile: str, client) -> str:
    chat = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1, anthropic_api_key=client.api_key,max_tokens_to_sample=650)

    prompt = ChatPromptTemplate.from_template("""
    <Rol>
    Asume el rol de un coach profesional, academico, investigador y experto con amplia experiencia en desarrollo comunitario. Tu misión es diseñar 2 propuestas de cursos adaptados al siguiente perfil:
    </Rol>

    <Perfil>
    {profile}
    </Perfil>
    
    <Para cada propuesta, incluye>
    1. Título conciso y atractivo. Formato: #### Titulo para redes sociales (6 palabras, sin dos puntos)

    2. Párrafo descriptivo y argumentativo que (MAXIMO 55 Palabras):
    - Detalle el contenido específico del curso (ej. Python: estructuras de datos, listas, tuplas).
    - Explique los beneficios tangibles para los participantes.
    - Demuestre la relevancia y aplicación práctica en contextos reales en paises en desarrollo en america latina.
    - Enfatice el desarrollo de habilidades blandas sobre el impacto académico.
    - Proporcione instrucciones claras sobre cómo se debe construir y desarrollar el curso.

    3. Lista de 3-5 palabras clave, utilizando terminología precisa de la disciplina. Formato  :blue[**Keywords**:] Word1, Word2, Word3, Word4, Word5, Word6
    4. Lista de herramientas open source recomendadas para el curso. Formato:  :blue[****Open Source**]: [Hrr1](link), [Hrr2](link), [Hrr3](link), [Hrr4](link), [Hrr5](link), [Hrr6](link) 
    </Para cada propuesta, incluye>                           
    
    <Consideraciones Importantes>
    - Las propuestas deben estar ligadas directamete a la expericiencia laboral y luego academica del perfil.
    - El curso tendra una duracion maxima de 2 horas.
    - Utiliza un lenguaje neutro y académico.
    - Enfócate en propuestas particularmente relevantes para contextos de paises en desarrollo en america latina y desafíos socioeconómicos.
    - Los cursos están dirigidos a individuos, no a empresas.
    - Prioriza métodos catedráticos y recursos de acceso libre debido a las limitaciones presupuestarias.
    - Concentra el contenido en desarrollar habilidades prácticas y blandas sobre conocimientos puramente académicos.
    """)

    chain = prompt | chat

    result = chain.invoke({
        "profile": profile
    })

    return result

def create_community_academic_presentation_schemas() -> List[ResponseSchema]:
    schemas = [
        ResponseSchema(name="context", description="Breve descripción del tema (40 palabras). Incluir área de estudio y relevancia para la comunidad."),
        ResponseSchema(name="slide1_title", description="Título conciso (6 palabras, sin dos puntos), atractivo en el contexto (america latina, Colombia) para la presentación."),
        ResponseSchema(name="slide1_objective", description="Objetivo principal de la sesión (1 oración 50 palabras)."),
        ResponseSchema(name="slide2_icebreaker_title", description="Título de la actividad dinámica inicial."),
        ResponseSchema(name="slide2_icebreaker_instructions", description="Instrucciones breves para actividad dinámica, divertida, participativa, reflexiva, agradable, sin materiales (máximo 65 palabras)."),
        ResponseSchema(name="slide2_icebreaker_purpose", description="Propósito de la actividad en relación con el tema (1 oración 20 palabras)."),
        ResponseSchema(name="slide3_rhetorical_question", description="Pregunta retórica para estimular la participación y reflexión. (contexto latino americano, Colombia)"),
        ResponseSchema(name="slide4_concept1_title", description="Título del primer concepto fundamental."),
        ResponseSchema(name="slide4_concept1_definition", description="Definición del primer concepto (máximo 30 palabras)."),
        ResponseSchema(name="slide5_concept2_title", description="Título del segundo concepto fundamental."),
        ResponseSchema(name="slide5_concept2_definition", description="Definición del segundo concepto (máximo 30 palabras)."),
        ResponseSchema(name="slide6_concept3_title", description="Título del tercer concepto fundamental."),
        ResponseSchema(name="slide6_concept3_definition", description="Definición del tercer concepto (máximo 30 palabras)."),
        ResponseSchema(name="slide7_real_world_application_title", description="Título de la sección de aplicación en el mundo real."),
        ResponseSchema(name="slide7_real_world_application_points", description="3-4 puntos numerados sobre cómo se aplica el tema en situaciones reales, contexto latino americano, Colombia."),
        ResponseSchema(name="slide8_leadership_insights_title", description="Título de la sección de insights de liderazgo."),
        ResponseSchema(name="slide8_leadership_insights_points", description="3-4 puntos numerados sobre liderazgo relacionados con el tema, contexto latino americano, Colombia."),
        ResponseSchema(name="slide9_critical_thinking_title", description="Título de la sección de pensamiento crítico."),
        ResponseSchema(name="slide9_critical_thinking_points", description="3-4 puntos numerados que fomenten el pensamiento crítico sobre el tema, contexto latino americano, Colombia."),
        ResponseSchema(name="slide10_problem_solving_title", description="Título de la sección de resolución de problemas."),
        ResponseSchema(name="slide10_problem_solving_points", description="3-4 estrategias numeradas de resolución de problemas aplicadas al tema, contexto latino americano, Colombia."),
        ResponseSchema(name="slide11_community_impact_title", description="Título de la sección de impacto comunitario."),
        ResponseSchema(name="slide11_community_impact_points", description="3-4 puntos numerados sobre cómo el tema puede impactar positivamente en la comunidad, contexto latino americano, Colombia."),
        ResponseSchema(name="slide12_open_discussion_questions", description="3 preguntas abiertas para fomentar la discusión grupal, contexto latino americano, Colombia."),
        ResponseSchema(name="open_source_resources", description="Lista de 3-4 recursos de código abierto o open source relevantes para explorar más el tema, colocar nombre recurso: definicion practica"),
        ResponseSchema(name="verified_references", description="Lista de 3-5 referencias bibliográficas de investigaciones o articulos cientificos en formato APA. Incluir solo si hay alta confianza en su exactitud, contexto latino americano, Colombia.")
    ]
    return schemas

def generate_community_academic_presentation_content(context: str, client) -> Dict:
    chat = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.2, anthropic_api_key=client.api_key, max_tokens_to_sample=2000)
    
    response_schemas = create_community_academic_presentation_schemas()
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template(
        """Genera contenido para una presentación catedratica, agradable, esta presentacion se da en el contexto de community based learning y el tema es sobre: {context}

        {format_instructions}

        Instrucciones:
        - Use lenguaje académico, neutro, accesible y relevante.
        - Incluya elementos interactivos y reflexivos.
        - Enfóquese en aplicaciones prácticas, liderazgo y pensamiento crítico.
        - Considere el uso de recursos de código abierto unicamente.
        - Considere pero no limite a contexto latino americano (Colombia).
        - La presentación es dirigida por un voluntario que comparte conocimiento con su comunidad.
        """
    )

    chain = prompt | chat | output_parser
    
    result = chain.invoke({
        "context": context,
        "format_instructions": format_instructions
    })
    
    return result

def convert_content_to_table(content: Dict, user_data: Dict) -> List[Dict[str, str]]:
    """
    Convierte el contenido generado en una tabla con columnas 'name' y 'description',
    incluyendo los datos de usuario al principio.
    
    :param content: Diccionario con el contenido generado
    :param user_data: Diccionario con los datos de usuario de Streamlit
    :return: Lista de diccionarios, cada uno representando una fila de la tabla
    """
    table = []
    
    # Agregar datos de usuario al principio
    for key, value in user_data.items():
        table.append({
            "name": key,
            "description": str(value)
        })
    
    # Agregar el contenido generado
    for key, value in content.items():
        if isinstance(value, list):
            table.append({
                "name": key,
                "description": "\n".join(f"- {item}" for item in value)
            })
        else:
            table.append({
                "name": key,
                "description": value
            })
    
    return table

def create_community_academic_presentation(topic: str, client):
    content = generate_community_academic_presentation_content(topic, client)
    return content

def generate_presentation(topic: str, user_data: Dict, client):
    content = create_community_academic_presentation(topic, client)
    return convert_content_to_table(content,user_data)









