from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Restaurant, Review, Reservation,Member,Category
from django.db.models import Q
from accounts.models import CustomUser
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import resolve_url,redirect
import datetime

#class TopView(TemplateView):
#    template_name = 'top.html'

class ManagementView(View):
    def get(self, request):
        template_name = 'management.html'
        dt_now = datetime.datetime.now()
        print('管理画面')
        context = {
            'now':dt_now,
            'testtext':'hollow'
            }
        return render(self.request, template_name, context)

    def post(self,request):
        pk = self.kwargs['pk']
        restaurant_id = Review.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})

class TopView(View):
    def get(self, request):
        template_name = 'top.html'
        dt_now = datetime.datetime.now()
        print('トップページ')
        context = {
            'now':dt_now,
            'testtext':'hollow'
            }
        return render(self.request, template_name, context)

    def post(self,request):
        pk = self.kwargs['pk']
        restaurant_id = Review.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})


class MypageView(TemplateView):
    template_name = 'main/Mypage.html'
    # def get_context_data(self, **kwargs):
    #     context = super(MypageView, self).get_context_data(**kwargs)
    #     username = self.request.user.name
    #     context.update(
    #         {            }
    #     )
        # return context

class ContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.update_context(context)
        return context

    def update_context(self, context):
        # 具体的な実装を具象クラスで行う
        raise NotImplementedError

    #指定のラベルでclassのデータを更新
    def return_context(self, labels):
        def update_context(context):
            for label in labels:
                context[label] = self.request.GET.get(label)
        
        self.update_context = update_context

class RestaurantDetailView(DetailView):
    model = Restaurant
    fields = '__all__'
    template_name_suffix = '_detail_form'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.return_context(['keyword', 'category'])

    def get_context_data(self, **kwargs):
        context = super(RestaurantDetailView, self).get_context_data(**kwargs)
        keyword = self.request.session['keyword']
        category = self.request.session['category']
        print('RestaurantDetailView_get_context')
        print(keyword)
        print(category)
        print(context)
        context.update(
            {
                'category':category,
                'keyword':keyword
            }
        )
        print(context)
        return context

class RestaurantListView(ContextMixin,ListView):
    model = Restaurant
    paginate_by = 5
    template_name = 'main/Restaurant_List.html'

    def get_queryset(self):
        print('店舗一覧フィルタ設定')
        keyword = self.request.GET.get('keyword')
        category = self.request.GET.get('category')
        print('session追加')
        self.request.session['keyword']=keyword
        self.request.session['category']=category
        print(self.request.session['keyword'])
        print(self.request.session['category'])
        if len(keyword) > 0 and len(category) == 0:
            queryset = Restaurant.objects.filter(Q(name__icontains = keyword))
        elif len(keyword) == 0 and len(category) > 0: 
            queryset = Restaurant.objects.filter( Q( category = category))
        elif len(keyword) == 0 and len(category) == 0:
            queryset = Restaurant.objects.all()
        else:
            queryset = Restaurant.objects.filter(Q(name__icontains = keyword) , Q( category = category))
        queryset = queryset.order_by('-budget')

 #       queryset = Restaurant.objects.filter(Q(name__icontains = keyword) | Q( category = category))
        print(queryset)
        return queryset

    def post(self,request):
        keyword = self.request.session['keyword']
        category = self.request.session['category']
        budget = self.request.POST.get('budget')
        lowprice = self.request.POST.get('lowprice')
        highprice = self.request.POST.get('highprice')
        evaluation=self.request.POST.get('evaluation')
        print('evaluation',evaluation)
        if len(keyword) > 0 and len(category) == 0:
            queryset = Restaurant.objects.filter(Q(name__icontains = keyword))
        elif len(keyword) == 0 and len(category) > 0: 
            queryset = Restaurant.objects.filter( Q( category = category))
        elif len(keyword) == 0 and len(category) == 0:
            queryset = Restaurant.objects.all()
        else:
            queryset = Restaurant.objects.filter(Q(name__icontains = keyword) , Q( category = category))

        queryset = queryset.filter(budget__gte = lowprice,budget__lte = highprice)
        queryset = queryset.filter(evaluation__gte = evaluation)
        queryset = queryset.order_by(budget)
        context = {
            'object_list':queryset,
            'selectorder':budget,
            'lowprice':lowprice,
            'highprice':highprice,
            'evaluation':evaluation,
        }
        return render(request, self.template_name, context)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



        self.return_context(['keyword', 'category'])

class ReviewListView(ListView):
    model = Review
    paginate_by = 5
    template_name = 'main/Review_List.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        if pk is None:
            pk = self.request.GET.get('restaurantid')
        queryset = Review.objects.filter( Q( restaurantid = pk))
        return queryset

    def get_context_data(self, **kwargs):
        restaurantid = self.kwargs['pk']
        context = super(ReviewListView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

class ReviewCreateView(CreateView):
    model = Review
    fields = '__all__'
    template_name_suffix = '_Create_form'

    def get_initial(self):
        initial = super().get_initial()
        restaurantid = self.request.GET.get('restaurantid')
        initial["restaurantid"] = restaurantid
        return initial

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(ReviewCreateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        restaurantid = self.request.GET.get('restaurantid')
        return reverse_lazy('review_list', kwargs={'pk': restaurantid})

###2024/05/16レッスンでの修正###
class ReviewUpdateView(UpdateView):
    model = Review
    fields = '__all__'
    template_name_suffix = '_Update_form'

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(ReviewUpdateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Review.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})

class ReviewDeleteView(DeleteView):
    model = Review
    fields = '__all__'
    template_name_suffix = '_Delete_form'
    success_url = reverse_lazy('review_list')

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(ReviewDeleteView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Review.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})

