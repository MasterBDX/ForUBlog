from posts.models import Category
from main.models import BlogInfo


def categories_processor(request):
    categories = Category.objects.all()
    obj = BlogInfo.objects.last()  
    return {'categories': categories,'info':obj}
