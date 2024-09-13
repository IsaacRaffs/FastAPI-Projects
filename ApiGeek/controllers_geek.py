from fastapi import APIRouter, status, HTTPException
from models import ProdutosGeekModel
from database import get_engine
from services  import ProdutosGeekService
from dtos import ProdutoDTO, AtualizarEstoqueDTO

#   objeto de rotas
router = APIRouter()

#   objeto de serviço
produto_service = ProdutosGeekService()


@router.get("/{id}")
def get_product_by_id(id: int):
    return produto_service.get_product_by_id(id=id)


@router.get("/")
def products_list(nome: str | None = None, preco: float | None = None, categoria : str | None = None, franquia: str | None = None):
  return produto_service.get_all_products(nome=nome, preco=preco, categoria=categoria, franquia=franquia)


@router.post('/', 
          response_model=ProdutosGeekModel, 
          status_code=status.HTTP_201_CREATED)
def add_product(product: ProdutoDTO):
    novo_produto = ProdutosGeekModel(
                            nome=product.nome,
                            desc=product.desc,
                            preco=product.preco,
                            qtd_estoque=product.qtd_estoque,
                            categoria=product.categoria,
                            franquia=product.franquia
        # nome=product.nome,
        # desc=product.desc,
        # preco=product.preco,
        # qtd_estoque=product.qtd_estoque,
        # categoria=product.categoria,
        # franquia=product.franquia
                            )
    return produto_service.save_product(novo_produto)


@router.put('/{id}')
def update_product(id: int, product: ProdutoDTO):
  db_produto = ProdutosGeekModel(
                            nome=product.nome,
                            desc=product.desc,
                            preco=product.preco,
                            qtd_estoque=product.qtd_estoque,
                            categoria=product.categoria,
                            franquia=product.franquia
                            )
  return produto_service.update_product(product=db_produto, id=id)


@router.put("/estoque/{id}")
def atualizar_estoque(id: int, dds: AtualizarEstoqueDTO):
    produto = produto_service.get_product_by_id(id=id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    try:
        produto_atualizado = produto_service.atualizar_estoque(id=id, dados_estoque=dds)
        return produto_atualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete('/{id}')
def delete_product(id: int):
   return produto_service.delete_product(id=id)