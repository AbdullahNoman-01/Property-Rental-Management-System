from django import forms
from .models import CampaignRequest


class CampaignRequestForm(forms.ModelForm):
    class Meta:
        model = CampaignRequest
        fields = [
            'full_name',
            'phone_number',
            'property_location',
            'campaign_package',
            'property_note',
        ]
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'field-input',
                    'placeholder': 'e.g. Abdullah Noman',
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'field-input',
                    'placeholder': '+880 1XXXXXXXXX',
                }
            ),
            'property_location': forms.TextInput(
                attrs={
                    'class': 'field-input',
                    'placeholder': 'e.g. Dhanmondi, Dhaka',
                }
            ),
            'campaign_package': forms.Select(
                attrs={'class': 'field-select'}
            ),
            'property_note': forms.Textarea(
                attrs={
                    'class': 'field-textarea',
                    'rows': 3,
                    'placeholder': (
                        'Tell us about the property '
                        '(e.g. 3-bed flat in Dhanmondi, Rent 35,000 BDT)...'
                    ),
                }
            ),
        }
        labels = {
            'full_name': 'Your Full Name',
            'phone_number': 'Phone Number',
            'property_location': 'Property Location',
            'campaign_package': 'Campaign Budget / Package',
            'property_note': 'Property Description or Note',
        }
