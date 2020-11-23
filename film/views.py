from django.shortcuts import render, redirect
from film.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from . import models
from .forms import UserForm, RegisterForm
import hashlib

import random


def film_all_data_list():
    set_id = 7000
    list_one = []

    for i in range(2, set_id):
        try:
            result = Data.objects.get(id=i)
            list_two = list()
            list_two.append(result.fl_title_str)
            list_two.append(result.fl_type_str)
            list_two.append(result.fl_data_str)
            list_two.append(result.fl_mainRole_str)
            list_two.append(result.fl_anotherName_str)
            list_two.append(result.fl_director_str)
            list_two.append(result.fl_scenarist_str)
            list_two.append(result.fl_length_str)
            list_two.append(result.fl_language_str)
            list_two.append(result.fl_commentNum)
            list_two.append(result.fl_replyNum)
            list_two.append(result.fl_grade)

            list_two.append(result.fl_id_poster)
            list_two.append(result.fl_intro)

            list_two.append(i)

            list_one.append(list_two)

            #                 '电影名称'0, '类型': 1, '发布日期' 2
            #                 '主演': 3 '另一个名字（又名）': 4
            #                 '导演':5, '编辑': 6, '片长':7
            #                 '语言': 8 '评论数': 9, '回评数': 10
            #                 '评分': 11
            #                 海报id(12)  简介（13） id(14)

        except ObjectDoesNotExist:
            i += 1
    return list_one


film_glo = film_all_data_list()
film_sort = sorted(film_glo, key=lambda x: x[11], reverse=True)


def take_second(elem):
    return elem[1]


def film_all_data():
    set_id = 3000
    arr = []
    for i in range(1, set_id):
        try:
            result = Data.objects.get(id=i)
            content = {
                '电影名称': result.fl_title_str, '类型': result.fl_type_str, '发布日期': result.fl_data_str,
                '主演': result.fl_mainRole_str, '另一个名字（又名）': result.fl_anotherName_str,
                '导演': result.fl_director_str, '编辑': result.fl_scenarist_str, '片长': result.fl_length_str,
                '语言': result.fl_language_str, '评论数': result.fl_commentNum, '回评数': result.fl_replyNum,
                '评分': result.fl_grade
            }
            arr.append(content)
        except ObjectDoesNotExist:
            pass
    return arr


def hell(request):
    return HttpResponse("Hello, world. You're at the Hello index.")


def search_film(request):

    return render(request, "MyTest.html",  locals())


def search(request):
    request.encoding = 'utf-8'
    arr = []
    out_list = []
    if 'T_search' in request.GET and request.GET['T_search']:
        text = request.GET['T_search']
        arr = fun_search2(text)

    for a_film_list in arr:
        concrete_film = {}
        if a_film_list:
            concrete_film_dict = a_film_list
            temp_film_title = concrete_film_dict["电影名称"]
            temp_film_grade = concrete_film_dict["评分"]
            temp_film_type = concrete_film_dict["类型"]
            temp_text = concrete_film_dict["简介"][:30]+"..."
            temp_film_synopsis = "剧情简介：" + temp_text
            concrete_film.setdefault('film_title', temp_film_title)  # 电影名称
            if not temp_film_grade:
                temp_film_grade = "5.6"
            concrete_film.setdefault('film_grade', temp_film_grade)  # 评分
            concrete_film.setdefault('film_type', temp_film_type)  # 类型
            concrete_film.setdefault('film_synopsis', temp_film_synopsis)  # 剧情简介
            concrete_film.setdefault('poster_id', concrete_film_dict["海报"])  #
            concrete_film.setdefault('id', concrete_film_dict["id"])  #
            concrete_film.setdefault('film_href', "?film_get=" + str(concrete_film_dict["id"]) + "#" + "")  #

            temp_tag_list = get_film_tag(temp_film_type)  # 获取具体的标签
            for tag_num in range(0, len(temp_tag_list)):
                concrete_film.setdefault('film_concrete_tag' + str(tag_num + 1), temp_tag_list[tag_num])

            temp_main_list = get_film_tag(concrete_film_dict["主演"])
            for main_num in range(0, len(temp_main_list)):
                concrete_film.setdefault('film_concrete_main' + str(main_num + 1), temp_main_list[main_num])

            temp_director_list = get_film_tag(concrete_film_dict["导演"])
            for di_num in range(0, len(temp_director_list)):
                concrete_film.setdefault('film_director' + str(di_num + 1), temp_director_list[di_num])

            temp_scenarist_list = get_film_tag(concrete_film_dict["编辑"])
            for sc_num in range(0, len(temp_scenarist_list)):
                concrete_film.setdefault('film_scenarist' + str(sc_num + 1), temp_scenarist_list[sc_num])
        out_list.append(concrete_film)

    return render(request, 'results.html', {"out_list": out_list},)


