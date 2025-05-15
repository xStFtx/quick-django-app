import os
import csv
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from supabase import create_client, Client
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.forms import CustomUserCreationForm

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def market_data_view(request):
    ticker = request.GET.get('ticker')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort_by', 'date')
    sort_dir = request.GET.get('sort_dir', 'desc')
    export = request.GET.get('export')

    query = supabase.table('market_data').select("*")
    if ticker:
        query = query.eq('ticker', ticker)
    if start_date:
        query = query.gte('date', start_date)
    if end_date:
        query = query.lte('date', end_date)
    data = query.execute()
    records = data.data if data and data.data else []

    # Dynamically determine columns, excluding unwanted fields
    exclude_fields = {'id', 'created_at'}
    columns = []
    if records:
        columns = [k for k in records[0].keys() if k not in exclude_fields]
    filtered_records = [
        {k: v for k, v in record.items() if k in columns}
        for record in records
    ]

    # Dynamic sorting
    if sort_by in columns:
        filtered_records.sort(
            key=lambda x: x.get(sort_by) or "",
            reverse=(sort_dir == 'desc')
        )

    # CSV export
    if export == 'csv' and filtered_records:
        def generate_csv():
            yield ','.join(columns) + '\n'
            for row in filtered_records:
                yield ','.join(str(row.get(col, "")) for col in columns) + '\n'
        response = StreamingHttpResponse(generate_csv(), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="market_data.csv"'
        return response

    paginator = Paginator(filtered_records, 20)
    page_obj = paginator.get_page(page_number)
    return render(request, 'market_data.html', {
        'page_obj': page_obj,
        'columns': columns,
        'has_results': bool(filtered_records),
        'sort_by': sort_by,
        'sort_dir': sort_dir,
    })

@login_required
def market_data_detail(request, pk):
    data = supabase.table('market_data').select("*").eq('id', pk).execute()
    if data.data:
        record = {k: v for k, v in data.data[0].items() if k not in ('id', 'created_at')}
    else:
        record = None
    return render(request, 'market_data_detail.html', {'record': record})