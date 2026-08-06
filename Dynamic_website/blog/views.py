from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post
from django.http import Http404
# Create your views here.

# Static Demo Data

#posts  = [
#       {'id':1, 'title': 'Post 1', 'content': 'Content of post 1'},
#        {'id':2, 'title': 'Post 2', 'content': 'Content of post 2'},
#        {'id':3, 'title': 'Post 3', 'content': 'Content of post 3'},
#        {'id':4, 'title': 'Post 4', 'content': 'Content of post 4'},        
#    ]


def index(request):
    blog_title = "Latest Posts"
    posts = Post.objects.all()
    return render(request, 'index.html', {'blog_title': blog_title, "posts": posts})

def detail(request, slug):

# Error handling
    try:
        post = Post.objects.get(slug=slug)
        related_post = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post does not exists")
    
    return render(request, 'detail.html', {'post': post, 'related_post': related_post})
