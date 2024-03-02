from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ExerciseForm
from .models import (
    LaxoutUser,
    Laxout_Exercise,
    IndexesLaxoutUser,
    IndexesPhysios,
    DoneWorkouts,
    SkippedExercises,
    DoneExercises,
    Coupon,
    LaxoutUserPains,
    PhysioIndexCreationLog,
    Uebungen_Models,
)
from . import models
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
import random
import string
from django.contrib.auth import logout, authenticate, login
from datetime import datetime
import json
from django.utils import timezone
from uuid import uuid4
from laxout import lax_ai


class ExercisesModel:
    def __init__(
        self,
        new_execution,
        new_name,
        new_dauer,
        new_videoPath,
        new_looping,
        new_added,
        new_instruction,
        new_timer,
        new_required,
        new_imagePath,
        new_appId,
        new_skippedAmount,
        new_id,
    ):
        self.execution = new_execution
        self.name = new_name
        self.dauer = new_dauer
        self.videoPath = new_videoPath
        self.looping = new_looping
        self.added = new_added
        self.instruction = new_instruction
        self.timer = new_timer
        self.required = new_required
        self.imagePath = new_imagePath
        self.appId = new_appId
        self.skippedAmount = new_skippedAmount
        self.id = new_id


def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect(
            "login"
        )  # Hier 'login' durch den Namen deiner Login-URL ersetzen
    else:
        # Du könntest hier auch eine eigene Logout-Seite rendern
        # return render(request, 'logout.html')
        pass


def random_string(length=100):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


def display_login_code(request, logintoken=None):
    return render(request, "laxout_app/display_code.html", {"login_token": logintoken})


