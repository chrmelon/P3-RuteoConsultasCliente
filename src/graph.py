"""
graph.py

Ensambla el grafo multi-agente usando LangGraph.

Este archivo define la "arquitectura" del sistema: que nodos existen,
en que orden se ejecutan y como se decide el routing entre ellos.

Diagrama del flujo:
    START
      |
      v
  [ORQUESTADOR]          <- clasifica la consulta del usuario
      |
      |--- RRHH?      ---> [AGENTE RRHH] ---> END
      |--- Finanzas?  ---> [AGENTE FINANZAS]  ---> END
      `--- Tech?      ---> [AGENTE TECH]      ---> END
"""

import os
import logging
from typing import Literal

import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph

from src.agents.orchestrator import build_orchestrator_node
from src.agents.rrhh_agent import build_rrhh_node
from src.agents.finanzas_agent import build_finanzas_node
from src.agents.tech_agent import build_tech_node
from src.state import AgentState

sys.path.append(str(Path(__file__).resolve().parent.parent))

load_dotenv()
logger = logging.getLogger(__name__)


# =============================================================================
# Funcion de Routing Condicional
# =============================================================================
# Esta funcion es llamada por LangGraph DESPUES de que el orquestador
# termina su trabajo. Lee state["department"] y retorna el nombre del
# siguiente nodo a ejecutar.
#
# Es una funcion pura: no llama al LLM, solo lee el estado y decide.
# =============================================================================

def route_department(
    state: AgentState,
) -> Literal["rrhh_agent", "finanzas_agent", "tech_agent"]:
    """
    Decide a que nodo ir basandose en el departamento elegido por el orquestador.

    Args:
        state: El estado actual del grafo (contiene "department")

    Returns:
        El nombre del nodo a ejecutar a continuacion.
    """
    department = (state.get("department") or "").upper()

    routes = {
        "RRHH": "rrhh_agent",
        "FINANZAS": "finanzas_agent",
        "TECH": "tech_agent",
    }

    destination = routes.get(department, "tech_agent")
    logger.info(f"[ROUTING] {department} -> {destination}")
    return destination  # type: ignore[return-value]


# =============================================================================
# Constructor del Grafo
# =============================================================================

def build_graph():
    """
    Construye y compila el grafo multi-agente.

    Returns:
        CompiledStateGraph: el grafo listo para invocar con .invoke()
    """
    # Inicializamos el modelo de lenguaje compartido por todos los agentes
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.1,
    )

    # Construimos los nodos usando las factory functions
    orchestrator_node = build_orchestrator_node(llm)
    rrhh_node = build_rrhh_node(llm)
    finanzas_node = build_finanzas_node(llm)
    tech_node = build_tech_node(llm)

    # Creamos el grafo con el estado definido en state.py
    builder = StateGraph(AgentState)

    # -------------------------------------------------------------------------
    # Registramos los nodos
    # -------------------------------------------------------------------------
    builder.add_node("orchestrator", orchestrator_node)
    builder.add_node("rrhh_agent", rrhh_node)
    builder.add_node("finanzas_agent", finanzas_node)
    builder.add_node("tech_agent", tech_node)

    # -------------------------------------------------------------------------
    # Definimos las conexiones (edges)
    # -------------------------------------------------------------------------

    # El punto de entrada siempre es el orquestador
    builder.add_edge(START, "orchestrator")

    # Despues del orquestador el routing es CONDICIONAL:
    # LangGraph llama a route_department(state) para saber a donde ir
    builder.add_conditional_edges(
        "orchestrator",
        route_department,
        {
            "rrhh_agent": "rrhh_agent",
            "finanzas_agent": "finanzas_agent",
            "tech_agent": "tech_agent",
        },
    )

    # Todos los agentes workers terminan en END
    builder.add_edge("rrhh_agent", END)
    builder.add_edge("finanzas_agent", END)
    builder.add_edge("tech_agent", END)

    return builder.compile()
