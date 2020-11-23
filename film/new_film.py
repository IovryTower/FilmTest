from django.shortcuts import render, redirect
import random
from film.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from . import models
from .forms import UserForm, RegisterForm
import hashlib
from . import views


def ranking(request):
    # films = views.film_glo
    # films.sort(key=lambda x: x[11], reverse=True)
    films = views.film_sort[:100]
    films.sort(key=lambda x: float(x[11])*float(x[9]), reverse=True)
    content = []
    get = 0
    for f in films:
        if get >= 50:
            break
        get += 1
        lis = list()
        lis.append(str(f[14]))  # id0 poster1 title2 data_main3 score4 num5
        lis.append(str(f[12]))
        lis.append(str(f[0]))
        data_m = str(f[2]) + '/' + str(f[3])
        lis.append(data_m)
        lis.append(str(f[11]))
        lis.append(str(f[9]))
        content.append(lis)

    return render(request, "login/ranking.html", {"h_films": content})


def last_film(request):
    films = views.film_glo
    films.sort(key=lambda x: x[2], reverse=True)
    content = []
    get = 0
    for f in films:
        if get >= 50:
            break
        get += 1
        lis = list()
        lis.append(str(f[14]))  # id0 poster1 title2 data_main3 score4 num5
        lis.append(str(f[12]))
        lis.append(str(f[0]))
        data_m = str(f[2]) + '/' + str(f[3])
        lis.append(data_m)
        lis.append(str(f[11]))
        lis.append(str(f[9]))
        content.append(lis)

    return render(request, "login/last_film.html", {"h_films": content})


def unpopular(request):
    films = views.film_sort[:3000]
    films.sort(key=lambda x: float(x[9]))
    temp = films[:50]
    temp.sort(key=lambda x: float(x[11]), reverse=True)
    content = []
    get = 0
    for f in temp:
        if get >= 50:
            break
        get += 1
        lis = list()
        lis.append(str(f[14]))  # id0 poster1 title2 data_main3 score4 num5
        lis.append(str(f[12]))
        lis.append(str(f[0]))
        data_m = str(f[2]) + '/' + str(f[3])
        lis.append(data_m)
        lis.append(str(f[11]))
        lis.append(str(f[9]))
        content.append(lis)

    return render(request, "login/unpopular.html", {"h_films": content})


def encounter(request):
    films = views.film_glo
    temp = random.sample(films, 50)
    content = []
    get = 0
    for f in temp:
        if get >= 50:
            break
        get += 1
        lis = list()
        lis.append(str(f[14]))  # id0 poster1 title2 data_main3 score4 num5
        lis.append(str(f[12]))
        lis.append(str(f[0]))
        data_m = str(f[2]) + '/' + str(f[3])
        lis.append(data_m)
        lis.append(str(f[11]))
        lis.append(str(f[9]))
        content.append(lis)

    # return render(request, "login/encounter.html", {"h_films": content})
    return render(request, "login/new_counter.html", {"h_films": content})


def high(request):
    films = views.film_glo
    films.sort(key=lambda x: x[11], reverse=True)
    content = []
    get = 0
    for f in films:
        if get >= 50:
            break
        get += 1
        lis = list()
        lis.append(str(f[14]))  # id0 poster1 title2 data_main3 score4 num5
        lis.append(str(f[12]))
        lis.append(str(f[0]))
        data_m = str(f[2]) + '/' + str(f[3])
        lis.append(data_m)
        lis.append(str(f[11]))
        lis.append(str(f[9]))
        content.append(lis)

    return render(request, "login/high.html", {"h_films": content})


def manage(request):
    user_info = list()
    comment_info = list()
    username = ""
    try:
        username = request.session['user_name']
    except KeyError:
        views.register(request)
    if username != "1":
        views.register(request)

    if request.POST:
        single_name = request.POST['single_name']
        del_comments = request.POST['input_comments']
        del_film = request.POST['input_film']
        pass_delete = request.POST['pass_del']  # "123"删除用户；"1234"删除用户评论
        if pass_delete == "123":
            if single_name != "1":
                User_f.objects.filter(name=single_name).delete()
                Comment_f.objects.filter(c_user_name=single_name).delete()
                Score_f.objects.filter(s_user_name=single_name).delete()
                Collection_f.objects.filter(coll_user_name=single_name).delete()

        elif pass_delete == "1234":

            Comment_f.objects.filter(c_user_name=single_name,
                                     c_content_str=del_comments, c_film_title=del_film).delete()
        else:
            pass

    set_manage = {}
    set_manage.setdefault("username", username)

    users_male = User_f.objects.filter()
    for u_m in users_male:
        a_info = list()
        a_info.append(u_m.name)   # 0 名字
        a_info.append(u_m.password)
        a_info.append(u_m.sex)
        a_info.append(u_m.email)
        a_info.append(u_m.user_movie_tag)
        a_info.append(u_m.user_address)
        user_info.append(a_info)
    set_manage.setdefault("user_info", user_info)

    comment_sql = Comment_f.objects.filter()
    for c_m in comment_sql:
        a_info = list()
        a_info.append(c_m.c_content_str)
        a_info.append(c_m.c_user_name)
        a_info.append(c_m.c_film_title)
        a_info.append(c_m.com_time)
        comment_info.append(a_info)
    comment_info.sort(key=lambda x: (x[1]), reverse=True)
    set_manage.setdefault("comment_sql", comment_info)

    return render(request, "login/manage.html", set_manage)

# end
