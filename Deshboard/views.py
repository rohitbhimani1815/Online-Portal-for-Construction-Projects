from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.

def userlogin(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            print(request.user.id)
            return redirect('SuHome')
        elif request.user.user_type == '2':
            return redirect('GoHome')
        elif request.user.user_type == '3':
            return redirect('OrHome')
    else:
        if request.method == 'POST':
            username =request.POST.get('username')
            password =request.POST.get('password')
            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)
                if user.user_type == '1':
                    return redirect("SuHome")
                elif user.user_type == '2':
                    return redirect("GoHome")
                elif user.user_type == '3':
                    return redirect("OrHome")
            else:
                messages.info(request, 'Username OR Password is incorrect.')
        
    contex={}
    return render(request, 'Deshboard/login.html',contex)

@login_required(login_url='login')
def userlogout(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        user=''
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    elif request.user.user_type == '3':
        user='Deshboard/Organizationuser/organization.html'
    contex = {'form':form,"user":user}
    return render(request, 'Deshboard/change_password.html',contex)