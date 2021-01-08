from fastapi import FastAPI

app = FastAPI()

print("Hello")

@app.get("/")
async def root():
    return {"message": "Hello World"}
