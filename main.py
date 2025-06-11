from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

DB_PATH = "pos_app.db"


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
def get_product(code: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT prd_id, code, name, price FROM product_master WHERE code = ?", (code,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "prd_id": row[0],
            "code": row[1],
            "name": row[2],
            "price": row[3]
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
def purchase(req: PurchaseRequest):
    total_amt = sum(item.prd_price for item in req.items)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # 取引登録
    cur.execute(
        "INSERT INTO transactions (emp_cd, store_cd, pos_no, total_amt) VALUES (?, ?, ?, ?)",
        (req.emp_cd, req.store_cd, req.pos_no, total_amt)
    )
    trd_id = cur.lastrowid
    # 取引明細登録
    for item in req.items:
        cur.execute(
            "INSERT INTO transaction_detail (trd_id, prd_id, prd_code, prd_name, prd_price) VALUES (?, ?, ?, ?, ?)",
            (trd_id, item.prd_id, item.prd_code, item.prd_name, item.prd_price)
        )
    conn.commit()
    conn.close()
    return {"success": True, "total_amt": total_amt} 