# Create your views here.
@login_required(login_url="login")
def home(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    print("Active Admin id{}".format(active_admin_user.is_superuser))
    users_filtert = LaxoutUser.objects.filter(created_by=request.user)
    user_amount = users_filtert.count()

    active_user_amount = 0
    for user in users_filtert:
        print(str(user.last_login_2.date) + "Last Login date")
        if days_between_today_and_date(user.last_login_2) < 14:
            active_user_amount += 1

    users = LaxoutUser.objects.all()
    user_list = []
    for user in users:
        if user.created_by == request.user:
            user_list.append(user)

    context = {
        "users": user_list,
        "user_amount": user_amount,
        "active_user_amount": active_user_amount,
        "is_superuser": active_admin_user.is_superuser,
    }
    return render(request, "laxout_app/home.html", context)


@login_required(login_url="login")
def create_exercise(request):
    if request.method == "POST":
        try:
            first = request.POST.get("first")
            second = request.POST.get("second")
        except json.JSONDecodeError as e:
            print("Error in Json Decode")

        form = ExerciseForm(request.POST)

        if form.is_valid():
            print("krass")
            exercise_instance = form.save(commit=False)
            exercise_instance.save()

            # Add First and Second instances
            if first is not None:
                exercise_instance.first.add(models.First.objects.create(first=first))
            if second is not None:
                exercise_instance.second.add(
                    models.Second.objects.create(second=second)
                )
            exercise_instance.second.add(models.Second.objects.create(second=7))

            print(exercise_instance)
            return redirect("/")  # Redirect to the exercise list view
    else:
        form = ExerciseForm()

    return render(request, "laxout_app/create_exercise.html", {"form": form})



def set_exercises_user(user_id, predicted_exercises):
    user = models.LaxoutUser.objects.get(id=user_id)
    for i in predicted_exercises:
        user.exercises.add(i)
    user.save()
    print("Hich")
    print(user.exercises.all())


@login_required(login_url="login")
def create_user(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            insteance = form.save(commit=False)
            insteance.created_by = request.user
            tree = models.LaxTree.objects.create()
            insteance.lax_tree_id = tree.id
            new_user_uid = str(uuid4())
            while LaxoutUser.objects.filter(user_uid=new_user_uid).exists():
                new_user_uid = str(uuid4())
            insteance.user_uid = new_user_uid
            print("User Uid:{}".format(insteance.user_uid))
            note = form.cleaned_data.get("note")
            predicted_exercises_ids = lax_ai.predict_exercise(note)
            exercises = []
            print(predicted_exercises_ids)

            insteance.save()

            for i in predicted_exercises_ids:
                user_instance = insteance

                # es wird geschaut, ob es schon eine Reihenfolge gibt

                if i != 0 and i < len(models.Uebungen_Models.objects.all()):
                    print("AI predicted exercise")
                    exercise_to_add = Laxout_Exercise.objects.create(
                        execution=Uebungen_Models.objects.get(id=i).execution,
                        name=Uebungen_Models.objects.get(id=i).name,
                        dauer=Uebungen_Models.objects.get(id=i).dauer,
                        videoPath=Uebungen_Models.objects.get(id=i).videoPath,
                        looping=Uebungen_Models.objects.get(id=i).looping,
                        added=False,
                        instruction="",
                        timer=Uebungen_Models.objects.get(id=i).timer,
                        required=Uebungen_Models.objects.get(id=i).required,
                        imagePath=Uebungen_Models.objects.get(id=i).imagePath,
                        appId=Uebungen_Models.objects.get(id=i).id,
                        onlineVideoPath=Uebungen_Models.objects.get(
                            id=i
                        ).onlineVideoPath,
                    )
                    exercises.append(exercise_to_add)

                

            set_exercises_user(insteance.id, exercises)
            print("ZZZ")
            print(exercises)
            print(insteance.id)
            print(lax_ai.predict_exercise(note))

            return redirect("/home")

    else:
        form = UserForm()
        return render(
            request,
            "laxout_app/create_user.html",
            {"form": form, "is_superuser": active_admin_user.is_superuser},
        )


@login_required(login_url="login")
def delete_user(request, id=None):
    if id != None:
        object_to_delte = LaxoutUser.objects.get(id=id)
        if request.user == object_to_delte.created_by:
            for exercis in object_to_delte.exercises.all():
                exercis.delete()
            for index in IndexesLaxoutUser.objects.filter(created_by=id).all():
                index.delete()
            for coupon in object_to_delte.coupons.all():
                coupon.delete()
            for doneWorkout in DoneWorkouts.objects.filter(laxout_user_id=id).all():
                doneWorkout.delete()
            for skippedExercise in SkippedExercises.objects.filter(
                laxout_user_id=id
            ).all():
                skippedExercise.delete()
            for doneExercise in DoneExercises.objects.filter(laxout_user_id=id).all():
                doneExercise.delete()
            for doneWorkout in DoneWorkouts.objects.filter(laxout_user_id=id).all():
                doneWorkout.delete()
            for order in models.Laxout_Exercise_Order_For_User.objects.filter(
                laxout_user_id=id
            ).all():
                order.delete()
            for pain in models.LaxoutUserPains.objects.filter(created_by=id).all():
                pain.delete()
            models.SuccessControll.objects.filter(created_by=id).delete()
            object_to_delte.delete()
        return redirect("/home")
    return redirect("/home")


@login_required(login_url="login")
def edit_user(request, id=None):
    user = LaxoutUser.objects.get(id=id)

    if request.method == "POST":
        user.last_meet = timezone.datetime.today()
        user.save()

    last_meet = user.last_meet.strftime("%Y-%m-%d")
    indexes = []
    workouts_instance = []
    workout_dates = []

    for index in IndexesLaxoutUser.objects.all():
        if index.created_by == id:
            indexes.append(index)

    for workout in DoneWorkouts.objects.all():
        if workout.laxout_user_id == id:
            workouts_instance.append(workout)

    workout_dates = [date.date.strftime("%Y-%m-%d") for date in workouts_instance]
    labels = []
    count = 0
    to_put = 0
    store = []
    users_indexes = []
    unique_w_d = set(workout_dates)
    workout_dates = list(unique_w_d)

    for index in indexes:
        if index.creation_date not in labels:
            labels.append(index.creation_date)

    for i in labels:
        for z in indexes:
            if i == z.creation_date:
                count += z.index
                store.append(z)

        to_put = count / len(store)
        count = 0
        store = []
        users_indexes.append(to_put)

    ###skip logik###
    
    current_exercises = user.exercises.all()

    current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
            laxout_user_id=id
        )  # es wird geschaut, ob es schon eine Reihenfolge gibt
    if len(current_order_objects) == 0 and len(current_exercises) != 0:
            print("There was a diffenrence")
            order = 1
            for i in current_exercises:
                models.Laxout_Exercise_Order_For_User.objects.create(
                    laxout_user_id=id, laxout_exercise_id=i.id, order=order
                )
                order += 1
            print("length")
            print(len(models.Laxout_Exercise_Order_For_User.objects.all()))

    lenght_order_objects_list = len(current_order_objects)

    print("LENGTH ORDER OBJECTS{}".format(len(current_order_objects)))

    users_exercises_skipped = []

    skipped_exercises = models.SkippedExercises.objects.filter(laxout_user_id=id)

    list_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )
    # print("LIST Skipped LENGTH {}".format(skipped_exercises))
    sorted_list = sorted(
        list_order_objects, key=lambda x: x.order
    )  # Werden der größe nach Sotiert
    # print("Sorted List {}".format(sorted_list))
    exercise_ids = []

    for i in sorted_list:
        exercise_ids.append(i.laxout_exercise_id)
    skipped_amount = 0

    for order in sorted_list:
        print("RELEVANT ERROR ID")
        print(order.laxout_exercise_id)
        try:
            exercise = models.Laxout_Exercise.objects.get(id=order.laxout_exercise_id)
            for skipped_exercis in skipped_exercises:

             if exercise.id == skipped_exercis.skipped_exercise_id:
                skipped_amount += 1
                print(skipped_amount)

            users_exercises_skipped.append(
            ExercisesModel(
                new_added=exercise.added,
                new_appId=exercise.appId,
                new_dauer=exercise.dauer,
                new_execution=exercise.execution,
                new_imagePath=exercise.imagePath,
                new_instruction=exercise.instruction,
                new_looping=exercise.looping,
                new_name=exercise.name,
                new_required=exercise.required,
                new_timer=exercise.timer,
                new_videoPath=exercise.videoPath,
                new_skippedAmount=skipped_amount,
                new_id=exercise.id,
            )
        )
            skipped_amount = 0

            skipped_amount = 0
        except:
            print("EXEPTION THROUGH DELETE AFTER AI GENERATION OF EXERCISES")
    
    
    print(
        "LENGHT EXERCISE LIST {}".format(users_exercises_skipped)
    )  # sie heißen nur skipped weil die skipped logik drinnen steckt, sind aber die ganz normalen Übungen
    print("Exercise ids from user with note:{}".format(user.note))
    for i in users_exercises_skipped:
        print(i.appId)
    laxout_user_pains_instances = models.LaxoutUserPains.objects.filter(created_by=id)
    index_labels = []
    month_year_instances = []
    zero_two_pain = []
    theree_five_pain = []
    six_eight_pain = []
    nine_ten_pain = []

    for she in laxout_user_pains_instances:
        append_she = True
        for i in month_year_instances:
            if i.for_month == she.for_month and i.for_year == she.for_year:
                append_she = False

        if append_she:
            index_labels.append(she.for_month)
            month_year_instances.append(she)

    for i in month_year_instances:
        current_pains = models.LaxoutUserPains.objects.filter(
            created_by=i.created_by, for_month=i.for_month, for_year=i.for_year
        )
        six_eight = 0
        zero_two = 0
        three_five = 0
        nine_ten = 0
        for ii in current_pains:
            six_eight = six_eight + ii.six_eight
            zero_two = zero_two + ii.zero_two
            three_five = three_five + ii.theree_five
            nine_ten = nine_ten + ii.nine_ten
        zero_two_pain.append(zero_two)
        theree_five_pain.append(three_five)
        six_eight_pain.append(six_eight)
        nine_ten_pain.append(nine_ten)

    average_pain_list_user = []
    for i in range(len(zero_two_pain)):
        average_pain = 0
        average_pain += zero_two_pain[i]
        average_pain += theree_five_pain[i]
        average_pain += six_eight_pain[i]
        average_pain += nine_ten_pain[i]
        average_pain = average_pain / 4
        average_pain_list_user.append(average_pain)

    better_success_controll_count = len(
        models.SuccessControll.objects.filter(created_by=user.id, better=True)
    )
    worse_success_controll_count = len(
        models.SuccessControll.objects.filter(created_by=user.id, better=False)
    )

    context = {
        "user": user,
        "users": user,
        "workouts": users_exercises_skipped,
        "userIndexes": json.dumps(users_indexes),
        "labels": json.dumps(labels),
        "workoutDates": json.dumps(workout_dates),
        "lastMeet": json.dumps(last_meet),
        "index_labels": json.dumps(index_labels),
        # "test": json.dumps(indexes),
        "zero_two_pain": json.dumps(zero_two_pain),
        "three_five_pain": json.dumps(theree_five_pain),
        "six_eight_pain": json.dumps(six_eight_pain),
        "nine_ten_pain": json.dumps(nine_ten_pain),
        "int": user.instruction_in_int,
        "better": better_success_controll_count,
        "worse": worse_success_controll_count,
    }

    return render(
        request,
        "laxout_app/edit_user.html",
        context,
    )


