from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Initialize the FastAPI app
app = FastAPI()

# Healthcheck API endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "OK", "message": "Service is running."},
        status_code=200,
    )
