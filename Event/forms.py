from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'is_private', 'time', 'final_time']
            # Thêm placeholder vào final_time
    # final_time = forms.DateTimeField(
    #     widget=forms.DateTimeInput(attrs={
    #         'placeholder': 'YYYY-MM-DD HH:MM:SS',
    #         'type': 'text'  # hoặc 'datetime-local' tùy thuộc vào nhu cầu
    #     })
    # )
