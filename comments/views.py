from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from users.models import User
from .models import Comment
from .forms import CommentForm, ContactForm
from django.contrib import messages
# Create your views here.

def post_comment(request, post_pk):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk = post_pk)
    if request.method == 'POST':
        #request.POST中包含用户提交的数据，是一个类字典对象
        form = CommentForm(request.POST)
        #检查表单的数据是否符合格式要求
        if form.is_valid():
            #生成Comment实例，()不保存到数据库
            comment = form.save(commit=False)
            #将评论和被评论文章关联
            comment.post = post
            comment.name = request.user
            comment.save()
            #当redirect函数接收到一个模型实例是，他会调用该模型实例的get_absolute_url方法
            #重定向到了get_absolute_url方法返回的url，也就是重定向到了该文章的详细页面。
            #redirect函数也可以传入URL
            messages.success(request, '提交成功！')
            return redirect(post)
        else:
            #反向查询文章对应的全部评论
            #xxx_set xxx为关联模型的类名(小写)
            comment_list = post.comment_set.all()
            context = {
                'post' : post,
                'form' : form,
                'comment_list' : comment_list
            }
            # messages.error(request, '提交失败，请检查格式！')
            return render(request, 'blog/detail.html', context=context)
    #不是post请求，说明用户没有提交数据，重定向到文章详情页。
    # messages.error(request, '提交失败！')
    return redirect(post)

def post_contact(request):
    newform = ContactForm()
    newcontext = {'form': newform}
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ContactForm(request.POST)
            context = {'form': form}
            if form.is_valid():
                contact = form.save()
                messages.success(request, '提交成功！')
                return render(request, 'blog/contact.html', context=newcontext)
                # return redirect('http://127.0.0.1:8000/contact/')
            else:
                # messages.error(request, '提交失败，请检查格式！')
                return render(request, 'blog/contact.html', context=context)
        # messages.error(request, '提交失败!')
        return render(request, 'blog/contact.html', context=newcontext)
    else:
        messages.error(request, '请登录账号后操作！')
        return render(request, 'blog/contact.html', context=newcontext)


