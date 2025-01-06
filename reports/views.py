from django.shortcuts import render
from django.db.models import Sum, F, Q, Value, DecimalField
from django.db.models.functions import TruncMonth, Coalesce
from transactions.models import Transaction, Category
from datetime import datetime, timedelta
from decimal import Decimal
from django.db import models


def index(request):
    
    months_of_year = range(1, 13)

    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)

    supercat_names = [choice[0] for choice in Category.SUPERCATEGORY_CHOICES] 

    table_1_data_queryset = Category.objects.filter(
        transaction__transaction_date__year=year,
        transaction__transaction_date__month=month,
        ).values(
                'supercategory',
        ).annotate(
                total_budget=Sum('budget_amount'),
                total_spent=Sum('transaction__amount'),
        )
    print(table_1_data_queryset)

    table_1_data_list = [(item['supercategory'], 
                          item['total_budget'].quantize(Decimal("0.01")) or 0, 
                          item['total_spent'].quantize(Decimal("0.01")) or 0, 
                          (item['total_budget'] - item['total_spent']).quantize(Decimal("0.01"))) 
                            for item in table_1_data_queryset]
    print(table_1_data_list)
    print()
    
    
    supercat_in_list = []
    for item in table_1_data_list:
        name = item[0]
        supercat_in_list.append(name)
    for item in supercat_names:
        if item not in supercat_in_list:
            table_1_data_list.append((item, 0, 0, 0))

    print(table_1_data_list)



    table_2_data_queryset = Category.objects.filter(
        transaction__transaction_date__year=year,
        transaction__transaction_date__month=month,
        ).values(
                'supercategory',
                'name',
                'budget_amount',
        ).annotate(
                total_spent=Sum('transaction__amount'),
                difference=F('budget_amount') - Sum('transaction__amount')
        )




    cat_names = Category.objects.values()

    supercategory_data = {}
    for item in table_2_data_queryset:
        supercategory = item['supercategory']
        category_data = (
                item['name'],
                item['budget_amount'].quantize(Decimal("0.01")),
                item['total_spent'].quantize(Decimal("0.01")),
                item['difference'].quantize(Decimal("0.01")),
                )
        if supercategory not in supercategory_data:
            supercategory_data[supercategory] = []
        supercategory_data[supercategory].append(category_data)

        

    for name in supercat_names:
        if name not in supercategory_data.keys():
            supercategory_data[name] = []
    
    for cat in cat_names:
        if cat['name'] not in supercategory_data[cat['supercategory']]:
            supercategory_data[cat['supercategory']].append((cat['name'], cat['budget_amount'], 0, 0))
            
    table_2_data_list = [(supercat, tuple(categories)) for supercat, categories in supercategory_data.items()]

    context = {
        'table_1_data_queryset': table_1_data_queryset,
        'table_1_data_list': table_1_data_list,
        'table_2_data_list': table_2_data_list,
        'months_of_year': months_of_year,
        'month': month,
        'year': year,
        'supercat_names': supercat_names,
    }
    
    return render(request, 'reports/reports.html', context)

def incomeVsExpence(request):

    today = datetime.today()
    default_start_date = datetime(today.year, 1, 1).date()
    first_of_next_month = datetime(today.year, today.month + 1, 1) if today.month < 12 else datetime(today.year + 1, 1, 1)
    default_end_date = (first_of_next_month - timedelta(days=1)).date()
    
    start_date = request.GET.get('start_date', str(default_start_date))
    end_date = request.GET.get('end_date', str(default_end_date))
    months_of_year = range(1,13)

    income_query = Transaction.objects.filter(
        transaction_date__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('transaction_date')  # Group transactions by month
    ).values(
        'month'
    ).annotate(
        income=Coalesce(Sum('amount', filter=Q(category__cost_type='Income')), Value(0, output_field=DecimalField())),
        cost=Coalesce(
            Sum('amount', filter=Q(category__cost_type__in=['Fixed Cost', 'Variable'])),
            Value(0, output_field=DecimalField())
        ),
        difference=F('income') - F('cost')  # Income minus the combined cost
    ).order_by('month')

    context = {
        'income_query': income_query,
        'start_date': start_date,
        'end_date': end_date,
        'months_of_year': months_of_year,
    }
    
    return render(request, 'reports/incomeVsExpence.html', context)

