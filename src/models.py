from dataclasses import dataclass


@dataclass
class Documento:
    cpf: str
    nome: str
    tipo_documento: str
    caminho_txt: str
    caminho_pdf: str
    valido: bool
    pontuacao: float
