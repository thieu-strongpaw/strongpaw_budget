from django.shortcuts import render
from django.db.models import Sum
from transactions.models import Transaction, Category
from datetime import datetime

def index(request):
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)

    transactions = Transaction.objects.filter(
        transaction_date__year=year,
        transaction_date__month=month
    ).values(
        'category__supercategory',
        'category__name'
    ).annotate(total_spent=Sum('amount')).order_by('category__supercategory', 'category__name')

    report_data = {supercat[0]: [] for supercat in Category.SUPERCATEGORY_CHOICES}
    totals = {supercat[0]: 0 for supercat in Category.SUPERCATEGORY_CHOICES}

    for txn in transactions:
        supercat = txn['category__supercategory']
        category = txn['category__name']
        total_spent = txn['total_spent']
        report_data[supercat].append({'category': category, 'total_spent': total_spent})
        totals[supercat] += total_spent

    totals_list = list(zip(totals.keys(), totals.values()))

    # TODO: this does not quite work. I need to shape the data in such a way that 
    # gets rid of the dic and uses list or tuple.
    #total_data_lst = list(zip(report_data.keys(), report_data.values()))


    report_data_list = [
        (supercat, report_data[supercat]) for supercat in report_data.keys()
    ]

    # Predefined ranges for templates
    supercategories = [choice[0] for choice in Category.SUPERCATEGORY_CHOICES]
    months = range(1, 13)

    context = {
        'totals_list': totals_list,
        'report_data_list': report_data_list,
        'year': year,
        'month': month,
        'supercategories': supercategories,
        'months': months,
    }
    
    return render(request, 'reports/reports.html', context)