def get_workout_list(first, second):
    to_return = []
    uebungen_to_append = []
    exercises_to_browse = models.Uebungen_Models.objects.all()
    # Nacken
    if first == 0 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)

    if first == 0 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 0 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 0 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=0).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Schultern
    if first == 1 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 1 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 1 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 1 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=1).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # mittlerer Rücken
    if first == 2 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 2 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 2 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 2 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=2).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # bauch rumpf
    if first == 3 and second == 0:
        uebungen_to_append = []
    if first == 3 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=3).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 3 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=3).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 3 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=3).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Unterer Rücken
    if first == 4 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 4 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 4 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)

    if first == 4 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=4).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Beine Füße
    if first == 5 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 5 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 5 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)
    if first == 5 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=5).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)
    # Arme Hände

    if first == 6 and second == 0:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=0).exists()
            ):
                to_return.append(i)
    if first == 6 and second == 1:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=1).exists()
            ):
                to_return.append(i)
    if first == 6 and second == 2:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=2).exists()
            ):
                to_return.append(i)

    if first == 6 and second == 7:
        for i in exercises_to_browse:
            all_firsts = i.first.all()
            all_second = i.second.all()
            if (
                all_firsts.filter(first=6).exists()
                and all_second.filter(second=7).exists()
            ):
                to_return.append(i)

    return to_return


