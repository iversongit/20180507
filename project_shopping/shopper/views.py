import random
import time

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from shopper.models import Banner, Nav, MustBuy, Shop, MainProducts, UserModel, session


def home(request):
    banner = Banner.objects.all()
    nav = Nav.objects.all()
    mustbuy = MustBuy.objects.all()

    shop_1 = Shop.objects.all()[0]
    shop_2_3 = Shop.objects.all()[1:3]
    shop_4_7 = Shop.objects.all()[3:7]
    shop_8_11 = Shop.objects.all()[7:11]

    mainproducts = MainProducts.objects.all()

    data = {
        "banner":banner,
        "nav":nav,
        "mustbuy":mustbuy,
        "shop_1":shop_1,
        "shop_2_3":shop_2_3,
        "shop_4_7":shop_4_7,
        "shop_8_11":shop_8_11,
        "mainproducts":mainproducts
    }
    return render(request,'home/home.html',data)

def login(request):
    if request.method == "GET":
        return render(request,'user/user_login.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("login-password:",password)
        # 一次只能一个用户登录
        if UserModel.objects.filter(username=username).exists() and not session.objects.all(): #　如果用户名存在
            user = UserModel.objects.get(username=username)
            if password == user.password:  # 验证密码
                s = 'abcdefghijklmnopqrstuvwxyz1234567890'
                ticket = ""
                for i in range(15):
                    # 获取随机的字符串，每次获取一个字符
                    ticket += random.choice(s)
                now_time = int(time.time()) # 1970.1.1到现在的秒数
                ticket_value = 'TK_' + ticket + str(now_time)
                # 绑定令牌到cookie里面
                response = HttpResponseRedirect("/shopapp/home")
                response.set_cookie("ticket",ticket_value,max_age=1000)
                # 存在数据库中
                session.objects.create(
                    session_key="ticket",
                    session_data=ticket_value,
                    u_id=user.id
                )
                # user.ticket = ticket
                # user.save()
                return response
            else:
                return render(request,"user/user_login.html")
        else:
            return render(request,"user/user_login.html")




def regist(request):
    if request.method == "GET":
        return render(request,"user/user_register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("regist-password:",password)
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        if sex == '男':
            sex = 1
        elif sex == '女':
            sex = 0
        icon = request.FILES.get('icon')
        UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            sex=sex,
            icon=icon
        )
        return HttpResponseRedirect("/shopapp/login/")

def logout(request):
    if request.method == "GET":
        response = HttpResponseRedirect("/shopapp/login/")
        ticket = request.COOKIES.get("ticket")
        response.delete_cookie("ticket")
        session.objects.get(session_data=ticket).delete()
        return response