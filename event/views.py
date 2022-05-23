from django.shortcuts import redirect, render
from .forms import RegisterEventPostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/members/login")
def add_event(request):
    if request.method == "POST":
        data = request.POST
        form = RegisterEventPostForm(data, instance=request.user)
        # Check if form is valid
        if form.is_valid():
            form.save()
            messages.success(request, ("Event created successfully!"))
            redirect("profile", user_id=request.user.id)
    context = {
        "event_form": RegisterEventPostForm
    }
    return render(request, "event/add_event.html", context)