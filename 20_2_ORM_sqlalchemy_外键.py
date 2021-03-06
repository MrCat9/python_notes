# -*- coding: utf-8 -*-
# 摘自 https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0014021031294178f993c85204e4d1b81ab032070641ce5000

from sqlalchemy import Column, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'users'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

    # 一对多:
    books = relationship('Book')


class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))

    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20), ForeignKey('users.id'))


# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/pymysql_test01')
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'

# 创建数据表
Base.metadata.create_all(engine)

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 查询数据
# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id == '5').one()
# 打印类型和对象的name属性:
for book in user.books:
    print('type:', type(book))
    print('name:', book.name)
# 关闭Session:
session.close()


# 当我们查询一个User对象时，该对象的books属性将返回一个包含若干个Book对象的list。
"""
type: <class '__main__.Book'>
name: home
type: <class '__main__.Book'>
name: home2
"""
