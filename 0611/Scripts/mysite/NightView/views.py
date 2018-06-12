from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from .models import Food,Nightview,User
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from itertools import chain
from django.contrib import messages
import datetime


# @csrf_exempt
# def index(request):
# 	request.encoding = 'utf-8'
	# foods = Food.objects.filter(create_time__lte=timezone.now()).order_by('create_time')
	# nightviews = Nightview.objects.filter(create_time__lte=timezone.now()).order_by('create_time')
	# return render(request,'index.html',{'foods':foods,'nightviews':nightviews})

@csrf_exempt
def index(request):

    if request.method == "POST":
        firstname = request.POST.get('firstname','')
        lastname = request.POST.get('lastname','')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if firstname == '' and lastname == '':
            if request.user.is_authenticated(): 
                return HttpResponseRedirect('/index/')
            
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/index/')
            else:
                return render(request,'index.html',{'user':user})

        elif firstname != None and lastname != None:
            new_user = User.objects.create_superuser(username, 'admin@example.com', password)
            new_user.first_name=firstname
            new_user.last_name=lastname
            new_user.save()
            return render(request,'index.html')
    else:
        return render(request,'index.html')

def foodmap(request,area=None,ac=None):
    
    foods = Food.objects.filter(area=area).order_by('area')
    a = int(area)

    if a == 0:
        area = "大安區"
    elif a == 1:
        area = "內湖區"
    elif a == 2:
        area = "信義區"
    elif a == 3:
        area = "板橋區" #新
    elif a == 4:
        area = "中正區"
    elif a == 5:
        area = "新店區" #新
    elif a == 6:
        area = "新莊區" #新
    elif a == 7:
        area = "士林區"
    elif a == 8:
        area = "中山區"
    elif a == 100:
        area = "台北市"
        global taipei
        taipei = Q()
        taipei = Q(area=0) | Q(area=1) | Q(area=2) | Q(area=4) | Q(area=7) | Q(area=8)
        foods = Food.objects.filter(taipei).order_by('area')
    elif a == 200:
        area = "新北市"
        global newpei
        newpei = Q()
        newpei = Q(area=3) | Q(area=5) | Q(area=6)
        foods = Food.objects.filter(newpei).order_by('area')
    else:
        area = "美食地圖"
        foods = Food.objects.filter(create_time__lte=timezone.now()).order_by('area')
    
    return render(request,'foodmap.html',{'foods':foods,'area':area})

def add_f(request,id=None,ac=None):
    user = User.objects.get(username=ac)
    previous = Food.objects.get(id=id)
    f_list = user.food.split(",")
    p_area = previous.area

    if id not in f_list:
        p = previous.area
        f = user.food
        f = f + id +","
        ne = user.is_next
        ne = ne + "0" +","
        user.food = f
        user.is_next = ne
        user.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, '已存在於我的行程')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def nightview(request,area=None):
    
    nv = Nightview.objects.filter(area=area).order_by('area')
    a = int(area)
    if a == 0:
        area = "大安區"
    elif a == 1:
        area = "內湖區"
    elif a == 2:
        area = "信義區"
    elif a == 3:
        area = "板橋區" #新
    elif a == 4:
        area = "中正區"
    elif a == 5:
        area = "新店區" #新
    elif a == 6:
        area = "新莊區" #新
    elif a == 7:
        area = "士林區"
    elif a == 8:
        area = "中山區"
    elif a == 100:
        area = "台北市"
        global taipei
        taipei = Q()
        taipei = Q(area=0) | Q(area=1) | Q(area=2) | Q(area=4) | Q(area=7) | Q(area=8)
        nv = Nightview.objects.filter(taipei).order_by('area')
    elif a == 200:
        area = "新北市"
        global newpei
        newpei = Q()
        newpei = Q(area=3) | Q(area=5) | Q(area=6)
        nv = Nightview.objects.filter(newpei).order_by('area')
    else:
        area = "夜遊景點"
        nv = Nightview.objects.filter(create_time__lte=timezone.now()).order_by('area')

    return render(request,'nightview.html',{'nightviews':nv,'area':area})

def add_n(request,id=None,ac=None):
    user = User.objects.get(username=ac)
    previous = Nightview.objects.get(id=id)
    n_list = user.nightview.split(",")
    if id not in n_list:
        p = previous.area
        n = user.nightview
        n = n + id +","
        ne = user.is_next
        ne = ne + "1" + ","
        user.nightview = n
        user.is_next = ne
        user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect('/nightview/'+str(p))

def mytrip(request,ac=None):

    user = User.objects.get(username=ac)
    food_list = user.food.split(",")
    nightview_list = user.nightview.split(",")
    isnext_list = user.is_next.split(",")

    del food_list[-1]
    del nightview_list[-1]
    del isnext_list[-1]

    global a
    a = Q()
    for i in range(0,len(nightview_list)):
        a |= Q(id=nightview_list[i])
    

    global b
    b = Q()
    for s in range(0,len(food_list)):
        b |= Q(id=food_list[s])


    nightviews = Nightview.objects.filter(a)
    foods = Food.objects.filter(b)

    mytrip = list()
    fcount = 0
    ncount = 0

    cost_time = 0
    total_food = len(food_list)
    total_nightview = len(nightview_list)
    for n in nightviews:
        cost_time += n.average_stop_time
    cost_time += total_nightview*10
    cost_time += (total_food)*20
    cost_time -= 1330
    if cost_time < 0:
        cost_time = 0
        for n in nightviews:
            cost_time += n.average_stop_time
        cost_time += total_nightview*10
        cost_time += (total_food)*20
    cost_hour = cost_time//60
    cost_min = cost_time%60

    now = datetime.datetime.now()
    end = datetime.timedelta(hours = int(cost_hour),minutes = int(cost_min))
    lastTime = now + end
    lastYear = lastTime.year
    lastMonth = lastTime.month
    lastDay = lastTime.day
    lastHour = lastTime.hour
    lastMinute = lastTime.minute

    if len(food_list) == 0 and len(nightview_list) == 0:
        cost_time = 0
        cost_min = 0
        cost_hour = 0


    for i in isnext_list:
        if i == "0" and fcount < len(food_list):
            mytrip.append(foods[fcount])
            fcount = fcount + 1
        elif i == "1" and ncount < len(nightview_list):
            mytrip.append(nightviews[ncount])
            ncount = ncount + 1
        elif fcount == len(food_list):
            fcount = fcount - 1
        elif ncount == len(nightview_list):
            ncount = ncount - 1

    return render(request,'mytrip.html',locals())



    

def myway(request,ac=None):
    user = User.objects.get(username=ac)

    return render(request,'myway.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cleantrip(request,ac=None):
    user = User.objects.get(username=ac)
    user.food = ""
    user.nightview = ""
    user.is_next = ""
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
