from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Category
import markdown
from comments.forms import CommentForm
# Create your views here.

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list':post_list})
def archives(request, year, month):
    #按条件查找
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    #获得分类对应的id号
    cate = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category = cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    #阅读量 +1
    post.increase_views()
    #将MarkDown渲染为html文本
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post' : post,
        'form' : form,
        'comment_list' : comment_list
    }
    return render(request, 'blog/detail.html', context = context)