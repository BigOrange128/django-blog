from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.
class Category(models.Model):
    #分类数据库模型
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Tag(models.Model):
    #标签数据库模型
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    #文章数据库模型

    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = models.TextField()

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)  #一对多
    tags = models.ManyToManyField(Tag, blank=True)   #多对多

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs = {'pk' : self.pk})

    #内部类，通过指定属性规定该类的特性
    class Meta:
        ordering = ['-created_time']
    #复写save方法
    def save(self, *args, **kwargs):
        if not self.excerpt:
            #初始化markdown类
            md = markdown.Markdown(
                extension_configs=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite'
                ] )
            #先将Markdown文本渲染成HTML文本, strip_tags去掉HTML标签
            self.excerpt = strip_tags(md.convert(self.body))[:180]
        #调用父类的save方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)