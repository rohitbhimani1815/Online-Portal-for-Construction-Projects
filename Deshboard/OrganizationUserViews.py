from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from .forms import UpdateUserForm,OrganizationUserProfileForm,AddPastProjectsForm
from .models import CustomUser,OrganizationUserProfile,CreateForm,CreateProject,FormData,trackProject,pastProject,applyProject as applysProject
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def profile(request):
    form = UpdateUserForm(instance=CustomUser.objects.get(id=request.user.id))
    profileForm = OrganizationUserProfileForm(instance=OrganizationUserProfile.objects.get(user=request.user))
    past_project = pastProject.objects.filter(user=request.user)
    if request.method =="POST":
        form = UpdateUserForm(request.POST, request.FILES,instance=CustomUser.objects.get(id=request.user.id))
        profileForm = OrganizationUserProfileForm(request.POST, request.FILES,instance=OrganizationUserProfile.objects.get(user=request.user))

        if form.is_valid() and profileForm.is_valid():
            form.save()
            profileForm.save()
            messages.success(request, 'Profile Updated Successfully')
        else:
            messages.error(request, 'Please Fill Details')
    contex={'profileForm':profileForm,'form':form,'past_project':past_project}
    return render(request, 'Deshboard/Organizationuser/profile.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def addPastProjects(request):
    if request.method == "POST":
        form = AddPastProjectsForm(request.POST)
        if form.is_valid():
            project_name = request.POST.get('project_name')
            project_description = request.POST.get('project_description')
            estimated_budget = request.POST.get('estimated_budget')
            estimated_project_duration = request.POST.get('estimated_project_duration')
            user = request.user
            project=pastProject(user=user,project_name=project_name,project_description=project_description,estimated_budget=estimated_budget,estimated_project_duration=estimated_project_duration)
            project.save()
            return JsonResponse(json.dumps("Success"),safe=False)
        else:
            return JsonResponse(json.dumps("Error"),safe=False)
    return JsonResponse(json.dumps("ok"),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def home(request):
    Total_Project = CreateProject.objects.all().count()
    Total_Applyed_Project = applysProject.objects.filter(user=request.user).count()
    Total_Current_Project = CreateProject.objects.filter(status='assigned',assigned_to=request.user).count()
    Total_Complete_Project = CreateProject.objects.filter(status='completed',assigned_to=request.user).count()
    contex = {'Total_Project':Total_Project,'Total_Applyed_Project':Total_Applyed_Project,
               'Total_Current_Project':Total_Current_Project,'Total_Complete_Project':Total_Complete_Project}
    return render(request,'Deshboard/Organizationuser/home.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def ShowProject(request):
    all_projects=CreateProject.objects.filter()
    contex = {'all_projects':all_projects}
    return render(request,"Deshboard/Organizationuser/showProject.html",contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def applyProjectDetail(request,pid):
    projects=CreateProject.objects.get(id=pid)
    form_data = FormData.objects.filter(user=request.user,project=projects)
    apply_project = applysProject.objects.filter(user=request.user,project=projects)
    if apply_project:
        project_applyed = True
    else:
        project_applyed = False

    fill_form_id=[i.form_name.id for i in form_data]
    project = [{'project_name':projects.project_name,
    'project_description':projects.project_description,
    'status':projects.status,
    'estimated_budget':projects.estimated_budget,
    'estimated_project_duration':projects.estimated_project_duration,
    'apply_start_date':str(projects.apply_start_date),
    'apply_end_date':str(projects.apply_end_date),
    'Forms':[{"form_name":i.form_name,"form_status":"form fill"} if (i.id in fill_form_id) else {"form_name":i.form_name,"form_status":"form not fill"} for i in projects.forms.all()],
    'project_applyed':project_applyed
              }]
    return JsonResponse(json.dumps(project),safe=False)

@csrf_exempt
@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def fillprojectform(request,pid,name):
    fillform = True
    project = CreateProject.objects.get(id=pid)
    form =  CreateForm.objects.get(form_name = name)
    form_fill=FormData.objects.filter(user = request.user,project = project,form_name= form)
    if form_fill:
        fillform = False
    elif request.method == 'POST':
        formdata = dict(request.POST.items())
        files = dict(request.FILES.items())
        submited_File={}
        for field_name,file in files.items():
            fs = FileSystemStorage(location=settings.MEDIA_ROOT+'/'+str(request.user.username))
            file_name = fs.save(file.name,file)
            file_url = settings.MEDIA_URL + str(request.user.username)+'/'+file_name
            submited_File[field_name]=[file_name,file_url]

        data = FormData(user = request.user,project = project,form_name= form,submited_data=formdata,submited_File=submited_File)
        data.save()
        return HttpResponse("Form File Successfully")
    contex = {"form":form.form_code,"fillform":fillform}
    return render(request,'Deshboard/Organizationuser/fillProjectForm.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def apply_Project_post(request,pid):
    
        if request.method == "POST":
            project = CreateProject.objects.get(id=pid)
            apply_project = applysProject(project=project,user=request.user)
            apply_project.save()
            project_form = FormData.objects.filter(user=request.user,project=project)
            for i in project_form:
                apply_project.forms.add(i.id)
            return HttpResponse('Project Apply Successfully')
        else:
            return HttpResponse('You Are Not authorized to Apply Project')


@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def showAppliedProject(request):
    project = applysProject.objects.filter(user=request.user)
    contex = {"applied_project":project}
    return render(request,'Deshboard/Organizationuser/appliedProject.html',contex)


@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def formshow(request,pid):

    projects=CreateProject.objects.get(id=pid,)
    project_form = projects.forms.all()
    form_data=[]
    for i in project_form:
        form_data.append(FormData.objects.filter(project=projects,form_name=i,user=request.user))
    contex = {"form_data":form_data}
    return render(request,"Deshboard/Organizationuser/showFormData.html",contex)


@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def showCurrentProject(request):
    Project = CreateProject.objects.filter(assigned_to=request.user,status="assigned")
    contex = {"current_Project":Project}
    return render(request,"Deshboard/Organizationuser/showCurrentProject.html",contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def trackProjectShow(request,pid):
    track_details = trackProject.objects.filter(project=pid)
    track_details_list =[]
    for track in track_details:
        track_details_list.append({
            'track_status':track.track_status,
            'track_description':track.track_description,
            'project_progress' : track.project_progress,
            'created_at':str(track.created_at.strftime("%d/%m/%Y %H:%M"))
        })
    return JsonResponse(json.dumps(track_details_list),safe=False)


@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def completeProject(request):
    project = CreateProject.objects.filter(assigned_to=request.user,status="completed")
    contex = {"complete_project": project}
    return render(request,'Deshboard/Organizationuser/completeProject.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['3'])
def completeProjectShow(request,pid):
    
    project = CreateProject.objects.get(id=pid,assigned_to=request.user)
    project_dteail={"complete_description":str(project.Complete_details),"complete_Rating":str(project.complete_Rating)}
    return JsonResponse(json.dumps(project_dteail),safe=False)


