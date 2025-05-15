import os
from rest_framework.views import APIView
from rest_framework.response import Response
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class HelloApiView(APIView):
    def get(self, request):
        return Response({"message": "Hello from the API!"})

class SupabaseDataView(APIView):
    def get(self, request):
        ticker = request.query_params.get('ticker')
        query = supabase.table('market_data').select("*")
        if ticker:
            query = query.eq('ticker', ticker)
        data = query.execute()
        # Optionally, sort by date descending
        records = sorted(data.data, key=lambda x: x.get('date', ''), reverse=True)
        return Response(records)
