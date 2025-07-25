from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm()
    return render(request, 'portfolio/add_stock.html', {'form': form})


from django.db.models import Q  # Add this at the top


'''def stock_list(request):
    query = request.GET.get('q')  # Get search query
    if query:
        stocks = Stock.objects.filter(
            Q(name__icontains=query) | Q(symbol__icontains=query)
        )
    else:
        stocks = Stock.objects.all()

    return render(request, 'portfolio/stock_list.html', {'stocks': stocks})'''


from django.shortcuts import get_object_or_404, redirect, render
from .models import Stock
from .forms import StockForm

def edit_stock(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)
    return render(request, 'portfolio/edit_stock.html', {'form': form})

def delete_stock(request, symbol):
    Stock.objects.filter(symbol=symbol).delete()
    return redirect('stock_list')






import yfinance as yf
from django.shortcuts import render
from django.db.models import Sum, F, FloatField
from .models import Stock
import json

def stock_list(request):
    stocks = Stock.objects.all()

    query = request.GET.get('q')  # Get search query
    if query:
        stocks = Stock.objects.filter(
            Q(name__icontains=query) | Q(symbol__icontains=query)
        )
    else:
        stocks = Stock.objects.all()

    stock_data = []
    labels = []
    values = []

    # Portfolio-wide stats
    total_invested = stocks.aggregate(
        total=Sum(F('quantity') * F('purchase_price'), output_field=FloatField())
    )['total'] or 0.0

    total_quantity = stocks.aggregate(total=Sum('quantity'))['total'] or 0
    avg_price = round(total_invested / total_quantity, 2) if total_quantity else 0.0

    for stock in stocks:
        try:
            ticker = yf.Ticker(stock.symbol)
            data = ticker.history(period='1d')
            current_price = data['Close'].iloc[-1] if not data.empty else float(stock.purchase_price)
        except:
            current_price = float(stock.purchase_price)

        total_amount_invested = float(stock.purchase_price) * stock.quantity
        total_current_value = current_price * stock.quantity
        gain_loss = total_current_value - total_amount_invested
        percent_change = (gain_loss / total_amount_invested * 100) if total_amount_invested else 0

        labels.append(f"{stock.symbol} (Current Value: {round(total_current_value,2)}, Gain: ₹{round(gain_loss, 2)})")
        values.append(round(stock.quantity))

        stock_data.append({
            'name': stock.name,
            'symbol': stock.symbol,
            'quantity': stock.quantity,
            'purchase_price': stock.purchase_price,
            'total_amount_invested': round(total_amount_invested, 2),
            'purchase_date': stock.purchase_date,
            'current_price': round(current_price, 2),
            'total_current_value': round(total_current_value, 2),
            'gain_loss': round(gain_loss, 2),
            'percent_change': round(percent_change, 2),
        })

    # ✅ Move these out of the loop
    total_current_value = sum(item['total_current_value'] for item in stock_data)
    net_gain_loss = total_current_value - total_invested
    sorted_stocks = sorted(stock_data, key=lambda x: x['gain_loss'])
    top_stock = max(stock_data, key=lambda x: x['gain_loss'], default=None)
    worst_stock = min(stock_data, key=lambda x: x['gain_loss'], default=None)
    daily_change = sum(s['gain_loss'] for s in stock_data)

    # ✅ Proper return context
    return render(request, 'portfolio/stock_list.html', {
        'stocks': stock_data,
        'total_invested': round(total_invested, 2),
        'total_quantity': total_quantity,
        'avg_price': avg_price,
        'labels': json.dumps(labels),
        'values': json.dumps(values),
        'total_current_value': round(total_current_value, 2),
        'net_gain_loss': round(net_gain_loss, 2),
        'top_stock': top_stock,
        'worst_stock': worst_stock,
        'daily_change': round(daily_change,2),
    })



import csv
from django.http import HttpResponse
from .models import Stock

def export_csv(request):
    from django.http import HttpResponse
    import csv
    import yfinance as yf
    from .models import Stock

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="portfolio.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Symbol', 'Quantity', 'Purchase Price',
        'Total Invested', 'Purchase Date',
        'Current Price', 'Current Value', 'Net Gain/Loss'
    ])

    stocks = Stock.objects.all()
    for stock in stocks:
        ticker = yf.Ticker(stock.symbol)
        data = ticker.history(period="1d")
        current_price = data["Close"].iloc[-1] if not data.empty else 0.0

        # Ensure all math is done in float
        purchase_price = float(stock.purchase_price)
        total_invested = float(stock.quantity) * purchase_price
        total_current_value = float(stock.quantity) * current_price
        gain_loss = total_current_value - total_invested

        writer.writerow([
            stock.name,
            stock.symbol,
            stock.quantity,
            f"{purchase_price:.2f}",
            f"{total_invested:.2f}",
            stock.purchase_date,
            f"{current_price:.2f}",
            f"{total_current_value:.2f}",
            f"{gain_loss:.2f}",
        ])

    return response


def export_csv(request):
    from django.http import HttpResponse
    import csv
    import yfinance as yf
    from .models import Stock

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="portfolio.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Name', 'Symbol', 'Quantity', 'Purchase Price',
        'Total Invested', 'Purchase Date',
        'Current Price', 'Current Value', 'Net Gain/Loss'
    ])

    stocks = Stock.objects.all()
    for stock in stocks:
        ticker = yf.Ticker(stock.symbol)
        data = ticker.history(period="1d")
        current_price = data["Close"].iloc[-1] if not data.empty else 0.0

        # Ensure all math is done in float
        purchase_price = float(stock.purchase_price)
        total_invested = float(stock.quantity) * purchase_price
        total_current_value = float(stock.quantity) * current_price
        gain_loss = total_current_value - total_invested

        writer.writerow([
            stock.name,
            stock.symbol,
            stock.quantity,
            f"{purchase_price:.2f}",
            f"{total_invested:.2f}",
            stock.purchase_date,
            f"{current_price:.2f}",
            f"{total_current_value:.2f}",
            f"{gain_loss:.2f}",
        ])

    return response


from django.http import JsonResponse
import yfinance as yf

def get_live_price(request, symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.info.get("regularMarketPrice", None)
        return JsonResponse({'price': live_price})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from django.shortcuts import render, get_object_or_404
from .models import Stock
from .models import Note

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    notes = Note.objects.filter(symbol=symbol).order_by('-created_at')
    #Static dummy data for now

    historical_data = {
        "labels": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
        "prices": [120, 125, 123, 130, 128, 135, 138]
    }
    chart_data = {
        "labels": ["2024-07-01", "2024-07-02", "2024-07-03", "2024-07-04", "2024-07-05"],
        "prices": [150, 152, 149, 153, 155]
    }
    if request.method == "POST":
        content = request.POST.get("note")
        if content:
            Note.objects.create(symbol=symbol, content=content)

    return render(request, "portfolio/stock_detail.html", {
        "stock": stock,
        "notes": notes,
        "labels": historical_data["labels"],
        "prices": historical_data["prices"],
        "symbol": symbol,
        "dummy_data": chart_data,
    })

# views.py
from django.shortcuts import get_object_or_404, redirect
from .models import Note

def delete_note(request, symbol, note_id):
    note = get_object_or_404(Note, id=note_id, symbol=symbol)
    note.delete()
    return redirect('stock_detail', symbol=symbol)

from .models import Note

def add_note(request, symbol):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Note.objects.create(symbol=symbol, content=content)
    return redirect('stock_detail', symbol=symbol)
