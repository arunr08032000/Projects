from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    blog_title = "Latest Posts"
    posts  = [
        {'id':1, 'title': 'Post 1', 'content': 'Content of post 1'},
        {'id':2, 'title': 'Post 2', 'content': 'Content of post 2'},
        {'id':3, 'title': 'Post 3', 'content': 'Content of post 3'},
        {'id':4, 'title': 'Post 4', 'content': 'Content of post 4'},        
    ]
    return render(request, 'index.html', {'blog_title': blog_title, "posts": posts})

def detail(request, post_id):
    return render(request, 'detail.html')
