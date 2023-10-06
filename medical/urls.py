from django.contrib.auth import views as auth_views
from django.urls import path

from medical import views

urlpatterns = [
    path("", views.login, name="login"),
    path("cad/", views.cad, name="cadastro"),
    # path('login/', views.login, name='login')
    path("logout/", views.logout, name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset_confirm/<slug:uidb64>/<slug:token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

    path('main/', views.main, name='main'),
    path('show_finalization_patient/', views.show_finalization_patient, name='show_finalization_patient'),

    # crud procedure secretaria
    path('show_procedure/', views.find_all_procedure, name='show_procedure'),
    path('create_procedure/', views.create_procedure, name='procedure'),
    path('update_procedure/<int:id>', views.update_procedure, name='update_procedure'),
    path("delete_procedure/<int:id>", views.delete_procedure, name="delete_procedure"),

    # crud recommendation secretaria
    path('show_recommendation/', views.find_all_recommendation, name='show_recommendation'),
    path('create_recommendation/', views.create_recommendation, name='reco'),
    path('update_recommendation/<int:id>', views.update_recommendation, name='update_recommendation'),
    path("delete_recommendation/<int:id>", views.delete_recommendation, name="delete_recommendation"),

    # crud patient
    path('show_patient/', views.find_all_patient, name='show_patient'),
    # path("create_patient/", views.create_patient, name="create_patient"),
    path('update_patient/<int:id>', views.update_patient, name='update_patient'), 
    path("delete_patient/<int:id>", views.delete_patient, name="delete_patient"),
    path("config_proc/<int:id>", views.config_proc, name="config_proc"),
    path("patient_config/<int:id>", views.patient_config, name="patient_config"),
    

    path("resetPassword/", views.resetPassword, name="resetPassword"),

    path("patient/", views.patient, name="patient"),
    path("calendar/", views.calendar, name="calendar"),

]   
