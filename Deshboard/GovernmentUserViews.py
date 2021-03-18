from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .forms import UpdateUserForm,GovermentUserProfileForm
from .models import CustomUser,GovermentUserProfile,CreateProject


# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['2'])
def profile(request):
    form = UpdateUserForm(instance=CustomUser.objects.get(id=request.user.id))
    profileForm = GovermentUserProfileForm(instance=GovermentUserProfile.objects.get(user=request.user))
    if request.method =="POST":
        form = UpdateUserForm(request.POST, request.FILES,instance=CustomUser.objects.get(id=request.user.id))
        profileForm = GovermentUserProfileForm(request.POST, request.FILES,instance=GovermentUserProfile.objects.get(user=request.user))

        if form.is_valid() and profileForm.is_valid():
            form.save()
            profileForm.save()
            messages.success(request, 'Profile Updated Successfully')
        else:
            messages.error(request, 'Please Fill Details')
    contex={'profileForm':profileForm,'form':form}
    return render(request, 'Deshboard/Governmentuser/profile.html',contex)



@login_required(login_url='login')
@allowed_users(allowed_roles=['2'])
def home(request):
    Total_Organization=CustomUser.objects.filter(user_type='3').count()
    Total_Project = CreateProject.objects.all().count()
    Total_Assigned_Project = CreateProject.objects.filter(status='assigned').count()
    Total_Complete_Project = CreateProject.objects.filter(status='completed').count()
    contex = {'Total_Organization':Total_Organization,'Total_Project':Total_Project,'Total_Assigned_Project':Total_Assigned_Project,'Total_Complete_Project':Total_Complete_Project}
    return render(request,'Deshboard/Governmentuser/home.html',contex)

