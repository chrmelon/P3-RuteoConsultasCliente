"""
agents/finanzas_agent.py

El Agente Especialista de Finanzas.
Solo se activa cuando el orquestador decide que la consulta es de Finanzas.

"""

import logging
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.state import AgentState
from src.tracing import observe, get_client

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_finanzas_node(llm: ChatOpenAI):
    """
    Factory function: construye y retorna el nodo del agente Finanzas.

    Genera respuestas sobre pagos, presupuestos, reportes financieros
    y procesos contables segun el prompt que definan los estudiantes.
    """
    @observe(name="finanzas_agent")
    def finanzas_node(state: AgentState) -> dict:
        """
        Nodo del grafo: genera una respuesta especializada en Finanzas.

        Input del estado: state["query"]
        Output al estado: {"response": ...}
        """
        query = state["query"]
        logger.info(f"[AGENTE FINANZAS] Procesando consulta: '{query}'")

        lf = get_client()
        lf.update_current_span(
            input={"query": query},
            metadata={"tags": ["specialist", "finanzas"]},
        )

        # Cargamos el prompt del archivo .md
        prompt_path = PROMPTS_DIR / "finanzas.md"
        system_prompt = prompt_path.read_text(encoding="utf-8")

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ])

        lf.update_current_span(output={"response": response.content})

        logger.info("[AGENTE FINANZAS] Respuesta generada correctamente.")
        return {"response": response.content}

    return finanzas_node
