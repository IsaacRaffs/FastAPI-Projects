from sqlmodel import Field, SQLModel


class ProdutosGeekModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    desc: str 
    preco: float
    qtd_estoque: int
    categoria: str
    franquia: str | None
