import flet as ft
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

def main(page: ft.Page):
    page.add(ft.Text("Hello, World from Flet!"))

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Embed Flet app in an HTML iframe
    return """
        <html>
            <head>
                <title>FastAPI + Flet</title>
            </head>
            <body>
                <h1>FastAPI + Flet Application</h1>
                <iframe src="http://localhost:8550" width="800" height="600"></iframe>
            </body>
        </html>
    """

def run_flet():
    # Run Flet app as a background task
    ft.app(target=main, view=ft.WEB_BROWSER)

if __name__ == "__main__":
    import threading
    import uvicorn

    # Run Flet in a separate thread
    threading.Thread(target=run_flet).start()

    # Run FastAPI with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
