from django.shortcuts import render

def home(request):
    return render(request, 'agrohome/index.html')