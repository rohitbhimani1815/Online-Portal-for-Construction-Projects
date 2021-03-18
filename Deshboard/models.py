from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1,"SuperUser"),(2,"GovernmentUser"),(3,"OrganizationUser"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=20)

class SuperUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True)
    Position = models.CharField(max_length=200, null=True,blank=True)
    education = models.CharField(max_length=255, null=True,blank=True)
    location = models.CharField(max_length=255, null=True,blank=True)
    experiance = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username
        

class GovermentUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    goverment_id=models.IntegerField(unique=True,null=True)
    job_role=models.CharField(max_length=200, null=True)
    phone = PhoneNumberField()
    education = models.CharField(max_length=255, null=True,blank=True)
    location = models.CharField(max_length=255, null=True,blank=True)
    experiance = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.user.username

class OrganizationUserProfile(models.Model):
    user = models.OneToOneField(CustomUser,null=True, on_delete=models.CASCADE)
    organization_id=models.IntegerField(unique=True,null=True)
    organization_name=models.CharField(max_length=200, null=True)
    phone = PhoneNumberField()
    total_project = models.IntegerField(null=True,default=0,blank=True)
    location = models.CharField(max_length=255, null=True,blank=True)
    experiance = models.TextField(null=True,blank=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.user.username

class CreateForm(models.Model):
    form_name = models.CharField(max_length=255,unique=True)
    form_code = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    updated_at= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.form_name

class CreateProject(models.Model):
    project_name = models.CharField(max_length=255, unique=True)
    project_description = models.TextField()
    status_choices = [('pending','pending'),('assigned','assigned'),('completed','completed')] 
    status = models.CharField(max_length=15,choices=status_choices,default='pending')
    forms = models.ManyToManyField(CreateForm)
    estimated_budget = models.CharField(max_length=30,null=True)
    estimated_project_duration = models.CharField(max_length=15,null=True)
    apply_start_date = models.DateTimeField(null=True)
    apply_end_date = models.DateTimeField(null=True)
    assigned_by = models.CharField(max_length=255,null=True)
    assigned_to = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    assigned_details = models.TextField(null=True)
    project_progress = models.IntegerField(null=True,default=0,blank=True)
    Complete_details = models.TextField(null=True)
    complete_Rating = models.DecimalField(max_digits=2, decimal_places=1,null=True)
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    updated_at= models.DateTimeField(auto_now_add=True, null=True)

    @property
    def is_On_Time(self):
        return (timezone.now() > self.apply_start_date) and (timezone.now() < self.apply_end_date)

    def __str__(self):
        return self.project_name


class FormData(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    project = models.ForeignKey(CreateProject, on_delete=models.CASCADE)
    form_name= models.ForeignKey(CreateForm,on_delete=models.PROTECT)
    submited_data = models.JSONField(null=True, blank=True)
    submited_File = models.JSONField(null=True, blank=True)
    submited_at= models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','project','form_name'],name='user_project_formName')]

    def __str__(self):
        return str(self.user)+" "+str(self.project)+" "+str(self.form_name)

class applyProject(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    project = models.ForeignKey(CreateProject, on_delete=models.CASCADE)
    forms = models.ManyToManyField(FormData)
    date_applyed = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user','project'],name='user_project_forms')]

    def __str__(self):
        return str(self.user)+" "+str(self.project)

class trackProject(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    project = models.ForeignKey(CreateProject, on_delete=models.CASCADE)
    track_status=models.CharField(max_length=255,null=True)
    track_description = models.TextField()
    project_progress = models.IntegerField(null=True,default=0,blank=True)
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    updated_at= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.track_status)+" "+str(self.project)+" "+str(self.user)


class pastProject(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    estimated_budget = models.CharField(max_length=30,null=True)
    estimated_project_duration = models.CharField(max_length=15,null=True)
    Complete_details = models.TextField(null=True)
    complete_Rating = models.DecimalField(max_digits=2, decimal_places=1,null=True)
    created_at= models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.user) +" "+ str(self.project_name)

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            SuperUserProfile.objects.create(user=instance)
        if instance.user_type==2:
            GovermentUserProfile.objects.create(user=instance)
        if instance.user_type==3:
            OrganizationUserProfile.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.superuserprofile.save()
    if instance.user_type==2:
        instance.govermentuserprofile.save()
    if instance.user_type==3:
        instance.organizationuserprofile.save()


@receiver(post_save,sender=pastProject)
def Update_user_profile_project(sender,instance,created,**kwargs):
    if created:
        print(instance)
        print(instance.user)
        profile = OrganizationUserProfile.objects.filter(user=instance.user).first()
        past_project_count = pastProject.objects.filter(user=instance.user).count()
        profile.total_project = past_project_count
        profile.save()
        print("project updated")
