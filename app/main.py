from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Enterprise Multi-Cloud AI DevOps Platform",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/api/health")
async def health():
    return {
        "project": "Enterprise Multi-Cloud AI DevOps Platform",
        "status": "running",
        "version": "1.0.0",
        "message": "Enterprise DevOps Platform is running successfully"
    }