class ReservationListView(ListView):
    model = Reservation
    paginate_by = 5
    template_name = 'main/Reservation_List.html'

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(ReservationListView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

class ReservationCreateView(CreateView):
    model = Reservation
    fields = '__all__'
    template_name_suffix = '_Create_form'

    def get_initial(self):
        initial = super().get_initial()
        restaurantid = self.request.GET.get('restaurantid')
        initial["restaurantid"] = restaurantid
        return initial

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(ReservationCreateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

class ReservationUpdateView(UpdateView):
    model = Reservation
    fields = '__all__'
    template_name_suffix = '_Update_form'

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(ReservationUpdateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Reservation.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})

class ReservationDeleteView(DeleteView):
    model = Reservation
    fields = '__all__'
    template_name_suffix = '_Delete_form'
    success_url = reverse_lazy('review_list')

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(ReservationDeleteView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Reservation.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('review_list', kwargs={'pk': restaurant_id})

class MemberListView(ListView):
    model = Member
    paginate_by = 5
    template_name = 'main/Member_List.html'

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(MemberListView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

class MemberCreateView(CreateView):
    model = Member
    fields = '__all__'
    template_name_suffix = '_Create_form'

    def get_initial(self):
        initial = super().get_initial()
        restaurantid = self.request.GET.get('restaurantid')
        initial["restaurantid"] = restaurantid
        return initial

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(MemberCreateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        restaurantid = self.request.GET.get('restaurantid')
        return reverse_lazy('member_list', kwargs={'pk': restaurantid})

class MemberUpdateView(View):
    model = CustomUser
    template_name = 'main/Member_Update_form.html'

    # def get_success_url(self):
    #     return reverse_lazy('top')

    # def form_invalid(self, form):
    #     print('check')
    #     print(form.errors)
    #     return super().form_invalid(form)

    def get(self,request):
        context = {}
        return render(request, self.template_name, context)
    
    def post(self,request):
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        cordnumber = self.request.POST.get('cordnumber')
        print('username',username)
        print('email',email)
        print('cordnumber',cordnumber)
        usermodel = self.model.objects.get(id=request.user.id)
        usermodel.username = username
        usermodel.email = email
        usermodel.save()
        context = {}
        return redirect(reverse_lazy('mypage'))

class CordInfoUpdateform(View):
    model = CustomUser
    template_name = 'main/CordInfo_Update_form.html'

    def get(self,request):
        context = {}
        return render(request, self.template_name, context)
    
    def post(self,request):
        cord_number = self.request.POST.get('cord_number')
        date_of_expiry = self.request.POST.get('date_of_expiry')
        security_key = self.request.POST.get('security_key')
        print('cord_number',cord_number)
        print('date_of_expiry',date_of_expiry)
        print('security_key',security_key)
        usermodel = self.model.objects.get(id=request.user.id)
        usermodel.cord_number = cord_number
        usermodel.date_of_expiry = date_of_expiry
        usermodel.security_key = security_key
        usermodel.is_subscribed = True
        usermodel.save()
        context = {}
        return redirect(reverse_lazy('mypage'))
    
class CordInfoDeleteform(View):
    model = CustomUser
    template_name = 'main/CordInfo_Delete_form.html'

    def get(self,request):
        context = {}
        return render(request, self.template_name, context)
    
    def post(self,request):
        usermodel = self.model.objects.get(id=request.user.id)
        usermodel.cord_number = None
        usermodel.date_of_expiry = None
        usermodel.security_key = None
        usermodel.is_subscribed = False
        usermodel.save()
        context = {}
        return redirect(reverse_lazy('mypage'))

class MemberDeleteView(DeleteView):
    model = Member
    fields = '__all__'
    template_name_suffix = '_Delete_form'
    success_url = reverse_lazy('member_list')

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(MemberDeleteView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Member.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('member_list', kwargs={'pk': restaurant_id})

class CategoryListView(ListView):
    model = Category
    paginate_by = 5
    template_name = 'main/Member_List.html'

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(CategoryListView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    template_name_suffix = '_Create_form'

    def get_initial(self):
        initial = super().get_initial()
        restaurantid = self.request.GET.get('restaurantid')
        initial["restaurantid"] = restaurantid
        return initial

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        restaurantid = self.request.GET.get('restaurantid')
        return reverse_lazy('member_list', kwargs={'pk': restaurantid})

class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'
    template_name_suffix = '_Update_form'

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Member.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('member_list', kwargs={'pk': restaurant_id})

class CategoryDeleteView(DeleteView):
    model = Category
    fields = '__all__'
    template_name_suffix = '_Delete_form'
    success_url = reverse_lazy('member_list')

    def get_context_data(self, **kwargs):
        restaurantid = self.request.GET.get('restaurantid')

        context = super(CategoryDeleteView, self).get_context_data(**kwargs)
        context.update({
            'restaurantid': restaurantid,
        })
        return context

    def get_success_url(self):
        pk = self.kwargs['pk']
        restaurant_id = Category.objects.filter(id=pk).first().restaurantid
        return reverse_lazy('member_list', kwargs={'pk': restaurant_id})    