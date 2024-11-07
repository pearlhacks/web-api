# main.py

import uvicorn
from fastapi import FastAPI
from routes.sheet import sheet_router

app = FastAPI()

# Include the router
app.include_router(sheet_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
