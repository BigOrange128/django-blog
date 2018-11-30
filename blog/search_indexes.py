from haystack import indexes
from .models import Post

#django haystack规定, 要对某个app下的数据进行全文检索，在该app下创建search_indexes文件
#创建一个XXIndex类，XX为被检索的模型
class PostIndex(indexes.SearchIndex, indexes.Indexable):
    #一个索引只能有一个document，使用此字段内容作为索引进行检索
    #document=True默认字段名为text
    #use_template为数据模板
    #模板里定义的字段，即为搜索引擎去搜索的字段。
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post
    def index_queryset(self, using=None):
        return self.get_model().objects.all()