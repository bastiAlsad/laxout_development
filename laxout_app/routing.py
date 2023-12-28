from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home" ),
    path("logout/", views.logout_view, name="logout"),
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("home/", views.home, name="home"),
    path("create-user/", views.create_user, name="create-user"),
    path("home/create-user/", views.create_user, name="create-user"),
    path("home/delete-user/<int:id>/", views.delete_user, name= "delete-user"),
    path("delete-user/<int:id>/", views.delete_user, name= "delete-user"),
    path("home/edit-user/<int:id>", views.edit_user, name="edit-user"),
    path("edit-user/<int:id>", views.edit_user, name="edit-user"),
    path("home/edit-user/edit-user-workout/", views.edit_user_workout, name="edit-user"),
    path("edit-user/edit-user-workout/", views.edit_user_workout, name="edit-user"),
    path("home/edit-user/delete-user-workout/", views.delete_user_workout, name="edit-user"),
    path("edit-user/delete-user-workout/", views.delete_user_workout, name="edit-user"),
    path("home/edit-user/add-exercises/<int:id>/", views.add_exercises, name="add-exercises"),
    path("edit-user/add-exercises/<int:id>/", views.add_exercises, name="add-exercises"),
    path("home/edit-user/add-exercises/<int:first>/<int:second>/", views.add_exercises, name="add-exercises"),
    path("edit-user/add-exercises/<int:first>/<int:second>/", views.add_exercises, name="add-exercises"),
    path("laxout/show-login-code/<str:logintoken>/", views.display_login_code, name="show-login-code"),
    path("analyses", views.analyses, name="analyses"),
    path("home/analyses", views.analyses, name="analyses"),
    path("home/edit-user/post-user-instruction/<int:id>/", views.post_user_instruction, name="edit-user"),
    path("edit-user/post-user-instruction/<int:id>/", views.post_user_instruction, name="edit-user"),
]