from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.contrib.auth import get_user_model
from .forms import SuperUserProfileForm,GovermentUserProfileForm,OrganizationUserProfileForm,CreateUserForm,CreateProjectForm,UpdateUserForm
from .models import CustomUser,SuperUserProfile,GovermentUserProfile,OrganizationUserProfile,CreateForm,CreateProject,applyProject,FormData,trackProject,pastProject
import json
from django.utils import timezone

# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def profile(request):
    form = UpdateUserForm(instance=CustomUser.objects.get(id=request.user.id))
    profileForm = SuperUserProfileForm(instance=SuperUserProfile.objects.get(user=request.user))
    if request.method =="POST":
        form = UpdateUserForm(request.POST,request.FILES,instance=CustomUser.objects.get(id=request.user.id))
        profileForm = SuperUserProfileForm(request.POST, request.FILES,instance=SuperUserProfile.objects.get(user=request.user))

        if form.is_valid() and profileForm.is_valid():
            form.save()
            profileForm.save()
            messages.success(request, 'Profile Updated Successfully')
        else:
            messages.error(request, 'Please Fill Details')
    contex={'profileForm':profileForm,'form':form}
    return render(request, 'Deshboard/Superuser/profile.html',contex)


@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def home(request):
    Total_Organization=CustomUser.objects.filter(user_type='3').count()
    Total_Goverment=CustomUser.objects.filter(user_type='2').count()
    Total_Project = CreateProject.objects.all().count()
    Total_Assigned_Project = CreateProject.objects.filter(status='assigned').count()
    Total_Complete_Project = CreateProject.objects.filter(status='completed').count()
    contex = {'Total_Organization':Total_Organization,'Total_Goverment':Total_Goverment,'Total_Project':Total_Project,
                'Total_Assigned_Project':Total_Assigned_Project,'Total_Complete_Project':Total_Complete_Project}
    return render(request,'Deshboard/Superuser/home.html',contex)


