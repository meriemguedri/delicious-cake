from django import forms
from .models import Review, Product

class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['text', 'stars']
        widgets = {
            'stars': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text':  forms.Textarea(attrs={'rows': 4}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'description', 'price', 'image',
                  'info_pdf', 'category', 'occasion', 'flavor', 'size']