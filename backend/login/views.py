from django.shortcuts import redirect, render
from django.contrib import  messages
from django.contrib.auth import login,authenticate,logout
from verify_email.email_handler import send_verification_email


from .models import User
from django.contrib.auth.forms import UserCreationForm 
from .forms import UserRegisterForm


def home(request):
    return render(request,'index.html')

def Login(request):
    if request.method == "POST":
        Email = request.POST['Email']
        password = request.POST['Password']
        print(Email)
        print(password)
        user = authenticate(request, username=Email, password=password)
        if user is not None:
            login(request,user)
            if 'next' in request.POST:
                print(request.POST['next'])
                return redirect(request.POST['next'])
            else:
                return redirect('home')
        else:
            messages.error(request,'Singn up? <a href="/user/signup">signup</a>', extra_tags='safe')
            return redirect('login')


    else:    
        return render(request,'login.html')



def signup(request):
    if request.method == 'POST':
    
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # mail = form.cleaned_data.get('email')
            inactive_user = send_verification_email(request, form)
            messages.success(request, 'a verification mail has been sent to your email')
            print('hai')    
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})
        # if 'login' in request.POST:
        #     return redirect('/login')
        # if 'google' in request.POST:
        #     pass
            

        
    # else:
    #     return render(request,'signup.html')



def logout_(request):
    logout(request)
    return redirect('/')


