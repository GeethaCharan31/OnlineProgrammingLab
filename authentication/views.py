from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # pre defined models package
from django.contrib import messages,auth


# Create your views here.
def index(request):
    return render(request, "auth/index.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')  # name of element in form
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            firstname=user.first_name
            return  render(request,"auth/index.html",{'firstname':firstname})
        else:
            messages.error(request,"Credentials Mismatch")
            return redirect('index')


    return render(request, "auth/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')  # name of element in form
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # we collected data from form now we make a model using contrib.auth.models User
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()

        # now to notify user about succesful registration we use django messages

        messages.success(request, "Your Account is succesfully created")

        return redirect("login")

    return render(request, "auth/register.html")


def logout(request):
    auth.logout(request)
    messages.success(request,"Logged Out Succesfully")
    return redirect('index')