def fun_search(get_text):
    arr = []
    try:
        # result = Data.objects.get(fl_title_str=get_text)
        result = Data.objects.get(id=get_text)
        content = {
            '电影名称': result.fl_title_str, '类型': result.fl_type_str, '发布日期': result.fl_data_str,
            '主演': result.fl_mainRole_str, '另一个名字（又名）': result.fl_anotherName_str,
            '导演': result.fl_director_str, '编辑': result.fl_scenarist_str, '片长': result.fl_length_str,
            '语言': result.fl_language_str, '评论数': result.fl_commentNum, '回评数': result.fl_replyNum,
            '评分': result.fl_grade, '海报id': result.fl_id_poster, '简介': result.fl_intro
              }
        arr.append(content)
    except ObjectDoesNotExist:
        pass

    return arr


def fun_search2(get_text):
    arr = []
    # 通过电影相关任何信息查找
    for i in range(0, len(film_glo)):
        # 通过电影相关任何信息查找get_text in film[i]..  模糊查询:
        if (get_text in film_glo[i][0]) or (get_text in film_glo[i][1]) or \
                (get_text in film_glo[i][2]) or (get_text in film_glo[i][3]) or\
                (get_text in film_glo[i][4]) or (get_text in film_glo[i][5]) or\
                (get_text in film_glo[i][6]) or (get_text in film_glo[i][8])or (get_text in film_glo[i][12]):
            content = {
                '电影名称': film_glo[i][0], '类型': film_glo[i][1], '发布日期': film_glo[i][2],
                '主演': film_glo[i][3], '另一个名字（又名）': film_glo[i][4],
                '导演': film_glo[i][5], '编辑': film_glo[i][6], '片长': film_glo[i][7],
                '语言': film_glo[i][8], '评论数': film_glo[i][9], '回评数': "0",
                '评分': film_glo[i][11], '海报': film_glo[i][12], 'id': film_glo[i][14],
                '简介': film_glo[i][13],
            }
            arr.append(content)

        if get_text == "全部分类" or get_text == "全部地区" or \
                get_text == "全部年代" or get_text == "全部标签":
            content = {
                '电影名称': film_glo[i][0], '类型': film_glo[i][1], '发布日期': film_glo[i][2],
                '主演': film_glo[i][3], '另一个名字（又名）': film_glo[i][4],
                '导演': film_glo[i][5], '编辑': film_glo[i][6], '片长': film_glo[i][7],
                '语言': film_glo[i][8], '评论数': film_glo[i][9], '回评数': "0",
                '评分': film_glo[i][11], '海报': film_glo[i][12], 'id': film_glo[i][14],
                '简介': film_glo[i][13],
            }
            arr.append(content)

    return arr


def get_film_tag(a_type_str):
        get_str = a_type_str
        get_tag_list = []
        if get_str:
            tag_temp = get_str.split(' ')
            for i in range(0, len(tag_temp)):
                str_tag_temp = str(tag_temp[i])
                none_space = str_tag_temp.strip()  # 去除为空格. 去除头空格
                get_tag_list.append(none_space)
        return get_tag_list


