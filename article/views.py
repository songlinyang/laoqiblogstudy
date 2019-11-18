from django.shortcuts import render,reverse
from django.shortcuts import get_object_or_404
from .models import ArticleColumn
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from .models import ArticleColumn
from .models import ArticlePost
from .forms import ArticleColumnForm
from .forms import ArticlePostForm
# Create your views here.

@login_required(login_url="accpunt/newlogin/")
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns,"column_form":column_form})

    if request.method == "POST":
        column_name = request.POST.get("column","")
        if column_name:
            columns = ArticleColumn.objects.filter(user_id=request.user.id,column=column_name)
            if columns:
                return HttpResponse('2')
            else:
                ArticleColumn.objects.create(user=request.user,column=column_name)
                return HttpResponse('1')
        else:
            return HttpResponse("获取表单数据异常")


@login_required(login_url="accpunt/newlogin/")
@csrf_exempt
@require_POST
def rename_article_column(request):
    column_name = request.POST.get("column_name","")
    column_id = request.POST.get("column_id","")
    if column_name and column_id:
        try:
            column = ArticleColumn.objects.filter(user=request.user.id,column=column_name)
            if column:
                return HttpResponse("已存在该栏目，不能新增")
            else:
                line = ArticleColumn.objects.get(id=column_id)
                line.column = column_name
                line.save()
                return HttpResponse('1')
        except:
            return HttpResponse('2')
    else:
       return HttpResponse("不能为空")

@login_required(login_url="accpunt/newlogin/")
@csrf_exempt
@require_POST
def del_article_column(request):
    column_id = request.POST.get("column_id","")
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


@login_required(login_url="accpunt/newlogin/")
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_forms = ArticlePostForm(data=request.POST)
        if article_post_forms.is_valid():
            #前端传回值
            data = article_post_forms.cleaned_data
            print("data{}:",data)

            #对应数据库模板写入值
            try:
                new_article_post_from = article_post_forms.save(commit=False)
                new_article_post_from.author = request.user
                new_article_post_from.column=request.user.article_column.get(id=request.POST["column_id"])
                new_article_post_from.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2") #没有对应的栏目
        else:
            return HttpResponse("3")

    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request,"article/column/article_post.html",{"article_post_form":article_post_form,"article_columns":article_columns})

"""
文章列表
"""
@login_required(login_url="accpunt/newlogin/")
def article_list(request):
    articles = ArticlePost.objects.filter(author=request.user)
    print(articles)
    return render(request,"article/column/article_list.html",{"articles":articles})


"""
文章详情
"""
@login_required(login_url="accpunt/newlogin/")
def article_detail(reqeust,id,slug):

    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(reqeust,"article/column/article_detail.html",{"article":article})
