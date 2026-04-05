from django.db import models
from django.conf import settings


class FinancialRecord(models.Model):
    class RecordType(models.TextChoices):
        INCOME  = 'income',  'Income'
        EXPENSE = 'expense', 'Expense'

    class Category(models.TextChoices):
        SALARY      = 'salary',      'Salary'
        INVESTMENT  = 'investment',  'Investment'
        FOOD        = 'food',        'Food'
        RENT        = 'rent',        'Rent'
        UTILITIES   = 'utilities',   'Utilities'
        TRANSPORT   = 'transport',   'Transport'
        HEALTHCARE  = 'healthcare',  'Healthcare'
        OTHER       = 'other',       'Other'

    user        = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='records')
    amount      = models.DecimalField(max_digits=12, decimal_places=2)
    record_type = models.CharField(max_length=10, choices=RecordType.choices)
    category    = models.CharField(max_length=20, choices=Category.choices,
                                   default=Category.OTHER)
    date        = models.DateField()
    notes       = models.TextField(blank=True)
    is_deleted  = models.BooleanField(default=False)   # soft delete
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.record_type} | {self.amount} | {self.date}'