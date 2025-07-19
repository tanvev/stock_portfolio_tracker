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

from django.db import models

class Note(models.Model):
    symbol = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.symbol} at {self.created_at}"

class PortfolioSnapshot(models.Model):
    date = models.DateField(auto_now_add=True)
    total_value = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Snapshot on {self.date} - ₹{self.total_value}"

from django.db import models

class Note(models.Model):
    symbol = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note on {self.symbol} at {self.created_at.strftime('%Y-%m-%d')}"
