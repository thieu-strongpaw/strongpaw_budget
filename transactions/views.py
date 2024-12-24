from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import transactions
from transactions.models import Transaction
from transactions.forms import TransactionForm

def index(request):
    PAGES_TO_SHOW = 10

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions_index')
    else:
        form = TransactionForm()

    transactions_list = Transaction.objects.all().order_by('-transaction_date')
    paginator = Paginator(transactions_list, PAGES_TO_SHOW)
    page_number = request.GET.get('page', 1)
    transactions = paginator.get_page(page_number)

    context = {
        "form": form,
        "transactions": transactions,
    }
    
    return render(request, 'transactions/transactions.html', context)
