from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import PostForm, BedForm, Booking, Search
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
from collections import Counter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from bs4 import BeautifulSoup
import requests
import feedparser
from pprint import pprint

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


def search(posts, name):
    strings = name.lower().split()
    category_posts = []
    for post in posts:
        for string in strings:
            data = post.name+" "+ post.city + " "+ post.area
            if string in data.lower().split():
                category_posts.append(post)
    
    result = [item for items, c in Counter(category_posts).most_common()
                                          for item in [items] * c]
    res = []
    for item in result:
        flag = True
        for r in res:
            if item.name == r.name:
                flag = False
                break
        if flag:
            res.append(item)
    return res

def home(request):
    posts = Post.objects.all().order_by("-covid_cap")
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    form = Search()
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/home.html', context)

def home_search(request, cats):
    posts = Post.objects.all().order_by("-covid_cap")
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    else:
        form = Search()
    posts  = search(posts, cats)
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/home.html', context)


# def home(request):
    
#     posts  = Post.objects.all().order_by("-covid_cap")
#     context={
#         'posts': Post.objects.all().order_by("-covid_cap")
#     }
#     return render(request, 'blog/home.html', context)

def about(request):
    
    return render(request, 'blog/about.html')

def data(request):
    return render(request, 'blog/data.html')

def chart(request):
    return render(request, 'blog/chart.html')

def image_size(img):
    if img.height > 300 or img.width > 300:
        img.height = 300
        img.width = 300
        return img

@login_required
def PostCreateView(request):
    post=Post.objects.filter(author = request.user)
    if len(post) == 0:
        if request.method== 'POST':
            form=PostForm(request.POST, request.FILES)
            # print("===================================",form.is_valid())
            if form.is_valid():
                form.instance.author = request.user
                img = form.instance.img1 
                print(img.height)

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
        post=post.first()
        return redirect("post-detail",pk=post.id)

# @login_required
def PostDetailView(request,pk):
    if request.method== 'POST':
        form=BedForm(request.POST)
        if form.is_valid():
            # form.save()
            rq =BedRequest()
            post = get_object_or_404(Post, pk=pk)
            rq.aadhar_number = form.cleaned_data.get('aadhar_number')
            rq.email = form.cleaned_data.get('email')
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
        post = get_object_or_404(Post, pk=pk)
        
        return render(request,'blog/post_detail.html', {
            "form": form,
            "post": post,
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
                if ch == '1':
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
        rq = get_object_or_404(BedRequest, pk=pk)

        return render(request,'blog/patient_detail.html', {
            "form": form,
            "post": rq,
        })

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = ['name', 'content', 'proof','covid_cap', 'norm_cap', 'city',
                'address', 'img1', 'img2', 'img3'
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
    category_posts = Post.objects.filter(city=cats)
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    else:
        form = Search()
    paginator = Paginator(category_posts, 9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/home.html', context)


def FilteredAreaView(request, cats):
    category_posts = Post.objects.filter(area=cats)
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    else:
        form = Search()
    paginator = Paginator(category_posts, 9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/home.html', context)

def FilteredTypeView(request, cats):
    category_posts = Post.objects.filter(type=cats)
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cats = form.cleaned_data.get('search')
            return redirect("home-search", cats)
    else:
        form = Search()
    paginator = Paginator(category_posts, 9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/home.html', context)

def cat_search_genre(request, cats, cat):
    category_posts = Post.objects.filter(city=cats)
    if request.method== 'POST':
        form = Search(request.POST)
        if form.is_valid():
            cat = form.cleaned_data.get('search')
            return redirect("cat-search-genre", cats, cat)
    else:
        form = Search()
    category_posts  = search(category_posts, cat)
    paginator = Paginator(category_posts, 9)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    context={
        'page': page,
        'post_list': post_list,
        'search_form': form,
    }
    return render(request, 'blog/home.html', context)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs=Post.objects.all()
        
        labels = []
        default_items = []

        for item in qs:
            labels.append(item.name)
            default_items.append(item.covid_cap+item.norm_cap)

        data = {
                "labels": labels,
                "default": default_items,
        }
        return Response(data)


def searchf(input, word, count):
    print(count)
    if input == word:
        count = count+1
    return count

def news(request):
    source =  requests.get('https://www.cnbctv18.com/healthcare/coronavirus-news-live-updates-india-mumbai-maharashtra-kerala-covid19-vaccine-lockdown-news-3-2-3-8804661.htm').text
    source2= requests.get('https://timesofindia.indiatimes.com/india/coronavirus-live-updates-april-3/liveblog/81302719.cms').text
    source3= requests.get('https://indianexpress.com/article/india/coronavirus-india-live-updates-second-wave-maharashtra-lockdown-covid-19-7256745/').text
    soup= BeautifulSoup(source3,'lxml')
    headline=[]
    body=[]
    input = "Maharashtra"
    count = 0
    
    # headline= soup.find('div',class_='arti-right').text
    for article in soup.find_all('div',class_='heading-lvblg'):
        
        for word in article.text.split():
            count = searchf(input, word, count)
        headline.append(article.text)

    print(count, "=================================================") 

    for article in soup.find_all('div',class_='body-lvblg'):
        # print(article.text)
        body.append(article.text)
    # content =soup.find_all('p')

    data=zip(headline,body)
    # print(data)
    context={
        # 'body':body,
        # 'headline':headline
        'data':data,
        'type': 'Local'
    }
    return render(request,'blog/about.html',context)

def Global(request):
    source3= requests.get('https://edition.cnn.com/world/live-news/coronavirus-pandemic-vaccine-updates-04-03-21/index.html?tab=all').text
    soup= BeautifulSoup(source3,'lxml')
    headline=[]
    body=[]
    
    # headline= soup.find('div',class_='arti-right').text
    for article in soup.find_all('h2'):
        # print(article.text)
        headline.append(article.text)
    for article in soup.find_all('div',class_='erzhuK'):
        print(article.text)
        body.append(article.text)
    # content =soup.find_all('p')

    data=zip(headline,body)
    # print(data)
    context={
        # 'body':body,
        # 'headline':headline
        'data':data,
        'type':"Global"
    }
    return render(request,'blog/about.html',context)