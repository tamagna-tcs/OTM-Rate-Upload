from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .custom_login_view import CustomLoginView

urlpatterns = [
    # path("<str:key>/login/", auth_views.LoginView.as_view(template_name="rate/common/login_page.html"), name="login"),
    path("<str:key>/login/", CustomLoginView.as_view(template_name="rate/common/login_page.html"), name="login"),
    path("<str:key>/logout/", views.logout_view, name="logout"),
    path("", views.home, name="home"),
    path("<str:key>/user/select-instance/", views.select_instance, name="select-instance"),
    path("<str:key>/user/generate-template-generic/", views.generate_template_generic, name="generate-template-generic"),
    path("<str:key>/user/upload-template/", views.upload_template, name="upload-template"),
    path("<str:key>/user/csv-uploaded/", views.csv_uploaded, name="csv-uploaded"),
    path("get-rate-types-ajax/", views.get_rate_types_ajax, name="get_rate_types_ajax"), 
    #path("get-template-batches-ajax/", views.get_template_batches_ajax, name="get_template_batches_ajax"), 
    path("get-contracts-ajax/", views.get_contracts_ajax, name="get_contracts_ajax"), 

    path("<str:key>/manager/dashboard/", views.manager_dashboard, name="manager-dashboard"),
    path("<str:key>/manager/dashboard/instance/add", views.add_instance, name="manager-instance-add"),
    path("<str:key>/manager/dashboard/instance/update/<int:id>", views.update_instance, name="manager-instance-update"),
    path("<str:key>/manager/dashboard/instance/delete/<int:id>", views.delete_instance, name="manager-instance-delete"),
    path("<str:key>/manager/dashboard/access/add", views.add_access, name="manager-access-add"),
    path("<str:key>/manager/dashboard/access/delete/<int:id>", views.delete_access, name="manager-access-delete"),
    path("<str:key>/manager/dashboard/profile/add", views.add_profile, name="manager-profile-add"),
    path("<str:key>/manager/dashboard/profile/update/<int:id>", views.update_profile, name="manager-profile-update"),
    path("<str:key>/manager/dashboard/profile/reset_password/<int:id>", views.reset_password, name="manager-profile-reset-password"),
    path("<str:key>/manager/dashboard/profile/delete/<int:id>", views.delete_profile, name="manager-profile-delete"),
    path("<str:key>/manager/dashboard/batch/delete/<int:id>", views.delete_batch, name="manager-batch-delete"),
    path("<str:key>/manager/dashboard/delete-template/<int:id>", views.master_admin_delete_template, name="master-template-delete"),

    path("<str:key>/change-password/", views.change_password, name="change-password"),

    path("login/", CustomLoginView.as_view(template_name="rate/common/login_page.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path("master/customers", views.master_admin_customers, name="master-customers"),
    path("master/manage-customer/<str:key>", views.master_admin_manage_customer, name="master-manage-customer"),
    path("master/edit-customer/<str:key>", views.master_admin_edit_customer, name="master-edit-customer"),
    path("master/add-customer", views.master_admin_add_customer, name="master-add-customer"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
