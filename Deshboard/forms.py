from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import SuperUserProfile,GovermentUserProfile,OrganizationUserProfile,CustomUser,CreateProject,pastProject

User = get_user_model()

class CreateUserForm(UserCreationForm):

	class Meta:
		model = User
		fields  =['username', 'email', 'password1', 'password2','first_name','last_name']

class UpdateUserForm(ModelForm):

	class Meta:
		model = User
		fields  =['username', 'email','first_name','last_name']
	

class SuperUserProfileForm(ModelForm):
	class Meta:
		model = SuperUserProfile
		fields = '__all__'
		exclude =['user']


class GovermentUserProfileForm(ModelForm):
	class Meta:
		model = GovermentUserProfile
		fields = '__all__'
		exclude =['user']


class OrganizationUserProfileForm(ModelForm):
	class Meta:
		model = OrganizationUserProfile
		fields = '__all__'
		exclude =['user','total_project']

class CreateProjectForm(ModelForm):
	class Meta:
		model = CreateProject
		fields = '__all__'
		exclude =['assigned_by','assigned_to','assigned_details','Complete_details','complete_Rating']

class AddPastProjectsForm(ModelForm):
	class Meta:
		model = pastProject
		fields = '__all__'
		exclude=['user','Complete_details','complete_Rating']