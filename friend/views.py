from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def friend_search_view(request, *args, **kwargs):
    context = {}
    if request.method == "GET":
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            search_results = User.objects.filter(username__startswith=search_query)
            accounts = [] # [(account, true), (account1, false)...]
            for account in search_results:
                accounts.append((account, False)) # Hardcode, to be corrected
            
            context["accounts"] = accounts

    return render(request, "friend/search_results.html", context)