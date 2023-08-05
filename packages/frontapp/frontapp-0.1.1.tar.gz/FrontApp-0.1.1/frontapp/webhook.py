import uvicorn
from fastapi import FastAPI

from frontapp import schemas

app = FastAPI()


@app.post("/")
def print_request(message: schemas.IncomingMessage):
    print(message)
    return 201


if __name__ == "__main__":
    uvicorn.run(app)
