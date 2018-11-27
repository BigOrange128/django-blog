from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    #显示在聚合阅读器上的标题
    title = "BigOrange个人博客"
    #跳转到网站的地址
    link = "139.224.13.65"
    #描述信息
    description = "Python, 数据库等学习记录。"
    #显示的内容条目
    def items(self):
        return Post.objects.all()
    #内容条目的标题
    def item_title(self, item):
        return '[%s] %s'%(item.category, item.title)
    #内容条目的描述
    def item_description(self, item):
        return item.body
