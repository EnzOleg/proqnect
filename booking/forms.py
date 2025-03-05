from django import forms
from .models import Booking

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['problem_description', 'available_times']
        widgets = {
            'problem_description': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Опишите вашу проблему'
            }),
            'available_times': forms.TextInput(attrs={
                'placeholder': 'Например: 2025-03-10 14:00, 2025-03-11 10:00'
            }),
        }

class ConfirmBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['scheduled_time']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
        }
