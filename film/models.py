from django.db import models


class FilmTag_f(models.Model):
    id = models.IntegerField(primary_key=True)
    ft_title = models.TextField(unique=False, max_length=2560)      # 电影名称
    ft_tag = models.CharField(max_length=128, blank=True, null=0)   # 标签


class User_f(models.Model):
    gender = (
        ('男', '男'),
        ('女', '女'),
    )

    movie_tag = (
        ('terrify', '惊悚'),
        ('action', '动作'),
        ('love', '爱情'),
        ('adventure', '冒险'),
        ('western', '欧美'),
        ('funny', '搞笑'),
        ('japan_and_korea', '日韩'),
        ('crime', '犯罪'),
        ('disaster', '灾难'),
    )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    user_personal = models.CharField(max_length=100, default='当前显示为默认标签，您可以点击右方修改进行修改')
    user_movie_tag = models.CharField(max_length=100, choices=movie_tag, default=" ")
    user_pic = models.CharField(max_length=100, default='/static/images/userPic.jpg')
    c_time = models.DateTimeField(auto_now=True)
    user_address = models.CharField(max_length=100, default='当前显示为默认地址，您可以点击右方修改进行修改')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Comment_f(models.Model):
    c_content_str = models.TextField(max_length=2560)
    c_user_name = models.CharField(max_length=128, default="01")
    c_film_title = models.CharField(max_length=128, default="坏孩子的秋天")
    com_time = models.DateTimeField(auto_now_add=True)


class Score_f(models.Model):
    s_score_str = models.CharField(max_length=32, default="5.6")
    s_user_name = models.CharField(max_length=128, default="01")
    s_film_title = models.CharField(max_length=128, default="坏孩子的秋天")
    score_time = models.DateTimeField(auto_now_add=True)


class Collection_f(models.Model):
    coll_user_name = models.CharField(max_length=128, default="01")
    coll_film_title = models.CharField(max_length=128, default="坏孩子的秋天")
    coll_time = models.DateTimeField(auto_now_add=True)


class Data(models.Model):
    fl_title_str = models.TextField()                                      # 电影名称
    fl_type_str = models.TextField(null=0, blank=True)                     # 类型
    fl_data_str = models.TextField(null=0, blank=True)                     # 发布日期/上映日期
    fl_mainRole_str = models.TextField(null=0, blank=True)                 # 主演
    fl_anotherName_str = models.TextField(null=0, blank=True)              # 另一个名字（又名）
    fl_director_str = models.TextField(null=0, blank=True)                 # 导演
    fl_scenarist_str = models.TextField(null=0, blank=True)                # 编辑
    fl_length_str = models.CharField(max_length=128, blank=True, null=0)    # 片长
    fl_language_str = models.TextField(null=0, blank=True)                 # 语言
    fl_commentNum = models.CharField(max_length=128, blank=True, default="500")              # 评论数
    fl_replyNum = models.CharField(max_length=128, blank=True, null=0)                # 回评数
    fl_grade = models.CharField(max_length=128, blank=True, default="5.6")                   # 评分

    fl_id_poster = models.TextField(max_length=128, default="miss_h")      # 对应海报id
    fl_country = models.CharField(max_length=128, blank=True, null=0)      # 电影的制片国家(如:"法国 / 美国")
    fl_url_d = models.CharField(max_length=128, blank=True, null=0)   # 豆瓣链接
    fl_url_i = models.CharField(max_length=128, blank=True, null=0)   # IMDb链接
    fl_intro = models.TextField(default="暂时没有简介")                                     # 简介


# python manage.py makemigrations
# python manage.py migrate
# python FilmTest/manage.py makemigrations
# python FilmTest/manage.py migrate
# python FilmTest/manage.py migrate --fake
# python manage.py migrate --fake
