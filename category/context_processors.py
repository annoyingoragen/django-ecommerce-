from .models import category

def category_menu_links(request):
    links=category.objects.all().values('slug','name')
    return dict(links=links)