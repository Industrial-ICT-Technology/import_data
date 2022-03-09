from django import forms
from .models import Review


class EmployeeRegistration(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_content']