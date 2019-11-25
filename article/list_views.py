from django.shortcuts import render
from django.core.paginator import PageNotAnInteger,EmptyPage,Paginator
from .models import ArticleColumn,ArticlePost

def article_titles(request):
    article_titles = ArticlePost.objects.all()
    paginator = Paginator(article_titles,2)
    page = request.GET.get('page')