@login_required(login_url="login")
def add_exercises(request, id=None, first=0, second=0):
    print("ececuted")
    workout_list = []
    if request.method == "GET":
        first = request.GET.get("first", 0)
        second = request.GET.get("second", 0)
        print(first)
        print(second)
        workout_list = get_workout_list(int(first), int(second))
        print("handled request")
        print(workout_list)
        return render(
            request, "laxout_app/add_exercises.html", {"workouts": workout_list}
        )
    if request.method == "POST":
        new_execution = request.POST.get("execution")
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        new_id = request.POST.get("id")
        print(new_dauer)
        if new_dauer == "":
            new_dauer = Uebungen_Models.objects.get(id=new_id).dauer

        user_instance = LaxoutUser.objects.get(id=id)

        current_exercises = user_instance.exercises.all()
        if len(current_exercises) != 0:
            models.SuccessControll.objects.filter(created_by=user_instance.id).delete()
        current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
            laxout_user_id=id
        )  # es wird geschaut, ob es schon eine Reihenfolge gibt
        if len(current_order_objects) == 0 and len(current_exercises) != 0:
            print("There was a diffenrence")
            order = 1
            for i in current_exercises:
                models.Laxout_Exercise_Order_For_User.objects.create(
                    laxout_user_id=id, laxout_exercise_id=i.id, order=order
                )
                order += 1
            print("length")
            print(len(models.Laxout_Exercise_Order_For_User.objects.all()))

        lenght_order_objects_list = len(current_order_objects)

        print("LENGTH ORDER OBJECTS{}".format(len(current_order_objects)))

        exercise_to_add = Laxout_Exercise.objects.create(
            execution=new_execution,
            name=Uebungen_Models.objects.get(id=new_id).name,
            dauer=new_dauer,
            videoPath=Uebungen_Models.objects.get(id=new_id).videoPath,
            looping=Uebungen_Models.objects.get(id=new_id).looping,
            added=False,
            instruction="",
            timer=Uebungen_Models.objects.get(id=new_id).timer,
            required=Uebungen_Models.objects.get(id=new_id).required,
            imagePath=Uebungen_Models.objects.get(id=new_id).imagePath,
            appId=new_id,
            onlineVideoPath=Uebungen_Models.objects.get(id=new_id).onlineVideoPath,
        )
        order_new_exercise = len(current_order_objects) + 1

        models.Laxout_Exercise_Order_For_User.objects.create(
            laxout_user_id=id,
            laxout_exercise_id=exercise_to_add.id,
            order=order_new_exercise,
        )

        print(exercise_to_add.dauer)
        exercise_to_add.save()
        user_instance.exercises.add(exercise_to_add)
        if request.user == user_instance.created_by:
            user_instance.save()

    workout_list = get_workout_list(0, 0)
    return render(
        request,
        "laxout_app/add_exercises.html",
        {"workouts": workout_list, "userId": id},
    )


