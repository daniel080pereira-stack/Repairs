from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Assistência Técnica - Base de Conhecimento")

# Dados demonstrativos: para produção, substituir por uma base de dados persistente.
ARTIGOS = [
    {
        "id": 1, "aparelho": "Máquina de café", "marca": "Krups", "modelo": "EA8108",
        "titulo": "A máquina não tira café",
        "problema": "A máquina liga, mas não sai café ou sai muito pouco.",
        "palavras_chave": ["não sai café", "pouco café", "bomba", "descalcificação", "obstrução"],
        "resolucao": "Verificar o nível de água e o depósito. Executar o ciclo de descalcificação conforme o manual. Confirmar se os bicos de saída estão obstruídos. Se o problema persistir, encaminhar para diagnóstico da bomba ou do circuito hidráulico."
    },
    {
        "id": 2, "aparelho": "Máquina de café", "marca": "Moulinex", "modelo": "Subito",
        "titulo": "A máquina apresenta fuga de água",
        "problema": "Existe água por baixo ou junto ao depósito.",
        "palavras_chave": ["fuga", "água", "depósito", "vedante", "junta"],
        "resolucao": "Retirar da tomada e verificar se o depósito está corretamente encaixado e sem fissuras. Inspecionar visualmente as juntas acessíveis. Não desmontar componentes elétricos com o aparelho ligado."
    },
    {
        "id": 3, "aparelho": "Torradeira", "marca": "Becken", "modelo": "BT-220",
        "titulo": "A torradeira não aquece",
        "problema": "A alavanca fica em baixo, mas as resistências não aquecem.",
        "palavras_chave": ["não aquece", "resistência", "alavanca", "corrente", "fusível"],
        "resolucao": "Confirmar a tomada e o cabo de alimentação. Com o aparelho desligado da corrente, verificar se existem migalhas a bloquear o mecanismo. Se continuar sem aquecer, encaminhar para verificação técnica das resistências e do circuito de controlo."
    },
    {
        "id": 4, "aparelho": "Varinha mágica", "marca": "Moulinex", "modelo": "Quickchef",
        "titulo": "O motor funciona, mas a lâmina não roda",
        "problema": "O motor faz ruído, mas o acessório não roda corretamente.",
        "palavras_chave": ["lâmina", "não roda", "motor", "acoplamento", "acessório"],
        "resolucao": "Desligar da tomada antes de inspecionar. Retirar e voltar a encaixar o acessório, procurando desgaste ou danos visíveis no acoplamento. Não utilizar se houver cheiro a queimado, ruído anormal ou aquecimento excessivo."
    },
    {
        "id": 5, "aparelho": "Alisador de cabelo", "marca": "Becken", "modelo": "BHS-200",
        "titulo": "O alisador não aquece",
        "problema": "O indicador acende, mas as placas permanecem frias.",
        "palavras_chave": ["não aquece", "placas frias", "temperatura", "indicador", "cabo"],
        "resolucao": "Verificar o cabo e a ficha quanto a danos visíveis e testar uma tomada funcional. Desligar imediatamente se existir cheiro a queimado ou cabo danificado. A verificação interna deve ser feita por técnico qualificado."
    },
]

class NovoArtigo(BaseModel):
    aparelho: str
    marca: str
    modelo: str
    titulo: str
    problema: str
    resolucao: str
    palavras_chave: Optional[List[str]] = []

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/artigos")
def listar_artigos(aparelho: str = "", marca: str = "", modelo: str = "", q: str = ""):
    termos = [t.lower() for t in q.split() if t.strip()]
    resultados = []
    for artigo in ARTIGOS:
        if aparelho and artigo["aparelho"].lower() != aparelho.lower():
            continue
        if marca and artigo["marca"].lower() != marca.lower():
            continue
        if modelo and artigo["modelo"].lower() != modelo.lower():
            continue
        texto = " ".join([
            artigo["titulo"], artigo["problema"], artigo["resolucao"],
            " ".join(artigo.get("palavras_chave", []))
        ]).lower()
        if termos and not any(t in texto for t in termos):
            continue
        resultados.append(artigo)
    return resultados

@app.post("/api/artigos")
def criar_artigo(novo: NovoArtigo):
    artigo = novo.model_dump()
    artigo["id"] = max([a["id"] for a in ARTIGOS], default=0) + 1
    ARTIGOS.append(artigo)
    return {"ok": True, "artigo": artigo}
