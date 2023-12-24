from sqlalchemy import Column, Integer, String, Date, \
    Float, Text, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.sql import text

from src.database import metadata, Base


class Product(Base):
    __tablename__ = 'Product'
    metadata = metadata

    id_product = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, unique=True)
    creation_date = Column(Date,
                           server_default=text('CURRENT_TIMESTAMP'))
    price = Column(Integer, nullable=False)
    genre = Column(Text, nullable=False)
    vers = Column(Float, nullable=False)
    main_product = Column(Integer,
                          ForeignKey(
                              'Product.id_product',
                              ondelete='no action',
                              onupdate="cascade"
                          ),
                          server_default='0'
                          )
    login_user = Column(String(50),
                        ForeignKey(
                            'User.login_user',
                            ondelete='no action',
                            onupdate="cascade"
                        ),
                        nullable=False)

    __table_args__ = (
        CheckConstraint(
            text(
                'main_product IS NULL OR main_product != id_product'),
            name='check_main_product'
        ),
        CheckConstraint(
            text('price >= 0'),
            name='control_price'
        )
    )
