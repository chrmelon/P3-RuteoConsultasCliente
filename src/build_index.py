#######################
# ---- Libraries ---- #
#######################

import yaml
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.logger import get_logger

logger = get_logger(__name__)

SCRIPT_DIR = Path(__file__).parent

PROJECT_ROOT = Path(__file__).parent.parent


def load_documents_from_folder(folder_path: Path):
    documents = []

    for file in folder_path.glob("**/*"):
        if file.suffix in [".txt", ".md"]:
            loader = TextLoader(str(file), encoding="utf-8")
            docs = loader.load()
            documents.extend(docs)

    return documents

def build_domain_index(domain_name: str, data_path: Path, config, embeddings):
    logger = get_logger(__name__)

    logger.info(f"Indexando dominio: {domain_name}")

    docs = load_documents_from_folder(data_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunk_size"],
        chunk_overlap=config["chunk_overlap"],
    )

    chunks = []
    for doc in docs:
        sub_chunks = splitter.split_text(doc.page_content)
        for c in sub_chunks:
            chunks.append(Document(
                                page_content=c,
                                metadata={
                                    "source": doc.metadata.get("source", "unknown"),
                                    "domain": domain_name
                                }
                            )
                        )

    persist_dir = PROJECT_ROOT / "chroma_db" / domain_name

    if config.get("rebuild", True):
        logger.info(f"Eliminando índice previo en {persist_dir}")
        shutil.rmtree(persist_dir, ignore_errors=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=f"{domain_name}_collection",
        persist_directory=str(persist_dir)
    )

    logger.info(f"{domain_name}: {len(chunks)} chunks indexados")

def build_index():
    logger = get_logger(__name__)

    with open(PROJECT_ROOT / "config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    load_dotenv()

    embeddings = OpenAIEmbeddings(model=config["embedding_model"])

    domains = {
        "hr": PROJECT_ROOT / "data" / "hr_docs",
        "tech": PROJECT_ROOT / "data" / "tech_docs",
        "finance": PROJECT_ROOT / "data" / "finance_docs",
    }

    for domain, path in domains.items():
        build_domain_index(domain, path, config, embeddings)

if __name__ == "__main__":
    build_index()