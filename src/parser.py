import re
import json
from pathlib import Path
from src.models import Documento
from .config import Config


def extrair_dados_txt(caminho_txt: Path) -> dict:
    with open(caminho_txt, "r", encoding="utf-8") as f:
        conteudo = f.read()

    padroes = {
        "cpf": r"CPF[\:\s]+([\d\.\-]+)",
        "nome": r"Nome[\:\s]+([A-Za-zÀ-ú\s]+)",
        "tipo_documento": r"Tipo Documento[\:\s]+(\w+)"
    }

    dados = {}
    for campo, regex in padroes.items():
        match = re.search(regex, conteudo)
        dados[campo] = match.group(1).strip() if match else None

    return dados


def carregar_validacao(cpf: str, tipo_doc: str) -> dict:
    caminho_json = Config.VALIDATION_DIR / f"{cpf}_{tipo_doc}.json"
    with open(caminho_json, "r") as f:
        return json.load(f)


def encontrar_pdf(cpf: str, tipo_doc: str) -> str:
    pasta_cpf = Config.DOCUMENTS_DIR / cpf.replace(".", "").replace("-", "")
    for arquivo in pasta_cpf.glob("*.pdf"):
        if tipo_doc.lower() in arquivo.name.lower():
            return str(arquivo)
    return None
