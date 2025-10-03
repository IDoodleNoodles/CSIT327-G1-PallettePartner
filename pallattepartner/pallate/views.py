from django.shortcuts import render

def landing(request):
    return render(request, 'pallate/index.html')

def login_view(request):
    return render(request, 'pallate/login.html')

def register(request):
    return render(request, 'pallate/register.html')

def dashboard(request):
    return render(request, 'pallate/dashboard.html')

def artist_profile(request):
    return render(request, "pallate/artist_profile.html")

def collaboration_detail(request):
    return render(request, "pallate/collaboration_detail.html")