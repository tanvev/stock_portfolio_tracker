from django import forms
from .models import Stock
from datetime import date

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'symbol', 'quantity', 'purchase_price', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')
        if price <= 0:
            raise forms.ValidationError("Purchase price must be positive.")
        return price

    def clean_purchase_date(self):
        p_date = self.cleaned_data.get('purchase_date')
        if p_date > date.today():
            raise forms.ValidationError("Purchase date cannot be in the future.")
        return p_date