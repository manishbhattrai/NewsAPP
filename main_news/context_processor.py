from .models import Category

## made this context processor file so that i can use below function in every templates.

def menu_links(request):

    links = Category.objects.all()
    return dict(links=links)