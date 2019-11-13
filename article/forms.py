from .models import ArticleColumn
from .models import ArticlePost
from django import forms

class ArticleColumnForm(forms.ModelForm):

    class Meta:
        model = ArticleColumn
        fields = ("column",)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ("title","body")




