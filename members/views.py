from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import re

def sign_page(request):
    return render(request, 'members/sign_up.html')

def log_page(request):
    return render(request, 'members/log_in.html')

# Sign Up System
def sign_up(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')

        # Password format validation
        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) \
            or not re.search(r"\d", password) or not re.search(r"[@$!%*_?&#]", password):
            return JsonResponse({'error': 'Password must be at least 8 characters long and include uppercase, lowercase, a number, and a special character.'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': f'"{email}" email already exists.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': f'"{username}" username already exists.'}, status=400)

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Log the user in
        login(request, user)

        return JsonResponse({'success': f'User "{username}" created and logged in.'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Log In System
def log_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        username = data.get('username', '').strip()
        password = data.get('password', '')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'success': f'User "{username}" logged in successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid Username or Password'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Log Out System
@login_required
def logout_user(request):
    logout(request)
    return redirect('log')