def film_list_a_type(get_type):
    arr_film_action = fun_search2(get_type)  # 类型： 动作 action
    film_action_all = []

    len_film_action = len(arr_film_action)
    if len_film_action > 50:
        len_film_action = 50
    for i in range(0, len_film_action):
        temp_action_name = str(arr_film_action[i]['电影名称'])  # str
        temp_action_grade = "评分：" + str(arr_film_action[i]['评分'])  # str
        temp_action_tag = get_film_tag(arr_film_action[i]["类型"])  # list
        if len(temp_action_name) > 6:
            temp_action_name = temp_action_name[0:6] + "..."
        if not str(arr_film_action[i]['评分']):
            temp_action_grade = "评分：暂无"
        film_content = {}
        film_content.setdefault('film_action_name', temp_action_name)
        film_content.setdefault('film_action_grade', temp_action_grade)
        film_content.setdefault('film_action_title', "http://amefilm1.pythonanywhere.com/film_info/?film_get=" +
                                str(arr_film_action[i]['电影名称']))

        for j in range(0, len(temp_action_tag)):
            film_content.setdefault('film_action_tag' + str(j + 1), temp_action_tag[j])
        film_action_all.append(film_content)

    return film_action_all


def film_type(request):
    # "film_terror"  "film_comedy" {"film_comedy": "class=active"}
    # {%  extends 'base.html' %}

    film_all_list = list()
    # 动作 爱情 悬疑 惊悚 喜剧 动画 灾难 古装 其他
    str_type = ["动作", "爱情", "悬疑", "惊悚", "喜剧", "动画", "灾难", "古装"]
    for i in range(0, len(str_type)):
        list_type_content = list()
        film_list_temp = film_list_a_type(str_type[i])  # list 0-50 ?

        temp_page1 = list()

        list_type_content.append(str_type[i])    # 0
        list_type_content.append("#collapse"+str(i))  # 1
        list_type_content.append("collapse"+str(i))  # 2
        temp_slice = list()
        for index_one in range(0, len(film_list_temp)):
            if (index_one % 9) == 0:
                temp_set_page_open = "tab-pane fade"  # 不打开
                if index_one == 0:
                    temp_set_page_open = "tab-pane fade in active"  # 打开
                temp_slice.append([film_list_temp[index_one:index_one+9], "action" +
                                  str(i)+str(index_one), temp_set_page_open])
                # 取出 0[0,9)  1[9,18)    2[18,27)    3[27,36)    4[36,45)
                str_page_name = str(int((index_one/9)+1))
                temp_page1.append(["#action" + str(i)+str(index_one), str_page_name])

        list_type_content.append(temp_slice)   # 3
        list_type_content.append(temp_page1)   # 4
        # list_type_content.append(temp_page        2)  # 5

        # rgb1 = random.randint(10, 99)
        # rgb2 = random.randint(10, 99)
        # rgb3 = random.randint(10, 99)
        # list_type_content.append("background: #99"+str(rgb2)+str(rgb3))  # 10 "background: #d9534f" 红色

        film_all_list.append(list_type_content)

    return render(request, "films.html", {"film_all_list": film_all_list})


