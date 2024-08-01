from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
 
    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    evaluation = models.CharField(max_length=10)
    budget = models.PositiveIntegerField()
    regularholiday = models.CharField(max_length=50)

    # オブジェクトの文字列表現を定義するために用いる特殊メソッド
    def __str__(self):
        return self.name

    # 新規作成・編集完了時のリダイレクト先
    def get_absolute_url(self):
        return reverse('restaurant_list')

class Review(models.Model):
    restaurantid =models.PositiveIntegerField(default=0)
    datetime = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    evaluation = models.CharField(max_length=10)
    postcontent = models.CharField(max_length=2000)

    # 新規作成・編集完了時のリダイレクト先
    def get_absolute_url(self):
        return reverse('review_list')

class Reservation(models.Model):
    username = models.CharField(max_length=200)
    restaurantid = models.PositiveIntegerField()
    reservationdate = models.CharField(max_length=10)
    numberofpeople = models.PositiveIntegerField()
    starttime = models.CharField(max_length=10)
    endtime = models.CharField(max_length=10)

    # 新規作成・編集完了時のリダイレクト先
    def get_absolute_url(self):
        return reverse('reservation_list')

class Member(models.Model):
    username = models.CharField(max_length=200)
    mail_address = models.CharField(max_length=200)
    creditcard_number = models.CharField(max_length=200)
    creditcard_name = models.CharField(max_length=200)
    security_code = models.CharField(max_length=10)


