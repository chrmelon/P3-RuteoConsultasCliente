"""
state.py

Define el estado compartido del grafo y el modelo de salida del orquestador.

"""

from typing import Literal, Optional, TypedDict
from pydantic import BaseModel


# =============================================================================
# Modelo de salida estructurada del Orquestador
# =============================================================================
# Este modelo le "obliga" al LLM a responder con un JSON valido que tenga
# exactamente estos campos. Si el LLM intenta poner otro departamento que no
# sea "RRHH", "Finance" o "Tech", Pydantic lo rechaza automaticamente.
#
# Aprende mas: esto se usa con llm.with_structured_output(DepartmentRoute)
# =============================================================================

class DepartmentRoute(BaseModel):
    """Decision de routing del agente orquestador."""

    department: Literal["RRHH", "Marketing", "Finanzas", "Tech"]
    """Departamento al que se deriva la consulta."""

    reason: str
    """Explicacion breve de por que se eligio ese departamento."""


# =============================================================================
# Estado del Grafo
# =============================================================================
# TypedDict define la "memoria compartida" entre todos los nodos del grafo.
# Cada nodo puede leer y escribir en este estado.
#
# Flujo:
#   1. El usuario envía 'query' (solo campo obligatorio al inicio)
#   2. El orquestador llena 'department' y 'reason'
#   3. El agente worker llena 'response'
# =============================================================================

class AgentState(TypedDict):
    query: str
    """La consulta original del usuario. Este es el unico campo requerido al inicio."""

    department: Optional[str]
    """Departamento seleccionado por el orquestador. Se llena despues del routing."""

    reason: Optional[str]
    """Por que el orquestador eligio ese departamento."""

    response: Optional[str]
    """Respuesta final generada por el agente especialista (RRHH o Tech)."""
