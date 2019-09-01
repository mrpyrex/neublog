import datetime
from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # author      = indexes.CharField(model_attr='user')
    created_at = indexes.DateTimeField(model_attr='created_at')
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Post

    def index_queryset(self, using=None):

        return self.get_model().objects.filter(created_at__lte=datetime.datetime.now())

    def prepare(self, obj):
        prepared_data = super(PostIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data
