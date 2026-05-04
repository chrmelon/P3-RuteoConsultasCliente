"""
src/evaluator.py

Evaluador automático de calidad de respuestas.
Usa LLM-as-a-Judge para puntuar cada respuesta en 3 dimensiones.
"""

import json
import logging
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.tracing import langfuse

logger = logging.getLogger(__name__)

EVAL_PROMPT = """Eres un evaluador experto de calidad de respuestas de asistentes de IA.

Dada una consulta del usuario y la respuesta del asistente, puntuá cada dimensión del 0.0 al 1.0:

- relevance: ¿La respuesta es relevante y responde a lo que preguntó el usuario?
- completeness: ¿La respuesta cubre todos los aspectos importantes de la consulta?
- accuracy: ¿La respuesta parece correcta, sin información errónea o confusa?

Respondé ÚNICAMENTE con un JSON válido, sin texto adicional:
{
  "relevance": 0.0,
  "completeness": 0.0,
  "accuracy": 0.0,
  "reasoning": "breve explicación de los puntajes"
}"""


def evaluate_response(
    trace_id: str,
    query: str,
    response: str,
    department: str,
    llm: ChatOpenAI,
) -> dict:
    """
    Evalúa la calidad de una respuesta y registra los scores en Langfuse.

    Args:
        trace_id:   ID del trace de Langfuse al que asociar los scores
        query:      Consulta original del usuario
        response:   Respuesta generada por el agente especialista
        department: Departamento que atendió la consulta
        llm:        Instancia del LLM a usar como juez

    Returns:
        dict con los scores calculados
    """
    logger.info(f"[EVALUADOR] Evaluando respuesta del agente {department}...")

    user_message = f"""CONSULTA DEL USUARIO:
{query}

RESPUESTA DEL ASISTENTE:
{response}"""

    try:
        result = llm.invoke([
            SystemMessage(content=EVAL_PROMPT),
            HumanMessage(content=user_message),
        ])

        # Parsear el JSON de respuesta
        scores = json.loads(result.content)

        # Registrar cada score en Langfuse v4 — se usa create_score()
        for dimension in ["relevance", "completeness", "accuracy"]:
            langfuse.create_score(
                trace_id=trace_id,
                name=dimension,
                value=scores[dimension],
                comment=scores.get("reasoning", ""),
            )

        logger.info(
            f"[EVALUADOR] Scores — "
            f"relevance: {scores['relevance']:.2f} | "
            f"completeness: {scores['completeness']:.2f} | "
            f"accuracy: {scores['accuracy']:.2f}"
        )

        return scores

    except Exception as e:
        logger.error(f"[EVALUADOR] Error al evaluar: {e}")
        return {}   