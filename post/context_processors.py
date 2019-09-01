from .models import PostCategory


def menu_links(request):
    links = PostCategory.objects.all()
    return dict(links=links)
