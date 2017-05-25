"""Registering the models we want to store in the search engine"""

from haystack import indexes
from .models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable) :
    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField(model_attr='publish')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().published.all()