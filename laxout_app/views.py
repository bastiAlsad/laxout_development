from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import (
    LaxoutUser,
    Laxout_Exercise,
    IndexesLaxoutUser,
    IndexesPhysios,
    DoneWorkouts,
    SkippedExercises,
)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
import random
import string
from django.contrib.auth import logout, authenticate, login
from datetime import datetime
import json
from django.utils import timezone


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
        new_id
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
    }
    return render(request, "laxout_app/home.html", context)


@login_required(login_url="login")
def create_user(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            insteance = form.save(commit=False)
            insteance.created_by = request.user
            insteance.save()
            return redirect("/home")

    else:
        form = UserForm()
        return render(request, "laxout_app/create_user.html", {"form": form})


@login_required(login_url="login")
def delete_user(request, id=None):
    if id != None:
        object_to_delte = LaxoutUser.objects.get(id=id)
        if request.user == object_to_delte.created_by:
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

    users_exercises = user.exercises.all()
    skipped_exercises_instances = SkippedExercises.objects.all()
    skipped_exercises = []
    skipped_amount = 0
    users_exercises_skipped = []

    for insteance in skipped_exercises_instances:
        try:
            search_contains = users_exercises.get(appId=insteance.skipped_exercise_id)
        except:
            search_contains = None
        if insteance.laxout_user_id == user.id and search_contains != None:
            skipped_exercises.append(insteance)



    for exercise in users_exercises:
        for skipped_exercis in skipped_exercises:
            if exercise.appId == skipped_exercis.skipped_exercise_id:
                skipped_amount += 1
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


    context = {
        "user": user,
        "users": user,
        "workouts": users_exercises_skipped,
        "userIndexes": json.dumps(users_indexes),
        "labels": json.dumps(labels),
        "workoutDates": json.dumps(workout_dates),
        "lastMeet": json.dumps(last_meet),
    }

    return render(
        request,
        "laxout_app/edit_user.html",
        context,
    )


def get_workout_list(first, second):
    to_return = []
    uebungen_to_append = []
    if first == 0 and second == 0:
        uebungen_to_append = [1, 2, 3, 23, 48, 49]
    if first == 0 and second == 1:
        uebungen_to_append = [24, 25, 27, 28]
    if first == 0 and second == 2:
        uebungen_to_append = [4, 5, 19, 20, 21, 22]
    if first == 1 and second == 0:
        uebungen_to_append = [1, 29, 30, 31, 41, 43, 44, 45, 46, 47, 48, 49, 67]
    if first == 1 and second == 1:
        uebungen_to_append = [26, 29, 37, 38, 39, 41, 42, 43, 64, 65, 66, 68, 69, 70]
    if first == 1 and second == 2:
        uebungen_to_append = [6, 7, 8, 9, 32, 33, 34, 35, 36]
    if first == 2 and second == 0:
        uebungen_to_append = [14, 117, 18, 105, 106, 107, 108, 109, 110]
    if first == 2 and second == 1:
        uebungen_to_append = [38, 96, 10, 103]
    if first == 2 and second == 2:
        uebungen_to_append = [15, 16, 94, 95]
    if first == 3 and second == 0:
        uebungen_to_append = []
    if first == 3 and second == 1:
        uebungen_to_append = [
            66,
            97,
            102,
            119,
            120,
            121,
            122,
            123,
            124,
            125,
            126,
            127,
            128,
            141,
        ]
    if first == 3 and second == 2:
        uebungen_to_append = [92, 93, 94, 95, 96, 112, 113, 114, 115, 116, 117, 118]
    if first == 4 and second == 0:
        uebungen_to_append = [
            10,
            11,
            105,
            106,
            107,
            108,
            134,
            142,
            143,
            144,
            145,
            146,
            147,
            158,
            165,
            166,
        ]
    if first == 4 and second == 1:
        uebungen_to_append = [
            97,
            98,
            99,
            100,
            101,
            102,
            103,
            124,
            135,
            136,
            137,
            138,
            139,
            140,
            141,
            158,
            165,
            166,
        ]
    if first == 4 and second == 2:
        uebungen_to_append = [
            12,
            13,
            94,
            95,
            112,
            113,
            114,
            115,
            117,
            118,
            129,
            130,
            131,
            132,
            133,
            134,
            148,
            149,
        ]
    if first == 5 and second == 0:
        uebungen_to_append = [40, 67, 104, 156, 158, 161, 162, 163, 164, 165]
    if first == 5 and second == 1:
        uebungen_to_append = [
            123,
            139,
            156,
            157,
            158,
            159,
            160,
            161,
            162,
            163,
            164,
            165,
            166,
            167,
            168,
        ]
    if first == 5 and second == 2:
        uebungen_to_append = [148, 149, 150, 151, 152, 153, 154, 155, 166, 168]
    if first == 6 and second == 0:
        uebungen_to_append = [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 63, 169]
    if first == 6 and second == 1:
        uebungen_to_append = [64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77]
    if first == 6 and second == 2:
        uebungen_to_append = [
            60,
            61,
            67,
            78,
            79,
            80,
            81,
            82,
            83,
            84,
            85,
            86,
            87,
            88,
            89,
            90,
            91,
            111,
        ]

    uebungen = Laxout_Exercise.objects.all()
    for i in uebungen:
        for z in uebungen_to_append:
            if i.id == z:
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
        user_instance = LaxoutUser.objects.get(id=id)
        exercise_to_add = Laxout_Exercise()
        exercise_to_add.execution = new_execution
        exercise_to_add.name = Laxout_Exercise.objects.get(id=new_id).name
        exercise_to_add.dauer = Laxout_Exercise.objects.get(id=new_id).dauer
        exercise_to_add.videoPath = Laxout_Exercise.objects.get(id=new_id).videoPath
        exercise_to_add.looping = Laxout_Exercise.objects.get(id=new_id).looping
        exercise_to_add.added = Laxout_Exercise.objects.get(id=new_id).added
        exercise_to_add.instruction = Laxout_Exercise.objects.get(id=new_id).instruction
        exercise_to_add.timer = Laxout_Exercise.objects.get(id=new_id).timer
        exercise_to_add.required = Laxout_Exercise.objects.get(id=new_id).required
        exercise_to_add.imagePath = Laxout_Exercise.objects.get(id=new_id).imagePath
        exercise_to_add.appId = new_id
        if new_dauer:
            exercise_to_add.dauer = new_dauer
        print(exercise_to_add.dauer)
        exercise_to_add.save()
        user_instance.exercises.add(exercise_to_add)
        if request.user == user_instance.created_by:
            user_instance.save()

    workout_list = get_workout_list(0, 0)
    return render(request, "laxout_app/add_exercises.html", {"workouts": workout_list})


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
        exercise_to_edit = user_instance.exercises.get(
            id=new_id
        )  
        if new_execution:
            exercise_to_edit.execution = new_execution
        if new_dauer:
            exercise_to_edit.dauer = new_dauer
        exercise_to_edit.save()
        user_instance.save()
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
        new_id = request.POST.get("id")
        user_id = request.POST.get("userId")
        user_instance = LaxoutUser.objects.get(id=user_id)
        exercise_to_edit = user_instance.exercises.get(
            id=new_id
        )  # <---- kann ich so auf die Übung zugreifen, die ich bearbeiten möchte ?
        if request.user == user_instance.created_by:
            exercise_to_edit.delete()
            user_instance.save()
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
    physio_index = devide / devide_by
    physio_instance = request.user
    try:
        physio_index_instance = IndexesPhysios.objects.get(
            for_month=datetime.now().month
        )
        physio_index_instance.indexs = physio_index
        physio_index_instance.save()
    except:
        IndexesPhysios.objects.create(created_by=physio_instance.id, logins=1)

    # how many active users
    active_user_amount = 0
    for user in users:
        print(str(user.last_login_2.date) + "Last Login date")
        if days_between_today_and_date(user.last_login_2) < 14:
            active_user_amount += 1

    logins = IndexesPhysios.objects.get(
        created_by=request.user.id, for_month=datetime.now().month
    ).logins
    tests = IndexesPhysios.objects.get(
        created_by=request.user.id, for_month=datetime.now().month
    ).tests

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
    zero_two_pain = []
    theree_five_pain = []
    six_eight_pain = []
    nine_ten_pain = []

    for she in all_instances:
        index_labels.append(she.for_month)

    for it in all_instances:
        indexes.append(it.indexs)

    for he in all_instances:
        zero_two_pain.append(he.zero_two)

    for we in all_instances:
        theree_five_pain.append(we.theree_five)

    for they in all_instances:
        six_eight_pain.append(they.six_eight)

    for me in all_instances:
        nine_ten_pain.append(me.nine_ten)

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
    }
    return render(request, "laxout_app/analyses.html", context)


@login_required(login_url="login")
def post_user_instruction(request, id = None):
    new_instruction = request.POST.get("instruction")
    user_insance = LaxoutUser.objects.get(id = id)
    user_insance.instruction = new_instruction
    user_insance.save()
    return HttpResponse("All clear")