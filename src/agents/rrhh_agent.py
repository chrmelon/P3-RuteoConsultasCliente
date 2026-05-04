"""
agents/rrhh_agent.py

El Agente Especialista de Recursos Humanos.
Solo se activa cuando el orquestador decide que la consulta es de RRHH.

"""

import logging
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.state import AgentState
from src.tracing import observe, get_client


logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_rrhh_node(llm: ChatOpenAI):
    """
    Factory function: construye y retorna el nodo del agente RRHH.

    A diferencia del orquestador, este agente NO usa with_structured_output
    porque su respuesta es texto libre (lenguaje natural para el usuario),
    no un JSON para tomar decisiones de routing.
    """

    @observe(name="rrhh_agent")
    def rrhh_node(state: AgentState) -> dict:
        """
        Nodo del grafo: genera una respuesta especializada en RRHH.

        Input del estado: state["query"]
        Output al estado: {"response": ...}
        """
        query = state["query"]
        logger.info(f"[AGENTE RRHH] Procesando consulta: '{query}'")

        lf = get_client()
        lf.update_current_span(
            input={"query": query},
            metadata={"tags": ["specialist", "rrhh"]},
        )

        # Cargamos el prompt del archivo .md
        prompt_path = PROMPTS_DIR / "rrhh.md"
        system_prompt = prompt_path.read_text(encoding="utf-8")

        # Llamamos al LLM con el prompt especializado
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ])

        lf.update_current_span(output={"response": response.content})

        logger.info("[AGENTE RRHH] Respuesta generada correctamente.")
        return {"response": response.content}

    return rrhh_node
