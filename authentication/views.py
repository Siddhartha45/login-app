from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if pass1 != pass2:
            messages.error(request, "passwords didn't match.")
            return redirect('signup')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email is already registered!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1,)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()
        
        messages.success(request, "Your account has been created successfully!")
        
        return redirect('signin')
    
    return render(request, "authentication/signup.html")

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})
            
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')
        
    return render(request, "authentication/login.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect('home')