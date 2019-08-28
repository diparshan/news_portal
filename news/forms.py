from django import forms
from news.models import News

class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "title", "story", "category", "cover_image"