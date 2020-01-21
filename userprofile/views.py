from django.shortcuts import render,redirect
# Create your views here.
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.decorators import login_required

def user_login(request):

	if request.method == 'POST':
		user_login_form = UserLoginForm(data=request.POST)
		if user_login_form.is_valid():
			data = user_login_form.cleaned_data
			user = authenticate(username=data['username'], password=data['password'])
			if user:
				login(request,user)
				return redirect('my_blog:article_list')
			else:
				return HttpResponse("账号或密码输入。请重新输入~")
		else:
			return HttpResponse("账号或密码输入不合法")
	elif request.method == 'GET':

		user_login_form = UserLoginForm()
		context = { 'form': user_login_form }
		return render(request, 'userprofile/login.html', context)
	else:
		return HttpResponse("请使用GET或POST请求数据")
def user_logout(request):
	logout(request)
	return redirect("my_blog:article_list")

#用户注册
def user_register(request):
	if request.method == 'POST':
		user_register_form = UserRegisterForm(data=request.POST)
		if user_register_form.is_valid():
			new_user = user_register_form.save(commit=False)
			# 设置密码
			new_user.set_password(user_register_form.cleaned_data['password'])
			new_user.save()
			# 保存好数据后立即登录并返回博客列表页面
			login(request, new_user)
			return redirect("my_blog:article_list")
		else:
			return HttpResponse("注册表单输入有误。请重新输入~")
	elif request.method == 'GET':
		user_register_form = UserRegisterForm()
		context = { 'form': user_register_form }
		return render(request, 'userprofile/register.html', context)
	else:
		return HttpResponse("请使用GET或POST请求数据")

@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # 验证登录用户、待删除用户是否相同
        if request.user == user:
            #退出登录，删除数据并返回博客列表
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限。")
    else:
        return HttpResponse("仅接受post请求。")