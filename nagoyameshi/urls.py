"""nagoyameshi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TopView.as_view(), name="top"),
    path('main/management/', views.ManagementView.as_view(), name="management"),
    path('main/',views.RestaurantListView.as_view(), name="restaurant_list"),
    path('main/detail/<int:pk>', views.RestaurantDetailView.as_view(), name="restaurant_detail"),
    path('main/reviewlist/<int:pk>',views.ReviewListView.as_view(), name="review_list"),
    path('main/reviewcreate/',views.ReviewCreateView.as_view(), name="review_create"),
    path('main/reviewupdate/<int:pk>',views.ReviewUpdateView.as_view(), name="review_update"),
    path('main/reviewdelete/<int:pk>',views.ReviewDeleteView.as_view(), name="review_delete"),
    path('main/reservationlist/',views.ReservationListView.as_view(), name="reservation_list"),
    path('main/reservationcreate/',views.ReservationCreateView.as_view(), name="reservation_create"),
    path('main/reservationupdate/<int:pk>',views.ReservationUpdateView.as_view(), name="reservation_update"),
    path('main/reservationdelete/<int:pk>',views.ReservationDeleteView.as_view(), name="reservation_delete"),
    path('main/memberlist/',views.MemberListView.as_view(), name="member_list"),
    path('main/membercreate/',views.MemberCreateView.as_view(), name="member_create"),
    path('main/memberupdate/',views.MemberUpdateView.as_view(), name="member_update"),
    path('main/cordinfoupdate/',views.CordInfoUpdateform.as_view(), name="cordinfo_update"),
    path('main/cordinfodelete/',views.CordInfoDeleteform.as_view(), name="cordinfo_delete"),
    path('main/memberdelete/<int:pk>',views.MemberDeleteView.as_view(), name="member_delete"),
    path('main/categorylist/',views.CategoryListView.as_view(), name="category_list"),
    path('main/categorycreate/',views.CategoryCreateView.as_view(), name="category_create"),
    path('main/categoryupdate/<int:pk>',views.CategoryUpdateView.as_view(), name="category_update"),
    path('main/categorydelete/<int:pk>',views.CategoryDeleteView.as_view(), name="category_delete"),
    path('mypage/', views.MypageView.as_view(), name="mypage"),
    path('accounts/', include('allauth.urls')),
]
