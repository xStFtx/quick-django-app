import os
from django.http import HttpResponse
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
    query = supabase.table('market_data').select("*")
    if ticker:
        query = query.eq('ticker', ticker)
    if start_date:
        query = query.gte('date', start_date)
    if end_date:
        query = query.lte('date', end_date)
    data = query.execute()
    records = sorted(data.data, key=lambda x: x.get('date', ''), reverse=True)

    # Dynamically determine columns, excluding unwanted fields
    exclude_fields = {'id', 'created_at'}
    columns = []
    if records:
        columns = [k for k in records[0].keys() if k not in exclude_fields]
    filtered_records = [
        {k: v for k, v in record.items() if k in columns}
        for record in records
    ]
    paginator = Paginator(filtered_records, 20)
    page_obj = paginator.get_page(page_number)
    return render(request, 'market_data.html', {
        'page_obj': page_obj,
        'columns': columns,
        'has_results': bool(filtered_records),
    })

@login_required
def market_data_detail(request, pk):
    data = supabase.table('market_data').select("*").eq('id', pk).execute()
    if data.data:
        record = {k: v for k, v in data.data[0].items() if k not in ('id', 'created_at')}
    else:
        record = None
    return render(request, 'market_data_detail.html', {'record': record})