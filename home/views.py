from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    """ A view to return the index page """
    if request.user.is_authenticated:
        return redirect("profile", user_id=request.user.id)
    
    return render(request, 'home/index.html', {})


def about(request):
    ''' render about us page '''

    template = "home/about.html"

    return render(request,
                  template)


def page_not_found_view(request, exception):
    """ A view to return the 404 Error page """
    return render(request, '404.html', status=404)