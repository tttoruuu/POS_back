from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Product, Transaction, TransactionDetail

app = FastAPI()

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 商品マスタ検索API
@app.get("/api/products/{code}")
def get_product(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.code == code).first()
    if product:
        return {
            "prd_id": product.prd_id,
            "code": product.code,
            "name": product.name,
            "price": product.price
        }
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# 購入API用のPydanticモデル
class Item(BaseModel):
    prd_id: int
    prd_code: str
    prd_name: str
    prd_price: int

class PurchaseRequest(BaseModel):
    emp_cd: str
    store_cd: str
    pos_no: str
    items: List[Item]

# 購入API
@app.post("/api/purchase")
def purchase(req: PurchaseRequest, db: Session = Depends(get_db)):
    total_amt = sum(item.prd_price for item in req.items)
    
    # 取引登録
    transaction = Transaction(
        emp_cd=req.emp_cd,
        store_cd=req.store_cd,
        pos_no=req.pos_no,
        total_amt=total_amt
    )
    db.add(transaction)
    db.flush()  # トランザクションIDを取得するためにフラッシュ
    
    # 取引明細登録
    for item in req.items:
        detail = TransactionDetail(
            trd_id=transaction.trd_id,
            prd_id=item.prd_id,
            prd_code=item.prd_code,
            prd_name=item.prd_name,
            prd_price=item.prd_price
        )
        db.add(detail)
    
    db.commit()
    return {"success": True, "total_amt": total_amt} 