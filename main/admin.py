from django.contrib import admin
from .models import Restaurant, Category, Review, Reservation, Member
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class RestaurantResource(resources.ModelResource):
    class Meta:
        model = Restaurant

# class RestaurantAdmin(admin.ModelAdmin):
#      list_display = ('id', 'name', 'category','address','evaluation','budget','regularholiday')
#      search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('name',)

class ReviewAdmin(admin.ModelAdmin):
     list_display = ('id', 'restaurantid', 'datetime', 'username', 'evaluation','postcontent')
     search_fields = ('username',)

class ReservationAdmin(admin.ModelAdmin):
     list_display = ('id', 'username', 'restaurantid', 'reservationdate', 'numberofpeople', 'starttime','endtime')
     search_fields = ('username',)

class MemberAdmin(admin.ModelAdmin):
     list_display = ('id', 'username', 'mail_address', 'creditcard_number', 'creditcard_name', 'security_code')
     search_fields = ('username',)

# admin.site.register(Restaurant, RestaurantAdmin)
@admin.register(Restaurant)
class RestaurantAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','name', 'category', 'address', 'evaluation', 'budget', 'regularholiday')
    search_fields = ('name',)
    resource_class = RestaurantResource
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Member, MemberAdmin)
