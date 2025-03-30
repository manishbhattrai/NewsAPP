from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def user_create(request):

    if request.method == 'POST':

        ##print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')


        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken.")

        if password1 is None or password2 is None:
            messages.error(request,"Password field are missing.")

        print(f"Password1: {password1}, Password2: {password2}")

        if password1 != password2:
            messages.error(request,"Password didn't match")
            return redirect('/signup')
        
        
        try:
            User.objects.create_user(username=username,email=email, password=password1)
            messages.success(request,"Account Created Successfully!")
            return redirect('/login')
        except Exception as e:
            messages.error(request, f"error:{e}")
            return redirect('/signup')
      
    
    return render(request,'signup.html')





def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request, "Invalid Username or Password.")
    return render(request,'login.html')






def user_logout(request):
    logout(request)
    return redirect('login')





