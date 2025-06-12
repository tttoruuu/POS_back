from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "product_master"

    prd_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)
    name = Column(String(100))
    price = Column(Integer)

class Transaction(Base):
    __tablename__ = "transactions"

    trd_id = Column(Integer, primary_key=True, index=True)
    emp_cd = Column(String(10))
    store_cd = Column(String(10))
    pos_no = Column(String(10))
    total_amt = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    details = relationship("TransactionDetail", back_populates="transaction")

class TransactionDetail(Base):
    __tablename__ = "transaction_detail"

    detail_id = Column(Integer, primary_key=True, index=True)
    trd_id = Column(Integer, ForeignKey("transactions.trd_id"))
    prd_id = Column(Integer)
    prd_code = Column(String(50))
    prd_name = Column(String(100))
    prd_price = Column(Integer)
    
    transaction = relationship("Transaction", back_populates="details") 