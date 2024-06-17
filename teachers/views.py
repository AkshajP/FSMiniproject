from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def login_teacher(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('teachers:dashboard')  # Replace with the correct URL name for teacher dashboard
        else:
            messages.info(request, 'Username or password is incorrect')
    
    return render(request, 'login.html')

def logout_teacher(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('teachers:login')

def register_teacher(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=name, password=password)
            login(request, user)
            messages.success(request, 'Registeration succesful')
            return render(request, 'teacher_dashboard.html')
    else:
        form = UserCreationForm()
    
    return render(request, 'register_teacher.html', {'form': form})

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')