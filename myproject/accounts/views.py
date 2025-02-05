from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse

def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')  
        else:
            messages.info(request, "Invalid credentials")
            return render(request, 'login.html')  
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')
        allowed_domains = ["gmail.com", "yahoo.com", "mnk.com"]
        email_domain = email.split("@")[-1]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return render(request, 'register.html')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                return render(request, 'register.html')
            elif email_domain not in allowed_domains:
                messages.info(request, "Please use a valid email address with @gmail.com, @yahoo.com, or @mnk.com")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.save()
                messages.info(request, 'User created successfully')
                return redirect('login')  
        else:
            messages.info(request, 'Passwords do not match')
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')
