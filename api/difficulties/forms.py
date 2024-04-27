from django import forms
from .models import Difficulty


class DifficultyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False

    class Meta:
        model = Difficulty
        fields = '__all__'
