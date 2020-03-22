from django import forms
from .models import todo
class todoForm(forms.ModelForm):
    class Meta:
        model = todo
        fields= ('id', 'title', 'completed')