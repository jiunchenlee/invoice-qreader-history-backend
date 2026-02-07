from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.supabase_client import HistoryService
import os

app = FastAPI(title="Invoice History API")

# 全面開放 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

history_service = HistoryService()

@app.get("/")
async def root():
    return {"status": "running", "service": "invoice-history-backend"}

@app.get("/api/invoices")
async def get_invoices(limit: int = 50):
    try:
        data = history_service.get_recent_invoices(limit)
        return {"success": True, "data": data}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": {"message": str(e)}}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
