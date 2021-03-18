from django.urls import path
from django.contrib.auth import views as auth_views
from . import views,SupreUserViews,OrganizationUserViews,GovernmentUserViews

urlpatterns = [

    path('',views.userlogin,name='login'),
    path('logout',views.userlogout,name='logout'),
    path('password_change', views.ChangePassword,name="password_change"),

    # supreUserViews
    path('suprofile/',SupreUserViews.profile,name="suprofile"),
    path('superuser/',SupreUserViews.home, name='SuHome'),
    path('createGovUser/',SupreUserViews.CreateGovUser, name='createGovUser'),
    path('createOrUser/',SupreUserViews.CreateOrUser, name='CreateOrUser'),
    path('createForm/',SupreUserViews.CreateFormfun, name='CreateForm'),
    path('showformList/',SupreUserViews.ShowformList, name='ShowformList'),
    path('showForm/<slug:pid>',SupreUserViews.formshow, name='ShowForm'),
    path('createProject',SupreUserViews.CreateProjectFun, name='CreateProject'),
    path('showProject',SupreUserViews.ShowProject, name='ShowProject'),
    path('showProjectDetail/<slug:pid>',SupreUserViews.ShowProjectDetail, name='ShowProjectDetail'),
    path('editProjectDetail/<slug:pid>',SupreUserViews.editProjectDetail, name='editProjectDetail'),
    path('deleteProject/<slug:pid>',SupreUserViews.deleteProject, name='deleteProject'),
    path('appliedProjectList',SupreUserViews.showAllProjects, name='appliedProjectList'),
    path('appliedProjectDetail/<slug:pid>',SupreUserViews.appliedProjectDetail, name='appliedProjectDetail'),
    path('assignProject/<slug:pid>',SupreUserViews.assignProject, name='assignProject'),
    path('trackProject/',SupreUserViews.trackProjectfun, name='trackProject'),
    path('trackProject/<slug:pid>',SupreUserViews.trackProjectadd, name='trackProjectadd'),
    path('completeProject/',SupreUserViews.completeProject, name='completeProject'),
    path('completeProjectAdd/<slug:pid>',SupreUserViews.completeProjectAdd, name='completeProjectAdd'),
    path('manageGovUser/',SupreUserViews.manageGovUser, name='manageGovUser'),
    path('manageOrUser/',SupreUserViews.manageOrUser, name='manageOrUser'),
    path('deleteUser/<slug:uid>',SupreUserViews.deleteUser, name='deleteUser'),
    path('GovProfileShow/<slug:uid>',SupreUserViews.GovProfileShow, name='GovProfileShow'),
    path('OrganizationProfileShow/<slug:uid>',SupreUserViews.OrganizationProfileShow, name='OrganizationProfileShow'),

    # GovernmentUserViews
    path('goprofile/',GovernmentUserViews.profile,name="goprofile"),
    path('government/',GovernmentUserViews.home, name='GoHome'),


    # OrganizationUserViews
    path('orprofile/',OrganizationUserViews.profile,name="orprofile"),
    path('addPastProjects/',OrganizationUserViews.addPastProjects,name="addPastProjects"),
    path('organization/',OrganizationUserViews.home, name='OrHome'),
    path('showProjectOr',OrganizationUserViews.ShowProject, name='showProjectOr'),
    path('applyProjectDetail/<slug:pid>',OrganizationUserViews.applyProjectDetail, name='applyProjectDetail'),
    path('fillprojectform/<slug:pid>/<str:name>',OrganizationUserViews.fillprojectform, name='fillprojectform'),
    path('applyFinalProject/<slug:pid>',OrganizationUserViews.apply_Project_post, name='apply_Project_post'),
    path('showAppliedProject/',OrganizationUserViews.showAppliedProject, name='showAppliedProject'),
    path('applyshowForm/<slug:pid>',OrganizationUserViews.formshow, name='applyShowForm'),
    path('showCurrentProject/',OrganizationUserViews.showCurrentProject, name='showCurrentProject'),
    path('trackProjectShow/<slug:pid>',OrganizationUserViews.trackProjectShow, name='trackProjectShow'),
    path('completeProjector/',OrganizationUserViews.completeProject, name='completeProjector'),
    path('completeProjectShow/<slug:pid>',OrganizationUserViews.completeProjectShow, name='completeProjectShow'),




    # reset_password

    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="Deshboard/password_reset.html"),
    name="reset_password"),

    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="Deshboard/password_reset_sent.html"),
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="Deshboard/password_reset_form.html"),
    name="password_reset_confirm"),

    path('reset_password_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="Deshboard/password_reset_done.html"),
    name="password_reset_complete"),


]
