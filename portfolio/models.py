from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    quantity = models.FloatField()
    purchase_price = models.FloatField()
    purchase_date = models.DateField()
    current_price = models.FloatField(null=True, blank=True)  # ✅ Add this field

    def __str__(self):
        return f"{self.name} ({self.symbol})"