def film_info(request):
    request.encoding = 'utf-8'
    concrete_film = {}       # 一个具体电影的dict
    concrete_film_list = []  # 一个具体电影的list
    concrete_yes = False     # 一个具体电影是否含有评论
    temp_film_title = ""     # 一个具体电影的名字
    com_list = []            # 一个具体电影的的一个具体评论的相关list
    try:
        str_user_name = request.session['user_name']
    except KeyError:
        return register(request)
    # str_user_name = request.session['user_name']  # 当前用户的用户名
    url_get_text = ""
    # film_get_score = ""
    # url_get_text = ""        # 一个具体电影的url打开时获得的title
    # com_get = ""              # 一个具体电影的被用户评论的一条内容

    # concrete_film = film[1]
    if request.method == 'GET':
        if 'film_get' in request.GET and request.GET['film_get']:
            url_get_text = request.GET['film_get']
        else:
            url_get_text = "No Film"
        # concrete_film_list = fun_search(url_get_text)
        concrete_film_list = fun_search(url_get_text)

    if concrete_film_list:
        concrete_yes = True
        concrete_film_dict = concrete_film_list[0]
        temp_film_title = concrete_film_dict["电影名称"]
        temp_film_grade = concrete_film_dict["评分"]
        temp_film_type = concrete_film_dict["类型"]
        temp_text = concrete_film_dict["简介"]
        poster_id = concrete_film_dict["海报id"]
        temp_film_synopsis = "剧情简介：" + temp_text
        concrete_film.setdefault('film_title', temp_film_title)  # 电影名称
        if not temp_film_grade:
            temp_film_grade = "5.6"
        concrete_film.setdefault('film_grade', temp_film_grade)  # 评分
        concrete_film.setdefault('film_type', temp_film_type)    # 类型
        concrete_film.setdefault('film_synopsis', temp_film_synopsis)  # 剧情简介
        concrete_film.setdefault("html_film_poster", poster_id)
        concrete_film.setdefault("html_id", url_get_text)

        temp_tag_list = get_film_tag(temp_film_type)  # 获取具体的标签
        for tag_num in range(0, len(temp_tag_list)):
            concrete_film.setdefault('film_concrete_tag' + str(tag_num + 1), temp_tag_list[tag_num])

        temp_main_list = get_film_tag(concrete_film_dict["主演"])
        for main_num in range(0, len(temp_main_list)):
            concrete_film.setdefault('film_concrete_main' + str(main_num + 1), temp_main_list[main_num])

        temp_director_list = get_film_tag(concrete_film_dict["导演"])
        for di_num in range(0, len(temp_director_list)):
            concrete_film.setdefault('film_director' + str(di_num + 1), temp_director_list[di_num])

        temp_scenarist_list = get_film_tag(concrete_film_dict["编辑"])
        for sc_num in range(0, len(temp_scenarist_list)):
            concrete_film.setdefault('film_scenarist' + str(sc_num + 1), temp_scenarist_list[sc_num])

    if request.method == 'POST':
            com_get = ""
            url_film = ""
            url_film_score = ""
            url_film_title = ""
            film_get_score = ""
            if request.POST.get('comment_content'):
                com_get = request.POST.get('comment_content')
            if request.POST.get('film_title'):
                url_film = request.POST.get('film_title')
            if request.POST.get('film_title_score'):
                url_film_score = request.POST.get('film_title_score')
            if request.POST.get('film_title_coll'):
                url_film_title = request.POST.get('film_title_coll')
            if request.POST.get('score'):
                film_get_score = request.POST.get('score')

            try:
                url_temp = ''
                if len(com_get) > 2:
                    add_com = Comment_f()
                    add_com.c_film_title = url_film
                    add_com.c_user_name = str_user_name
                    add_com.c_content_str = com_get
                    add_com.save()
                    url_temp = url_film

                if film_get_score:
                    add_score = Score_f()
                    add_score.s_film_title = url_film_score
                    add_score.s_user_name = str_user_name
                    add_score.s_score_str = film_get_score
                    add_score.save()
                    url_temp = url_film_score

                if url_film_title:
                    add_coll = Collection_f()
                    add_coll.coll_film_title = url_film_title
                    add_coll.coll_user_name = str_user_name
                    add_coll.save()
                    url_temp = url_film_title

                # return redirect("http://amefilm1.pythonanywhere.com//film_info/?film_get=" + url_temp)
                print(url_temp)
                return redirect("../film_info/?film_get=" + url_temp)
            except ObjectDoesNotExist:
                print("error123")

    # 获得评论：
    if concrete_yes:
        sql_com = Comment_f.objects.filter(c_film_title=url_get_text)
        for i in sql_com:
            href_to_see = "../others_page/?tade_name="+i.c_user_name
            if i.c_user_name == request.session['user_name']:
                href_to_see = "../user_page/"
            content = {'film_title': i.c_film_title, 'user_name': i.c_user_name, 'com_time': i.com_time,
                       "content_str": i.c_content_str, "other_href": href_to_see}
            com_list.append(content)
        concrete_film.setdefault("all_com", com_list)
        concrete_film.setdefault("com_length", str(len(com_list)))

    #  获取当前用户是否评分该电影，并加载
    sql_score = Score_f.objects.filter(s_user_name=str_user_name)
    for score_i in sql_score:
        if score_i.s_film_title == url_get_text:
            concrete_film.setdefault("html_to_score", score_i.s_score_str)
            break

    sql_coll = Collection_f.objects.filter(coll_user_name=str_user_name)
    for score_i in sql_coll:
        if score_i.coll_film_title == url_get_text:
            concrete_film.setdefault("html_to_coll", "已收藏")
            break

    list_like_film = push_fur(url_get_text, str_user_name)
    list_like_film = list(set(list_like_film))
    concrete_film.setdefault("html_film_like_list", list_like_film[:12])

    return render(request, "film_info.html",  {"concrete_film_view": concrete_film})


