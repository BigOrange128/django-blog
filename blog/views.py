from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Post, Category, Tag
import markdown
from comments.forms import CommentForm, ContactForm
from django.views.generic import ListView, DetailView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        paginator_data = self.pagination_data(paginator, page, is_paginated)
        context.update(paginator_data)
        return context
    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        #左侧连续页面
        left = []
        right = []
        #左侧省略号
        left_has_more = False
        right_has_more = False
        #第一页页码
        first = False
        last = False
        #当前页码
        page_number = page.number
        #总页数
        total_pages = paginator.num_pages
        #页面列表[1, 2, 3, 4]
        page_range = paginator.page_range
        #如果有足够页面，显示三页连续,跟省略号
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:
                          (page_number - 1) if (page_number - 1) > 0 else 0]
        right = page_range[page_number : page_number + 2]
        if right:
            #连续页面最后一个小于最后一页
            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True
        if left:
            if left[0] > 1:
                right = True
            if left[0] > 2:
                left_has_more = True

        data = {
            'left':left,
            'right':right,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,
            'first':first,
            'last':last
        }
        return data
class BlogView(IndexView):
    template_name = 'blog/blog.html'
class ArchivesView(IndexView):
    #覆写父类方法，按条件查找
    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'), created_time__month=self.kwargs.get('month'))

class CategoryView(IndexView):
    #这里的pk为分类对应的id号并非文章
    def get_queryset(self):
        #通过分类的id号获得分类对象
        cate = get_object_or_404(Category, pk = self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category = cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk = self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags = tag)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 当 get 方法被调用后，才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return  response
    def get_object(self, queryset=None):
         md = markdown.Markdown(extensions=[
                                      'markdown.extensions.extra',
                                      #代码高亮
                                      'markdown.extensions.codehilite',
                                      #标题标签'markdown.extensions.toc',
                                       TocExtension(slugify=slugify),
                                    ])
         post = super(PostDetailView, self).get_object(queryset=None)
         post.body = md.convert(post.body)
         post.toc = md.toc
         return post
    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list
        })
        return context
    # post = get_object_or_404(Post, pk = pk)
    # #阅读量 +1
    # post.increase_views()
    # #将MarkDown渲染为html文本
    # post.body = markdown.markdown(post.body,
    #                               extensions=[
    #                                   'markdown.extensions.extra',
    #                                   'markdown.extensions.codehilite',
    #                                   'markdown.extensions.toc',
    #                                 ])
    # form = CommentForm()
    # comment_list = post.comment_set.all()
    # context = {
    #     'post' : post,
    #     'form' : form,
    #     'comment_list' : comment_list
    # }
    # return render(request, 'blog/detail.html', context = context)

def Contact(request):
    form = ContactForm()
    context = {'form' : form}
    return render(request,'blog/contact.html', context = context)

def About(request):
    return render(request, 'blog/about.html')
