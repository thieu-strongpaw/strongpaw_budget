from django.db import models
from django.utils import choices

class Account(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    FIXED = 'Fixed'
    VARIABLE = "Variable"
    INCOME = 'Income'
    SAVINGS = 'Savings'
    COST_CHOICES = [
        (FIXED, "Fixed Cost"),
        (VARIABLE, "Variable"),
        (INCOME, "Income"),
        (SAVINGS, "SAVINGS"),
    ]

    HOUSING = 'Housing'
    TRANSPORTATION = 'Transportation'
    FOOD = 'Food'
    ENTERTAINMENT = 'Entertainment'
    OTHER = 'Other'
    INCOME = 'Income'
    SUPERCATEGORY_CHOICES = [
        (HOUSING, "Housing"),
        (TRANSPORTATION, "Transportation"),
        (FOOD, "Food"),
        (ENTERTAINMENT, "Entertainment"),
        (OTHER, "Other"),
        (INCOME, "Income"),
    ]

    name = models.CharField(max_length=50, unique=True)
    cost_type = models.CharField(max_length=10, choices=COST_CHOICES, default=VARIABLE)
    supercategory = models.CharField(max_length=20, choices=SUPERCATEGORY_CHOICES, default=OTHER)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"

class Transaction(models.Model):
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_date}, {self.amount}, {self.account}"
