from django.shortcuts import render, redirect
# Create your views here.
from .models import ArticlePost
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入栏目Model
from .models import ArticleColumn
# 引入HttpResponse
from django.http import HttpResponse
# 引入User模型
from django.contrib.auth.models import User
# 引入分页模块
from django.core.paginator import Paginator
# 引入 Q 对象
from django.db.models import Q
#引入装饰器
from django.contrib.auth.decorators import login_required
import markdown

def index(request):
	return render(request,'index.html')
def article_list(request):
	#查询文章数量
	num = len(ArticlePost.objects.all())
	search = request.GET.get('search')
	order = request.GET.get('order')
	# 用户搜索逻辑
	if search:
		if order == 'total_view':
			# 用 Q对象 进行联合搜索
			article_list = ArticlePost.objects.filter(
				Q(title__icontains=search) |
				Q(body__icontains=search)
			).order_by('-total_view')
		else:
			article_list = ArticlePost.objects.filter(
				Q(title__icontains=search) |
				Q(body__icontains=search)
			)
	else:
		# 将 search 参数重置为空
		search = ''
		if order == 'total_view':
			article_list = ArticlePost.objects.all().order_by('-total_view')
		else:
			article_list = ArticlePost.objects.all()
	#每页显示一篇文章
	paginator = Paginator(article_list,5)
	page = request.GET.get('page')
	articles = paginator.get_page(page)
	context = {'articles':articles,'order':order,'search':search,'num':num}

	return render(request,'my_blog/list.html',context)

def article_detail(request,id):

	#取出相应的文章
	article = ArticlePost.objects.get(id=id)
	#浏览次数
	#只更新total_view字段
	article.total_view +=1
	article.save(update_fields=['total_view'])
	# 将markdown语法渲染成html样式
	md = markdown.Markdown(
		extensions=[
		# 包含 缩写、表格等常用扩展
		'markdown.extensions.extra',
		# 语法高亮扩展
		'markdown.extensions.codehilite',
		#目录扩展
		'markdown.extensions.toc',
		])
	#需要传递给模板的对象
	article.body = md.convert(article.body)
	context = {'article':article,'toc':md.toc}

	return render(request,'my_blog/detail.html',context)
def article_create(request):

	if request.method == "POST":
		article_post_form = ArticlePostForm(data=request.POST)
		if article_post_form.is_valid():
			new_article = article_post_form.save(commit=False)
			new_article.author = User.objects.get(id=1)
			if request.POST['column'] != 'none':
				new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
			new_article.save()
			return redirect("my_blog:article_list")
		else:
			return HttpResponse("表单内容有误，请重新填写。")
	else:
		article_post_form = ArticlePostForm()
		columns = ArticleColumn.objects.all()
		context = {'article_post_form':article_post_form,'columns':columns}
		return render(request,'my_blog/create.html',context)
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request,id):
	if request.method == 'POST':
		article = ArticlePost.objects.get(id=id)

		article.delete()

		return redirect("my_blog:article_list")
	else:
		return HttpResponse("仅允许post")
@login_required(login_url='/userprofile/login/')
def article_update(request,id):

	article = ArticlePost.objects.get(id=id)
	if request.method == 'POST':
		article_post_form = ArticlePostForm(data=request.POST)
		if article_post_form.is_valid():
			article.title = request.POST['title']
			article.body = request.POST['body']
			if request.POST['column'] != 'none':
				#这一行代码需要详细解释
				article.column = ArticleColumn.objects.get(id=request.POST['column'])
			else:
				article.column = None
			article.save()
			return redirect("my_blog:article_detail",id=id)
		else:
			return HttpResponse("表单内容有误，请重新填写。")
	else:
		article_post_form = ArticlePostForm()
		columns = ArticleColumn.objects.all()
		context = {'article':article,'article_post_form':article_post_form,'columns':columns}
		return render(request, 'my_blog/update.html', context)

