from sqlalchemy import Column, Integer, String, \
    DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import text

from src.database import Base, metadata


class Transaction(Base):
    __tablename__ = 'Transaction'
    metadata = metadata

    id_product = Column(Integer,
                        ForeignKey(
                            'Product.id_product',
                            ondelete="no action",
                            onupdate="cascade"),
                        primary_key=True, nullable=False)
    login_user = Column(String(50),
                        ForeignKey(
                            'User.login_user',
                            ondelete="no action",
                            onupdate="cascade"
                        ),
                        primary_key=True, nullable=False)
    final_price = Column(Integer, nullable=False)
    trans_datetime = Column(DateTime,
                            server_default=text('CURRENT_TIMESTAMP'))

    __table_args__ = (
        CheckConstraint(
            text('final_price >= 0'),
            name='final_price_check'
        ),
    )
