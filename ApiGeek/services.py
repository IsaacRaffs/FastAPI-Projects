from sqlmodel import Session, select
from sqlalchemy import update
from database import get_engine
from models import ProdutosGeekModel
from fastapi import status, HTTPException
from dtos import ProdutoDTO, AtualizarEstoqueDTO

class ProdutosGeekService():
    def __init__(self):
        engine = get_engine()
        self.session = Session(engine)
  
    def get_product_by_id(self, id: int):
        sttm = select(ProdutosGeekModel).where(ProdutosGeekModel.id==id)
        return self.session.exec(sttm).one_or_none() 
  
    def get_all_products(self, nome: str | None = None, preco: float | None = None, categoria: str | None = None, franquia: str | None = None):
        if nome != None:
            sttm = select(ProdutosGeekModel).where(ProdutosGeekModel.nome==nome)
        elif preco != None:
            sttm = select(ProdutosGeekModel).where(ProdutosGeekModel.preco==preco)
        elif categoria != None:
            sttm = select(ProdutosGeekModel).where(ProdutosGeekModel.categoria==categoria)
        elif franquia != None:
            sttm = select(ProdutosGeekModel).where(ProdutosGeekModel.franquia==franquia)
        else:
            sttm = select(ProdutosGeekModel)
        return self.session.exec(sttm).all()
  
    def save_product(self, product: ProdutosGeekModel):
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def atualizar_estoque(self, id: int, dados_estoque: AtualizarEstoqueDTO):
        produto = self.get_product_by_id(id)
        if not produto:
            raise ValueError("produto não encontrado")
        
        nova_quantidade = produto.qtd_estoque + dados_estoque.quantidade

        if nova_quantidade < 0:
            raise ValueError("não é possível vender mais do que o estoque disponível")

        produto.qtd_estoque = nova_quantidade
        self.session.commit()
        self.session.refresh(produto)
        return produto

    def delete_product(self, id: int):
        produto = self.get_product_by_id(id)
        if produto.qtd_estoque > 0:
            raise HTTPException(status_code=400)
        
        self.session.delete(produto)
        self.session.commit()
        return {"ok": status.HTTP_200_OK}
