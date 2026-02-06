from db import base

class user(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,index=True)
    email=Column(String,unique=True,index=True)
    password=Column(String)