from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import api

# Initialize the app
app = FastAPI()

origins = [
    "http://localhost:3001",
    "localhost:3001"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api.router)


# GET operation at route '/'
@app.get('/')
def root_api():
    return {"message": "Welcome to Todo list"}

# if __name__ == "__main__":
#     uvicorn.run("app.api:app", host = "0.0.0.0", port = 8000, reload = True)