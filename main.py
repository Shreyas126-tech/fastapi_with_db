from fastapi import FastAPI
from routes.user_routes import router as user_router
from db import get_db
from models import base
import os
from sqlalchemy import create_engine
app=FastAPI()

app.include_router(user_router)
if not os.path.exists("./test.db"):
    engine = create_engine(DATABASE_URL)
    base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)
