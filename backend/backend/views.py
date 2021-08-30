from django.shortcuts import render,redirect
from login.models import mailinglist
from farmer.models import fruits
from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER
from django.views.decorators.clickjacking import xframe_options_sameorigin


def home(request):
    '''
    **Functionality**

    *if the request method is get :-*


    displays home page to the users

    *if the request method  is post :-*

    it takes the entered email id and stores it in a model :model:`login.mailinglist`.
    

    **Template:**

    :template:`home.html`



    '''
    if request.method == "POST":
        email = request.POST['email']
        a = mailinglist(email = email)
        a.save()

        return redirect('/')
    return render(request,'home.html')


@xframe_options_sameorigin
def about(request):

    '''
    **Functionality**

    
    Displays about page to the user 
    
    '''
    if request.method == "POST":
        email = request.POST['email']
        subject = request.POST['subject']
        text = request.POST['text']

        send_mail(subject,text,email,[EMAIL_HOST_USER],fail_silently=False)

        return redirect('/about')

    return render(request,'about.html')