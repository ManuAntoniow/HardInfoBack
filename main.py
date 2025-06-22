from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, products
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API de Favoritos", version="1.0.0")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {"message": "el ping pong pero sin el ping pero si el pong mira: PONG"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
