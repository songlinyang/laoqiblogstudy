from django.urls import path,include
from . import views

app_name="myblog"
urlpatterns = [
    path('',views.index,name="index"),
    path('blog/',views.blog_title,name="blog_title"),
    path('blog/<int:article_id>',views.blog_article,name="blog_article"),
]