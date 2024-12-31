from django.shortcuts import render
from django.db.models import Sum
from transactions.models import Transaction, Category
from datetime import datetime
from decimal import Decimal

def index(request):
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)

    transactions = Transaction.objects.filter(
        transaction_date__year=year,
        transaction_date__month=month
    ).values(
        'category__supercategory',
        'category__name',
        'category__budget_amount',
    ).annotate(total_spent=Sum('amount')).order_by('category__supercategory', 'category__name')

    
    report_data = {supercat[0]: [] for supercat in Category.SUPERCATEGORY_CHOICES}
    totals = {supercat[0]: 0 for supercat in Category.SUPERCATEGORY_CHOICES}

    for txn in transactions:
        supercat = txn['category__supercategory']
        category = txn['category__name']
        total_spent = txn['total_spent'].quantize(Decimal("0.01"))
        budget_amount = txn['category__budget_amount'].quantize(Decimal("0.01"))
        budget_over_under = budget_amount - total_spent
        report_data[supercat].append({'supercat': supercat, 'category': category, 'total_spent': total_spent, 'budget_amount': budget_amount,'budget_over_under' : budget_over_under,})
        totals[supercat] += total_spent

    supercat_totals_list = list(zip(totals.keys(), totals.values()))

    report_data_list = [
        (supercat, report_data[supercat]) for supercat in report_data.keys()
    ]

    # Predefined ranges for templates
    supercategories = [choice[0] for choice in Category.SUPERCATEGORY_CHOICES]
    months = range(1, 13)


    category_by_supercat_list = []
    for supercat, report_data[supercat] in report_data_list:
        temp_list = []
        for item in report_data[supercat]:
            supcat, cat, tot, bud, over_und = item.values()
            cat_tot = (supcat, cat, tot, bud, over_und)
            temp_list.append(cat_tot)
        category_by_supercat_list.append(temp_list) 

    target_positive = "green"
    target_negitive = "red"
    target_color = (target_positive, target_negitive)

    context = {
        'supercat_totals_list': supercat_totals_list,
        'report_data_list': report_data_list,
        'year': year,
        'month': month,
        'supercategories': supercategories,
        'months': months,
        'category_by_supercat_list': category_by_supercat_list,
        'target_color': target_color,
    }
    
    return render(request, 'reports/reports.html', context)

def monthlyReport(request):
    
    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)

    transactions = Transaction.objects.filter(
        transaction_date__year=year,
        transaction_date__month=month
    ).values(
        'category__supercategory',
        'category__name',
        'category__budget_amount',
    ).annotate(total_spent=Sum('amount')).order_by('category__supercategory', 'category__name')

    
    report_data = {supercat[0]: [] for supercat in Category.SUPERCATEGORY_CHOICES}
    totals = {supercat[0]: 0 for supercat in Category.SUPERCATEGORY_CHOICES}

    for txn in transactions:
        supercat = txn['category__supercategory']
        category = txn['category__name']
        total_spent = txn['total_spent'].quantize(Decimal("0.01"))
        budget_amount = txn['category__budget_amount'].quantize(Decimal("0.01"))
        budget_over_under = budget_amount - total_spent
        report_data[supercat].append({'supercat': supercat, 'category': category, 'total_spent': total_spent, 'budget_amount': budget_amount,'budget_over_under' : budget_over_under,})
        totals[supercat] += total_spent

    supercat_totals_list = list(zip(totals.keys(), totals.values()))

    report_data_list = [
        (supercat, report_data[supercat]) for supercat in report_data.keys()
    ]

    # Predefined ranges for templates
    supercategories = [choice[0] for choice in Category.SUPERCATEGORY_CHOICES]
    months = range(1, 13)


    category_by_supercat_list = []
    for supercat, report_data[supercat] in report_data_list:
        temp_list = []
        for item in report_data[supercat]:
            supcat, cat, tot, bud, over_und = item.values()
            cat_tot = (supcat, cat, tot, bud, over_und)
            temp_list.append(cat_tot)
        category_by_supercat_list.append(temp_list) 

    target_positive = "green"
    target_negitive = "red"
    target_color = (target_positive, target_negitive)

    context = {
        'supercat_totals_list': supercat_totals_list,
        'report_data_list': report_data_list,
        'year': year,
        'month': month,
        'supercategories': supercategories,
        'months': months,
        'category_by_supercat_list': category_by_supercat_list,
        'target_color': target_color,
    }
    
    return render(request, 'reports/monthReport.html', context)