@login_required(login_url="login")
def edit_user_workout(
    request,
    id=None,
):
    if request.method == "POST":
        new_execution = request.POST.get("execution")
        print("new execution:{}".format(new_execution))
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        new_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        print("new dauer:{}".format(new_dauer))
        print("new id:{}".format(new_id))
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(id=new_id)
        if new_execution:
            exercise_to_edit.execution = new_execution
        if new_dauer:
            exercise_to_edit.dauer = new_dauer
        exercise_to_edit.save()
        user_instance.save()
        models.SuccessControll.objects.filter(created_by=user_instance.id).delete()
    return render(
        request,
        "laxout_app/edit_user.html",
    )


@login_required(login_url="login")
def delete_user_workout(
    request,
    id=None,
):
    if request.method == "POST":
        to_delete_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(
            id=to_delete_id
        )  # <---- kann ich so auf die Übung zugreifen, die ich bearbeiten möchte ?
        if request.user == user_instance.created_by:
            exercise_to_edit.delete()
            user_instance.save()
            print("to delete id")
            print(to_delete_id)
            to_delete = models.Laxout_Exercise_Order_For_User.objects.get(
                laxout_exercise_id=to_delete_id, laxout_user_id=user_id
            )
            to_delete.delete()

            list_order_exercises = models.Laxout_Exercise_Order_For_User.objects.filter(
                laxout_user_id=id
            )
            if len(list_order_exercises) != 0:
                right_order_exercises = []
                for i in list_order_exercises:
                    right_order_exercises.append(
                        models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
                    )

                sorted_list = sorted(right_order_exercises, key=lambda x: x.order)
                order = 1
                for i in sorted_list:
                    instance = models.Laxout_Exercise_Order_For_User.objects.get(
                        laxout_exercise_id=i.laxout_exercise_id,
                        laxout_user_id=i.laxout_user_id,
                    ).order = order
                    instance.save()
                    order += 1
            models.SuccessControll.objects.filter(created_by=user_instance.id).delete()
    return render(
        request,
        "laxout_app/edit_user.html",
    )


