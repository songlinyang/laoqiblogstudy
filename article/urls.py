from django.urls import path
from . import views

app_name = "article"
urlpatterns = [
    path('article-column/',views.article_column,name="article_column"),
    path('rename_article_column/',views.rename_article_column,name="rename_article_column"),
    path('delete_article_column/',views.del_article_column,name="del_article_column"),
    path('article-post/',views.article_post,name="article_post"),
    path('article-list/',views.article_list,name="article_list"),
    path('article-detail/<id>/<slug>/',views.article_detail,name="article_detail"),
    path('del-article/',views.del_article_post,name="del_article"),
    path('redit-article/<article_id>/',views.redit_article_post,name="redit_article"),
]