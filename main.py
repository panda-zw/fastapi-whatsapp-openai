from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "Server is running!"


app.include_router(whatsapp_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
