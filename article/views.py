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
from traceback import print_exc
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
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
        except Exception as e:
            print_exc(e)
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
            except Exception as e:
                print_exc(e)
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
    articles_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(articles_list,10)  # 10表示每一页，存在10条数据，从article_list返回的所有条目中进行分页
    page = request.GET.get("page")
    try:
        current_page = paginator.page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request,"article/column/article_list.html",{"articles":articles,"page":current_page})


"""
文章详情
"""
@login_required(login_url="accpunt/newlogin/")
def article_detail(reqeust,id,slug):

    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(reqeust,"article/column/article_detail.html",{"article":article})

"""
删除文章列表
"""
@login_required(login_url="account/newlogin/")
@csrf_exempt
@require_POST
def del_article_post(reqeust):
    post_id = reqeust.POST.get("article_id","")
    try:
        article_list = ArticlePost.objects.get(id=post_id)
        article_list.delete()
        return HttpResponse("1")
    except:
        return HttpResponse('0')

@login_required(login_url="account/newlogin/")
@csrf_exempt
def redit_article_post(request,article_id):
    #编辑进入查看
    if request.method == "GET":
        try:
            article_columns = request.user.article_column.all()
            article = ArticlePost.objects.get(id=article_id)
            this_article_form = ArticlePostForm(initial={"title":article.title})
            this_article_column = article.column
            return render(request,"article/column/redit_article.html",{
                "article":article, #文章标题
                "article_columns":article_columns, #栏目类型
                "this_article_form":this_article_form,
                "this_article_column":this_article_column
            })
        except Exception as e:
            print("hello")
            print_exc(e)
            return HttpResponse("2")

    #编辑开始提交
    elif request.method == "POST":
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST["column_id"])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("0")
