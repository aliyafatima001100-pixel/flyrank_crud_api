from fastapi import FastAPI
app = FastAPI(title="Task API", version="1.0")
@app.get("/")
def api_info():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }
@app.get("/health")
def health():
    return {"status": "ok"}