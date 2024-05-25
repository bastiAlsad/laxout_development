"""
URL configuration for laxout project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("laxout_app.routing")),
    path("", include("django.contrib.auth.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path("autorise", api_views.autorise_laxout_user),
    re_path("api/test", api_views.get_username),
    re_path("uebungen", api_views.get_exercises),
    re_path("indexpost", api_views.post_leistungs_index),
    re_path("coinsget", api_views.get_laxcoins_amount),
    re_path("painsadd", api_views.post_pain_level),
    re_path("couponsget", api_views.get_coupons),
    re_path("couponbuy", api_views.buy_coupon),
    re_path("coupongetuser", api_views.get_coupons_for_user),
    re_path("coupondeleteuser", api_views.delete_coupon_user),
    re_path("exercisefinish", api_views.finish_exercise),
    re_path("exerciseskip", api_views.skip_exercise),
    re_path("workoutfinish", api_views.finish_workout),
    re_path("instructionget", api_views.get_intruction),
    re_path("progressweekget", api_views.get_progress_week),
    re_path("getindividualindexes", api_views.get_individual_indexes),
    # re_path("buywaterdrops", api_views.buy_water_drops),
    re_path("pourlaxtree", api_views.pour_lax_tree),
    re_path("getwaterdrops", api_views.get_water_drops),
    re_path("getcondition", api_views.get_condition),
    re_path("postsuccesscontroll", api_views.post_success_controll),
    re_path("getsuccessdata", api_views.get_success_data),
    re_path("postmessage", api_views.post_message_chat),
    re_path("getmessages", api_views.get_messages),
    re_path("checkmessageuser", api_views.check_if_user_has_new_messages),
    re_path("createuserapp", api_views.create_user_through_app),
    re_path("couponbuysovendus", api_views.buy_sovendus_coupon),
    re_path("uniqueuidsovendus", api_views.get_unique_customer_uid),
    re_path("createwebcode", api_views.create_web_code),
    re_path("logwebuserin",api_views.log_webuser_in),
    re_path("getwebworkout", api_views.get_web_workout),
    path("getwebinstruction", api_views.get_web_intruction),
    path("getwebsuccesweek", api_views.get_progress_week_web),
    path("websuccespost", api_views.post_web_progress_conrtroll),
    path("webcompleteworkout", api_views.finish_workout_web),
    path("webskipexercise", api_views.skip_exercise_web),
    path("webfinishexercise", api_views.finish_exercise_web),
    path("webaddsomepain",api_views.post_pain_level_web)
]
#Test