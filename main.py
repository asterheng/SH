import flet as ft
from fastapi import FastAPI
from chainlit.utils import mount_chainlit
import uvicorn


app = FastAPI()

def main(page: ft.Page):
    page.add(ft.Text("Hello, World from Flet!"))
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}

mount_chainlit(app=app, target="app.py", path="/SH")

if __name__ == "__main__":
    # Start Flet in a separate thread
    ft.app(main)
