from langchain_anthropic import ChatAnthropic
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Tuple

class EvaluationCriteria(BaseModel):
    Claridad: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva constructiva concisa, sugerencia de mejora, y dos preguntas para profundizar en la claridad)")
    Relevancia: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, sugerencia de mejora, y dos preguntas para profundizar en la relevancia.)")
    Viabilidad: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, sugerencia de mejora, y dos preguntas para profundizar en la viabilidad.)")
    Impacto: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, sugerencia de mejora, y dos preguntas para profundizar en el impacto.)")
    Titulo: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, sugerencia de mejora (si aplica), y dos preguntas para profundizar en el título.)")
    Objetivos: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, reescribe mejores objetivos, y dos preguntas para profundizar en los objetivos.)")
    Idea: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, sugerencia de mejora, y dos preguntas para profundizar en la idea.)")
    Actividades: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, reescribe actividades mejoradas, y dos preguntas para profundizar en las actividades.)")
    Metodologia: Tuple[int, str] = Field(description="Puntaje (1-5) y (crítica constructiva concisa, sugerencia de mejora, y dos preguntas para profundizar en la metodología.)")

#model="claude-3-haiku-20240307"
# model="claude-3-5-sonnet-20240620"
def evaluate_proposal_langchain(proposal, client):
    chat = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.1, anthropic_api_key=client.api_key)

    parser = PydanticOutputParser(pydantic_object=EvaluationCriteria)

    prompt = ChatPromptTemplate.from_template("""
    Eres un experto en revisión de propuestas de cursos académicos practicos para la comunidad. 
    Tu tarea es analizar a fondo la propuesta proporcionada usando todos los detalles proporcionados de los cuales eres experto.
    Debes calificar de forma critica y coherente y de manera empatica y siempre segunda persona singular responde a cada metrica. 

                                                                                        
    Propuesta del curso:
    {proposal}

    Sin perder el estandar y la calidad de la respuesta usa maximo 120 tokens por cada metrica 
    {format_instructions}

    Asegúrate de que tu respuesta siga estrictamente el formato requerido.
    """)

    chain = prompt | chat | parser

    result = chain.invoke({
        "proposal": proposal,
        "format_instructions": parser.get_format_instructions()
    })

    return result.dict()