def index(request):
    content = []
    get = 0
    film_get = film_sort[:200]
    film_rand = random.sample(film_get, 30)
    for f in film_rand:
        if get >= 12:
            break
        lis = list()
        lis.append(str(f[14]))  # id0 poster1 title2 data_main3 score4 num5 i6
        lis.append(str(f[12]))
        lis.append(str(f[0])[:7])
        content.append(lis)
        get += 1
    return render(request, 'login/index.html', {"film_rand": content})


def login(request):
    if request.session.get('is_login', None):
        return redirect(".././")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User_f.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['user_sex'] = user.sex
                    request.session['user_personal'] = user.user_personal
                    request.session['user_pic'] = user.user_pic
                    request.session['user_movie_tag'] = user.user_movie_tag
                    request.session['user_address'] = user.user_address
                    request.session['user_c_time'] = user.c_time
                    return redirect('.././')
                else:
                    message = "密码不正确！"
            except ObjectDoesNotExist:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User_f.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User_f.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User_f.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('.././login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('.././')
    request.session.flush()

    return redirect('.././')


def search2(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入搜索电影的关键词'
        return render(request, 'results.html', locals())
    else:
        return render(request, 'results.html', locals())


def others_page(request):
    if request.method == "GET":
        username = request.GET['tade_name']
        user = models.User_f.objects.get(name=username)
        request.session['tade_id'] = user.id
        request.session['tade_name'] = user.name
        request.session['tade_sex'] = user.sex
        request.session['tade_personal'] = user.user_personal
        request.session['tade_pic'] = user.user_pic
        request.session['tade_movie_tag'] = user.user_movie_tag
        request.session['tade_c_time'] = user.c_time
        return render(request, 'login/otherPage.html', locals())
    return render(request, 'login/otherPage.html', locals())


def user_page(request):
    username = ""
    try:
        username = request.session['user_name']
    except KeyError:
        register(request)

    # if username == "1":
    #     return render(request, 'login/manage.html')

    edit = models.User_f.objects.get(name=username)
    edit_temp = 0
    edit_personal = ""
    edit_movie_tag = ""
    edit_address = ""
    edit_user_pic = ""
    user_to_html_dict = {}
    all_user_com_list = []
    list_film_like = []

    com_user_get = Comment_f.objects.filter(c_user_name=username)  # 获取当前用户的评论

    coll_int = 1
    for i_com in com_user_get:
        temp_time_str = str(i_com.com_time).split(".")
        user_film = Data.objects.get(id=i_com.c_film_title)
        content = {"c_user_name": i_com.c_user_name, "c_content_str": i_com.c_content_str,
                   "c_film_title": user_film.fl_title_str, "com_time": temp_time_str[0],
                   "collapse": "collapse"+str(coll_int), "id": i_com.c_film_title,
                   }
        coll_int += 1
        all_user_com_list.append(content)
    user_to_html_dict.setdefault("all_user_com_list", all_user_com_list)
    user_to_html_dict.setdefault("username", username)

    get_user_coll = Collection_f.objects.filter(coll_user_name=username)
    for film_a_film in get_user_coll:
        temp_id = film_a_film.coll_film_title
        user_film = Data.objects.get(id=temp_id)
        list_film_like.append([temp_id, user_film.fl_title_str[:10]+"...", user_film.fl_id_poster])
    user_to_html_dict.setdefault("film_collection", list_film_like)

    if request.method == "POST":
        check_box_list = request.POST.getlist("check_box_list")
        for str_tag in check_box_list:
            if not edit_movie_tag:
                edit_movie_tag += str_tag
            else:
                edit_movie_tag += " " + str_tag
        edit.user_movie_tag = edit_movie_tag
        request.session['user_movie_tag'] = edit_movie_tag
        edit.save()

    if request.method == "GET":
        if 'edit_personal' in request.GET and request.GET['edit_personal']:
            edit_personal = request.GET['edit_personal']
            edit_temp = 1
        elif 'edit_movie_tag' in request.GET and request.GET['edit_movie_tag']:
            edit_movie_tag = request.GET['edit_movie_tag']
            edit_temp = 2
        elif 'edit_address' in request.GET and request.GET['edit_address']:
            edit_address = request.GET['edit_address']
            edit_temp = 3
        elif 'edit_user_pic' in request.GET and request.GET['edit_user_pic']:
            edit_user_pic = request.GET['edit_user_pic']
            edit_temp = 4

        if edit_temp == 1 and edit_personal:  # 获取数据
            edit.user_personal = edit_personal
            request.session['user_personal'] = edit_personal
            edit.save()
            return render(request, 'login/userPage.html', user_to_html_dict)
        elif edit_temp == 2 and edit_movie_tag:
            edit.user_movie_tag = edit_movie_tag
            request.session['user_movie_tag'] = edit_movie_tag
            edit.save()
            return render(request, 'login/userPage.html', user_to_html_dict)
        elif edit_temp == 3 and edit_address:
            edit.user_address = edit_address
            request.session['user_address'] = edit_address
            edit.save()
            return render(request, 'login/userPage.html', user_to_html_dict)
        elif edit_temp == 4 and edit_user_pic:
            edit.user_pic = edit_user_pic
            request.session['user_pic'] = edit_user_pic
            edit.save()
            return render(request, 'login/userPage.html', user_to_html_dict)
        else:
            return render(request, 'login/userPage.html', user_to_html_dict)

    return render(request, 'login/userPage.html', user_to_html_dict)


def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def push(str_user_name):
    this_user = User_f.objects.filter(name=str_user_name).first()
    movies = []
    index_s = []
    result = []
    user_tags = []
    if this_user.user_movie_tag:
        user_tags = get_film_tag(this_user.user_movie_tag)

    for user_tag in user_tags:
        temps = FilmTag_f.objects.filter(ft_tag=user_tag)
        if movies:
            for temp in temps:
                if temp.ft_title in movies:
                    index_s[movies.index(temp.ft_title)] += 1
                else:
                    movies.append(temp.ft_title)
                    index_s.append(1)
        else:
            for temp in temps:
                movies.append(temp.ft_title)
                index_s.append(1)
    for movie in movies:
        grade = ""
        for film_temp in film_glo:
            if film_temp[0] == movie:
                grade = film_temp[11]
                break
        if grade:
            result.append((movie, index_s[movies.index(movie)]+float(grade)*0.52))
        else:
            result.append((movie, index_s[movies.index(movie)] + 5.6 * 0.52))
    result.sort(key=take_second, reverse=True)

    return result[:10]


#  text_film 电影名, str_user_name当前用户名
def push_fur(text_film, str_user_name):
    result = []
    # 收藏这个电影的用户list
    users_coll = Collection_f.objects.filter(coll_film_title=text_film)
    for user_coll in users_coll:
        # 这个用户收藏的一些电影list
        user_collections = Collection_f.objects.filter(coll_user_name=user_coll.coll_user_name)
        for user_collection in user_collections:
            if user_collection.coll_user_name == str_user_name:
                pass
            else:
                result.append(user_collection.coll_film_title)

    return result


def recommend(request):
    try:
        str_user_name = request.session['user_name']
    except KeyError:
        return register(request)
    # str_user_name = request.session['user_name']  # 当前用户的用户名
    rec_film = push(str_user_name)
    out_list = []
    arr = []
    list_rec_score = []

    for film_get in rec_film:
        temp_film_dict = fun_search2(film_get[0])
        list_rec_score.append(str(int(film_get[1])))
        arr.append(temp_film_dict[0])

    for i_num in range(0, len(arr)):
        concrete_film = {}
        if arr[i_num]:
            concrete_film_dict = arr[i_num]
            temp_film_title = concrete_film_dict["电影名称"]
            temp_film_grade = concrete_film_dict["评分"]
            temp_film_type = concrete_film_dict["类型"]
            temp_text = concrete_film_dict["简介"]
            temp_film_synopsis = "剧情简介：" + temp_text
            concrete_film.setdefault('film_title', temp_film_title)  # 电影名称
            if not temp_film_grade:
                temp_film_grade = "5.6"
            concrete_film.setdefault('film_grade', temp_film_grade)  # 评分
            concrete_film.setdefault('film_type', temp_film_type)  # 类型
            concrete_film.setdefault('film_synopsis', temp_film_synopsis)  # 剧情简介
            concrete_film.setdefault('film_href', "?film_get=" + str(concrete_film_dict["id"]) + "#" + "")
            concrete_film.setdefault('rec_score', list_rec_score[i_num])
            concrete_film.setdefault('poster_id', concrete_film_dict["海报"])
            concrete_film.setdefault('id', concrete_film_dict["id"])

            temp_tag_list = get_film_tag(temp_film_type)  # 获取具体的标签
            for tag_num in range(0, len(temp_tag_list)):
                concrete_film.setdefault('film_concrete_tag' + str(tag_num + 1), temp_tag_list[tag_num])

            temp_main_list = get_film_tag(concrete_film_dict["主演"])
            for main_num in range(0, len(temp_main_list)):
                concrete_film.setdefault('film_concrete_main' + str(main_num + 1), temp_main_list[main_num])

            temp_director_list = get_film_tag(concrete_film_dict["导演"])
            for di_num in range(0, len(temp_director_list)):
                concrete_film.setdefault('film_director' + str(di_num + 1), temp_director_list[di_num])

            temp_scenarist_list = get_film_tag(concrete_film_dict["编辑"])
            for sc_num in range(0, len(temp_scenarist_list)):
                concrete_film.setdefault('film_scenarist' + str(sc_num + 1), temp_scenarist_list[sc_num])
        out_list.append(concrete_film)

    return render(request, 'recommend.html', {"out_list": out_list})


def film_list_tag(get_type):
    arr_film_action = fun_search2(get_type)  # 类型： 动作 action

    film_action_all = []

    len_film_action = len(arr_film_action)
    if len_film_action > 50:
        len_film_action = 50
    for i in range(0, len_film_action):
        temp_action_name = str(arr_film_action[i]['电影名称'])  # str
        temp_url = str(arr_film_action[i]['海报'])  # str
        temp_action_grade = "评分：" + str(arr_film_action[i]['评分'])  # str
        temp_action_tag = get_film_tag(arr_film_action[i]["类型"])  # list
        if len(temp_action_name) > 6:
            temp_action_name = temp_action_name[0:6] + "..."
        if not str(arr_film_action[i]['评分']):
            temp_action_grade = "评分：暂无"
        film_content = {}
        film_content.setdefault('film_action_name', temp_action_name)
        film_content.setdefault('film_action_grade', temp_action_grade)
        film_content.setdefault('film_url', temp_url)
        film_content.setdefault('film_action_title', "../film_info/?film_get="
                                + str(arr_film_action[i]['id']))

        for j in range(0, len(temp_action_tag)):
            film_content.setdefault('film_action_tag' + str(j + 1), temp_action_tag[j])
        film_action_all.append(film_content)

    return film_action_all


def films(request):
    option = []
    if request.method == "GET" and request.GET:
        if request.GET.get("options"):
            option.append(request.GET.get("options"))  # 全部分类

        if request.GET.get("options2"):
            option.append(request.GET.get("options2"))  # 全部地区

        if request.GET.get("options3"):
            option.append(request.GET.get("options3"))  # 全部年代

        if request.GET.get("options4"):
            option.append(request.GET.get("options4"))  # 全部标签

    if not option:
        option.append("剧情")

    all_list_film = []
    for list_temp in option:
        if list_temp:
            all_list_film[len(all_list_film):len(all_list_film)] = film_list_tag(list_temp)

    return render(request, "films_2.html", {"all": all_list_film})

# python manage.py createsuperuser
# root 2219608412@qq.com Czq168168168

