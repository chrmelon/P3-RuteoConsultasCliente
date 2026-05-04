"""
main.py

Punto de entrada del Sistema Multi-Agente por linea de comandos (CLI).

Uso:
    python src.multi_agent_system.py --query "Tu consulta aqui"

Ejemplos:
    python src.multi_agent_system.py --query "Como solicito mis vacaciones?"
    python src.multi_agent_system.py --query "El servidor de produccion esta caido"
    python src.multi_agent_system.py --query "Cual es la politica de home office?"

"""

import argparse
import sys
from langchain_openai import ChatOpenAI
from pathlib import Path
from dotenv import load_dotenv
from src.graph import build_graph
from src.logger import get_logger
from src.tracing import langfuse, observe
from src.evaluator import evaluate_response
from langfuse import get_client

logger = get_logger(__name__)

sys.path.append(str(Path(__file__).resolve().parent.parent))

load_dotenv()

@observe(name="consulta_usuario")
def go():
    # -------------------------------------------------------------------------
    # Configuracion de argumentos CLI
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Sistema Multi-Agente - Orquestador + Workers",
        epilog='Ejemplo: python src.multi_agent_system.py --query "Como solicito vacaciones?"',
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="La consulta del usuario para el sistema multi-agente",
    )
    args = parser.parse_args()

    query = args.query.strip()
    if not query:
        logger.error("La consulta no puede estar vacia.")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Construccion y ejecucion del grafo
    # -------------------------------------------------------------------------
    logger.info("=" * 60)
    logger.info("SISTEMA MULTI-AGENTE")
    logger.info("=" * 60)
    logger.info(f"Consulta recibida: '{query}'")
    logger.info("-" * 60)

    try:
        graph = build_graph()

        # Ejecutamos el grafo con la consulta del usuario
        # El estado inicial solo necesita 'query', el resto lo van llenando los nodos
        result = graph.invoke({"query": query})

        # ── Evaluación automática de calidad ──────────────────
        trace_id = get_client().get_current_trace_id()

        if result.get("response") and trace_id:
            evaluate_response(
                trace_id=trace_id,
                query=query,
                response=result["response"],
                department=result.get("department", "unknown"),
                llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
            )
        # ──────────────────────────────────────────────────────

    except Exception as e:
        logger.error(f"Error al ejecutar el grafo: {e}")
        logger.error("Verifica que tu OPENAI_API_KEY sea valida y que los prompts esten completos.")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # Mostrar resultado
    # -------------------------------------------------------------------------
    logger.info("-" * 60)
    logger.info(f"DEPARTAMENTO: {result.get('department', 'N/A')}")
    logger.info(f"RAZON DEL ROUTING: {result.get('reason', 'N/A')}")
    logger.info("-" * 60)

    print("\n" + "=" * 60)
    print("RESPUESTA DEL AGENTE ESPECIALISTA:")
    print("=" * 60)
    print(result.get("response", "Sin respuesta"))
    print("=" * 60 + "\n")


if __name__ == "__main__":
    go()
