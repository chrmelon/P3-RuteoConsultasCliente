"""
agents/tech_agent.py

El Agente Especialista de Tecnologia.
Solo se activa cuando el orquestador decide que la consulta es de Tech.

"""

import logging
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.state import AgentState
from src.tracing import observe, get_client

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_tech_node(llm: ChatOpenAI):
    """
    Factory function: construye y retorna el nodo del agente Tech.

    Identico en estructura al agente RRHH, pero carga su propio prompt
    especializado en temas de tecnologia e infraestructura.
    """
    @observe(name="tech_agent")
    def tech_node(state: AgentState) -> dict:
        """
        Nodo del grafo: genera una respuesta especializada en Tech.

        Input del estado: state["query"]
        Output al estado: {"response": ...}
        """
        query = state["query"]
        logger.info(f"[AGENTE TECH] Procesando consulta: '{query}'")

        lf = get_client()
        lf.update_current_span(
            input={"query": query},
            metadata={"tags": ["specialist", "tech"]},
        )

        # Cargamos el prompt del archivo .md
        prompt_path = PROMPTS_DIR / "tech.md"
        system_prompt = prompt_path.read_text(encoding="utf-8")

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ])

        lf.update_current_span(output={"response": response.content})

        logger.info("[AGENTE TECH] Respuesta generada correctamente.")
        return {"response": response.content}

    return tech_node
