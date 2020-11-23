from django.shortcuts import render
from film.models import *

import csv
path = './film/data/'


def start_film(request):
    request.encoding = 'utf-8'
    if 'T_search' in request.GET and request.GET['T_search']:
        text = request.GET['T_search']
        # print(text)
        init_film(text)
    return render(request, "MyTest.html", locals())


def init_film(text):
    path_film = './film/data/'+text
    with open(path_film, 'r', encoding="utf-8") as f:
        reader = csv.reader(f)
        films = list(reader)  # ***** all **电影信息
        test = 0
        id_tag = 1
        for film in films:
            # for fou in film:
            #     print(fou)
            test += 1
            if test >= 3000:
                break
            if not film:
                continue
            # id_poster = (film[0].split("﻿id："))[-1]  # 对应海报的id/ id：
            id_poster = film[0][4:]
            if test == 1:
                id_poster = id_poster[1:]

            f_title = film[1]    # 电影名
            f_score = film[2]    # 电影的评分
            f_nums = (film[3].split("参评人数："))[-1]    # 电影的参评人数
            f_types = (film[4].split("类型："))[-1]  # 电影的类型(如:"剧情 动作 犯罪")
            # print(id_poster, f_title, f_score, f_nums, f_types)

            f_country = (film[5].split("制片国家: "))[-1]  # 电影的制片国家(如:"法国 / 美国")
            f_language = (film[6].split("语言:"))[-1]  # 电影的语言(如:"英语 / 意大利语 / 法语")
            f_r_data = (film[7].split("上映日期："))[-1]  # 电影的上映日期(如:"1994-09-14(法国)")
            f_length = (film[8].split("片长："))[-1]  # 电影的片长(如:"110分钟(剧场版)")
            f_another_name = (film[9].split("又名:"))[-1]  # 电影的又名(如:"杀手莱昂 / 终极追杀令(台) / 杀手里昂")
            f_directors = (film[10].split("导演:"))[-1]  # 导演(如:"吕克·贝松")
            f_scenarist_name = (film[11].split("编剧:"))[-1]  # 编剧(如:"吕克·贝松")
            f_main_roles = (film[12].split("主演:"))[-1]  # 主演(如:"让·雷诺 / 娜塔莉·波特曼 / 加里·奥德曼)
            # print(f_country, f_language, f_r_data, f_length,
            #       f_another_name, f_directors, f_scenarist_name, f_main_roles)

            f_url_d = (film[13].split("豆瓣链接："))[-1][:127]  # 豆瓣链接(如:"https://movie.douban.com/subject/1295644/")
            f_url_i = (film[14].split("IMDb链接："))[-1][:127]  # IMDb链接(如:" https://www.imdb.com/title/tt0110413")
            f_intro = (film[15].split("简介："))[-1]  # 简介
            # print(f_url_d)
            # print(f_url_i)
            # print(f_intro)

            tb_film = Data()
            # 给对象赋值
            tb_film.fl_title_str = f_title
            tb_film.fl_type_str = f_types
            tb_film.fl_data_str = f_r_data
            tb_film.fl_commentNum = f_nums
            tb_film.fl_replyNum = 0  # 回评数
            tb_film.fl_grade = f_score
            tb_film.fl_mainRole_str = f_main_roles
            tb_film.fl_anotherName_str = f_another_name
            tb_film.fl_director_str = f_directors
            tb_film.fl_scenarist_str = f_scenarist_name
            tb_film.fl_length_str = f_length
            tb_film.fl_language_str = f_language

            tb_film.fl_id_poster = id_poster
            tb_film.fl_country = f_country
            tb_film.fl_url_d = f_url_d
            tb_film.fl_url_i = f_url_i
            tb_film.fl_intro = f_intro

            # 插入数据
            tb_film.save()

            types = list(map(str, f_types.split(" ")))
            # print(types)
            for tag in types:
                if not tag:
                    continue
                tb_types = FilmTag_f()
                tb_types.id = id_tag
                id_tag += 1
                tb_types.ft_title = id_poster
                tb_types.ft_tag = tag
                tb_types.save()

#  film_data
