from django.shortcuts import render
from .models import ArticleColumn
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/account/newlogin/")
def article_column(request):
    columns = ArticleColumn.objects.filter(user=request.user)
    return render(request,"article/column/article_column.html",{"columns":columns})
