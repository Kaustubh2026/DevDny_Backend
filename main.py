from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from routes import event_routes, weather_routes, recommendation_routes
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Event Planner")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(event_routes.router, prefix="/events", tags=["events"])
app.include_router(weather_routes.router, prefix="/weather", tags=["weather"])
app.include_router(recommendation_routes.router, prefix="/recommendations", tags=["recommendations"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 