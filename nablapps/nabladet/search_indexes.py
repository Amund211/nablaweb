from haystack import indexes
from .models import Nablad

class NabladIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    get_model_name = indexes.CharField(model_attr='get_model_name')
    
    def get_model(self):
        return Nablad