@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def CreateGovUser(request):
    form = CreateUserForm()
    profileForm = GovermentUserProfileForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profileForm = GovermentUserProfileForm(request.POST)
        if form.is_valid() and profileForm.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            job_role = request.POST.get('job_role')
            goverment_id = request.POST.get('goverment_id')
            phone = request.POST.get('phone')

            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, first_name=first_name,last_name=last_name, password=password,user_type=2)

            userProfile = GovermentUserProfile.objects.get(user=user)
            userProfile.job_role = job_role
            userProfile.goverment_id = goverment_id
            userProfile.phone = phone
            userProfile.save()
            messages.success(request, 'Account Created Successfully with username '+request.POST['username'])
    contex = {"form":form,"profileForm":profileForm}
    return render(request,'Deshboard/Superuser/createGovUser.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def CreateOrUser(request):
    form = CreateUserForm()
    profileForm = OrganizationUserProfileForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profileForm = OrganizationUserProfileForm(request.POST)
        if form.is_valid() and profileForm.is_valid():
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            organization_name = request.POST.get('organization_name')
            organization_id = request.POST.get('organization_id')
            phone = request.POST.get('phone')

            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, first_name=first_name,last_name=last_name, password=password,user_type=3)

            userProfile = OrganizationUserProfile.objects.get(user=user)
            userProfile.organization_name = organization_name
            userProfile.organization_id = organization_id
            userProfile.phone = phone
            userProfile.save()
            messages.success(request, 'Account Created Successfully with username '+request.POST['username'])
    contex = {"form":form,"profileForm":profileForm}
    return render(request,'Deshboard/Superuser/createOrUser.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def CreateFormfun(request):
    if request.method == "POST":
        formcode=request.POST["formcode"]
        formname = request.POST["formname"]
        f= CreateForm(form_name=formname,form_code=formcode)
        f.save()
        return HttpResponse("Form Create Successfully")
    return render(request,'Deshboard/Superuser/createForm.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def ShowformList(request):
    myform = CreateForm.objects.all()
    user=''
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex={"formnames":myform,'user':user}
    return render(request,"Deshboard/Superuser/ShowformList.html",contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def formshow(request,pid):

    myform =  CreateForm.objects.get(id = pid)
    contex={"form":myform.form_code}
    return render(request,"Deshboard/Superuser/showform.html",contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def CreateProjectFun(request):

    form = CreateProjectForm()
    all_form_name = CreateForm.objects.all()
    if request.method == 'POST':
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Project Created Successfully')
        else:
            messages.error(request, 'Please Check Details')
    contex={"form":form,"all_form_name":all_form_name}
    return render(request,"Deshboard/Superuser/createProject.html",contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def ShowProject(request):
    all_projects=CreateProject.objects.all()
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex = {'all_projects':all_projects,'user':user}
    return render(request,"Deshboard/Superuser/showProject.html",contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2','3'])
def ShowProjectDetail(request,pid):
    projects=CreateProject.objects.get(id=pid)
    project = [{'project_name':projects.project_name,
    'project_description':projects.project_description,
    'status':projects.status,
    'estimated_budget':projects.estimated_budget,
    'estimated_project_duration':projects.estimated_project_duration,
    'apply_start_date':str(projects.apply_start_date.strftime("%d/%m/%Y %H:%M")),
    'apply_end_date':str(projects.apply_end_date.strftime("%d/%m/%Y %H:%M")),
    'Forms':[i.form_name for i in projects.forms.all()],
    'assigned_by':projects.assigned_by,
    'assigned_to':str(projects.assigned_to),
    'created_at':str(projects.created_at.strftime("%d/%m/%Y %H:%M")),
    'updated_at':str(projects.updated_at.strftime("%d/%m/%Y %H:%M"))
              }]
    return JsonResponse(json.dumps(project),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def editProjectDetail(request,pid):

    if request.method =="POST":
        projects=CreateProject.objects.get(id=pid)
        form =CreateProjectForm(request.POST,instance=projects)
        if form.is_valid():
            obj=form.save()
            projects.updated_at = timezone.now()
            projects.save()
            messages.success(request, 'Project Updated Successfully')

        else:
            messages.error(request, 'Error While Updating Project')
        return JsonResponse(json.dumps("Project Update"),safe=False)
    projects=CreateProject.objects.get(id=pid)
    all_form_name = CreateForm.objects.all()
    project_form_selected= projects.forms.all()
    all_form = {}
    for i in all_form_name:
        if i in project_form_selected:
            all_form[i.form_name]=[i.id,"selected"]
        else:
            all_form[i.form_name]=[i.id,"Notselected"]
    project_data =[{
        "project_name":projects.project_name,
        "project_description":projects.project_description,
        "status":projects.status,
        "forms":all_form,
        "estimated_budget":projects.estimated_budget,
        "estimated_project_duration":projects.estimated_project_duration,
        "apply_start_date":str(projects.apply_start_date.strftime("%m/%d/%Y %H:%M")),
        "apply_end_date":str(projects.apply_end_date.strftime("%m/%d/%Y %H:%M")),
        }]
    return JsonResponse(json.dumps(project_data),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def deleteProject(request,pid):
    if request.method == "POST":
        try:
            CreateProject.objects.get(id=pid).delete()
            return JsonResponse(json.dumps("Project Delete"),safe=False)
        except:
            return JsonResponse(json.dumps("ProjectDeleteError"),safe=False)
    return JsonResponse(json.dumps("Project Delete"),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def showAllProjects(request):
    all_projects=CreateProject.objects.all()
    detail={}
    for project in all_projects:
        if applyProject.objects.filter(project=project):
            detail[project.id]=applyProject.objects.filter(project=project)
    user=''
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex={"all_projects":all_projects,"detail":detail,'user':user}
    return render(request,'Deshboard/Superuser/appliedProjectList.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def appliedProjectDetail(request,pid):
    
    projects=CreateProject.objects.get(id=pid)
    project_form = projects.forms.all()
    form_data=[]
    for i in project_form:
        form_data.append(FormData.objects.filter(project=projects,form_name=i))
    user=''
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex = {"form_data":form_data,'user':user}
    return render(request,'Deshboard/Superuser/showFormData.html',contex)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def assignProject(request,pid):
    if request.method == "POST" and request.is_ajax:
        select_org = request.POST.get('select_org')
        Assign_description = request.POST.get('Assign_description')
        if select_org==None:
            return JsonResponse(json.dumps("select Organization"),safe=False)
        demo=applyProject.objects.filter(project=pid,user__id=select_org)
        if demo:
            demo=demo[0]
            project= CreateProject.objects.get(id=demo.project.id)
            project.assigned_by = request.user.username
            project.assigned_to = get_user_model().objects.get(id=select_org)
            project.assigned_details = Assign_description
            project.updated_at = timezone.now()
            project.status = "assigned"
            project.save()
        return JsonResponse(json.dumps("OK"),safe=False)
    else:
        applied_project = applyProject.objects.filter(project=pid)
        applied_detail={}
        if applied_project:
            applied_detail["project_name"]=applied_project[0].project.project_name
            applied_org=[]
            for i in applied_project:
                applied_org.append([i.user.id,i.user.username])
            applied_detail["applied_org"]=applied_org
        else:
            applied_detail["project_name"]=applied_project[0].project.project_name
            applied_detail["applied_org"]=[]
    return JsonResponse(json.dumps(applied_detail),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def trackProjectfun(request):
    assign_project = CreateProject.objects.filter(status="assigned")
    user=''
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex = {"assign_project":assign_project,"user":user}
    return render(request,'Deshboard/Superuser/trackProject.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def trackProjectadd(request,pid):
    if request.method == "POST":
        project =CreateProject.objects.get(id=pid)
        track_status = request.POST.get('Track_Status')
        track_description = request.POST.get('Track_description')
        project_progress = request.POST.get('project_progress')
        track_obj=trackProject(user=request.user,project=project,track_status=track_status,track_description=track_description,project_progress=project_progress)
        track_obj.save()
        project.project_progress = project_progress
        project.save()
        return JsonResponse(json.dumps("OK"),safe=False)
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
@allowed_users(allowed_roles=['1','2'])
def completeProject(request):
    project = CreateProject.objects.exclude(status="pending")
    user=''
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex = {"complete_project": project,'user':user}
    return render(request,'Deshboard/Superuser/completeProject.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def completeProjectAdd(request,pid):
    if request.method == "POST":
        project = CreateProject.objects.get(id=pid)
        project.Complete_details=request.POST.get('complete_description')
        project.complete_Rating=request.POST.get('rating')
        project.status='completed'
        project.save()

        pastProject.objects.create(user=project.assigned_to,project_name=project.project_name,project_description=project.project_description,estimated_budget=project.estimated_budget,estimated_project_duration=project.estimated_project_duration,Complete_details=project.Complete_details,complete_Rating=project.complete_Rating).save()
        return JsonResponse(json.dumps("OK"),safe=False)
    else:
        project = CreateProject.objects.get(id=pid)
        project_dteail={"complete_description":str(project.Complete_details),"complete_Rating":str(project.complete_Rating)}
        return JsonResponse(json.dumps(project_dteail),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def manageGovUser(request):
    Gov_user = GovermentUserProfile.objects.all()
    contex = {'Gov_user':Gov_user}
    return render(request,'Deshboard/Superuser/manageGovUser.html',contex)


@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def manageOrUser(request):
    Or_user = OrganizationUserProfile.objects.all()
    if request.user.user_type == '1':
        user='Deshboard/Superuser/superuser.html'
    elif request.user.user_type == '2':
        user='Deshboard/Governmentuser/government.html'
    contex = {'Or_user':Or_user,'user':user}
    return render(request,'Deshboard/Superuser/manageOrUser.html',contex)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def deleteUser(request,uid):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=uid)
            user.delete()
            return JsonResponse(json.dumps("Success"),safe=False)
        except:
            return JsonResponse(json.dumps("Error"),safe=False)
    return JsonResponse(json.dumps("ok"),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1'])
def GovProfileShow(request,uid):
    user=GovermentUserProfile.objects.filter(user__id=uid).first()
    data="Error"
    if user:
        data=[
            {
                'user_img':user.profile_pic.url,
                'username':user.user.username,
                'job_role':user.job_role,
                'full_name':user.user.get_full_name(),
                'email':user.user.email,
                'date_joined':str(user.user.date_joined.strftime("%m/%d/%Y %H:%M")),
                'education':user.education,
                'location':user.location,
                'phone':str(user.phone),
                'experiance':user.experiance


            }
        ]

    return JsonResponse(json.dumps(data),safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['1','2'])
def OrganizationProfileShow(request,uid):
    user=OrganizationUserProfile.objects.filter(user__id=uid).first()
    data="Error"
    if user:
        data=[
            {
                'user_img':user.profile_pic.url,
                'username':user.user.username,
                'Organization_name':user.organization_name,
                'full_name':user.user.get_full_name(),
                'email':user.user.email,
                'date_joined':str(user.user.date_joined.strftime("%m/%d/%Y %H:%M")),
                'total_project':user.total_project,
                'location':user.location,
                'phone':str(user.phone),
                'experiance':user.experiance


            }
        ]
        user_pastProject = pastProject.objects.filter(user__id=uid)
        past_project_detail =[]
        for i in user_pastProject:
            past_project_detail.append({
                'id':i.id,
                'project_name':i.project_name,
                'project_description':i.project_description,
                'estimated_budget':i.estimated_budget,
                'estimated_project_duration':i.estimated_project_duration,
                'Complete_details':i.Complete_details,
                'complete_Rating':str(i.complete_Rating)
            })
        data.append(past_project_detail)

    return JsonResponse(json.dumps(data),safe=False)

