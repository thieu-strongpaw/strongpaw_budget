from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from transactions.models import Transaction, Category
from datetime import datetime, timedelta
from decimal import Decimal
from calendar import month_name

def index(request):
    
    months_of_year = range(1, 13)

    year = request.GET.get('year', datetime.now().year)
    month = request.GET.get('month', datetime.now().month)

    table_1_data_queryset = Category.objects.filter(
        transaction__transaction_date__year=year,
        transaction__transaction_date__month=month,
        ).values(
                'supercategory',
        ).annotate(
                total_budget=Sum('budget_amount'),
                total_spent=Sum('transaction__amount'),
        )

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


    table_1_data_list = [(item['supercategory'], 
                          item['total_budget'].quantize(Decimal("0.01")) or 0, 
                          item['total_spent'].quantize(Decimal("0.01")) or 0, 
                          (item['total_budget'] - item['total_spent']).quantize(Decimal("0.01"))) 
                            for item in table_1_data_queryset]

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

    table_2_data_list = [(supercat, tuple(categories)) for supercat, categories in supercategory_data.items()]
    print(table_2_data_list)
    
    sorted(table_1_data_list, key=lambda item: item[0])

    supercat_name_list = [(item[0]) for item in table_1_data_list]

    context = {
        'table_1_data_list': table_1_data_list,
        'table_2_data_list': table_2_data_list,
        'supercat_name_list': supercat_name_list,
        'months_of_year': months_of_year,
        'month': month,
        'year': year,
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

    queryset_income_vs_expence = Transaction.objects.filter(
            transaction_date__range=(start_date, end_date)
            ).annotate(
                    month=TruncMonth('transaction_date')
            ).values(
                    'month'
            ).annotate(
                    income=Sum('amount', filter=F('category__cost_type') == 'Income'),
                    var_cost=Sum('amount', filter=F('categroy__cost_type') == 'Fixed'),
                    fix_cost=Sum('amount', filter=F('category__cost_type') == 'Variable'),
            ).order_by('month')


    table_1_data = []
    for item in queryset_income_vs_expence:
        month = item['month']
        print(f'month: {month}')
        income = item['income']
        print(f'incom: {income}')
        var_cost = item['var_cost']
        fix_cost = item['fix_cost']
        cost = var_cost + fix_cost
        dif = income - cost
        table_1_data.append((month, income, cost, dif))

    for i in table_1_data: print(i)
            

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'months_of_year': months_of_year,
    }
    
    return render(request, 'reports/incomeVsExpence.html', context)