def days_between_today_and_date(input_datetime):
    # Assuming last_login_2 is stored in the same timezone as the server
    input_datetime = input_datetime.replace(tzinfo=None)  # Make it naive
    current_datetime = datetime.now()

    time_difference = current_datetime - input_datetime
    days_difference = time_difference.days

    return days_difference


@login_required(login_url="login")
def analyses(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    # how many users
    users = LaxoutUser.objects.filter(created_by=request.user)
    user_amount = users.count()
    user_indexes = IndexesLaxoutUser.objects.filter(
        created_by=request.user.id, creation_date=datetime.now().month
    )
    devide_by = len(user_indexes)
    devide = 0

    for user_index in user_indexes:
        devide += user_index.index

    if devide == 0:
        physio_index = 0

    else:
        physio_index = devide / devide_by

    if physio_index == None:
        physio_index = 0
        print("physio index was none")

    active_user_amount = 0

    for user in users:
        print(str(user.last_login_2.date) + "Last Login date")
        if days_between_today_and_date(user.last_login_2) < 14:
            active_user_amount += 1

    all_physio_indexes = IndexesPhysios.objects.filter(
        for_month=datetime.now().month,
        created_by=request.user.id,
        for_year=datetime.now().year,
    )

    if len(all_physio_indexes) != 0:
        current_physio_index_object = all_physio_indexes[len(all_physio_indexes) - 1]
    if len(all_physio_indexes) == 0:
        try:
            PhysioIndexCreationLog.objects.get(
                created_by=request.user.id,
                for_month=datetime.now().month,
                for_year=datetime.now().year,
            )
        except:
            current_physio_index_object = IndexesPhysios.objects.create(
                for_month=datetime.now().month, created_by=request.user.id
            )
            PhysioIndexCreationLog.objects.create(created_by=request.user.id)

    current_physio_index_object.indexs = physio_index
    current_physio_index_object.save()

    logins = current_physio_index_object.logins
    tests = current_physio_index_object.tests
    # tests = 0
    # logins = 0

    all_instances = IndexesPhysios.objects.filter(created_by=request.user.id)

    substitude_instances = []
    counter = 0
    if len(all_instances) > 10:
        for insteance in all_instances:
            if counter > len(all_instances) - 10:
                substitude_instances.append(insteance)
            counter += 1
        all_instances = substitude_instances

    indexes = []
    index_labels = []
    laxout_user_pains_instances = LaxoutUserPains.objects.filter(
        admin_id=request.user.id
    )
    month_year_instances = []
    zero_two_pain = []
    theree_five_pain = []
    six_eight_pain = []
    nine_ten_pain = []

    print("LENGHT Pains LIST {}".format(len(laxout_user_pains_instances)))

    for she in laxout_user_pains_instances:
        append_month_year = True
        for i in month_year_instances:
            if i.for_month == she.for_month and i.for_year == she.for_year:
                append_month_year = False

        if append_month_year:
            month_year_instances.append(she)
            index_labels.append(she.for_month)

    for i in month_year_instances:
        current_pains = models.LaxoutUserPains.objects.filter(
            created_by=i.created_by, for_month=i.for_month, for_year=i.for_year
        )
        six_eight = 0
        zero_two = 0
        three_five = 0
        nine_ten = 0

        for ii in current_pains:
            six_eight = six_eight + ii.six_eight
            zero_two = zero_two + ii.zero_two
            three_five = three_five + ii.theree_five
            nine_ten = nine_ten + ii.nine_ten
        zero_two_pain.append(zero_two)
        theree_five_pain.append(three_five)
        six_eight_pain.append(six_eight)
        nine_ten_pain.append(nine_ten)

    print("9-10{}".format(nine_ten_pain))
    print("8-6{}".format(six_eight_pain))
    print("3-5{}".format(theree_five_pain))
    print("0-2{}".format(zero_two_pain))

    context = {
        "user_amount": user_amount,
        "active_user_amount": active_user_amount,
        "logins": logins,
        "tests": tests,
        "index_labels": json.dumps(index_labels),
        "test": json.dumps(indexes),
        "zero_two_pain": json.dumps(zero_two_pain),
        "three_five_pain": json.dumps(theree_five_pain),
        "six_eight_pain": json.dumps(six_eight_pain),
        "nine_ten_pain": json.dumps(nine_ten_pain),
        "is_superuser": active_admin_user.is_superuser,
    }
    return render(request, "laxout_app/analyses.html", context)


@login_required(login_url="login")
def post_user_instruction(request, id=None):
    new_instruction = request.POST.get("instruction")
    user_insance = LaxoutUser.objects.get(id=id)
    user_insance.instruction = new_instruction
    user_insance.save()
    return HttpResponse("All clear")


@login_required(login_url="login")
def post_user_mail(request, id=None):
    new_mail = request.POST.get("mail")
    user_insance = LaxoutUser.objects.get(id=id)
    user_insance.email_adress = new_mail
    user_insance.save()
    return HttpResponse("All clear")


class UebungList:
    def __init__(
        self,
        looping,
        timer,
        execution,
        name,
        videoPath,
        dauer,
        imagePath,
        added,
        instruction,
        required,
        onlineVidePath,
    ):
        self.looping = looping
        self.timer = timer
        self.execution = execution
        self.name = name
        self.videoPath = videoPath
        self.dauer = dauer
        self.imagePath = imagePath
        self.added = added
        self.instruction = instruction
        self.required = required
        self.onlineVidePath = onlineVidePath


@login_required(login_url="login")
def admin_power(request):

    # for i in models.LaxoutUser.objects.all():
    #     laxout_tree = models.LaxTree.objects.create()
    #     i.lax_tree_id = laxout_tree.id
    #     i.save()
    server_tasks.manage_lax_trees()
    server_tasks.send_emails()

    return HttpResponse("all clear")


@login_required(login_url="login")
def move_up(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        user = models.LaxoutUser.objects.get(id=id)
        item_to_move_up = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, laxout_exercise_id=exercise_id
        )
        if item_to_move_up.order == 1:
            return HttpResponse("INVALID MOVE UP: FIRST ITEM IN LIST")
        order_to_move_up = item_to_move_up.order
        order_to_move_down = item_to_move_up.order - 1
        item_to_move_down = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, order=order_to_move_down
        )
        item_to_move_up.order = order_to_move_down
        item_to_move_up.save()
        item_to_move_down.order = order_to_move_up
        item_to_move_down.save()

        context = {"exercises": user.exercises.all()}
        return render(request, "laxout_app/edit_user.html", context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def move_down(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        user = models.LaxoutUser.objects.get(id=id)
        item_to_move_down = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, laxout_exercise_id=exercise_id
        )
        if item_to_move_down.order == len(
            models.Laxout_Exercise_Order_For_User.objects.filter(laxout_user_id=id)
        ):
            return HttpResponse("INVALID MOVE UP: FIRST ITEM IN LIST")

        order_to_move_down = item_to_move_down.order
        order_to_move_up = item_to_move_down.order + 1

        item_to_move_up = models.Laxout_Exercise_Order_For_User.objects.get(
            laxout_user_id=id, order=order_to_move_up
        )

        item_to_move_up.order = order_to_move_down
        item_to_move_up.save()

        item_to_move_down.order = order_to_move_up
        item_to_move_down.save()

        context = {"exercises": user.exercises.all()}
        return render(request, "laxout_app/edit_user.html", context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def set_instruction_int(request):
    try:
        user = models.LaxoutUser.objects.get(id=request.POST.get("id"))
        print(user.id)
        instruction_int = request.POST.get("int")
        print(instruction_int)
        user.instruction_in_int = instruction_int
        user.save()
        return HttpResponse("OK 2_0_0")
    except:
        print(Exception)
        print("Kacke")
        return HttpResponse("ERROR INTERNAL 4_0_4")
