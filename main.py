import uvicorn
from fastapi import FastAPI
from fastapi.logger import logger

from config.config import read
from core.functions import startup

app = FastAPI(
    title="SyncLink Client API",
    description="Specification of the SyncLink Client API",
    version="0.1.0",
)

# app.include_router(eth_router, prefix='/eth')


@app.on_event("startup")
async def startup_event():
    await startup()

if __name__ == "__main__":
    config = read('config.yaml')

    docs_addr = config['addr'] if config['addr'] != "0.0.0.0" else "127.0.0.1"
    docs_port = config['port']
    docs_line = '=' * 75
    print(docs_line)
    print(
        f"Server starting, find API docs at http://{docs_addr}:{docs_port}/docs")
    print(docs_line)

    uvicorn.run("main:app", host=config['addr'],
                port=config['port'], reload=True)
