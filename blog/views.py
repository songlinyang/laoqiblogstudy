from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse

from blog.models import BlogArticles

# Create your views here.

def index(request):
    return HttpResponse("欢迎进入博客首页，以后这里开始展示内容")


def blog_title(request):
    blogs = BlogArticles.objects.all()
    print("hello",blogs)
    return render(request,"blogs/title.html",{"blogs":blogs})

def blog_article(reqeust,article_id):
    article = get_object_or_404(BlogArticles,id=article_id)
    pub = article.publish
    return render(reqeust,"blogs/content.html",{"article":article,"publish":pub})