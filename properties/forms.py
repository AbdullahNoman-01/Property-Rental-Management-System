from django import forms
from .models import Property, RentalRequest


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'property_type',
            'location',
            'monthly_rent',
            'bedrooms',
            'bathrooms',
            'image',
            'availability_status',
        ]

class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your message to the property owner...'
            }),
        }