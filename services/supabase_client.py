import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

class HistoryService:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_SERVICE_KEY")
        if not self.url or not self.key:
            print("⚠️ SUPABASE_URL or SUPABASE_SERVICE_KEY is missing!")
            self.client = None
        else:
            self.client = create_client(self.url, self.key)

    def get_recent_invoices(self, limit: int = 50):
        if not self.client: return []
        try:
            # 這是最核心、最穩定的查詢語法
            res = self.client.table("invoices").select("*").order("created_at", desc=True).limit(limit).execute()
            return res.data
        except Exception as e:
            print(f"❌ Database Query Error: {e}")
            raise e
