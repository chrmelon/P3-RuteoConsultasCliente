"""
agents/orchestrator.py

El Agente Orquestador: el "cerebro" del sistema.
Su unica responsabilidad es leer la consulta del usuario y decidir
a que departamento derivarla (RRHH , Tech o Finanzas).

"""

import logging
from pathlib import Path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from src.state import AgentState, DepartmentRoute
from src.tracing import langfuse, observe, get_client

logger = logging.getLogger(__name__)

# Ruta al directorio de prompts, relativa a este archivo
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def build_orchestrator_node(llm: ChatOpenAI):
    """
    Factory function: construye y retorna el nodo orquestador.

    Usa with_structured_output para forzar al LLM a responder con
    un JSON valido segun el modelo DepartmentRoute (ver state.py).

    Esto es mas robusto que json_mode=True porque Pydantic valida
    que el departamento sea exactamente "RRHH",  "Tech" o "Finance".
    """
    # Configuramos el LLM para que su output sea validado por DepartmentRoute
    structured_llm = llm.with_structured_output(DepartmentRoute)

    @observe(name="orchestrator")  # Langfuse v4: crea un span automáticamente

    def orchestrator_node(state: AgentState) -> dict:
        """
        Nodo del grafo: clasifica la consulta y retorna el departamento.

        Input del estado: state["query"]
        Output al estado: {"department": ..., "reason": ...}
        """
        query = state["query"]

        logger.info(f"[ORQUESTADOR] Analizando consulta: '{query}'")

        # Registramos el input en el span actual de Langfuse
        lf = get_client()
        lf.update_current_span(
            input={"query": query},
            metadata={"tags": ["routing", "orchestrator"]},  
        )

        # Cargamos el prompt del archivo .md
        prompt_path = PROMPTS_DIR / "orchestrator.md"
        system_prompt = prompt_path.read_text(encoding="utf-8")


        # Llamamos al LLM con el prompt del sistema y la consulta del usuario
        result: DepartmentRoute = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=query),
        ])


        output = {
            "department": result.department,
            "reason": result.reason,
        }

        # Registramos el output en el span actual de Langfuse
        lf.update_current_span(output=output)

        logger.info(f"[ORQUESTADOR] Departamento seleccionado: {result.department}")
        logger.info(f"[ORQUESTADOR] Razon: {result.reason}")

        # Retornamos solo los campos que este nodo actualiza
        return output

    return orchestrator_node
