from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from .decorators import isAuthenticate, unAuthenticate
from .service import phoneVerfication, sendCode
# Create your views here.

def home(request):
    return render(request, 'user/index.html')

@unAuthenticate
def user_login(request):
    if request.method == "POST":
        phone, password = request.POST.get("phone", None), request.POST.get("password", None)
        user = authenticate(phone=phone, password=password)
        if user:
            login(request, user)
            return redirect("profile")
    return render(request, 'user/login.html')

@isAuthenticate
def user_logout(request):
    logout(request)
    return redirect('/')

@unAuthenticate
def registration(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            phone, password = request.POST.get("phone", None), request.POST.get("password", None)            

            request.session['phone'] = phone
            request = sendCode(request)
            return render(request, 'user/verification.html')    
            
    return render(request, 'user/registration.html', {'form':form})
@unAuthenticate
def verification(request):
    if request.method == "POST":
        c_code = request.POST.get('code', None)
        phone = request.session.get('phone', None)
        r = phoneVerfication(request, c_code, phone)
        if r:
            return redirect('profile')
    return render(request, 'user/verification.html')    

@isAuthenticate
def profile(request):
    return render(request, 'user/profile.html')

