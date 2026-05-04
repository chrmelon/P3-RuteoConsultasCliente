# P3 — Sistema Multi-Agente con Ruteo y RAG por Dominio

> **Asistente inteligente** que recibe consultas en lenguaje natural, las clasifica automáticamente y las deriva al agente especialista correcto (RRHH, Finanzas o Tech), cada uno con su propia base de conocimiento (RAG).

---

## Índice

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura](#arquitectura)
3. [Estructura de Archivos](#estructura-de-archivos)
4. [Requisitos Previos](#requisitos-previos)
5. [Instalación](#instalación)
6. [Configuración de API Keys](#configuración-de-api-keys)
7. [Construcción del Índice RAG](#construcción-del-índice-rag)
8. [Cómo Ejecutar el Sistema](#cómo-ejecutar-el-sistema)
9. [Ejemplos de Uso](#ejemplos-de-uso)
10. [Suite de Tests](#suite-de-tests)
11. [Observabilidad con Langfuse](#observabilidad-con-langfuse)
12. [Notas de Configuración](#notas-de-configuración)
13. [Limitaciones Conocidas](#limitaciones-conocidas)

---

## Descripción del Proyecto

Este proyecto implementa un **sistema multi-agente** construido con LangGraph y LangChain. El sistema resuelve el problema de centralizar consultas de empleados o clientes que pertenecen a distintas áreas, evitando que el usuario tenga que saber a qué departamento dirigirse.

**¿Qué hace el sistema?**

1. El usuario escribe una consulta en lenguaje natural.
2. El **Agente Orquestador** analiza la consulta y decide a qué departamento pertenece.
3. El **Agente Especialista** correspondiente responde usando su base de conocimiento RAG específica.
4. Todo el flujo queda registrado en **Langfuse** para monitoreo y análisis.

**Departamentos soportados:**

| Departamento | Ejemplos de consultas |
|---|---|
| 🧑‍💼 RRHH | Vacaciones, home office, datos personales, sueldos |
| 💰 Finanzas | Pagos, facturas, cobros, presupuestos |
| 💻 Tech | Errores de sistema, servidores caídos, problemas de acceso |

---

## Arquitectura

```
Usuario
   │
   ▼
┌─────────────────────┐
│  Agente Orquestador │  ← GPT-4o-mini + Structured Output (Pydantic)
│  (orchestrator.py)  │    Decide: RRHH | Finanzas | Tech
└─────────────────────┘
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌────────┐ ┌─────────┐ ┌──────┐
│  RRHH  │ │Finanzas │ │ Tech │  ← Agentes especialistas
│ Agent  │ │  Agent  │ │Agent │    con RAG por dominio
└────────┘ └─────────┘ └──────┘
    │           │           │
    └─────┬─────┘           │
          ▼                 ▼
     ChromaDB (vectorstore por dominio)
          │
          ▼
      Respuesta final al usuario
```

**Stack tecnológico:**

- **LangGraph** — Orquestación del flujo multi-agente
- **LangChain** — Abstracción de LLMs y RAG
- **OpenAI GPT-4o-mini** — Modelo de lenguaje principal
- **ChromaDB** — Vector store local para el RAG
- **Langfuse** — Observabilidad y trazabilidad
- **Pydantic** — Validación del output estructurado del orquestador

---

## Estructura de Archivos

```
P3-RuteoConsulasCliente/
│
├── src/
│   ├── agents/
│   │   ├── orchestrator.py      # Agente orquestador: clasifica la consulta
│   │   ├── rrhh_agent.py        # Agente especialista de RRHH
│   │   ├── finanzas_agent.py    # Agente especialista de Finanzas
│   │   └── tech_agent.py        # Agente especialista de Tech
│   │
│   ├── prompts/
│   │   ├── orchestrator.md      # Prompt del orquestador
│   │   ├── rrhh.md              # Prompt del agente RRHH
│   │   ├── finanzas.md          # Prompt del agente Finanzas
│   │   └── tech.md              # Prompt del agente Tech
│   │
│   ├── graph.py                 # Ensamblado del grafo LangGraph
│   ├── state.py                 # Estado compartido y modelo Pydantic
│   ├── tracing.py               # Inicialización del cliente Langfuse
│   ├── build_index.py           # Script para construir los índices RAG
│   ├── multi_agent_system.py    # Punto de entrada CLI
│   ├── test_querys.py           # Runner de tests automatizados
│   └── logger.py                # Logger con colores ANSI
│
├── data/
│   ├── hr_docs/                 # Documentos base de RRHH (.txt / .md)
│   ├── finance_docs/            # Documentos base de Finanzas
│   └── tech_docs/               # Documentos base de Tech
│
├── tests/
│   └── test_querys.json         # 15 casos de prueba con departamento esperado
│
├── chroma_db/                   # Vector store generado automáticamente
├── config.yaml                  # Configuración del sistema
├── requirements.txt             # Dependencias del proyecto
└── .env                         # Variables de entorno (no se sube a git)
```

---

## Requisitos Previos

- Python **3.10** o superior
- Cuenta en [OpenAI](https://platform.openai.com/) con API key activa
- Cuenta en [Langfuse](https://cloud.langfuse.com/) (gratuita) para observabilidad

---

## Instalación

### 1. Clonar o descomprimir el proyecto

```bash
cd C:\Dev
# Si es un zip, descomprimir en C:\Dev\P3-RuteoConsulasCliente
```

### 2. Crear el entorno virtual

```bash
cd C:\Dev\P3-RuteoConsulasCliente
python -m venv .venv
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

> Verificá que el prompt muestre `(.venv)` antes de continuar.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

> La instalación puede tardar 2–5 minutos. Se instalan LangChain, LangGraph, ChromaDB, Langfuse y otras librerías.

---

## Configuración de API Keys

### 1. Crear el archivo `.env`

En la raíz del proyecto, creá un archivo llamado `.env` (podés copiar `.env_example`):

```bash
cp .env_example .env
```

### 2. Completar las variables

Abrí `.env` con cualquier editor y completá los valores:

```env
# ── OpenAI ──────────────────────────────────────────────
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Langfuse (Observabilidad) ────────────────────────────
# Obtener en: https://cloud.langfuse.com → Settings → API Keys
LANGFUSE_PUBLIC_KEY=pk-lf-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGFUSE_SECRET_KEY=sk-lf-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LANGFUSE_HOST=https://cloud.langfuse.com

# ── Modelo (opcional, por defecto gpt-4o-mini) ───────────
OPENAI_MODEL=gpt-4o-mini
```

### ¿Dónde obtener las keys?

**OpenAI:**
1. Ir a [platform.openai.com](https://platform.openai.com/)
2. Menú → API Keys → Create new secret key

**Langfuse:**
1. Ir a [cloud.langfuse.com](https://cloud.langfuse.com/)
2. Crear cuenta gratuita
3. Crear un proyecto nuevo
4. Settings → API Keys → Create new key

> ⚠️ **Importante:** Nunca subas el archivo `.env` a Git. Ya está incluido en `.gitignore`.

---

## Construcción del Índice RAG

Antes de ejecutar el sistema por primera vez, hay que construir los vectores de los documentos base.

### 1. Verificar que hay documentos en las carpetas `data/`

```
data/
├── hr_docs/        ← Documentos de RRHH (políticas, beneficios, etc.)
├── finance_docs/   ← Documentos de Finanzas (procedimientos, políticas)
└── tech_docs/      ← Documentos de Tech (guías, procedimientos)
```

Los archivos pueden ser `.txt`, `.pdf` o `.md`.

### 2. Ejecutar el indexador

```bash
python -m src.build_index
```

**Output esperado:**
```
INFO | Indexando dominio: hr
INFO | hr: 52 chunks indexados
INFO | Indexando dominio: tech
INFO | tech: 56 chunks indexados
INFO | Indexando dominio: finance
INFO | finance: 57 chunks indexados
```

Esto genera la carpeta `chroma_db/` con los índices vectoriales. Solo es necesario ejecutarlo **una vez**, o cada vez que se modifiquen los documentos base.

---

## Cómo Ejecutar el Sistema

### Ejecución por línea de comandos (CLI)

El punto de entrada principal es `src/multi_agent_system.py`:

```bash
python -m src.multi_agent_system --query "Tu consulta aquí"
```

**Output esperado:**
```
17:09:54 │ __main__  │ INFO │ ========================================
17:09:54 │ __main__  │ INFO │ SISTEMA MULTI-AGENTE
17:09:54 │ __main__  │ INFO │ ========================================
17:09:54 │ __main__  │ INFO │ Consulta recibida: 'no puedo realizar el pago'
17:09:54 │ __main__  │ INFO │ DEPARTAMENTO: Finanzas
17:09:54 │ __main__  │ INFO │ RAZON DEL ROUTING: La consulta está relacionada con un problema de pago

============================================================
RESPUESTA DEL AGENTE ESPECIALISTA:
============================================================
Para resolver el problema con tu pago, te recomiendo...
============================================================
```

---

## Ejemplos de Uso

### Consultas de RRHH

```bash
python -m src.multi_agent_system --query "¿Cómo solicito mis vacaciones?"
```
```bash
python -m src.multi_agent_system --query "¿Cuál es la política de home office?"
```
```bash
python -m src.multi_agent_system --query "Quiero saber cómo pedir un aumento de sueldo"
```

### Consultas de Finanzas

```bash
python -m src.multi_agent_system --query "No puedo realizar un pago"
```
```bash
python -m src.multi_agent_system --query "¿Cómo se calculan los impuestos en mi factura?"
```
```bash
python -m src.multi_agent_system --query "Detecté un cobro incorrecto en mi factura"
```

### Consultas de Tech

```bash
python -m src.multi_agent_system --query "No puedo iniciar sesión en el sistema"
```
```bash
python -m src.multi_agent_system --query "El servidor de producción está caído"
```
```bash
python -m src.multi_agent_system --query "El sistema me tira error 500 al guardar datos"
```

### Consultas ambiguas (el sistema decide)

```bash
python -m src.multi_agent_system --query "No sé a quién contactar para un problema interno"
```
```bash
python -m src.multi_agent_system --query "Mi cuenta fue suspendida, ¿qué hago?"
```

---

## Suite de Tests

El proyecto incluye 15 casos de prueba predefinidos con el departamento esperado para cada consulta.

### Ejecutar todos los tests

```bash
python -m src.test_querys
```

**Output esperado:**
```
=== EJECUTANDO TESTS ===

1. ¿Cómo solicito vacaciones?
   Esperado: RRHH
   Predicho: RRHH
   Resultado: ✅

2. No puedo iniciar sesión en el sistema
   Esperado: Tech
   Predicho: Tech
   Resultado: ✅

...

==================================================
Accuracy: 15/15 = 100.00%
==================================================
```

### Casos de prueba incluidos

| # | Consulta | Departamento esperado |
|---|---|---|
| 1 | ¿Cómo solicito vacaciones? | RRHH |
| 2 | ¿Cuántos días de vacaciones tengo disponibles? | RRHH |
| 3 | ¿Cuál es la política de home office? | RRHH |
| 4 | No puedo iniciar sesión en el sistema | Tech |
| 5 | El servidor de producción está caído | Tech |
| 6 | La aplicación está muy lenta | Tech |
| 7 | No puedo realizar un pago | Finanzas |
| 8 | ¿Cómo se calculan los impuestos en mi factura? | Finanzas |
| 9 | Detecté un cobro incorrecto en mi factura | Finanzas |
| 10 | Necesito cambiar mis datos personales | RRHH |
| 11 | El sistema me tira error 500 al guardar datos | Tech |
| 12 | Mi cuenta fue suspendida por falta de pago | Finanzas |
| 13 | No sé a quién contactar para un problema interno | RRHH |
| 14 | Quiero saber cómo pedir un aumento de sueldo | RRHH |
| 15 | El sistema no responde y no puedo trabajar | Tech |

---

## Observabilidad con Langfuse

El sistema registra automáticamente cada ejecución en Langfuse, incluyendo:

- **Input** de cada agente (la consulta recibida)
- **Output** de cada agente (la respuesta o el departamento elegido)
- **Metadata** con tags por tipo de agente
- **Latencia** de cada llamada al LLM

### Ver las trazas

1. Ir a [cloud.langfuse.com](https://cloud.langfuse.com/)
2. Seleccionar tu proyecto
3. Ir a **Tracing** en el menú lateral

Cada ejecución aparece como un span con el nombre del agente (`orchestrator`, `rrhh_agent`, `finanzas_agent`, `tech_agent`) y tambien hace trace de la consulta del usuario (`consulta_usuario`).

### Estructura de una traza completa

```
📦 orchestrator          ← Clasifica la consulta
    input:  {"query": "no puedo realizar el pago"}
    output: {"department": "Finanzas", "reason": "..."}

📦 finanzas_agent        ← Responde la consulta
    input:  {"query": "no puedo realizar el pago"}
    output: {"response": "Para resolver el problema..."}
```

---

## Notas de Configuración

### config.yaml

```yaml
llm_model: gpt-4o-mini          # Modelo principal del LLM
embedding_model: text-embedding-3-small  # Modelo para generar embeddings
chunk_size: 300                  # Tamaño de cada chunk en el RAG
chunk_overlap: 50                # Solapamiento entre chunks
retrieval_k: 5                   # Cantidad de chunks recuperados por consulta
compression_threshold: 0.40      # Umbral de similitud para filtrar resultados
max_tokens: 1000                 # Máximo de tokens en la respuesta
rebuild: true                    # Reconstruir el índice en cada ejecución de build_index
```

### Personalizar los prompts

Los prompts de cada agente están en `src/prompts/`. Se pueden editar libremente en formato Markdown:

- `orchestrator.md` — Define cómo el orquestador clasifica las consultas
- `rrhh.md` — Define el comportamiento y tono del agente de RRHH
- `finanzas.md` — Define el comportamiento del agente de Finanzas
- `tech.md` — Define el comportamiento del agente de Tech

> Después de modificar un prompt, no hace falta reiniciar nada — el archivo se lee en cada ejecución.

### Agregar documentos al RAG

1. Agregar archivos `.txt` o `.md` a la carpeta correspondiente en `data/`
2. Volver a ejecutar `python -m src.build_index`
3. El sistema ya usa la nueva base de conocimiento

---

## Limitaciones Conocidas

### 1. Sin memoria conversacional
El sistema procesa cada consulta de forma independiente. No recuerda conversaciones anteriores ni el contexto de mensajes previos.

### 2. Routing puede fallar en consultas muy ambiguas
Consultas como "tengo un problema" sin más contexto pueden ser derivadas al departamento incorrecto. El orquestador hace su mejor esfuerzo, pero necesita información suficiente para decidir.

### 3. El RAG depende de la calidad de los documentos
Si las carpetas `data/hr_docs/`, `data/finance_docs/` o `data/tech_docs/` están vacías o con documentos irrelevantes, las respuestas de los agentes especialistas serán genéricas.

### 4. ChromaDB es local
El vector store se guarda en disco en la carpeta `chroma_db/`. No es una solución distribuida ni escalable para producción con múltiples usuarios simultáneos.

### 5. Costos de API de OpenAI
Cada consulta realiza al menos 2 llamadas al LLM (orquestador + agente especialista). Con consultas frecuentes, los costos de API pueden crecer. Se recomienda monitorear el uso desde el dashboard de OpenAI.
