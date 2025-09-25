from django import forms
from .models import Listing, ListingImage
from django.forms import modelformset_factory

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'condition', 'price', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: MacBook Pro 13inch 2020 - Còn mới 99%'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Mô tả chi tiết sản phẩm...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1.500.000'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Tầng 3, Tòa A'}),
        }

class ListingImageForm(forms.ModelForm):
    class Meta:
        model = ListingImage
        fields = ['image', 'alt_text']

# formset cho nhiều ảnh
ListingImageFormSet = modelformset_factory(
    ListingImage,
    form=ListingImageForm,
    extra=3,
    can_delete=True
)
