import pandas as pd
from pathlib import Path
from .config import Config
from .models import Documento
from .parser import extrair_dados_txt, carregar_validacao, encontrar_pdf


def sanitizar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and format the data before exporting"""
    # remover espaços extras
    df["nome"] = df["nome"].str.replace("\n", " ").str.strip()
    df["caminho_txt"] = df["caminho_txt"].str.replace(str(Config.BASE_DIR), "")
    df["caminho_pdf"] = df["caminho_pdf"].str.replace(str(Config.BASE_DIR), "")
    df.fillna({"caminho_pdf": "N/A"}, inplace=True)
    
    return df


def executar_pipeline():
    documentos = []
    for caminho_txt in Config.RAW_TXT_DIR.glob("*.txt"):
        try:
            dados_txt = extrair_dados_txt(caminho_txt)
            cpf = dados_txt["cpf"].replace(".", "").replace("-", "")
            tipo_doc = dados_txt["tipo_documento"]
            validacao = carregar_validacao(cpf, tipo_doc)
            caminho_pdf = encontrar_pdf(cpf, tipo_doc)
            doc = Documento(
                cpf=cpf,
                nome=dados_txt["nome"],
                tipo_documento=tipo_doc,
                caminho_txt=str(caminho_txt),
                caminho_pdf=caminho_pdf,
                valido=validacao["valido"],
                pontuacao=validacao["pontuacao"]
            )
            documentos.append(doc.__dict__)
        except Exception as e:
            print(f"Error processing {caminho_txt.name}: {str(e)}")

    df = pd.DataFrame(documentos)
    df = sanitizar_dados(df)
    df.to_csv(
        Config.PROCESSED_DIR / "documentos.csv",
        index=False,
        encoding="utf-8",
        quotechar='"',
        escapechar="\\",
        lineterminator="\n",
    )


if __name__ == "__main__":
    executar_pipeline()