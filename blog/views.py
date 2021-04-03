from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm, BedForm, Booking
from django.core.mail import send_mail
from django.contrib import messages
from .models import Post, BedRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView
)
from rest_framework.response import Response
from django.http import JsonResponse
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings
from django.core.mail import send_mail

def mainHome(request):
    # objects = []
    # qty = []
    # queryset = Post.objects.all()
    # for entry in queryset:
    #     objects.append(entry.name)
    #     qty.append(entry.covid_cap+entry.norm_cap)
    # y_pos = np.arange(len(objects))
    # plt.bar(y_pos, qty, align='center', alpha=0.5)
    # plt.xticks(y_pos, objects)
    # plt.ylabel('No of Beds')
    # plt.title('Hospital')
    # plt.savefig('media/barchart.png')
    return render(request, 'blog/index.html',)

def home(request):
    
    posts  = Post.objects.all().order_by("-covid_cap")
    context={
        'posts': Post.objects.all().order_by("-covid_cap")
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html')

@login_required
def PostCreateView(request):
    if len(Post.objects.filter(author = request.user)) == 0:
        if request.method== 'POST':
            form=PostForm(request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.save() 
                
                messages.success(request, f'Your hospital is registered!')
                return redirect("blog-home")
        else:
            form=PostForm()
            context = {
                "form": form,
            }
            return render(request,'blog/post_form.html',context)
    else:
        messages.warning(request, f"You already have entered your hospital")
        return redirect("blog-home")

# @login_required
def PostDetailView(request,pk):
    if request.method== 'POST':
        form=BedForm(request.POST)
        if form.is_valid():
            # form.save()
            rq =BedRequest()
            post = get_object_or_404(Post, pk=pk)
            rq.aadhar_number = form.cleaned_data.get('aadhar_number')
            
            rq.phone_number = form.cleaned_data.get('phone_number')
            rq.name = form.cleaned_data.get('name')
            rq.address = form.cleaned_data.get('address')
            rq.city = form.cleaned_data.get('city')
            rq.pin_code = form.cleaned_data.get('pin_code')
            rq.gender = form.cleaned_data.get('gender')
            rq.age = form.cleaned_data.get('age')
            rq.co_mobidity = form.cleaned_data.get('co_mobidity')
            rq.ambulance_required= form.cleaned_data.get('ambulance_required')
            rq.scheme = form.cleaned_data.get('scheme')
            rq.health_centre = post.author.username
            rq.tested = form.cleaned_data.get('tested')
            rq.symptoms = form.cleaned_data.get('symptoms')
           
            rq.save()
            return redirect('blog-home')          
        else:
            pass
    else:
        form=BedForm()
        
        return render(request,'blog/post_detail.html', {
            "form": form,
            "post": get_object_or_404(Post, pk=pk),
        })

# class PatientDetailView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     template_name = 


def PatientDetailView(request, pk):
    if request.method== 'POST':
        form=Booking(request.POST)
        if form.is_valid():
            ch = form.cleaned_data.get('choice')
            if ch != 3:
                post = Post.objects.filter(author = request.user).first()
                if ch == 1:
                    post.covid_cap -= 1
                else:
                    post.norm_cap -= 1
                post.save()
                rq = BedRequest.objects.filter(pk = pk).first()
                send_mail('COVID Saathi has some good news for you!',f' {request.user} has accepted your booking!',settings.EMAIL_HOST_USER,[f'{rq.email}'],fail_silently=False)
                BedRequest.objects.filter(aadhar_number = rq.aadhar_number).delete()
            else:
                BedRequest.objects.filter(pk = pk).delete()
        return redirect('dash-view')  
    else:
        form =Booking()
        
        return render(request,'blog/patient_detail.html', {
            "form": form,
            "post": get_object_or_404(BedRequest, pk=pk),
        })

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['name', 'content', 'covid_cap', 'norm_cap', 'city',
                'address'
            ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def FilteredPatientView(request):
    requests = BedRequest.objects.filter(health_centre = request.user)
    posts = Post.objects.filter(author = request.user)
    context = {
        'requests' : requests,
        'posts': posts
    }
    print(requests)
    return render(request, 'blog/dashboard.html',context)


# def get_data(request, *args, **kwargs):
#     data = {
#         "sales": 100,
#         "customers": 10,
#     }
#     return JsonResponse(data) # http response

# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request, format=None):
#         qs=Post.objects.all()
        
#         labels = []
#         default_items = []

#         for item in qs:
#             labels.append(item.name)
#             default_items.append(item.covid_cap+item.norm_cap)

#         data = {
#                 "labels": labels,
#                 "default": default_items,
#         }
#         return Response(data)

def bed_chart(request):
    labels = []
    data = []

    queryset = Post.objects.all()
    for entry in queryset:
        labels.append(entry.name)
        data.append(entry.covid_cap+item.norm_cap)
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def FilteredCityView(request, cats):
    category_posts = []
    # users = Post.objects.filter(city=cats)
    posts = Post.objects.filter(city=cats)
    # for post in posts:
    #    if post.author.profile.blood_group == cats:
    #        category_posts.append(post)

    return render(request, 'blog/categories.html', {'cats': cats, 'posts': posts})


def FilteredAreaView(request, cats):
    category_posts = []
    # users = Post.objects.filter(city=cats)
    posts = Post.objects.filter(area=cats)
    # for post in posts:
    #    if post.author.profile.blood_group == cats:
    #        category_posts.append(post)

    return render(request, 'blog/categories.html', {'cats': cats, 'posts': posts})