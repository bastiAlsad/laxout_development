from django.shortcuts import render
from string import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

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
from .leistungsnachweise import pdf
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


def send_user_welcome_email(email, user_uid):
    # SMTP-Verbindungsinformationen
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'laxoutapp@gmail.com'
    smtp_password = 'aliy rfnz mtmx xwif'

    # E-Mail-Inhalte
    sender_email = 'laxoutapp@gmail.com'
    receiver_email = email
    subject = 'Herzlich Willkommen'
    link = f"https://dashboardlaxout.eu.pythonanywhere.com/laxout/show-login-code/{user_uid}"

    # HTML-Inhalt der E-Mail
    html_template = Template("""
    <!DOCTYPE html>
    <html lang="de">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Willkommen bei Unsere Firma</title>
        <style>
            .wave {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: auto;
                z-index: -1;
            }
        </style>
    </head>

    <body style="font-family: Arial, sans-serif; position: relative;">

        <!-- Wellenförmige Trennlinie -->
        <svg class="wave" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
            <path fill="rgb(243, 242, 244)" fill-opacity="1"
                d="M0,224L48,234.7C96,245,192,267,288,240C384,213,480,139,576,138.7C672,139,768,213,864,229.3C960,245,1056,203,1152,170.7C1248,139,1344,117,1392,106.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1048,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z">
            </path>
        </svg>
        <!-- Firmenlogo -->
        <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="https://laxoutapp.com/wp-content/uploads/elementor/thumbs/Original-on-Transparent-2-Kopie-qdvaef4t4wosp4blnwuth1860qdc3tupxko88fkwvo.png"
                    alt="Firmenlogo" style="max-width: 200px;">
            </div>

            <!-- Willkommensnachricht -->
            <div style="text-align: center; margin-bottom: 20px;">
                <h1>Willkommen!</h1>
                <p>Vielen Dank für Ihre Anmeldung bei Laxout. Wir freuen uns, Sie als Nutzer unserer App begrüßen zu dürfen.
                </p>
                <p>Für die Nutzung der App bitten wir Sie, den im Leistungsnachweis (befindet sich im Anhang) genannten
                    Betrag an unser Firmenkonto zu überweisen.</p>
                <p>Dannach können Sie auch schon auf den <a href="${link}" style=" color: blue;">Loslegen</a> Button drücken und mit Ihrem Training beginnen!</p>
                <div style="text-align: center; margin: 50px;">
                    <button
                        style="height: 50px; width: 140px; border-radius: 10px; background-color: rgb(176, 224, 230); color: black; cursor: pointer; border: none;">
                        <a href="${link}" style="text-decoration: none; color: white;">Loslegen</a>
                    </button>
                </div>
                <p>Viel Spaß wünscht Ihnen</p>
                <br>
                <p>Ihr Laxout-Team</p>
            </div>

            <!-- Social-Media-Icons -->
            <div style="display: flex; justify-content: center; margin: 40px;">
                <div style="margin-right: 20px;">
                    <a href="https://www.linkedin.com/company/laxout/">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor"
                            class="bi bi-linkedin" viewBox="0 0 16 16">
                            <path fill="rgb(0,0,0)"
                                d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                        </svg>
                    </a>
                </div>
                <div>
                    <a href="https://www.instagram.com/laxoutapp/">
                        <svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" fill="currentColor"
                            class="bi bi-instagram" viewBox="0 0 16 16">
                            <path fill="rgb(0,0,0)"
                                d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334" />
                        </svg>
                    </a>
                </div>
            </div>

            <!-- Footer-Text -->
            <small style="text-align: center; margin-bottom: 50px;">©2024 Laxout, Steffen Friedrich, Firmensitz: Brünnsteinstraße 49, 85435
                Erding. Alle Rechte vorbehalten.</small>
        </div>


    </body>

    </html>
    """)

    # Erstellen der MIME-Multipart-Nachricht
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Hinzufügen des HTML-Inhalts zur Nachricht
    html_content = html_template.substitute(link=link)
    msg.attach(MIMEText(html_content, 'html'))
    billing_model, created = models.BillingCount.objects.get_or_create(id=1)
    billing_count = str(billing_model.billing_count)
    new_billing_count = billing_model.billing_count+1
    billing_model.billing_count = new_billing_count
    billing_model.save()
    current_billing_id = ""
    how_many_zeros = 12-len(billing_count)
    for i in range(how_many_zeros):
        current_billing_id+= "0"
    current_billing_id+= billing_count
    #Produktion
    #/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/ 
    #Dev
    #D:/DEV/laxout_backend_development/laxout/laxout_app/leistungsnachweise/
    print(f"Current billing Id {current_billing_id}")
    input_pdf_path = "/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_vorlage.pdf"  # Passe den Pfad zur vorhandenen PDF-Datei an D:/DEV/laxout_backend_development/laxout/laxout_app/leistungsnachweise/leistungsnachweis
    output_pdf_path = f"/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_{current_billing_id}.pdf"  # Passe den Pfad für die neu erstellte PDF-Datei an
    pdf.modifyPdf(input_pdf_path,output_pdf_path,current_billing_id)

    # Pfad zur PDF-Datei
    pdf_attachment_path = f"/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_{current_billing_id}.pdf"

    # Hinzufügen der PDF-Datei als Anhang
    with open(pdf_attachment_path, 'rb') as pdf_attachment:
        part = MIMEApplication(pdf_attachment.read(), 'pdf')
        part.add_header('Content-Disposition', f'attachment; filename= {pdf_attachment_path}')
        msg.attach(part)

    # SMTP-Verbindung und Versenden der E-Mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    



    # sender = "laxoutapp@gmail.com"
    # password = "aliy rfnz mtmx xwif"
    # subject = "Herzlich Willkommen bei Laxout"
    # link = f"https://dashboardlaxout.eu.pythonanywhere.com/laxout/show-login-code/{user_uid}"
    # body = f"Hallo, \nschön dass sie sich für Laxout entschieden haben ! \nSie erhalten Ihr individuelles Workout, indem Sie die App über folgenden Link herunterladen:\n{link} \nAußerdem benötigt Laxout während des Anmeldeprozesses außerdem Zugriff auf Ihre Zwischenablage des Smartphones.\n \nViel Erfolg wünscht Ihnen Ihr Laxout-Team "
    # reciever = email
    # message = MIMEMultipart()
    # message["From"] = sender
    # message["Subject"] = subject
    # message.attach(MIMEText(body, "plain"))
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(sender, password)
    # text = message.as_string()
    # server.sendmail(sender, reciever, text)
    # server.quit()

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
            insteance.save()
            email = form.cleaned_data.get("email_adress")
            print("Sfjashfkashfkjashfkjs")
            note = request.POST.get("selected_illness")
            if form.cleaned_data.get("note") is "":
                print("Note was None")
                insteance.note = note
            insteance.save()
            # lax_ai.train_model(request.user.id)
            # predicted_exercises_ids = lax_ai.predict_exercise(note)

            exercises = []
            print(f"note{note}")

            ai_training_data = models.AiTrainingData.objects.filter(illness=note).last()

            # , created_by=request.user.id

            if ai_training_data != None:
                predicted_exercises_ids = []

                for i in ai_training_data.related_exercises.all():
                    predicted_exercises_ids.append(i.exercise_id)

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
            # print(lax_ai.predict_exercise(note))
            send_user_welcome_email(email, insteance.user_uid)
            models.ChatDataModel.objects.create(message = "Willkommen bei der Laxout Chat funktion. Sollten Sie Fragen zur App oder zu Übungen haben, können Sie diese hier stellen. Viel Spaß beim benutzen der App!", created_by = insteance.id, admin_id = request.user.id)
            return redirect("/home")

    else:
        ilness_list_obj = models.AiTrainingData.objects.all()
        ilness_list = []
        for i in ilness_list_obj:
            if i.illness not in ilness_list:
                filterd_objects = ilness_list_obj.filter(illness=i.illness)
                item = filterd_objects.last()
                print(item.illness)
                ilness_list.append(item.illness)

        # for i in ilness_list_obj:
        #     ilness_list.append(i.illness)
        form = UserForm()
        return render(
            request,
            "laxout_app/create_user.html",
            {
                "form": form,
                "is_superuser": active_admin_user.is_superuser,
                "illness_list": ilness_list,
            },
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
    # if user.note != "":
    #     old_training_data = models.AiTrainingData.objects.filter(created_for=user.id)
    #     for i in old_training_data:
    #         i.related_exercises.all().delete()
    #     old_training_data.delete()
    #     ai_training_data = models.AiTrainingData.objects.create(
    #         illness=user.note, created_by=request.user.id, created_for=user.id
    #     )

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
        # print("RELEVANT ERROR ID")
        # print(order.laxout_exercise_id)
        try:
            # ai_training_data.related_exercises.add(
            #     models.AiExercise.objects.create(
            #         exercise_id=models.Laxout_Exercise.objects.get(
            #             id=order.laxout_exercise_id
            #         ).appId
            #     )
            # )
            print("Error in SOrted list wasnt caused due ai")
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

    # Train ai with the new data
    # lax_ai.train_model(request.user.id)

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


from . import signals


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


additionalUebungList2 = [  # Übnungen Papi
    UebungList(# 202
        looping=False,
        timer=True,
        execution="Gehen Sie in den Vierfüßlerstand. Positionieren Sie Ihre Hände auf Höhe der Schultern und Ihre Knie hüftbreit auseinander. Achten Sie darauf, den Bauch während der gesamten Übung anzuspannen.",
        name="Versteckter Liegestütz vorwärts",
        videoPath="assets/videos/verLiegestuetzVorwaerts.mp4",
        dauer=30,
        imagePath="assets/images/verLiegestuetzVorwaerts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="",
    ),
    UebungList(# 203
        looping=False,
        timer=True,
        execution="Gehen Sie in den Vierfüßlerstand. Positionieren Sie Ihre Hände auf Höhe der Schultern und Ihre Knie hüftbreit auseinander. Achten Sie darauf, den Bauch während der gesamten Übung anzuspannen.",
        name="Versteckter Liegestütz rückwärts",
        videoPath="assets/videos/verLiegestuetzRueckwaerts.mp4",
        dauer=30,
        imagePath="assets/images/verLiegestuetzRueckwaerts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="",
    ),
    UebungList(# 204
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren rechten Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Rückenstrecker im Einbeinstand rechts",
        videoPath="assets/videos/rueckenstreckerEinbeinR.mp4",
        dauer=30,
        imagePath="assets/images/rueckenstreckerEinbeinR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 205
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren linken Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Rückenstrecker im Einbeinstand links",
        videoPath="assets/videos/rueckenstreckerEinbeinL.mp4",
        dauer=30,
        imagePath="assets/images/rueckenstreckerEinbeinL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 206
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren rechten Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Brustwirbelsäule im Einbeistand rechts",
        videoPath="assets/videos/bwsEinbeinR.mp4",
        dauer=30,
        imagePath="assets/images/bwsEinbeinR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 207
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren linken Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Brustwirbelsäule im Einbeistand links",
        videoPath="assets/videos/bwsEinbeinL.mp4",
        dauer=30,
        imagePath="assets/images/bwsEinbeinL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 208
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und Drehen Sie die Daumen nach außen. Bringen Sie außerdem Ihre Schulterblätter zusammen und versuchen Sie während der Übung die Balance zu halten.",
        name="Kräftigung Hüfte im Einbeistand rechts",
        videoPath="assets/videos/kraeftigungHuefteEinbeinR.mp4",
        dauer=30,
        imagePath="assets/images/kraeftigungHuefteEinbeinR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 209
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und Drehen Sie die Daumen nach außen. Bringen Sie außerdem Ihre Schulterblätter zusammen und versuchen Sie während der Übung die Balance zu halten.",
        name="Kräftigung Hüfte im Einbeistand links",
        videoPath="assets/videos/kraeftigungHuefteEinbeinL.mp4",
        dauer=30,
        imagePath="assets/images/kraeftigungHuefteEinbeinL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 210
        looping=False,
        timer=True,
        execution="Gehen Sie in den Vierfüßler Stand auf einer Matte. Ihr Rücken muss gerade sein. Strecken Sie nun abwechselnd das rechte Bein und den linken Arm und das linke Bein und den rechten Arm aus. Strecken Sie so weit, dass sich eine Waagerechte zwischen Rücken, Arm und Bein bildet.",
        name="Kräftigung im Viefüßlerstand (schwer)",
        videoPath="assets/videos/kraeftigungVierfueßlerstandS.mp4",
        dauer=30,
        imagePath="assets/images/kraeftigungVierfueßlerstandS.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
]


uebungen_to_append00 = []  # Nacken
uebungen_to_append01 = []
uebungen_to_append02 = []
uebungen_to_append07 = []
uebungen_to_append10 = [206,207,210]  # Schultern
uebungen_to_append11 = []
uebungen_to_append12 = []
uebungen_to_append17 = [206,207,210]
uebungen_to_append20 = [202,203,204,205,206,207,210]  # Mittlerer Rücken
uebungen_to_append21 = [202, 203,204,205,206,207,210]
uebungen_to_append22 = []
uebungen_to_append27 = [202, 203,204,205,206,207,210]
uebungen_to_append30 = []  # Bauch Rumpf
uebungen_to_append31 = []
uebungen_to_append32 = []
uebungen_to_append37 = []
uebungen_to_append40 = [202,203,204,205,206,207,208,209,210]  # Unterer Rücken
uebungen_to_append41 = [202,203,204,205,206,207,208,209,210]
uebungen_to_append42 = []
uebungen_to_append47 = [202,203,204,205,206,207,208,209,210]
uebungen_to_append50 = []  # Beine Füße
uebungen_to_append51 = []
uebungen_to_append52 = []
uebungen_to_append57 = []
uebungen_to_append60 = []  # Arme Hände
uebungen_to_append61 = []
uebungen_to_append62 = []
uebungen_to_append67 = []


def inizialize_first_second():
    for i in uebungen_to_append00:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append01:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append02:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append07:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append10:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append11:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append12:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append17:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append20:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append21:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append22:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append27:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append30:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append31:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append32:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append37:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append40:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append41:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append42:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append47:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append50:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append51:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append52:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append57:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append60:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append61:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append62:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append67:
        instance_exercise = models.Uebungen_Models.objects.get(id=i)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
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


# Liste von Übungen
uebungen = [
    UebungList(
        looping=True,
        timer=True,
        execution="Führen Sie die Übung im aufrechten Stand durch und achten Sie auf eine gerade Wirbelsäule. Die Blikrichtung ist nach vorne.",
        name="Schulterblattkreisen",
        videoPath="assets/videos/schuterblattkreisen.mp4",
        dauer=30,
        imagePath="assets/images/schulterblattkreisen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath= "https://youtu.be/jFGkSAmt3jI",
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Wichtig ist, dass Sie aufrecht an der Stuhlkante sitzten und Ihre Schultern hängen lassen. Führen Sie die Übung bitte langsam aus.",
        name="Halbkreise Links",
        videoPath="assets/videos/Halbkreisnackenlinks.mp4",
        dauer=30,
        imagePath="assets/images/halbkreiseLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/44v3LKOQkVs"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Wichtig ist, dass Sie aufrecht an der Stuhlkante sitzten und Ihre Schultern hängen lassen. Führen Sie die Übung bitte langsam aus.",
        name="Halbkreise Rechts",
        videoPath="assets/videos/HalbkreisNackenrechts.mp4",
        dauer=30,
        imagePath="assets/images/halbkreiseRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/VtZs7yu_dyI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Gehen Sie langsam in die Dehnung, halten Sie sie und bewegen Sie Ihre Schultern nicht. Außerdem ist es gut, wenn Sie aufrecht sitzten und Sie den freien Arm in Richtung Boden bewegen. Sind Sie fertig mit der Übung, verlassen Sie die Dehnung bitte nicht zu schnell.",
        name="Dehnung Links Hinten",
        videoPath="assets/videos/nackenLinksHinten.mp4",
        dauer=30,
        imagePath="assets/images/nackenLinksHinten.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/gWu3B5UqHjU",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Gehen Sie langsam in die Dehnung, halten Sie sie und bewegen Sie Ihre Schultern nicht. Außerdem ist es gut, wenn Sie aufrecht sitzten und Sie den freien Arm in Richtung Boden bewegen. Sind Sie fertig mit der Übung, verlassen Sie die Dehnung bitte nicht zu schnell.",
        name="Dehnung Rechts Hinten",
        videoPath="assets/videos/nackenRechtsHinten.mp4",
        dauer=30,
        imagePath="assets/images/nackenRechtsHinten.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/x752jP5KfyU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Legen Sie Ihre Hände im geschätzen 45 Grad Winkel wie gezeigt an die Wand. Dannach machen Sie bitte einen Ausfallschritt nach vorne, woraufhin Sie Ihr Gewicht langsam nach vorne verlagern.",
        name="Schulterdehnung 45 Grad",
        videoPath="assets/videos/schulterdehnung.mp4",
        dauer=30,
        imagePath="assets/images/schulterdehnug45.png",
        added=False,
        instruction="",
        required="Wandecke",
        onlineVidePath="https://youtu.be/0xQiN5FbLEY",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Legen Sie Ihre Hände so hoch wie möglich an die Wand, wie als ob Sie jemand nach oben zieht. Dannach machen Sie bitte einen Ausfallschritt nach vorne, woraufhin Sie Ihr Gewicht langsam nach vorne verlagern.",
        name="Schulterdehnung 90 Grad",
        videoPath="assets/videos/schulterdehnungGerade.mp4",
        dauer=30,
        imagePath="assets/images/schulterdehnung90.png",
        added=False,
        instruction="",
        required="Wand/Tür",
        onlineVidePath="https://youtu.be/N9lxp4sA5EM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lassen Sie Ihren Nacken locker, wärend sich die Hände auf Gesäßhöhre verschränken. Die Schultern gehen nun hinten zusammen, während die Hände nach unten gezogen werden. Bitte gehen Sie langsam in diese Dehnung.",
        name="Aufrichten",
        videoPath="assets/videos/aufrichtenoberkoerper.mp4",
        dauer=30,
        imagePath="assets/images/aufrichten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/zqBmTOsSaO8"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Ihre Hände sind auf Brusthöhe, während Sie sich langsam nach vorne neigen, als ob jemand an deinen Unterarmen zieht. Stellen Sie sich vor, Sie wollten etwas vor Ihnen umarmen.",
        name="Bagger",
        videoPath="assets/videos/bagger.mp4",
        dauer=30,
        imagePath="assets/images/bagger.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/CgCJbMCpuU4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setze dich aufrecht an die Stuhlkante und beginne mit dem Becken zu kreisen. Der Oberkörper muss möglichst ruhig bleiben.",
        name="Bewegung Unterer Rücken",
        videoPath="assets/videos/beckenschaukel.mp4",
        dauer=30,
        imagePath="assets/images/bewegungUntererRuecken.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/oIpWIe1oeMU"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Sie schauen gerade nach oben zur Decke. Legen Sie Ihre Beine langsam und abwechselnd links und rechts zur Seite ab. Achten Sie hierbei darauf, dass sich Ihr Oberkörper nicht bewegt.",
        name="Hüftrollen",
        videoPath="assets/videos/Plumpsenrechtslinks.mp4",
        dauer=30,
        imagePath="assets/images/plumpsen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/NxWtZWNRwx0"
    ),

    UebungList(# kein Video
        looping=False,
        timer=True,
        execution="Du schaust gerade nach oben zur Decke. Dannach legst du deine Beine langsam zur Seite ab und hältst die Dehnung. Dabei bewegt sich dein Oberkörper nicht.",
        name="Dehnung Unterer Rücken rechts",
        videoPath="assets/videos/untererRueckenrechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnunUnterRueckenR.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Imm4kNNWtr8"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Du schaust gerade nach oben zur Decke. Dannach legst du deine Beine langsam zur Seite ab und hältst die Dehnung. Dabei bewegt sich dein Oberkörper nicht",
        name="Dehnung Unterer Rücken links",
        videoPath="assets/videos/untererRueckenlinks.mp4",
        dauer=30,
        imagePath="assets/images/DehnungUntererRueckenL.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/N3jNoQSuoos"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich so an die Stuhlkante, dass die Knie auseinander sind und Sie aufrecht sitzen. Bei der Drehnung darf sich das Becken nicht bewegen. Tipp nehmen Sie hierfür dine Hände, wie gezeigt vor die Brust.",
        name="Rotation Oberkörper",
        videoPath="assets/videos/rotationMittlererR.mp4",
        dauer=30,
        imagePath="assets/images/RotationOberkoerper.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/bM5QIh9G2hc"
    ),                                                                                                                                                                                                              
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich so an die Stuhlkante, dass die Knie auseinander sind und Sie aufrecht sitzen. Neigen Sie sich nun mit ausgestrecktem Arm zur Seite und versuchen Sie tief zu atmen. Schaun Sie dabei auf den Boden, der gerade vor Ihnen ist.",
        name="Seitliche Dehnung links",
        videoPath="assets/videos/seitlicheDehnunglins.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfdehnungLS.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/IZ0yEvc5SoU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich so an die Stuhlkante, dass die Knie auseinander sind und Sie aufrecht sitzen. Neigen Sie sich nun mit ausgestrecktem Arm zur Seite und versuchen Sie tief zu atmen. Schaun Sie dabei auf den Boden, der gerade vor Ihnen ist.",
        name="Seitliche Dehnung rechts",
        videoPath="assets/videos/seitlicheDehnungm.rechts.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfdehnungRS.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/LdaT-uqtkuA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lege dir für diese Übung am besten ein Kissen wie gezeigt unter. Dannach geht der ausgestreckte Arm zur anderen Seite, während du ihm nachschaust und dein Kopf sich mit ihm mitbewegt.",
        name="Brustwirbelsäule links",
        videoPath="assets/videos/brustwirbelsauleLinks.mp4",
        dauer=30,
        imagePath="assets/images/BrustwirbelsauleL.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/v4GZpH6C0uI"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Lege dir für diese Übung am besten ein Kissen wie gezeigt unter. Dannach geht der ausgestreckte Arm zur anderen Seite, während du ihm nachschaust und dein Kopf sich mit ihm mitbewegt.",
        name="Brustwirbelsäule rechts",
        videoPath="assets/videos/brustwirbelsauleRechts.mp4",
        dauer=30,
        imagePath="assets/images/BrustwirbelsauleR.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/NKQts1Ebsfw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht auf einen Stuhl. Legen Sie Ihre Hände an den Hinterkopf. Beugen Sie Ihren Nacken nach vorne und spüren Sie eine leichte Dehnung im Bereich der Halswirbelsäule. Bitte reißen Sie nicht an Ihrem Nacken.",
        name="Dehnung HWS hinten",
        videoPath="assets/videos/DehnungHwsHinten.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsHinten.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/ZVfJk2vkmJY"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Legen Sie rechte Hand ans linke Schlüsselbein. Neigen Sie Ihren Kopf langsam nach rechts hinten und spüren Sie die Dehnung im Bereich der Halswirbelsäule. Achten Sie auf einen geraden Rücken.",
        name="Dehnung HWS links vorne",
        videoPath="assets/videos/DehnungHwsLinksVorne.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsLinksVorne.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/nVhWy_Zo44A"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Legen Sie die linke Hand ans rechte Schlüsselbein. Neigen Sie Ihren Kopf langsam nach links hinten und spüren Sie die Dehnung im Bereich der Halswirbelsäule. Achten Sie auf einen geraden Rücken.",
        name="Dehnung HWS rechts vorne",
        videoPath="assets/videos/DehnungHwsRechtsVorne.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsRechtsVorne.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/KfnRkpDCNeM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Legen Sie eine Hand auf die Stirn. Neigen Sie Ihren Kopf langsam und vorsichtig nach hinten, um eine Dehnung im Bereich der Halswirbelsäule zu spüren. Achten Sie auf einen geraden Rücken. Seien Sie vorsichtig, um Schwindel zu vermeiden, und brechen Sie die Übung bei Bedarf ab.",
        name="Dehnung HWS vorne",
        videoPath="assets/videos/DehnungHwsVorne.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHwsVorne.png",
        added=False,
        instruction="",
        required="Stuhl mit Lehne",
        onlineVidePath="https://youtu.be/eBDLpqOF5Go"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Sitzen Sie aufrecht oder stehen Sie gerade. Neigen Sie den Kopf zur rechten Schulter, so weit wie es bequem ist, und halten Sie diese Position für 5 Sekunden. Gehen Sie zurück zur Ausgangsposition und wiederholen Sie die Übung auf der linken Seite. Führen Sie die Übung in der Geschwindigkeit wie vorgemacht aus und machen Sie die Übung 15 mal.",
        name="Nacken seitliche Neigungen",
        videoPath="assets/videos/NackenSeitlicheNeigungen.mp4",
        dauer=15,
        imagePath="assets/images/NackenSeitlicheNeigungen.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/7mz1mrMjQrw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Drücken Sie Ihre Handfläche gegen die Stirn und halten Sie den Kopf dabei stabil. Halten Sie den Widerstand für 5-10 Sekunden. Wiederholen Sie dies, indem Sie die Handflächen gegen die Seiten des Kopfes und den Hinterkopf drücken.",
        name="Nacken Kräftigung Drücken",
        videoPath="assets/videos/NackenDruecken.mp4",
        dauer=15,
        imagePath="assets/images/NackenKraeftigungDruecken.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/IhsZRVPnG_E"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie 2 Wasserflaschen in die Hände. Sitzen Sie aufrecht. Ziehen Sie Ihre Schultern in 2-3 Sekunden ca. 30-mal hoch und lassen Sie sie langsam absenken.",
        name="Schultern Hochziehen",
        videoPath="assets/videos/SchulternHochziehen.mp4",
        dauer=30,
        imagePath="assets/images/SchulternHochziehen.png",
        added=False,
        instruction="",
        required="2 Wasserflaschen",
        onlineVidePath="https://youtu.be/zWFyKhItfow"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Hinsetzen und nach vorne lehnen. Der Oberkörper bildet einen Winkel von ca. 45 Grad zu den Beinen. Heben Sie Ihre Arme beidseitig wie ein Vogel gerade nach oben. Führen Sie die Übung langsam aus. Optional: Verwenden Sie Gewichte.",
        name="Kräftigung Rotatoren",
        videoPath="assets/videos/KraeftigungRotatoren.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungRotatoren.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/OOTxwlqru78"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Setzen Sie Ihre rechte Hand auf einen Tisch. Stellen Sie Ihren Fuß auf der Seite, wo die Hand ist, einen Schritt nach vorne. Halten Sie eine Gewicht/Wasserflasche in der anderen Hand. Lehnen Sie sich leicht nach vorne. Ziehen Sie den Arm mit dem Gewicht möglichst nah am Körper und möglichst gerade zur Decke hoch.",
        name="Trapez Muskulatur links",
        videoPath="assets/videos/TrapezMuskulaturL.mp4",
        dauer=20,
        imagePath="assets/images/TrapezMuskulaturL.png",
        added=False,
        instruction="",
        required="Gewicht/Wasserflasche",
        onlineVidePath="https://youtu.be/UncBhm17jNg"

    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Setzen Sie Ihre linke Hand auf einen Tisch. Stellen Sie Ihren Fuß auf der Seite, wo die Hand ist, einen Schritt nach vorne. Halten Sie eine Gewicht/Wasserflasche in der anderen Hand. Lehnen Sie sich leicht nach vorne. Ziehen Sie den Arm mit dem Gewicht möglichst nah am Körper und möglichst gerade zur Decke hoch.",
        name="Trapez Muskulatur rechts",
        videoPath="assets/videos/TrapezMuskulaturR.mp4",
        dauer=20,
        imagePath="assets/images/TrapezMuskulaturR.png",
        added=False,
        instruction="",
        required="Gewicht/Wasserflasche",
        onlineVidePath="https://youtu.be/P8HFabQdJ54"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht. Die linke Schulter beginnt nun Kreise nach hinten zu machen. Leicht versetzt davon macht auch die rechte Schulter Kreise indem sie erst nach Oben, dann nach Hinten, dann nach unten und dann wieder zurück geht.",
        name="Schulterkreisen größer werden",
        videoPath="assets/videos/SchGroesser.mp4",
        dauer=30,
        imagePath="assets/images/SchulterkreisenGroeßerWerden.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/_-mvpirfTMU"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich aufrecht hin. Eine Hand (z.B. die linke Hand) berührt die rechte Schulter, während die andere Hand (rechts) den Bauch etwas oberhalb der Hüfte umfasst. Die Arme sind also wie bei einer Umarmung. Anschließend wechselt die linke Hand zum Bauch, während die rechte Hand die Schulter berührt. Diese Übung kann auch im Sitzen durchgeführt werden.",
        name="Verschränken Mobilisation Schultergürtel",
        videoPath="assets/videos/VerschraenkenMobilisationSchulterguertel.mp4",
        dauer=60,
        imagePath="assets/images/VerschraenkenMobilisationSchulterguertel.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/sEN1lli6lUo"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Machen Sie ein leichtes Hohlkreuz, wobei Sie das Brustbein anheben. Die Arme gehen nach oben, und die Unterarme bilden einen 90-Grad-Winkel mit den Oberarmen. Die Ellbogen verlaufen parallel zum Körper, und die Handflächen zeigen in einer offenen Position nach vorne und in einer geschlossenen Position zum Kopf. Atmen Sie beim Auseinanderbewegen der Ellenbogen ein und beim Zusammenführen der Ellenbogen aus. Im Verlauf der Übung können Sie das Tempo leicht steigern.",
        name="Mobilisation Schultergürtel",
        videoPath="assets/videos/MobilisationSchulterguertel.mp4",
        dauer=60,
        imagePath="assets/images/MobilisationSchulterguertel.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/gngSnM56xdM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf den Boden. Ihre Arme gehen hinter den Rücken auf den Boden, als ob Sie sich abstützen würden. Halten Sie Ihre Füße leicht angewinkelt. Ihre Ellenbogen bleiben gerade, während Sie Ihre Hände langsam nach hinten tippeln, bis sie eine Dehnung spüren. Dann drücken sie die Hände gegen den Boden, bis sie eine leichte bis mittelstarke Dehnung spüren. Führen Sie die Übung etwa 60 Sekunden aus. Achten Sie darauf, dass nur die Arme nach hinten gehen und der Schultergürtel fixiert bleibt.",
        name="Dehnung im Halbliegen",
        videoPath="assets/videos/DehnungImHalbliegen.mp4",
        dauer=60,
        imagePath="assets/images/DehnungImHalbliegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/YKStW6oT8bQ"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Liegen Sie mit dem Bauch auf einer Matte. Ihr Kopf ist nach rechts, oder links gedreht, und Ihre Arme sind etwa 45 Grad vom Körper seitlich ausgestreckt. Ziehen Sie Ihre Schultern nach außen aus den Schultergelenken, indem Sie mit den Fingerspitzen nach außen tippeln. Führen Sie die Übung etwa 60 Sekunden lang aus.",
        name="Dehnung in Bauchlage",
        videoPath="assets/videos/DehnungInBauchlage.mp4",
        dauer=60,
        imagePath="assets/images/DehnungInBauchlage.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/cmi1bekkkuE"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht. Ihr Ziel ist es jetzt, dass sich die Hände hinter dem Rücken berühren: Ihre linke Hand kommt von unten, und die rechte Hand, die von oben kommt, versucht, die linke Handfläche, wenn möglich, hinter dem Rücken zu berühren. Dehnen Sie nicht zu stark.",
        name="Dehnung Rechte Schulter",
        videoPath="assets/videos/DehnungRechteSchulter.mp4",
        dauer=40,
        imagePath="assets/images/DehnungRechteSchulter.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/R0NmFKcFB1Y"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht. Ihr Ziel ist es jetzt, dass sich die Hände hinter dem Rücken berühren: Ihre rechte Hand kommt von unten, und die linke Hand, die von oben kommt, versucht, die linke Handfläche, wenn möglich, hinter dem Rücken zu berühren. Dehnen Sie nicht zu stark.",
        name="Dehnung Linke Schulter",
        videoPath="assets/videos/DehnungLinkeSchulter.mp4",
        dauer=40,
        imagePath="assets/images/DehnungLinkeSchulter.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/5cyxyTi_gss"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Knien Sie sich zunächst auf eine Matte. Machen Sie es dann wie eine Katze, lassen Sie ihren Oberkörper nach vorne absinken, bleiben sie mit den Knien und den Füßen am Boden und strecken sie ihre Hände soweit wie möglich nach vorne aus. Schieben sie ihren Oberkörper dann nach hinten um eine leichte Dehnung im Bereich der Schultern zu spüren. Achten Sie auf eine tiefe Atmung.",
        name="Kinderstellung",
        videoPath="assets/videos/Kinderstellung.mp4",
        dauer=30,
        imagePath="assets/images/Kinderstellung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/4uMgVmPnl9E"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Stehen Sie aufrecht, Ellenbogen sind am Rumpf des Körpers. Ober zu unter Arme sind im 90 Grad Winkel. Ellenbogen gehen nun seitlich nach oben bis sich eine Waagerechte zwischen linkem Oberarm, Schultern und rechtem Oberarm bildet. Wichtig: Nacken entspannen, langsam ausführen, leicht in die Kniee und Rücken Gerade lassen.",
        name="Schulterkräftigung im Stehen",
        videoPath="assets/videos/SchulterkraeftigungStehen.mp4",
        dauer=30,
        imagePath="assets/images/SchulterkraeftigungImStehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/vAozR51VE-k"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Stehen Sie zunächst aufrecht und beugen Sie sich dann mit geradem Rücken leicht nach vorne. Ellenbogen sind wieder eng am Rumpf und es ist ein 90 Grad Winkel zwischen Ober- und Unterarmen. Die Ellenbogen gehen nun nah am Rumpf schräg nach oben und dann wieder nach unten, als würden Sie etwas vom Boden schräg hochziehen und wieder hinunterstoßen. Strecken Sie ihre Arme, wenn Sie in der 'hinunterstoßen'-Phase sind kurz ganz aus.",
        name="Ellenbogenhochziehen",
        videoPath="assets/videos/Ellenbogenhochziehen.mp4",
        dauer=30,
        imagePath="assets/images/Ellenbogenhochziehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/w06qcM8N_lE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht mit den Händen vor Ihrem Körper ausgestreckt. Die Handflächen sollten nach unten zeigen. Führen Sie schnelle, auf- und abgehende Bewegungen durch. Dabei sollten die Arme vollständig ausgestreckt sein. Achten Sie darauf, dass der Nacken entlastet bleibt.",
        name="Paddeln",
        videoPath="assets/videos/Paddeln.mp4",
        dauer=30,
        imagePath="assets/images/Paddeln.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/ILpL1uiaLkc"

    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Mobilisation Sprunggelenk links: Setzen Sie sich auf eine Matte, ein Bett oder eine Liege. Strecken Sie Ihre Füße aus. Die Fußspitzen zeigen nach oben. Kippen Sie nun Ihr linkes Fußgelenk nach vorne, soweit es geht, und Das ganz langsam. Achten Sie darauf, dass Ihr Bein und der Fuß gerade sind und nicht zur Seite wegkippen. Gehen Sie mit Ihrem Fußgelenk anschließend in die Ausgangsstellung und kippen Sie ihn dann wieder nach vorne. Der Vorgang des Vorkippens dauert ca. einen langen Ausatmer. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Mobilisation Sprunggelenk links",
        videoPath="assets/videos/MSprunglelenkLinks.mp4",
        dauer=20,
        imagePath="assets/images/mspruL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/cGe7uvkSAQ4"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Ihre Arme befinden sich im 90-Grad-Winkel zum Rumpf und waagerecht zu den Schultern. Die Handflächen zeigen zum Boden, und die Arme sind ausgestreckt. Rotieren Sie in aufrechter Haltung nun Ihre Handflächen. Halten Sie die Arme dabei oben, für etwa 45 Sekunden.",
        name="Schulterkreiseln",
        videoPath="assets/videos/Schulterkreiseln.mp4",
        dauer=45,
        imagePath="assets/images/Schulterkreiseln.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/21EYxRuNwZ0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Stehen Sie aufrecht und halten Sie eine Hantel/ Wasserflasche in jeder Hand, während Ihre Arme seitlich herabhängen. Heben Sie nun langsam beide Arme vor sich bis auf Schulterhöhe und senken Sie sie kontrolliert zurück. Der Rücken sollte gerade sein, der Blick nach vorne gerichtet und Sie gehen sie leicht in die Knie wobei sie den Bauch für die Stabilität und zur Entlastung des Rückens leicht anspannen. Wiederholen Sie diese Bewegung 10 bis 15 Mal. Die Hanteln sind hierbei erforderlich.",
        name="Vorderes Schulterheben",
        videoPath="assets/videos/VorderesSchulterheben.mp4",
        dauer=30,
        imagePath="assets/images/VorderesSchulterheben.png",
        added=False,
        instruction="",
        required="Hanteln/ Waserflasche",
        onlineVidePath="https://youtu.be/zLcK8hDzoqU"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht, leicht in den Knien, und legen Sie Ihre Arme gestreckt übereinander vor Ihrem Körper. Bewegen Sie dann Ihre Arme auseinander und dann jeweils hinter Ihren Rücken und versuchen Sie, sie so nah wie möglich aneinander zu bringen. Führen Sie diese Bewegung kontinuierlich aus und achten Sie auf einen geraden Rücken.",
        name="Schere",
        videoPath="assets/videos/Schere.mp4",
        dauer=60,
        imagePath="assets/images/Schere.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/f7hleF7Eqjk"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich mit leicht gespreizten Beinen und leicht nach vorne gebeugtem Oberkörper hin. Beugen Sie den Rücken leicht nach vorne und legen Sie Ihren linken Arm auf den Oberschenkel. Ihr rechter Arm hängt locker. Durch Gewichtsverlagerung bringen Sie den rechten Arm in eine Pendelbewegung. Der Rücken sollte gerade sein.",
        name="Schulterpendeln Rechts",
        videoPath="assets/videos/SchulterpendelnRechts.mp4",
        dauer=60,
        imagePath="assets/images/SchulterpendelnRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/JmBxk3XZolw"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich mit leicht gespreizten Beinen und leicht nach vorne gebeugtem Oberkörper hin. Beugen Sie den Rücken leicht nach vorne und legen Sie Ihren rechten Arm auf den Oberschenkel. Ihr linker Arm hängt locker. Durch Gewichtsverlagerung bringen Sie den rechten Arm in eine Pendelbewegung. Der Rücken sollte gerade sein.",
        name="Schulterpendeln Links",
        videoPath="assets/videos/SchulterpendelnLinks.mp4",
        dauer=60,
        imagePath="assets/images/SchulterpendelnLinks2.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/dIm3wSRUx3w"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht, leicht in den Knien. Lassen Sie Ihre Arme wie eine Windmühle nach vorne kreisen, während Ihr Kopf nach vorne schaut. Der Rücken sollte gerade bleiben und der Oberkörper sich möglichst wenig mitbewegen. Achten Sie darauf, Ihren Bauch anzuspannen.",
        name="Armkreisen/ Windmühle nach vorne",
        videoPath="assets/videos/WindmuehleVorne.mp4",
        dauer=60,
        imagePath="assets/images/WindmuehleVorne.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/9Hqb4qGZG3w"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht, leicht in den Knien. Lassen Sie Ihre Arme wie eine Windmühle nach hinten kreisen, während Ihr Kopf nach vorne schaut.",
        name="Armkreisen/ Windmühle nach hinten",
        videoPath="assets/videos/WindmuehleHinten.mp4",
        dauer=60,
        imagePath="assets/images/WindmuehleHinten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/QcTXvtULl3I"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Ziehen Sie Ihre Schultern zuerst nach oben und führen Sie dann kleine Kreisbewegungen mit Ihren Schultern nach hinten aus. Hierbei bewegen sich die Schultern auch nach unten. Beginnen Sie von vorne. Der Nacken ist dabei entspannt und sie stehen aufrecht, leicht in den Knien.",
        name="Schulterkreisen nach hinten",
        videoPath="assets/videos/SchulterkreisenHinten.mp4",
        dauer=40,
        imagePath="assets/images/SchulterkreisenHinten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/VatSJUlsR7s"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie aufrecht. Ziehen Sie Ihre Schultern zuerst nach oben und führen Sie dann eine Kreisbewegung mit Ihren Schultern nach vorne aus. Danach gehen Ihre Schultern nach unten und daraufhin zurück auf ihre Ausgangsposition. Beginnen Sie von vorne. Der Nacken ist dabei entspannt und sie stehen aufrecht, leicht in den Knien.",
        name="Schulterkreisen nach vorne",
        videoPath="assets/videos/SchulterkreisenVorne.mp4",
        dauer=40,
        imagePath="assets/images/SchulterkreisenVorne.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/6ytDZ0al-yA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht und strecken Sie Ihren rechten Arm aus, woraufhin der Arm leicht nach unten geht, sodass der Arm nun schräg nach unten zeigt. Die Handfläche zeigt nach vorne. Ihre linke Hand geht nun unter dem rechten Arm durch und greift den rechten Daumen, um ihn sanft zum Körper zu ziehen. Achten Sie darauf, dass sie nur eine leichte Dehnung spüren und den Daumen nicht zu stark zu sich ziehen.",
        name="Daumendehnung rechts",
        videoPath="assets/videos/DaumenDehnungRechts.mp4",
        dauer=30,
        imagePath="assets/images/DaumenDehnungRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/Zm1skfJizG4"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Gehen Sie zunächst in den Vierfüßlerstand mit einem geraden Rücken. Drehen Sie dann Ihre Fingerspitzen nach außen, sodass sie in Richtung Ihrer Knie zeigen, um eine leichte Dehnung in den Unterarmen zu fühlen. Lehnen Sie sich dabei vorsichtig nach hinten, soweit es möglich ist, ohne Schmerzen zu spüren.",
        name="Dehnung Unterarme",
        videoPath="assets/videos/DehnugUnterarme.mp4",
        dauer=40,
        imagePath="assets/images/DehnugUnterarme.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/D9YnMFANEjI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Knien Sie sich zunächst auf eine Matte. Strecken Sie den linken Arm nach vorne aus. Umschließen sie dann den Daumen mit der Faust. Knicken sie nun das Handgelenk nahch unten ab und halten sie mit ihrer rechten Hand die linke Hand in der Faustposition. Stützen sie sich nun auf dem linken Handrücken vorsichtig und langsam ab, wenn sie in die abgewandte Position des Vierfüßlerstandes gehen. Achten sie auf einen geraden Rücken. ",
        name="Dehnung Handgelenk links",
        videoPath="assets/videos/DehnungHandgelenkLinks3.mp4",
        dauer=40,
        imagePath="assets/images/DehnungHandgelenkLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/sHdsLWoDblw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Knien Sie sich zunächst auf eine Matte. Strecken Sie den rechten Arm nach vorne aus. Umschließen sie dann den Daumen mit der Faust. Knicken sie nun das Handgelenk nahch unten ab und halten sie mit ihrer rechten Hand die linke Hand in der Faustposition. Stützen sie sich nun auf dem linken Handrücken vorsichtig und langsam ab, wenn sie in die abgewandte Position des Vierfüßlerstandes gehen. Achten sie auf einen geraden Rücken. ",
        name="Dehnung Handgelenk rechts",
        videoPath="assets/videos/DehnungHandgelenkRechts.mp4",
        dauer=40,
        imagePath="assets/images/DehnungHandgelenkRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/VTXvLgJQvI0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Strecken Sie Ihren rechten Arm aus und legen Sie die Handfläche an die Wand. Drehen Sie diese Hand nach rechts, sodass die Fingerspitzen nach unten zeigen. Schieben Sie Ihren Oberkörper in Richtung der Wand, um eine leichte Dehnung zu spüren. Lassen Sie ihren Arm durchgestreckt.",
        name="Rechte Unterarmdehnung",
        videoPath="assets/videos/UnterarmRechts.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmRechtsWand.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/FAXsQ8zay8U"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Strecken Sie Ihren linken Arm aus und legen Sie die Handfläche an die Wand. Drehen Sie diese Hand nach links, sodass die Fingerspitzen nach unten zeigen. Schieben Sie Ihren Oberkörper in Richtung der Wand, um eine leichte Dehnung zu spüren. Lassen Sie ihren Arm durchgestreckt.",
        name="Linke Unterarmdehnung",
        videoPath="assets/videos/UnterarmLinks.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmLinksWand.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/2e8yCIb5PLY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stellen Sie sich vor eine Wand und ballen Sie mit der linken Hand eine Faust. Strecken sie den linken Arm aus und rotieren Sie die Faust, sodass der Daumen zum Boden zeigt. Knicken Sie dann das Handgelenk nach außen ab und drücken Sie den Handrücken anschließen vorsichtig und langsam gegen die Wand, bis ein 90-Grad-Winkel zwischen Unterarm und Handrücken entsteht. Führen Sie diese Bewegung mit gestreckten Arm aus uns stehen sie seitlich zur Wand ",
        name="Dehnung Handrücken Rechts",
        videoPath="assets/videos/DehnungHandrueckenRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHandrueckenRechts.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/V_f61S10Et4"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stellen Sie sich vor eine Wand und ballen Sie mit der linken Hand eine Faust. Strecken sie den linken Arm aus und rotieren Sie die Faust, sodass der Daumen zum Boden zeigt. Knicken Sie dann das Handgelenk nach außen ab und drücken Sie den Handrücken anschließen vorsichtig und langsam gegen die Wand, bis ein 90-Grad-Winkel zwischen Unterarm und Handrücken entsteht. Führen Sie diese Bewegung mit gestreckten Arm aus uns stehen sie seitlich zur Wand ",
        name="Dehnung Handrücken Links",
        videoPath="assets/videos/DehnungHandrueckenLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehnungHandrueckenLinks.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/EyS7f2zBXSA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Ihre rechte Hand berührt Ihre rechte hintere Schulter, und die Unterseite des Oberarms ist an der Wand angelehnt. Ihre linke Hand zieht mit den Fingern Ihre rechte Hand am Handgelenk in Richtung Boden. Achten Sie darauf, dass der Ellenbogen gerade nach oben zeigt und nicht zur Seite abknickt. Dehnen Sie nicht zu stark und brechen Sie die Übung bei Bedarf ab.",
        name="Dehnung für Tennisarm rechts",
        videoPath="assets/videos/DehnungTennisarmRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnungTennisarmRechts.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/40HuYS6Fh0U"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Ihre linke Hand berührt Ihre linke hintere Schulter, und die Unterseite des Oberarms ist an der Wand angelehnt. Ihre rechte Hand zieht mit den Fingern Ihre linke Hand am Handgelenk in Richtung Boden. Achten Sie darauf, dass der Ellenbogen gerade nach oben zeigt und nicht zur Seite abknickt. Dehnen Sie nicht zu stark und brechen Sie die Übung bei Bedarf ab.",
        name="Dehnung für Tennisarm links",
        videoPath="assets/videos/DehungTennisarmLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehungTennisarmLinks.png",
        added=False,
        instruction="",
        required="Wand",
        onlineVidePath="https://youtu.be/H78nspGhd-k"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich aufrecht hin. Heben Sie den linken Arm nun seitlich an, bis ein ca. 30 Grad großer Winkel zwischen Rumpf und Arm entsteht. Der Handrückem zeigt nach vorne und Sie nehmen Ihrnen Daumen nun in die Handfläche als würden Sie eine 4 zeigen. Die linke Schulter geht nun soweit wie möglich nach unten, wobei der Arm seitlich ausgestreckt bleibt. Wenn Sie noch keine Dehnung sprüren Versetzen Sie den Arm weiter nach hinten und heben Sie ihn seitlich leicht an. Neigen Sie den Kopf nach rechts und spüren Sie eine sanfte Dehnung im Bereich des Arms. Drehen Sie den Arm nun 3 mal sodass der Handrücken zunächst nach vorne und dann nach hintern zeigt. Anschließend halten Sie die Dehnung für ein paar Sekunden und routiren ihren Arm dann anschließen aus dem Schultergelenk 3 mal. Dann halten Sie die Dehnung wieder kurz. Zum Schluß ziehen sie die Schulter nocheinmal 3 mal nach oben und senken sie wieder ab. Der Handrücken zeigt außer bei der Drehung des Armes immer nach vorne und der Daumen verlässt seine Position nicht. Gehen Sie nicht über 5 auf einer Schmerzskala. ",
        name="Armnerven Mobilisation links",
        videoPath="assets/videos/ArmnervenmobilisationLinks2.mp4",
        dauer=50,
        imagePath="assets/images/ArmnervenmobilisationLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/bzyosU-Y55o"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stellen Sie sich aufrecht hin. Heben Sie den rechten Arm nun seitlich an, bis ein ca. 30 Grad großer Winkel zwischen Rumpf und Arm entsteht. Der Handrückem zeigt nach vorne und Sie nehmen Ihrnen Daumen nun in die Handfläche als würden Sie eine 4 zeigen. Die rechte Schulter geht nun soweit wie möglich nach unten, wobei der Arm seitlich ausgestreckt bleibt. Wenn Sie noch keine Dehnung sprüren Versetzen Sie den Arm weiter nach hinten und heben Sie ihn seitlich leicht an. Neigen Sie den Kopf nach links und spüren Sie eine sanfte Dehnung im Bereich des Arms. Drehen Sie den Arm nun 3 mal sodass der Handrücken zunächst nach vorne und dann nach hintern zeigt. Anschließend halten Sie die Dehnung für ein paar Sekunden und routiren ihren Arm dann anschließen aus dem Schultergelenk 3 mal. Dann halten Sie die Dehnung wieder kurz. Zum Schluß ziehen sie die Schulter nocheinmal 3 mal nach oben und senken sie wieder ab. Der Handrücken zeigt außer bei der Drehung des Armes immer nach vorne und der Daumen verlässt seine Position nicht. Gehen Sie nicht über 5 auf einer Schmerzskala. ",
        name="Armnerven Mobilisation rechts",
        videoPath="assets/videos/ArmnervenmobilisationRechts3.mp4",
        dauer=50,
        imagePath="assets/images/ArmnervenmobilisationRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Nmy27Q0Kitw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht oder stehen Sie aufrecht. Ihre rechte Hand geht nun zwischen die Schulterblätter. Versuchen Sie ihre rechten Fingerspitzen so nah wie möglich zum Boden zu bekommen und achten Sie darauf, dass die Handfläche möglichst mitig und wirklich zwischen den Schulterblättern ist. Ihre linke Hand zieht vorsichtig den rechten Ellenbogen nach links. Achten Sie darauf, die Dehnung sanft und kontrolliert auszuführen, um den Trizeps zu dehnen. Halten Sie die Position und atmen Sie ruhig. Falls Sie Schmerzen verspüren, brechen Sie die Übung sofort ab.",
        name="Trizepsdehnung rechts",
        videoPath="assets/videos/TrizepsDehnungRechts.mp4",
        dauer=40,
        imagePath="assets/images/TrizepsDehnungRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Pz2PSdm7XJI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich aufrecht oder stehen Sie aufrecht. Ihre linke Hand geht nun zwischen die Schulterblätter.Versuchen Sie ihre rechten Fingerspitzen so nah wie möglich zum Boden zu bekommen und achten Sie darauf, dass die Handfläche möglichst mitig und wirklich zwischen den Schulterblättern ist. Ihre rechte Hand zieht vorsichtig den linken Ellenbogen nach rechts. Achten Sie darauf, die Dehnung sanft und kontrolliert auszuführen, um den Trizeps zu dehnen. Halten Sie die Position und atmen Sie ruhig. Falls Sie Schmerzen verspüren, brechen Sie die Übung sofort ab.",
        name="Trizepsdehnung links",
        videoPath="assets/videos/TrizepsDehnungLinks.mp4",
        dauer=40,
        imagePath="assets/images/TrizepsDehnungLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/cfYr1iIllFc"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und bewahren Sie eine aufrechte Haltung. Breiten Sie Ihre Arme seitlich aus und strecken Sie sie, sodass eine waagerechte Linie zwischen Ihren Schultern und Armen entsteht. Zu Beginn zeigen Handflächen und Kopf nach oben. Halten Sie Ihren Rücken während der gesamten Übung gerade. Drehen Sie nun Handflächen und Kopf nach vorne, soweit es geht, und kehren Sie zur Ausgangsposition zurück. Halten Sie Ihre Finger während der Übung möglichst gespreizt.",
        name="Armkräftigung",
        videoPath="assets/videos/Armkraeftigung3.mp4",
        dauer=60,
        imagePath="assets/images/Armkraeftigung.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/MTU4B5bv0UU"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Nehmen Sie eine aufrechte Sitzposition ein. Imitieren Sie die Armbewegungen eines Kaktus: Ihr linker Arm bildet einen 90-Grad-Winkel zwischen Ober- und Unterarm und zeigt zum Boden, während Ihre Handfläche nach hinten gerichtet ist. Ihr rechter Arm bildet ebenfalls einen 90-Grad-Winkel zwischen Ober- und Unterarm, zeigt zur Decke und die Handfläche ist nach vorne gerichtet. Achten Sie darauf, dass der Schultergürtel fixiert bleibt.",
        name="Kaktus",
        videoPath="assets/videos/Kaktus.mp4",
        dauer=60,
        imagePath="assets/images/Kaktus.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/eZ1Qbc1UkQk"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Begeben Sie sich in die Position für einen Liegestütz, allerdings stützen sie Ihr Gewicht auf den Knien ab und nicht wie beim normalen Liegestütz auf den Füßen. Ihr Rücken sollte während der Übung gerade sein, und Ihre Hände sollten sich etwa auf Höhe der Schultern am Boden befinden. Beim Hochkommen aus der Liegestützposition atmen Sie aus und beim runtergehen atmen Sie ein.",
        name="Abgewandte Liegestütz",
        videoPath="assets/videos/AbgewandterLiegestuetz2.mp4",
        dauer=15,
        imagePath="assets/images/AbgewandterLiegestuetz.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/m74EFFeDNDE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Beginnen Sie in aufrechter Haltung, stehen Sie mit den Füßen zusammen und die Arme an den Seiten. Springen Sie in die Luft und spreizen Sie die Beine zur Seite, während Sie gleichzeitig die Arme über den Kopf heben. Landen Sie wieder in einer aufrechten Position und führen Sie die Beine und Arme wieder zusammen.",
        name="Hampelmann",
        videoPath="assets/videos/Hampelmann.mp4",
        dauer=60,
        imagePath="assets/images/Hampelmann.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/IXYwjyezEoY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Legen Sie sich auf die linke Seite. Ihr rechter Arm stützt Sie und Ihr Oberkörper ist leicht verdreht, während Ihr linker Arm sie umarmt. Der stützende Arm sollte etwa auf Schulterhöhe sein, und ihre Beine sollten die ganze Zeit am Boden bleiben und sind versetzt zueinander. Senken Sie Ihren Oberkörper seitlich ab, sodass Ihr rechter Arm unter Belastung steht. Drücken Sie sich mit dem rechten Arm wieder nach oben. Achten Sie darauf, die Bewegung kontrolliert auszuführen und atmen Sie ruhig. Die Übung erfordert Stabilität und Kraft in den seitlichen Muskeln.",
        name="Armkräftigung Seitlicher Liegestütz rechts",
        videoPath="assets/videos/SeitlicherLiegestuetzR.mp4",
        dauer=15,
        imagePath="assets/images/ArmkraeftigungSeitlicherLiegestuetzR.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/F7s8RS4bJs8"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Legen Sie sich auf die rechte Seite. Ihr linker Arm stützt Sie und Ihr Oberkörper ist leicht verdreht, während Ihr rechter Arm sie umarmt. Der stützende Arm sollte etwa auf Schulterhöhe sein, und ihre Beine sollten die ganze Zeit am Boden bleiben und sind versetzt zueinander. Senken Sie Ihren Oberkörper seitlich ab, sodass Ihr linker Arm unter Belastung steht. Drücken Sie sich mit dem linken Arm wieder nach oben. Achten Sie darauf, die Bewegung kontrolliert auszuführen und atmen Sie ruhig. Die Übung erfordert Stabilität und Kraft in den seitlichen Muskeln.",
        name="Armkräftigung Seitlicher Liegestütz links",
        videoPath="assets/videos/SeitlicherLiegestuetzL.mp4",
        dauer=15,
        imagePath="assets/images/ArmkraeftigungSeitlicherLiegestuetzL.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/q1V5v-_Fgrc"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Setzen Sie sich aufrecht auf eine Matte. Setzen Sie Ihre Hände hinter Ihrem Rücken ab, sodass sie Sie stützen. Drehen Sie Ihre Fingerspitzen so, dass sie in Richtung Ihres Gesäßes zeigen. Drücken Sie sich aus den Schultern heraus nach oben, sodass ihr Gesäß über dem Boden schwebt und sie den Boden nur mit den Versen und ihren Handflächen berühren. Senken Sie ihr Gesäß nun wieder in Richtung Boden ab und heben Sie es wieder, als würden Sie Dips für den Trizeps machen. Spannen Sie während der Übung Ihren Bauch an und achten Sie darauf, dass Ihre Beine und Ihr Oberkörper eine möglichst gerade Linie bilden. Achten Sie außerdem darauf, die Bewegung kontrolliert auszuführen und atmen Sie gleichmäßig. Diese Übung stärkt Ihre Trizeps-Muskulatur und erfordert Stabilität im Oberkörper.",
        name="Trizeps Dips im Liegenden Sitz",
        videoPath="assets/videos/TrizepsDipsImLiegen.mp4",
        dauer=12,
        imagePath="assets/images/TrizepsDipsImLiegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3p41QJQ0PGQ"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die linke Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Halten Sie Ihren Rücken gerade und beugen Sie leicht die Knie, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche sollte dabei parallel zum Boden sein. Diese Übung dient dem gezielten Training Ihres linken Bizeps und verbessert die Kraft und Ausdauer in dieser Muskelgruppe.",
        name="Bizeps links",
        videoPath="assets/videos/BizepsLinks2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsLinks.png",
        added=False,
        instruction="",
        required="Wasserflaschen",
        onlineVidePath="https://youtu.be/uTh6OeySo4A"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die rechte Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Halten Sie Ihren Rücken gerade und beugen Sie leicht die Knie, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche sollte dabei parallel zum Boden sein. Diese Übung dient dem gezielten Training Ihres rechten Bizeps und verbessert die Kraft und Ausdauer in dieser Muskelgruppe.",
        name="Bizeps rechts",
        videoPath="assets/videos/BizepsRechts2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsRechts.png",
        added=False,
        instruction="",
        required="Wasserflaschen",
        onlineVidePath="https://youtu.be/DVdEktILMf4"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die rechte Hand und eine in die linke Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Halten Sie Ihren Rücken gerade und beugen Sie leicht die Knie, wenn Sie stehen. Halten Sie Ihre Ellenbogen während der Übung nah am Körper, während Sie die Wasserflaschen nach oben bewegen. Die Flaschen sollten dabei parallel zum Boden sein. Diese Übung dient dem gezielten Training beider Bizeps und verbessert die Kraft und Ausdauer in dieser Muskelgruppe.",
        name="Bizeps beidseitig",
        videoPath="assets/videos/BizepsBeidseitig2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsBeidseitig.png",
        added=False,
        instruction="",
        required="Wasserflaschen",
        onlineVidePath="https://youtu.be/4tbXggIXm7M"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und beugen Sie sich nach vorne, sodass Ihr linker Ellenbogen auf Ihrem linken Oberschenkel ruht. Nehmen Sie eine Wasserflasche in die linke Hand. Heben und senken Sie Ihr Handgelenk, während Ihr Rücken gerade ist und der Ellenbogen am Oberschenkel bleibt. Führen Sie diese Bewegung etwa 40 Sekunden lang im gezeigten Tempo aus, um Ihre Unterarmmuskulatur zu stärken.",
        name="Unterarm links",
        videoPath="assets/videos/UnterarmLinks.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmLinks.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/2TAcpv-MNbY"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und beugen Sie sich nach vorne, sodass Ihr rechter Ellenbogen auf Ihrem rechten Oberschenkel ruht. Nehmen Sie eine Wasserflasche in die rechte Hand. Heben und senken Sie Ihr Handgelenk, während Ihr Rücken gerade ist und der Ellenbogen am Oberschenkel bleibt. Führen Sie diese Bewegung etwa 40 Sekunden lang im gezeigten Tempo aus, um Ihre Unterarmmuskulatur zu stärken.",
        name="Unterarm rechts",
        videoPath="assets/videos/UnterarmRechts.mp4",
        dauer=40,
        imagePath="assets/images/UnterarmRechts.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/DVruqdMzhzc"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die linke Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Ihr Rücken sollte gerade sein, und Sie können leicht in die Knie gehen, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche ist anfangs nach vorne gerichtet (parallel zu Fußspitzen) und dreht sich während des Hochbewegens so, dass sie in der Endposition parallel zum Boden ist. Diese Übung zielt auf die Kräftigung des linken Bizeps und Trizeps ab und verbessert die Kraft und Ausdauer in diesen Muskelgruppen.",
        name="Bizeps und Trizeps links",
        videoPath="assets/videos/BizepsTrizepsLinks2.mp4",
        dauer=20,
        imagePath="assets/images/BizepsTrizepsLinks.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/c7OFz_3dxfg"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Nehmen Sie eine Wasserflasche in die rechte Hand. Wählen Sie das Gewicht so, dass Sie die Übung 20-mal hintereinander ausführen können. Stehen Sie gerade oder sitzen Sie aufrecht. Ihr Rücken sollte gerade sein, und Sie können leicht in die Knie gehen, wenn Sie stehen. Halten Sie Ihren Ellenbogen während der Übung nah am Körper, während Sie die Wasserflasche nach oben bewegen. Die Flasche ist anfangs nach vorne gerichtet (parallel zu Fußspitzen) und dreht sich während des Hochbewegens so, dass sie in der Endposition parallel zum Boden ist. Diese Übung zielt auf die Kräftigung des rechten Bizeps und Trizeps ab und verbessert die Kraft und Ausdauer in diesen Muskelgruppen.",
        name="Bizeps und Trizeps rechts",
        videoPath="assets/videos/BizepsTrizepsRechts.mp4",
        dauer=20,
        imagePath="assets/images/BizepsTrizepsRechts.png",
        added=False,
        instruction="",
        required="Wasserflasche",
        onlineVidePath="https://youtu.be/qhGDiUV_z5w"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie gerade oder setzen Sie sich aufrecht hin. Strecken Sie den linken Arm aus, ballen Sie eine Faust und halten Sie mit der rechten Hand Ihren Bizeps fest. Der Handrücken schaut zunächst nach unten. Führen Sie einen Ellenbogenkreis im Uhrzeigersinn aus, indem die Faust zum Kinn geht und dann so weit wie möglich außen zurück zur ausgestreckten Position. Jetzt sollte der Handrücken nach unten zeigen. Während der Kreisbewegung drehen Sie den Bizeps leicht nach links. Drehen Sie nun anschließend ihre Hand um 180 Grad, sodass diese sich wieder in der Position vom Anfang befindet. Beginnen Sie von vorn.",
        name="Mobilisierung Elle links",
        videoPath="assets/videos/MobilisationElleLinks.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationElleLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/TJBmoiZJHm0"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stehen Sie gerade oder setzen Sie sich aufrecht hin. Strecken Sie den rechten Arm aus, ballen Sie eine Faust und halten Sie mit der linken Hand Ihren Bizeps fest. Der Handrücken schaut zunächst nach unten. Führen Sie einen Ellenbogenkreis gegen den Uhrzeigersinn aus, indem die Faust zum Kinn geht und dann so weit wie möglich außen zurück zur ausgestreckten Position. Jetzt sollte der Handrücken nach unten zeigen. Während der Kreisbewegung drehen Sie den Bizeps leicht nach links. Drehen Sie nun anschließend ihre Hand um 180 Grad, sodass diese sich wieder in der Position vom Anfang befindet. Beginnen Sie von vorn.",
        name="Mobilisierung Elle rechts",
        videoPath="assets/videos/MobilisationElleRechts.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationElleRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/YwqVTiQQE74"

    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf den Boden und legen Sie Ihren Unterarm auf einer Tischkante ab, sodass Ihr Handgelenk freischwebt. Sie können sich auch auf einen Stuhl setzen, allerdings brauchen Sie dann einen höheren Tisch. Beugen Sie das Handgelenk nach oben und halten Sie die Position für einige Sekunden. Beugen Sie das Handgelenk dann nach unten und halten Sie erneut. Achten Sie darauf, nicht zu stark zu dehnen.",
        name="Handgelenkflexion und -Extension Rechts",
        videoPath="assets/videos/HandgelenkFlexionRechts.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkFlexionRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/acN2yuFGOKs"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl und halten Sie Ihren Oberarm nach vorne ausgestreckt. Beugen Sie den Ellenbogen auf der linken Seite, indem Sie die Handfläche zur rechten Schulter bringen, und strecken Sie den Arm anschließend wieder nach vorne aus. Machen Sie dasselbe für die andere Seite.",
        name="Ellenbogen beugen, strecken",
        videoPath="assets/videos/EllenbogenBeugenStrecken.mp4",
        dauer=30,
        imagePath="assets/images/EllenbogenBeugenStrecken.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/Gi4DyesJXR4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Halten Sie Ihre Hände gerade vor sich, mit ausgestreckten Fingern. Bewegen Sie Ihre Handgelenke in einer Kreisbewegung im Uhrzeigersinn und dann gegen den Uhrzeigersinn. Fangen Sie zunächst mit einem langsamen Tempo an und werden Sie dann ein wenig schneller.",
        name="Kreissäge mit den Händen",
        videoPath="assets/videos/KreissaegeMitHaenden.mp4",
        dauer=30,
        imagePath="assets/images/KreissaegeMitHaenden.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/DjbDmPpoQL0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den rechten Arm aus. Zeigen Sie nun mit den Fingerspitzen zur Decke, bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung oben rechts",
        videoPath="assets/videos/HandgelenkDehnungObenRechts.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungObenRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/GEt3XifhExE"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den linken Arm aus. Zeigen Sie nun mit den Fingerspitzen zur Decke, bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung oben links",
        videoPath="assets/videos/HandgelenkDehnungObenLinks.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungObenLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/FMA2BekeJl0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den linken Arm aus. Zeigen Sie nun mit den Fingerspitzen zum Boden, bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung unten links",
        videoPath="assets/videos/HandgelenkDehnungUntenLinks.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungUntenLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/eAff2QhVFDs"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Setzen Sie sich auf einen Stuhl oder stehen Sie, strecken Sie den rechten Arm aus. Zeigen Sie nun mit den Fingerspitzen zum Boden , bis ein 90-Grad-Winkel zwischen Unterarm und Handfläche entsteht. Ziehen Sie nun mit der freien Hand die Fingerspitzen leicht in Ihre Richtung, bis zu einer mittelstarken Dehnung. Bitte üben Sie nicht zu viel Zug auf das Handgelenk aus und brechen Sie die Übung bei Schmerzen sofort ab.",
        name="Handgelenkdehnung unten rechts",
        videoPath="assets/videos/HandgelenkDehnungUntenRechts.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkDehnungUntenRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/y79A_grklp4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Sie können die Übung bei Bedarf abbrechen.Mobilisation Speiche links: Stellen Sie sich aufrecht hin (auch im aufrechten Sitzen möglich). Strecken Sie den linken Arm seitlich aus. Der Daumen ist so, als würden Sie eine 4 zeigen und die Handfläche zeigt zunächst nach oben. Führen Sie die Fingerspitzen in einer abwärts Kreisbewegung zur Taille. Die Schulter darf nicht zu weit nach vorne gehen. Fixieren Sie sie daher mit der freien Hand. Versuchen Sie den Kreis zu vollenden, sodass die Handfläche am Ende wieder nach oben zeigt. Drehen Sie die Handfläche, sodass sie wieder in der Ausgangsposition ist und beginnen Sie von vorne.",
        name="Mobilisation Speiche rechts",
        videoPath="assets/videos/MobilisationSpeicheRechts.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationSpeicheRechts.png",
        added=False,
        instruction="",
        required="Optional Stuhl",
        onlineVidePath="https://youtu.be/2shtAOYyX_Y"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Sie können die Übung bei Bedarf abbrechen.Mobilisation Speiche links: Stellen Sie sich aufrecht hin (auch im aufrechten Sitzen möglich). Strecken Sie den rechten Arm seitlich aus. Der Daumen ist so, als würden Sie eine 4 zeigen und die Handfläche zeigt zunächst nach oben. Führen Sie die Fingerspitzen in einer abwärts Kreisbewegung zur Taille. Die Schulter darf nicht zu weit nach vorne gehen. Fixieren Sie sie daher mit der freien Hand. Versuchen Sie den Kreis zu vollenden, sodass die Handfläche am Ende wieder nach oben zeigt. Drehen Sie die Handfläche, sodass sie wieder in der Ausgangsposition ist und beginnen Sie von vorne.",
        name="Mobilisation Speiche links",
        videoPath="assets/videos/MobilisationSpeicheLinks.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationSpeicheLinks.png",
        added=False,
        instruction="",
        required="Optional Stuhl",
        onlineVidePath="https://youtu.be/mJ_raWeOUvE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Brechen Sie die Übung bei Bedarf ab.Armmobilisation links (Tennisarm): Stellen Sie sich aufrecht hin oder sitzen Sie aufrecht. Strecken Sie den linken Arm seitlich aus. Senken Sie den Arm nun so, dass er nur noch leicht vom Körper absteht (ca. 30 Grad Winkel). Bringen Sie den Daumen in eine Position, sodass Sie ihn mit den restlichen Fingern umschließen könnten, als ob Sie eine 4 zeigen würden. Drehen Sie den Arm nach hinten, sodass der Daumen nach hinten zeigt. Fassen Sie mit der rechten Hand auf Ihre Schulter und senken Sie die Schulter ab. Der Oberkörper bleibt gerade. Neigen Sie Ihren Kopf nach rechts und heben Sie den Arm seitlich, bis Sie eine 4 auf der Schmerzskala von 1-10 fühlen. Schulter und Arm bleiben unten.",
        name="Armmobilisation links (Tennisarm)",
        videoPath="assets/videos/ArmmobilisationTennisarmLinks2.mp4",
        dauer=40,
        imagePath="assets/images/ArmmobilisationTennisarmLinks.png",
        added=False,
        instruction="",
        required="Optional: Stuhl",
        onlineVidePath="https://youtu.be/5Is-XsSKPeY"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Brechen Sie die Übung bei Bedarf ab.Armmobilisation rechts (Tennisarm): Stellen Sie sich aufrecht hin oder sitzen Sie aufrecht. Strecken Sie den rechten Arm seitlich aus. Senken Sie den Arm nun so, dass er nur noch leicht vom Körper absteht (ca. 30 Grad Winkel). Bringen Sie den Daumen in eine Position, sodass Sie ihn mit den restlichen Fingern umschließen könnten, als ob Sie eine 4 zeigen würden. Drehen Sie den Arm nach hinten, sodass der Daumen nach hinten zeigt. Fassen Sie mit der linken Hand auf Ihre Schulter und senken Sie die Schulter ab. Der Oberkörper bleibt gerade. Neigen Sie Ihren Kopf nach rechts und heben Sie den Arm seitlich, bis Sie eine 4 auf der Schmerzskala von 1-10 fühlen. Schulter und Arm bleiben unten.",
        name="Armmobilisation rechts (Tennisarm)",
        videoPath="assets/videos/ArmmobilisationTennisarmRechts2.mp4",
        dauer=40,
        imagePath="assets/images/ArmmobilisationTennisarmRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/gB292C-2RFM"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Brechen Sie die Übung bei Bedarf ab.Handgelenke Mobilisieren: Setzen Sie sich aufrecht hin oder stehen Sie aufrecht. Verschränken Sie die Hände wie bei einem Gebet. Beginnen Sie nun die Handgelenke zu bewegen und kreisförmige Bewegungen mit den Händen zu machen. Versuchen Sie möglichst aufrecht zu stehen und beginnen Sie mit kleinen Kreisen und einer langsamen Frequenz. Werden Sie im Verlauf der Übung ein wenig schneller und machen Sie immer größere Kreise",
        name="Handgelenke Mobilisieren",
        videoPath="assets/videos/HandgelenkeMobilisieren.mp4",
        dauer=20,
        imagePath="assets/images/HandgelenkeMobilisieren.png",
        added=False,
        instruction="",
        required="Optional: Stuhl",
        onlineVidePath="https://youtu.be/GGMBnpa7s30"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Seitliche Rumpfdehnung rechts: Sitzen Sie aufrecht und heben Sie den rechten Arm nach ausgestreckt oben. Beugen Sie Ihren Oberkörper sanft zur linken Seite, während Sie die rechte Hand über den Kopf ziehen und die andere nach unten richtung Boden bewegen. Halten Sie die Dehnung für 30 Sekunden und achten Sie darauf, dass ihr Rücken gerade bleibt und die Hüfte sich nicht bewegt.",
        name="Seitliche Rumpfdehnung rechts",
        videoPath="assets/videos/seitlicheDehnungmRechts.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfDehnugRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/EuHs16lRh_Y"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Seitliche Rumpfdehnung links: Sitzen Sie aufrecht und heben Sie den linken Arm ausgestreckt nach oben. Beugen Sie Ihren Oberkörper sanft zur rechten Seite, während Sie die linke Hand über den Kopf ziehen und die andere nach unten richtung Boden bewegen. Halten Sie die Dehnung für 30 Sekunden und achten Sie darauf, dass ihr Rücken gerade bleibt und die Hüfte sich nicht bewegt.",
        name="Seitliche Rumpfdehnung links",
        videoPath="assets/videos/SeitlicheRumpfDehnugLinks.mp4",
        dauer=30,
        imagePath="assets/images/SeitlicheRumpfdehnungLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/c0eLPrqEloU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Thorakale Drehung links: Setzen Sie sich auf einen Stuhl, Rücken gerade. Legen Sie die linke Hand auf die rechte Außenseite Ihres rechten Oberschenkels. Drehen Sie Ihren Oberkörper nach rechts und benutzen Sie Ihre rechte Hand, um den Boden hinter Ihnen zu greifen. Halten Sie die Drehung für 15-30 Sekunden. Versuchen Sie die Hüfte nicht zu bewegen.",
        name="Thorakale Drehung links",
        videoPath="assets/videos/ThorakaleDenungLinks.mp4",
        dauer=30,
        imagePath="assets/images/ThorakaleDenungLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/54MWXbEI608"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Thorakale Drehung rechts: Setzen Sie sich auf einen Stuhl, Rücken gerade. Legen Sie die rechte Hand auf die linke Außenseite Ihres linken Oberschenkels. Drehen Sie Ihren Oberkörper nach links und benutzen Sie Ihre linke Hand, um den Boden hinter Ihnen zu greifen. Halten Sie die Drehung für 15-30 Sekunden. Versuchen Sie die Hüfte nicht zu bewegen.",
        name="Thorakale Drehung rechts",
        videoPath="assets/videos/ThorakaleDenungRechts.mp4",
        dauer=30,
        imagePath="assets/images/ThorakaleDenungRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/Y6xEdoEQbg4"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Katzen-Kuh-Dehnung: Beginnen Sie die Übung auf Händen und Knien im Vierfüßlerstand, mit den Händen unter den Schultern und den Knien unter den Hüften. Bei der Einatmung senken Sie den Rücken nach unten, heben den Kopf und schauen nach oben (Kuh-Haltung). Bei der Ausatmung runden Sie den Rücken, ziehen das Kinn zur Brust.",
        name="Katzen-Kuh-Dehnung",
        videoPath="assets/videos/KatzenKuhDehnung.mp4",
        dauer=30,
        imagePath="assets/images/KatzenKuhDehnung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/kbN_1oDYkqA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Erleichterte Plank: Stützen Sie sich mit den Händen und den Knien auf einer Matte ab. Ihr Rücken ist gerade, der Kopf schaut nach vorne.",
        name="Erleichterte Plank",
        videoPath="assets/videos/ErleichtertePlank.mp4",
        dauer=40,
        imagePath="assets/images/ErleichtertePlank.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/JUK4Y4mGMLg"
    ),
    UebungList(
        looping=False,
        timer=False,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Heben/Senken: Legen Sie sich mit dem Bauch auf eine Matte. Winkeln Sie die Arme seitlich an. Der Kopf schaut in den Boden. Heben Sie nun Ihren Oberkörper nach oben und senken ihn langsam wieder ab. Die Arme sind die ganze Zeit in der Luft. Vergessen Sie nicht zu atmen.",
        name="Heben/Senken",
        videoPath="assets/videos/HebenSenken.mp4",
        dauer=20,
        imagePath="assets/images/HebenSenken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/EIEfU7KiwIU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Kräftigung Rücken: Legen Sie sich mit dem Bauch auf eine Matte. Heben Sie die Arme leicht an, halten Sie sie nah am Körper und zeigen Sie mit den Fingerspitzen nach hinten. Heben Sie Ihren Oberkörper leicht an. Halten Sie diese Position und beginnen Sie die Beine anzuwinkeln und wieder abzusenken. Der Blick ist nach unten gerichtet.",
        name="Kräftigung Unterer Rücken",
        videoPath="assets/videos/KraeftigungUntererRuecken.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungUntererRuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/wdyW0yIUTzY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Fliegen: Legen Sie sich mit dem Bauch auf eine Matte. Strecken Sie Ihre Arme seitlich aus, mit 90 Grad zwischen Oberkörper und Armen. Der Kopf schaut in den Boden. Heben Sie nun Ihre Arme mit dem Oberkörper nach oben, als würden Sie mit den Flügeln schlagen, und senken ihn langsam wieder ab.",
        name="Fliegen",
        videoPath="assets/videos/Fliegen.mp4",
        dauer=30,
        imagePath="assets/images/Fliegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3hUW6XvQn4Y"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Kräftigung im Vierfüßler Stand: Gehen Sie in den Vierfüßler Stand auf einer Matte. Ihr Rücken muss gerade sein. Strecken Sie nun abwechselnd das rechte Bein und den linken Arm und das linke Bein und den rechten Arm aus. Strecken Sie so weit, dass sich eine Waagerechte zwischen Rücken, Arm und Bein bildet.",
        name="Kräftigung im Vierfüßler Stand",
        videoPath="assets/videos/Vierfuesslerstand.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungImViefueßlerstand.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/EcKsFt7XfmI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Kräftigung Rücken/Bauch: Gehen Sie auf einer Matte in den Liegestütz (Hände ca. unter den Schultern Füße nah beieinander, Blick leicht nach vorne). Schieben Sie Ihren Oberkörper nun mit geradem Rücken und Kopf langsam leicht nach vorne, und wieder zurück. Versuchen Sie, stabil zu bleiben. Wenn Ihnen die Übung zu schwer fällt können sie sich auch auf den Knien abstützen. Achten Sie aber bitte die ganze Zeit darauf, dass ihr Rücken gerade ist.",
        name="Kräftigung Rücken und Bauch",
        videoPath="assets/videos/KraeftigungRueckenUndBauch.mp4",
        dauer=30,
        imagePath="assets/images/KraeftigungRueckenUndBauch.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/YcQeV6q-PD0"
    ),
    UebungList(
        looping=False,
        timer=False,
        execution="Sie können die Übung bei Bedarf bzw. Schmerzen unverzüglich abbrechen.Ruderübung mit Theraband: Befestigen Sie ein Theraband an einem festen Punkt, ca auf Bauchnabelhöhe. Nehmen Sie die Enden des Therabands in beide Hände und stehen Sie mit leicht gebeugten Knien. Ziehen Sie das Theraband zu sich, während Sie den Rücken gerade halten und die Ellbogen eng am Körper behalten. Spannen Sie den Bauch dabei an.",
        name="Ruderübung mit Theraband",
        videoPath="assets/videos/RuderuebungMitTheraband.mp4",
        dauer=30,
        imagePath="assets/images/RuderuebungMitTheraband.png",
        added=False,
        instruction="",
        required="Theraband",
        onlineVidePath="https://youtu.be/27Ouh_6GGj0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Mobilisation Sprunggelenk rechts: Setzen Sie sich auf eine Matte, ein Bett oder eine Liege. Strecken Sie Ihre Füße aus. Die Fußspitzen zeigen nach oben. Kippen Sie nun Ihr rechtes Fußgelenk nach vorne, soweit es geht, und Das ganz langsam. Achten Sie darauf, dass Ihr Bein und der Fuß gerade sind und nicht zur Seite wegkippen. Gehen Sie mit Ihrem Fußgelenk anschließend in die Ausgangsstellung und kippen Sie ihn dann wieder nach vorne. Der Vorgang des Vorkippens dauern ca. einen langen Ausatmer. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Mobilisation Sprunggelenk rechts",
        videoPath="assets/videos/MSprunglelenkRechts.mp4",
        dauer=20,
        imagePath="assets/images/mspru.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/CsUOtiueZtQ"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Aufdrehen im Vierfüßler Stand links: Gehen Sie in den Vierfüßler Stand. Strecken Sie nun Ihr rechtes Bein nach hinten aus. Drehen Sie Ihren linken Arm nach außen und stützen Sie sich mit der rechten Hand ab. Schauen Sie dem Arm hinterher. Führen Sie die Bewegung langsam aus. Tauchen Sie dann ab, indem Ihr linker Arm unter Ihrem Körper hindurchgeht und Ihr Oberkörper sich leicht öffnet.",
        name="Aufdrehen im Vierfüßler Stand links",
        videoPath="assets/videos/AufdrehenVLinks.mp4",
        dauer=60,
        imagePath="assets/images/AufdrehenVLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Wu1OzuT5c-8"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Aufdrehen im Vierfüßler Stand rechts: Gehen Sie in den Vierfüßler Stand. Strecken Sie nun Ihr linkes Bein nach hinten aus. Drehen Sie Ihren rechten Arm nach außen und stützen Sie sich mit der linken Hand ab. Schauen Sie dem Arm hinterher. Führen Sie die Bewegung langsam aus. Tauchen Sie dann ab, indem Ihr rechter Arm unter Ihrem Körper hindurchgeht und Ihr Oberkörper sich leicht öffnet.",
        name="Aufdrehen im Vierfüßler Stand rechts",
        videoPath="assets/videos/AufdrehenVRechts.mp4",
        dauer=60,
        imagePath="assets/images/AufdrehenVRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/ni7Ndtnyg8s"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Aufdrehen im Stehen: Stellen Sie sich hin. Beugen Sie sich nach vorne, sodass Oberkörper und Beine einen 90-Grad-Winkel bilden. Lassen Sie Ihre Arme baumeln und achten Sie auf einen geraden Rücken. Ihr linker Arm geht nun seitlich nach oben wie ein Flügelschlag, während der rechte Arm weiter locker nach unten hängt. Ihr Kopf schaut dem Arm, der gerade hoch geht, hinterher. Dann geht der Arm wieder zurück, und der rechte Arm ist derjenige, der hochgeht. Führen Sie das Ganze im gezeigten Tempo für etwa 1 Minute aus.",
        name="Aufdrehen im Stehen",
        videoPath="assets/videos/AufdrehenImStehen2.mp4",
        dauer=60,
        imagePath="assets/images/AufdrehenImStehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/AGBMjoUHsPQ"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Drehung im Stehen: Verschränken Sie Ihre Arme vor dem Oberkörper, während Sie aufrecht stehen. Ihre Schultern sind tief und unten. Ihr Kopf ist gerade und schaut nach vorne. Drehen Sie sich ausatmend auf die eine Seite, dann einatmend zurück zur Ausgangsposition und dann ausatmend zur anderen Seite. Führen Sie diese Übung für ca. 1 Minute aus, sie kann auch im Sitzen ausgeführt werden. Ihr Bauch sollte leicht angespannt sein und ihre Beine in einer stabilen Stellung und die Knie sollten leicht gebeugt sein.",
        name="Drehung im Stehen",
        videoPath="assets/videos/DrehungImStehen.mp4",
        dauer=60,
        imagePath="assets/images/DrehungImStehen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/XS96zl2e804"),
    UebungList(
        looping=True,
        timer=True,
        execution="Öffnen und schließen BWS: Stellen Sie sich breitbeinig hin. Strecken Sie Ihre Arme nach oben, dannach lehnen Sie sich nach hinten und spreizen Ihre Finger auseinander. Die Daumen sollten nach hinten zeigen, und Sie sollten während dieser Bewegung einatmen. Atmen Sie aus und führen Sie mit Ihren ausgestreckten Armen eine Kreisbewegung aus. Achten Sie darauf, den Bauch anzuspannen.",
        name="Öffnen BWS",
        videoPath="assets/videos/OeffnenBWS.mp4",
        dauer=60,
        imagePath="assets/images/oeffnenBWS.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/4aDc9GLT1bo"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Mobilisierung Oberer Rücken: Stehen Sie breitbeinig und aufrecht. Strecken Sie beide Arme nach oben und fassen Sie sich selbst an den Händen, so als würden Sie sich selbst in die Länge ziehen. Achten Sie dabei darauf, nicht ins Hohlkreuz zu gehen. Beginnen Sie nun im stabilen Stand, Ihren Oberkörper in kreisartigen Bewegungen hin und her zu schwingen. Die Arme bleiben oben und der Rücken gerade, wobei sie versuchen die Drehung aus dem Rücken heraus zu machen.",
        name="Mobilisierung Oberer Rücken",
        videoPath="assets/videos/MORuecken.mp4",
        dauer=60,
        imagePath="assets/images/MobilisationObererRuecken.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/RoZ_XFUCQ6A"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Handgelenkflexion und -Extension links: Setzen Sie sich auf den Boden und legen Sie Ihren Unterarm auf einer Tischkante ab, sodass Ihr Handgelenk freischwebt. Sie können sich auch auf einen Stuhl setzen, allerdings brauchen Sie dann einen höheren Tisch. Beugen Sie das Handgelenk nach oben und halten Sie die Position für einige Sekunden. Beugen Sie das Handgelenk dann nach unten und halten Sie erneut. Achten Sie darauf, nicht zu stark zu dehnen.",
        name="Handgelenkflexion und -Extension links",
        videoPath="assets/videos/HandgelenkFlexionLinks.mp4",
        dauer=30,
        imagePath="assets/images/HandgelenkFlexionLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/-zwuxR5K5pA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Rumpf unterer Rücken rechts: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr linkes Bein an und lassen Sie es nach rechts kippen. Drehen Sie Ihre Hüfte ebenfalls nach rechts. Ihre Schultern bleiben am Boden, sodass Sie sich verdrehen. Das rechte Bein bleibt ausgestreckt. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Rumpf unterer Rücken rechts",
        videoPath="assets/videos/DehnungRumpfUntererRueckenRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehnungRumpfUntererRueckenRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/rz9ITNqHmOY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Rumpf unterer Rücken links: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr linkes Bein an und lassen Sie es nach rechts kippen. Drehen Sie Ihre Hüfte ebenfalls nach rechts. Ihre Schultern bleiben am Boden, sodass Sie sich verdrehen. Das rechte Bein bleibt ausgestreckt. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Rumpf unterer Rücken links",
        videoPath="assets/videos/DehnungRumpfUntererRueckenLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehnungRumpfUntererRueckenLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/2C4r5b3OwFc"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Rumpfdehnung rechts: Stehen Sie aufrecht und strecken Sie die Arme über den Kopf. Beugen Sie Ihren Oberkörper sanft zur Seite, während Ihre Hände gestreckt über Ihnen sind und Sie sich in die Länge ziehen. Halten Sie die Dehnung für 15-20 Sekunden auf jeder Seite und wiederholen Sie sie mehrmals. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Rumpfdehnung rechts",
        videoPath="assets/videos/SeitlicheRumpfDehnugRechts.mp4",
        dauer=15,
        imagePath="assets/images/SeitlicheRumpfDehnugRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/UQx0DGGF78Y"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Rumpfdehnung links: Stehen Sie aufrecht und strecken Sie die Arme über den Kopf. Beugen Sie Ihren Oberkörper sanft zur Seite, während Ihre Hände gestreckt über Ihnen sind und Sie sich in die Länge ziehen. Halten Sie die Dehnung für 15-20 Sekunden auf jeder Seite und wiederholen Sie sie mehrmals. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Rumpfdehnung links",
        videoPath="assets/videos/SeitlicheRumpfDehnugLinks.mp4",
        dauer=15,
        imagePath="assets/images/SeitlicheRumpfdehnungLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/9xNuqENu7MY"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Kobradehnung: Legen Sie sich mit Bauch auf eine Matte. Stützen Sie sich nun mit den Händen ab, als wären Sie eine Kobra. Halten Sie die Dehnung und überstrecken Sie den Kopf leicht. Sollten Sie Schmerzen/Schwindel spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Kobradehnung",
        videoPath="assets/videos/Kobradehnung.mp4",
        dauer=30,
        imagePath="assets/images/Kobradehnung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Z4DQUb6rLsQ"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Lendenwirbeldehnung links: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr linkes Knie an und lassen Sie es nach rechts fallen. Drehen Sie Ihre Hüfte, sodass ein 90-Grad-Winkel zwischen dem Boden und Ihrem Gesäß entsteht. Strecken Sie den linken Arm seitlich aus. Die rechte Hand liegt am linken Knie und zieht dieses leicht in Richtung Boden. Atmen Sie natürlich und schauen sie zur linken Hand.",
        name="Lendenwirbeldehnung links",
        videoPath="assets/videos/LendernwirbeldehnungLinks.mp4",
        dauer=30,
        imagePath="assets/images/LendernwirbeldehnungLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/h2H-mFxIOd0"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Lendenwirbeldehnung rechts: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihr rechtes Knie an und lassen Sie es nach links fallen. Drehen Sie Ihre Hüfte, sodass ein 90-Grad-Winkel zwischen dem Boden und Ihrem Gesäß entsteht. Strecken Sie den rechten Arm seitlich aus. Die linke Hand liegt am rechtem Knie und zieht dieses leicht in Richtung Boden. Atmen Sie natürlich und schauen sie zur rechten Hand",
        name="Lendenwirbeldehnung rechts",
        videoPath="assets/videos/LendenwirbeldehnungRechts.mp4",
        dauer=30,
        imagePath="assets/images/LendenwirbeldehnungRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3FTm-Pv4M4E"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Bauchpresse: Legen Sie sich mit dem Rücken auf eine Matte. Knie beugen, Arme nach oben strecken. Heben Sie den Oberkörper dann mit Hilfe der Bauchmuskeln vom Boden ab. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Bauchpresse",
        videoPath="assets/videos/Bauchpresse3.mp4",
        dauer=12,
        imagePath="assets/images/Bauchpresse.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/SpCWj5PBYJk"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Russische Drehung: Setzen Sie sich auf eine Matte. Heben Sie Ihre Beine vom Boden ab und lehnen Sie Ihren Oberkörper nach hinten. Verschränken Sie Ihre Arme vor dem Oberkörper. Beginnen Sie sich abwechselnd nach rechts und dann nach links zu drehen. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Russische Drehung",
        videoPath="assets/videos/RussischeDrehung.mp4",
        dauer=30,
        imagePath="assets/images/RussischeDrehung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/jGdCFO5Z3c0"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Bergsteiger: Gehen Sie über eine Matte in die Liegestützposition. Halten Sie den Rücken gerade und tun Sie so, als würden Sie einen Berg hinauflaufen. Ihre Arme stützen Sie. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Bergsteiger",
        videoPath="assets/videos/Bergsteiger2.mp4",
        dauer=40,
        imagePath="assets/images/Bergsteiger.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/BYLJb8IXdoU"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Fersenaschlag: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie Ihre Knie an. Heben Sie Ihren Oberkörper leicht vom Boden ab und halten Sie Ihren Hals in einer natürlichen Position. Ihre Arme sind nah am Körper. Berühren Sie nun abwechselnd mit Ihrer rechten Hand Ihre rechte Ferse und umgekehrt. Ihr Oberkörper bleibt oben. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Fersenaschlag",
        videoPath="assets/videos/Fersenanschlag2.mp4",
        dauer=30,
        imagePath="assets/images/Fersenanschlag.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/f7DbKiLrLHQ"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Beinhebung: Liegen Sie mit dem Rücken auf einer Matte. Ihre Hände sind nah am Körper und Ihre Beine sind gestreckt. Heben Sie Ihre Beine nun nach oben. Sie bleiben dabei gestreckt. Ihr Kopf schaut die ganze Zeit nach oben. Senken Sie die Beine und wiederholen Sie die Übung. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Beinhebung",
        videoPath="assets/videos/Beinhebung.mp4",
        dauer=15,
        imagePath="assets/images/Beinhebung.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/vGZNPmdk1Ew"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Unterarmstütz: Führen Sie die Übung auf einer Matte aus. Der Rücken sollte gerade sein. Falls Ihnen die Übung zu schwer fällt, können Sie sich auf den Knien abstützen. Halten Sie diese Position. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Unterarmstütz",
        videoPath="assets/videos/Unteramstuetz.mp4",
        dauer=30,
        imagePath="assets/images/Unterarmstuetz.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/S7r-k1Wr2Ww"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Plank links: Liegen Sie auf einer Matte auf einer Seite und stützen Sie sich auf den linken Unterarm. Heben Sie Ihre Hüften, so dass Ihr Körper eine gerade Linie bildet. Halten Sie die Position, während Ihr freier Arm nah am Körper auf Ihrer Hüfte liegt. Sie können auch den rechten Fuß nach oben tun, wenn Ihnen die Übung zu leicht fällt. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Plank links",
        videoPath="assets/videos/SPlankLinks.mp4",
        dauer=30,
        imagePath="assets/images/SeitlichePlankLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/hzJvSYPNXhs"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Seitliche Plank rechts: Liegen Sie auf einer Matte auf einer Seite und stützen Sie sich auf den rechten Unterarm. Heben Sie Ihre Hüften, so dass Ihr Körper eine gerade Linie bildet. Halten Sie die Position, während Ihr freier Arm nah am Körper auf Ihrer Hüfte liegt. Sie können auch den linken Fuß nach oben tun, wenn Ihnen die Übung zu leicht fällt. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Seitliche Plank rechts",
        videoPath="assets/videos/SPlankRechts.mp4",
        dauer=30,
        imagePath="assets/images/SeitlichePlankRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/KZ2YCBsi_k0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Sit-Ups: Legen Sie sich auf den Rücken auf eine Matte mit gebeugten Knien. Halten Sie die Hände hinter dem Kopf oder über der Brust gekreuzt. Spannen Sie die Bauchmuskeln an und heben Sie Ihren Oberkörper langsam und kontrolliert vom Boden ab, während Sie ausatmen. Senken Sie sich langsam und kontrolliert ab, während Sie einatmen. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Sit-Ups",
        videoPath="assets/videos/SitUps.mp4",
        dauer=15,
        imagePath="assets/images/SitUps.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/mS2zFc6X3TE"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stärkung Bauchmuskeln: Legen Sie sich auf den Rücken auf eine Matte. Winkeln Sie Ihre Beine an, sodass ein rechter Winkel zwischen Waden und Unterschenkel entsteht. Drücken Sie Ihre Knie nun nach vorne und halten Sie mit den Bauchmuskeln/Beinen dagegen. Halten Sie die Position. Achten Sie darauf, kein Hohlkreuz zu machen. Sollten Sie starke Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Stärkung Bauchmuskeln",
        videoPath="assets/videos/SBauchmuskeln.mp4",
        dauer=30,
        imagePath="assets/images/StaerkungBauchmuskeln.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/qlp47zcmgMo"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="ISG-Dehnen rechts: Gehen Sie in den Kniestand auf einer Matte. Stellen Sie den linken Fuß nach vorne, sodass ein rechter Winkel zwischen Wade und Unterschenkel entsteht. Ihr Oberkörper ist kerzengerade. Die Blickrichtung ist gerade, und Sie fangen nun an, Ihren Oberkörper nach vorne zu schieben. Halten Sie diese Position für etwa eine Minute. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="ISG-Dehnen rechts",
        videoPath="assets/videos/ISGRechts.mp4",
        dauer=60,
        imagePath="assets/images/ISGDehnenRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/zEbejHx8UTo"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="ISG-Dehnen links: Gehen Sie in den Kniestand auf einer Matte. Stellen Sie den rechten Fuß nach vorne, sodass ein rechter Winkel zwischen Wade und Unterschenkel entsteht. Ihr Oberkörper ist kerzengerade. Die Blickrichtung ist gerade, und Sie fangen nun an, Ihren Oberkörper nach vorne zu schieben. Halten Sie diese Position für etwa eine Minute. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="ISG-Dehnen links",
        videoPath="assets/videos/ISGLinks.mp4",
        dauer=60,
        imagePath="assets/images/ISGDehnenLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/jOSKrACCJlw"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Hüftbeuger Dehnung rechts: Gehen Sie zunächst in den Kniestand auf einer Matte. Nehmen Sie den linken Fuß nach vorne, sodass Sie einen rechten Winkel im Knie haben. Fußgelenk und Knie sind in einer Linie. Nehmen Sie Ihre Hände nach oben und schieben Sie Ihre Hüfte nun mit geradem Rücken nach vorne. Ihre Füße bleiben am Boden. Halten Sie diese Position. Sollten Sie Schmerzen spüren brechen Sie die Übung bitte ab.",
        name="Hüftbeuger Dehnung rechts",
        videoPath="assets/videos/HueftbeugerRechts.mp4",
        dauer=30,
        imagePath="assets/images/HueftbeugerDehnenRechts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/wiX7cNIQs_M"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Hüftbeuger Dehnung links: Gehen Sie zunächst in den Kniestand auf einer Matte. Nehmen Sie den linken Fuß nach vorne, sodass Sie einen rechten Winkel im Knie haben. Fußgelenk und Knie sind in einer Linie. Nehmen Sie Ihre Hände nach oben und schieben Sie Ihre Hüfte nun mit geradem Rücken nach vorne. Ihre Füße bleiben am Boden. Halten Sie diese Position. Sollten Sie Schmerzen spüren brechen Sie die Übung bitte sofort ab.",
        name="Hüftbeuger Dehnung links",
        videoPath="assets/videos/HueftbeugerLinks.mp4",
        dauer=30,
        imagePath="assets/images/HueftbeugerDehnenLinks.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/EbzpcQUSOtc"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Entlastung LWS/Unterer Rücken: Stellen Sie einen Stuhl an ein Ende der Matte oder positionieren Sie die Matte vor einem Sofa/niedrigem Tisch, auf dem Sie Ihre Füße ablegen können. Legen Sie sich dann mit dem Rücken auf die Matte und legen Sie Ihre Füße auf dem eben beschriebene Objekt ab. Es sollte ein rechter Winkel im Knie entstehen. Vermeiden Sie ein Hohlkreuz und entspannen Sie Ihren unteren Rücken. Sollten Sie Schmerzen spüren oder eine Dehnung, die nicht im Zielbereich liegt, brechen Sie die Übung bitte sofort ab.",
        name="Entlastung LWS/Unterer Rücken",
        videoPath="assets/videos/EntlastungLWS.mp4",
        dauer=60,
        imagePath="assets/images/EntlastungLWS.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/cwotOq8FSwU"#
        ###########################################################################################################
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Zusammenrollen: Legen Sie sich mit dem Rücken auf eine Matte. Winkeln Sie anschließend die Knie mit Hilfe der Arme an und ziehen Sie sie in Richtung Brust. Ziehen Sie die Knie soweit, dass Sie Ihre Arme wie gezeigt zu einem Paket verschnüren können. Atmen Sie ganz ruhig und entspannt.",
        name="Zusammenrollen",
        videoPath="assets/videos/Zusammenrollen.mp4",
        dauer=30,
        imagePath="assets/images/Zusammenrollen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/_O0gn-U2hlk"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Stärkung Unterer Rücken: Legen Sie sich in Bauchlage auf eine Matte. Strecken Sie Arme und Füße aus. Ihr Blick ist zum Boden gerichtet. Heben Sie abwechselnd den linken Arm, den rechten Fuß und den rechten Arm, den linken Fuß vom Boden ab. Legen Sie die Arme und die Beine während der Übung nicht ab, sondern versuchen Sie die Spannung zu halten. Achten Sie außerdem darauf, dass ihre Arme und Beine die ganze Zeit ausgestreckt sind. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Stärkung Unterer Rücken",
        videoPath="assets/videos/StaerkungURuecke.mp4",
        dauer=40,
        imagePath="assets/images/StaerkungUntererRuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/3B2Z01vr0N8"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Kräftigung U. Rücken: Gehen Sie idealerweise auf einer Matte in den Vierfüßlerstand. Heben Sie Ihre Knie leicht vom Boden ab und stützen Sie ihr Gewicht auf den Zehenspitzen, wobei ihr Rücken gerade bleibt. Tippen Sie nun abwechselnd mit dem rechten Knie (Das Linke geht mit) auf die linke Seite, etwa auf Höhe Ihrer linken Hand und dann mit dem linken Knie (Das Rechte geht mit) etwa auf Höhe der Rechten Hand. Während dieser Bewegung sollte ein ca. 90 Grad großer Winkel Zwischen ihrem Bauch und den Oberschenkeln erhalten bleiben. Versuchen Sie, den oberen Rücken gerade zu halten, während sich Ihre Hüfte und Ihr unterer Rücken drehen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kräftigung U. Rücken",
        videoPath="assets/videos/StaerkungUNRuecken.mp4",
        dauer=60,
        imagePath="assets/images/StaerkungURuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/Tt2VIMA0e6g"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Kräftigung in Rückenlage: Legen Sie sich mit dem Rücken auf eine Matte. Setzen Sie Ihre Hände rechts und links neben dem Körper ab. Heben Sie nun Ihr Gesäß leicht vom Boden ab und stützen Sie sich mit den Händen oder legen Sie sie, wenn es von der Kraftanstrengung her geht am besten auf Ihrer Hüfte ab. Halten Sie diese Position für 45 Sekunden und atmen Sie ganz natürlich. Der Blick ist dabei zur Decke gerichtet.",
        name="Kräftigung in Rückenlage",
        videoPath="assets/videos/KraeRueckenlage.mp4",
        dauer=45,
        imagePath="assets/images/KraeftigunginRueckenlage.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/QB0LjdFCfHA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Po Brücke: Legen Sie sich mit dem Rücken auf eine Matte. Setzen Sie Ihre Hände rechts und links neben dem Körper ab. Ziehen Sie Ihre Füße an und stellen Sie sie auf dem Boden ab, sodass die Waden senkrecht zum Boden sind. Drücken Sie nun Ihren unteren Rücken nach oben, sodass nur der Schulterbereich und Ihre Füße den Boden berühren. Verschränken Sie Ihre Arme unter Ihrem Gesäß.",
        name="Po Brücke",
        videoPath="assets/videos/Po-Bruecke.mp4",
        dauer=40,
        imagePath="assets/images/PoBruecke.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/pEK5XSs2qsY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kniebeugen: Stehen Sie aufrecht, die Füße schulterbreit auseinander. Strecken Sie ihre Arme zur Stabilisation gerade nach vorne aus und richten Sie ihren Blick ebenfalls nach vorne. Beugen Sie die Knie und senken Sie sich, als ob Sie sich setzen würden. Stellen Sie sicher, dass Ihre Knie nicht über Ihre Zehen hinausragen und während der Bewegung nicht nach innen gehen. Kehren Sie zur aufrechten Position zurück.",
        name="Kniebeugen",
        videoPath="assets/videos/Kniebeugen.mp4",
        dauer=20,
        imagePath="assets/images/Kniebeugen.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/qmHBoTsihoM"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Rückenstrecker auf dem Boden: Legen Sie sich auf den Bauch und strecken Sie die Arme vor den Kopf nach vorne aus. Heben Sie Arme und Beine gleichzeitig für ca. 5 Sekunden an und halten Sie diese Position. Senken Sie dann Arme und Beine ab, allerdings nur so, dass Sie den Boden nicht berühren und die Spannung erhalten bleibt. Heben Sie ihre Arme und Füße erneut an. Achten Sie darauf, dass ihr Blick in Richtung Boden ist und Arme, sowie Füße die ganze Zeit ausgestreckt sind. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Rückenstrecker auf dem Boden",
        videoPath="assets/videos/Rueckenstrecker.mp4",
        dauer=40,
        imagePath="assets/images/RueckenstreckerBoden.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/F9iyR-G_at8"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Unterarmstütz: Führen Sie die Übung auf einer Matte aus. Gehen Sie nun in den Unterarmstütz, sodass sich ihr Gewicht auf die Unterarme und die Zehen verteilt. Beine, Becken und Oberkörper bilden eine Linie und der Rücken ist gerade. Wenn die Übung zu schwer fällt, können Sie sich auf den Knien abstützen aber heben Sie nicht ihr Gesäß, ansonsten verliert diese Übung ihre Wirkung. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Unterarmstütz (leichter)",
        videoPath="assets/videos/ErleichtertePlank.mp4",
        dauer=30,
        imagePath="assets/images/ErleichtertePlank.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/7-kXz-cVoDY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="ISG öffnen: Legen Sie ein eingerolltes Handtuch auf eine Matte. Legen Sie sich nun auf die Matte, sodass das Handtuch unter dem Hintern ist und mittig, zwischen den Pobacken liegt. Es sollte bis zum mittleren Rücken reichen. Halten Sie Ihren Rücken am Boden, während die Knie angewinkelt werden. Drücken Sie dann die Knie nach außen und schließen Sie sie wieder. Wiederholen Sie dies etwa 15-mal. Ihre Hände stützen seitlich ab. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="ISG öffnen",
        videoPath="assets/videos/ISG-oeffnen.mp4",
        dauer=15,
        imagePath="assets/images/ISGoefnnen.png",
        added=False,
        instruction="",
        required="Matte + Handtuch",
        onlineVidePath="https://youtu.be/Q1jS228pF5k"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="ISG-Mobilisieren: Legen Sie ein eingerolltes Handtuch auf eine Matte. Legen Sie sich nun auf die Matte, sodass das Handtuch unter dem Hintern ist und mittig zwischen den Pobacken liegt. Es sollte bis zum unteren Rücken reichen. Halten Sie Ihren Rücken am Boden. Die Knie gehen nach oben, sodass sich ein 90 Grad Winkel zwischen Wade und Unterschenkel bildet. Stellen Sie sich vor, Sie würden in der Luft ein Mini-Fahrrad fahren und bewegen Sie Ihre Füße in kurzer Sequenz vor und zurück. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="ISG-Mobilisieren",
        videoPath="assets/videos/ISG-Mobilisieren.mp4",
        dauer=40,
        imagePath="assets/images/ISGMobilisieren.png",
        added=False,
        instruction="",
        required="Matte + Handtuch",
        onlineVidePath="https://youtu.be/_td9lk1GOUA"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Becken Kippen: Legen Sie sich mit dem Rücken auf eine Matte. Stellen Sie Ihre Füße so auf, dass sie Kontakt mit dem Boden haben. Legen Sie Ihre Hände auf das Becken. Spannen Sie Ihre Bauch- und Gesäßmuskeln an, sodass Ihre Lendenwirbelsäule gegen den Boden gedrückt wird, und atmen Sie dabei aus. Kommen Sie anschließend in ein leichtes Hohlkreuz und atmen Sie dabei ein. Wiederholen Sie die Bewegung. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Becken Kippen",
        videoPath="assets/videos/BeckenKippen.mp4",
        dauer=15,
        imagePath="assets/images/BeckenKippen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/LI2sTBCvLz4"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Mobilisation Hüfte: Legen Sie sich mit dem Rücken auf eine Matte oder ein Bett. Ziehen Sie abwechselnd den linken und dann den rechten Fuß zum Körper, indem Sie Ihr Knie anwinkeln und Ihre Ferse dabei am Boden streifen. Achten Sie darauf, dass Ihr unterer Rücken am Boden fixiert bleibt. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Mobilisation Hüfte (leicht)",
        videoPath="assets/videos/MobilisationHuefteL.mp4",
        dauer=40,
        imagePath="assets/images/MobilisationHuefteLeicht.png",
        added=False,
        instruction="",
        required="Matte/Bett",
        onlineVidePath="https://youtu.be/jm6u63O9Ne0"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Mobilisationsübung: Hüftkreisen Rechts: Stehen Sie auf einem Bein und halten Sie sich, wenn nötig, an einer Wand fest. Kreisen Sie das nicht am Boden stehende Bein langsam in einer großen Kreisbewegung nach vorne, dann zur Seite und dann nach hinten. Wiederholen Sie die Bewegung in die entgegengesetzte Richtung. Das kreisende Bein sollte ausgestreckt sein, und der Oberkörper möglichst gerade. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name=" Hüftkreisen Rechts",
        videoPath="assets/videos/HueftkreisenRechts.mp4",
        dauer=50,
        imagePath="assets/images/HueftkreisenRechts.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/BR8kgXuYAPk"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Mobilisationsübung: Hüftkreisen Links: Stehen Sie auf einem Bein und halten Sie sich, wenn nötig, an einer Wand fest. Kreisen Sie das nicht am Boden stehende Bein langsam in einer großen Kreisbewegung nach vorne, dann zur Seite und dann nach hinten. Wiederholen Sie die Bewegung in die entgegengesetzte Richtung. Das kreisende Bein sollte ausgestreckt sein, und der Oberkörper möglichst gerade. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Hüftkreisen Links",
        videoPath="assets/videos/HueftkreisenLinks.mp4",
        dauer=50,
        imagePath="assets/images/HueftkreisenLinks.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/s86j1yJg6PA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Leistendehnung Rechts im Liegen: Setzen Sie sich auf eine Matte. Nehmen Sie Ihren linken Fuß und richten Sie ihn so aus, dass das Schienbein parallel zur kurzen Mattenvorderseite ist und der Oberschenkel parallel zur langen Mattenseite ist. Nehmen Sie Ihren rechten Fuß nach hinten und stützen Sie sich mit einem Arm nach hinten ab. Lehnen Sie Ihren Oberkörper leicht auf die linke vordere Seite. Das hinteres Bein ist möglichst gerade, ebenso wie der Rücken. Legen Sie ihre freie Hand auf dem Knie des angewinkelten Fußes. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Leistendehnung Rechts im Liegen",
        videoPath="assets/videos/LeistendehnungR.mp4",
        dauer=110,
        imagePath="assets/images/LeistendehnungRechtsimLiegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/QrvfRHwwH4Q"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Leistendehnung Links im Liegen: Setzen Sie sich auf eine Matte. Nehmen Sie Ihren rechten Fuß und richten Sie ihn so aus, dass das Schienbein parallel zur kurzen Mattenvorderseite ist und der Oberschenkel parallel zur langen Mattenseite ist. Nehmen Sie Ihren linken Fuß nach hinten und stützen Sie sich mit einem Arm nach hinten ab. Lehnen Sie Ihren Oberkörper leicht auf die rechte vordere Seite. Das hinteres Bein ist möglichst gerade, ebenso wie der Rücken. Legen Sie ihre freie Hand auf dem Knie des angewinkelten Fußes. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Leistendehnung Links im Liegen",
        videoPath="assets/videos/LeistendehnungL.mp4",
        dauer=110,
        imagePath="assets/images/LeistendehnungLinksimLiegen.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/74859z3armM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Oberschenkeldehnung Links im Stehen: Stellen Sie sich optional an eine Wand. Stützen Sie sich ab und stellen Sie sich auf ein Bein. In diesem Fall sollten Sie auf dem rechten Bein stehen und Ihr linkes Bein anziehen. Nehmen Sie den linken Fuß in die Hand, sodass es im Oberschenkel zieht. Achten Sie darauf, dass die Knie möglichst nah nebeneinander sind und der Rücken gerade ist. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Oberschenkeldehnung Links im Stehen",
        videoPath="assets/videos/OberschenkeldehnungL.mp4",
        dauer=50,
        imagePath="assets/images/OberschenkelL.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/zIkLYjww8Xo"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Oberschenkeldehnung Rechts im Stehen: Stellen Sie sich optional an eine Wand. Stützen Sie sich ab und stellen Sie sich auf ein Bein. In diesem Fall sollten Sie auf dem linken Bein stehen und Ihr rechtes Bein anziehen. Nehmen Sie den rechten Fuß in die Hand, sodass es im Oberschenkel zieht. Achten Sie darauf, dass die Knie möglichst nah nebeneinander sind und der Rücken gerade ist. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Oberschenkeldehnung Rechts im Stehen",
        videoPath="assets/videos/OberschenkeldehnungR.mp4",
        dauer=50,
        imagePath="assets/images/OberschenkelR.png",
        added=False,
        instruction="",
        required="Optional: Wand",
        onlineVidePath="https://youtu.be/4ILbRparn4Q"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Unterschenkel links (Bei Meniskus): Legen Sie sich auf ein Bett oder eine Matte. Sie benötigen einen Gürtel. Winkeln Sie Ihr linkes Bein an und legen Sie den Gürtel so um den linken Fuß, dass Sie beide Enden in der Hand halten und den Fuß zu sich ziehen können. Heben Sie den linken Fuß nach oben, üben Sie leichten Zug über den Gürtel aus und versuchen Sie, das Knie durchzustrecken. Achten Sie darauf, dass der untere Rücken fixiert bleibt und sich kein Hohlkreuz bildet. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Unterschenkel links (Bei Meniskus)",
        videoPath="assets/videos/UnterschenkelLinks.mp4",
        dauer=40,
        imagePath="assets/images/DehnungUnterschenkelLinks.png",
        added=False,
        instruction="",
        required="Gürtel +  Matte/Bett",
        onlineVidePath="https://youtu.be/_qmRLY-DSJ4"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnung Unterschenkel rechts (Bei Meniskus): Legen Sie sich auf ein Bett oder eine Matte. Sie benötigen einen Gürtel. Winkeln Sie Ihr rechtes Bein an und legen Sie den Gürtel so um den rechten Fuß, dass Sie beide Enden in der Hand halten und den Fuß zu sich ziehen können. Heben Sie den rechten Fuß nach oben, üben Sie leichten Zug über den Gürtel aus und versuchen Sie, das Knie durchzustrecken. Achten Sie darauf, dass der untere Rücken fixiert bleibt und sich kein Hohlkreuz bildet. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnung Unterschenkel rechts (Bei Meniskus)",
        videoPath="assets/videos/UnterschenkelRechts.mp4",
        dauer=40,
        imagePath="assets/images/DehnungUnterschenkelRechts.png",
        added=False,
        instruction="",
        required="Gürtel + Matte",
        onlineVidePath="https://youtu.be/pV3LgKXtP98"

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnen: Wadenmuskulatur. Ausführung: Stehen Sie etwa einen Schritt von einer Wand entfernt. Legen Sie die Handflächen zum Stützen leicht über Kopfhöhe an die Wand. Platzieren Sie das linke Bein nach hinten und beugen Sie das vordere Bein. Drücken Sie die Ferse des hinteren Beins in Richtung Boden, um die Wade zu dehnen. Schieben Sie dann anschließend ihren Oberkörper in Richtung Wand. Achten Sie dabei auf einen geraden Rücken, ein gestrecktes hinteres Bein und darauf, dass die Verse am Boden bleibt. Halten Sie die Dehnung für 20-30 Sekunden auf beiden Seiten. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnen: Wadenmuskulatur rechts",
        videoPath="assets/videos/WadenmuskulaturRechts.mp4",
        dauer=30,
        imagePath="assets/images/DehungWadenmuskulaturRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/ndPX0jiL-yM"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Dehnen: Wadenmuskulatur. Ausführung: Stehen Sie etwa einen Schritt von einer Wand entfernt. Legen Sie die Handflächen zum Stützen leicht über Kopfhöhe an die Wand. Platzieren Sie das rechte Bein nach hinten und beugen Sie das vordere Bein. Drücken Sie die Ferse des hinteren Beins in Richtung Boden, um die Wade zu dehnen. Schieben Sie dann anschließend ihren Oberkörper in Richtung Wand. Achten Sie dabei auf einen geraden Rücken, ein gestrecktes hinteres Bein und darauf, dass die Verse am Boden bleibt. Halten Sie die Dehnung für 20-30 Sekunden auf beiden Seiten. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Dehnen: Wadenmuskulatur links",
        videoPath="assets/videos/WadenmuskulaturLinks.mp4",
        dauer=30,
        imagePath="assets/images/DehungWadenmuskulaturLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/NrgkeAodF1o"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Einbeinstand links: Stellen Sie sich auf Ihren linken Fuß. Achten Sie darauf, dass Ihr Knie etwas nach außen zeigt. Federn Sie Ihr linkes Bein leicht ein und versuchen Sie, nur auf dem linken Fuß zu stehen und sich auszubalancieren. Bewegen Sie Ihr freies Bein nach Möglichkeit ein wenig in alle Richtungen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Einbeinstand links",
        videoPath="assets/videos/EinbeinstandL.mp4",
        dauer=60,
        imagePath="assets/images/EinbeinstandLinks.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/oFrGun0-R_o"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Kräftigung Wade: Nehmen Sie sich einen Stuhl mit Lehne. Stellen Sie sich davor und legen Sie Ihre Hände auf der Lehne ab. Gehen Sie auf die Zehenspitzen und halten Sie die Position kurz. Gehen Sie dann anschließend in die Hocke, nur soweit runter wie es geht, und halten Sie die Position. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kräftigung Waden",
        videoPath="assets/videos/KraeftigungWaden.mp4",
        dauer=60,
        imagePath="assets/images/KraeftigungWade.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/XRmHrfgaLkY"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Beinheben: Legen Sie sich auf den Bauch. Heben Sie ein Bein nach oben, während Sie das Gesäß anspannen. Senken Sie das Bein langsam ab. Achten Sie darauf, dass das Bein, welches oben ist, ausgestreckt ist und so weit wie möglich nach oben geht. Der untere Rücken sollte fixiert am Boden bleiben und ein Hohlkreuz sollte vermieden werden. Führen Sie die Übung auf einer Matte aus. Führen sie insgesamt die angegebene Anzahl der Wiederholungen abwechselnd mit dem rechten und dem linken Oberschenkel aus. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Beinheben Bauchlage",
        videoPath="assets/videos/BeinhebenBauch.mp4",
        dauer=40,
        imagePath="assets/images/KraeftigungUntererRuecken.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="https://youtu.be/kn1NYZaZwo0"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung: Quadrizeps Muskulatur links: Setzen Sie sich auf einen Stuhl mit aufrechtem Rücken. Heben Sie das linke gestreckte Bein an und halten Sie es für 5-10 Sekunden in der Luft. Senken Sie das Bein langsam ab. Wiederholen Sie diese Übung 10–15-mal. Stützen Sie sich bestenfalls mit ihren Händen an der Seite des Stuhles ab, um für Stabilität zu sorgen. Der Rücken, vor allem jedoch der untere Rücken sollte, falls vorhanden an der geraden Lehne des Stuhles fixiert bleiben. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Quadrizeps Muskulatur links",
        videoPath="assets/videos/QuadrizepsLinks.mp4",
        dauer=30,
        imagePath="assets/images/QuadrizeptsLinks.png",
        added=False,
        instruction="",
        required="Stuhl mit gerader Lehne",
        onlineVidePath="https://youtu.be/fKWBQrcdVkg"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung: Quadrizeps Muskulatur rechts: Setzen Sie sich auf einen Stuhl mit aufrechtem Rücken. Heben Sie das rechte gestreckte Bein an und halten Sie es für 5-10 Sekunden in der Luft. Senken Sie das Bein langsam ab. Wiederholen Sie diese Übung 10–15-mal. Stützen Sie sich bestenfalls mit ihren Händen an der Seite des Stuhles ab, um für Stabilität zu sorgen. Der Rücken, vor allem jedoch der untere Rücken sollte, falls vorhanden an der geraden Lehne des Stuhles fixiert bleiben. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Quadrizeps Muskulatur rechts",
        videoPath="assets/videos/QuadrizepsRechts.mp4",
        dauer=30,
        imagePath="assets/images/QuadrizeptsRechts.png",
        added=False,
        instruction="",
        required="Stuhl mit gerader Lehne",
        onlineVidePath="https://youtu.be/hTFWDHUh2Ps"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung Sprunggelenk rechts (Fußheben): Setzen Sie sich auf einen Stuhl. Machen Sie Ihren Rücken gerade und aufrecht und stellen Sie Ihre Füße auf dem Boden ab. Heben Sie nun Ihre rechte Fußspitze leicht an, wobei Ihre Ferse am Boden bleibt. Führen Sie die Übung langsam aus und achten Sie darauf, keine Schmerzen zu verursachen. Senken Sie Ihre Fußspitze wieder und beginnen Sie von vorne. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Sprunggelenk rechts (Fußheben)",
        videoPath="assets/videos/SprunggelenkRechts.mp4",
        dauer=15,
        imagePath="assets/images/SprungelenkRechts.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/UGN5LIz8C1A"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kräftigung Sprunggelenk links (Fußheben): Setzen Sie sich auf einen Stuhl. Machen Sie Ihren Rücken gerade und aufrecht und stellen Sie Ihre Füße auf dem Boden ab. Heben Sie nun Ihre linke Fußspitze leicht an, wobei Ihre Ferse am Boden bleibt. Führen Sie die Übung langsam aus und achten Sie darauf, keine Schmerzen zu verursachen. Senken Sie Ihre Fußspitze wieder und beginnen Sie von vorne. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Sprunggelenk links (Fußheben)",
        videoPath="assets/videos/SprunggelenkLinks.mp4",
        dauer=15,
        imagePath="assets/images/SprungelenkLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/MvM0dd2occU"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Kräftigung Sprunggelenk links: Stellen Sie sich auf Ihr linkes Bein und legen sie gegebenenfalls ein Handtuch unter ihren Fuß. Versuchen Sie sich nicht abzustützen, da dies die Wirkung der Übung verringert. Strecken Sie Ihr rechtes Bein aus, sodass es in der Luft ist, einschließlich Ihrer Fußspitzen. Tippen Sie nun mit der Fußspitze vor sich auf den Boden und dann hinter sich. Versuchen Sie diese Bewegung auch seitwärts auszuführen, aber bleiben Sie dabei gerade und versuchen Sie, sich auszubalancieren. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab. Ist ihr Sprunggelenk aufgrund einer vor kurzem passierten Verletzung sehr instabil, stützen Sie sich bitte trotzdem ab, um ein umknicken zu vermeiden.",
        name="Kräftigung Sprunggelenk links",
        videoPath="assets/videos/KrSprunggelenkL.mp4",
        dauer=60,
        imagePath="assets/images/KraeftigungSprunggelenkLinks.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/69JU4-_mnlA"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Kräftigung Sprunggelenk rechts: Stellen Sie sich auf Ihr rechtes Bein und legen sie gegebenenfalls ein Handtuch unter ihren Fuß. Versuchen Sie sich nicht abzustützen, da dies die Wirkung der Übung verringert. Strecken Sie Ihr linkes Bein aus, sodass es in der Luft ist, einschließlich Ihrer Fußspitzen. Tippen Sie nun mit der Fußspitze vor sich auf den Boden und dann hinter sich. Versuchen Sie diese Bewegung auch seitwärts auszuführen, aber bleiben Sie dabei gerade und versuchen Sie, sich auszubalancieren. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab. Ist ihr Sprunggelenk aufgrund einer vor kurzem passierten Verletzung sehr instabil, stützen Sie sich bitte trotzdem ab, um ein umknicken zu vermeiden.",
        name="Kräftigung Sprunggelenk rechts",
        videoPath="assets/videos/KrSprunggelenkR.mp4",
        dauer=60,
        imagePath="assets/images/KraeftigungSprunggelenkRechts.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/kVFdDteho7I"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Knie vorne Hoch: Stellen Sie sich aufrecht hin. Schauen Sie nach vorne und ziehen Sie abwechselnd Ihr rechtes und dann Ihr linkes Knie nach oben. Das Knie sollte etwa auf Hüfthöhe gehen. Spannen Sie den Bauch dabei an. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Knie vorne Hoch",
        videoPath="assets/videos/KnieeVorneHoch.mp4",
        dauer=60,
        imagePath="assets/images/Knieevornehoch.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/1MaGukXPMiY"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Führen Sie die Übung langsam aus. Beginnen Sie hiefür mit aufrechter Haltung und den Füßen schulterbreit auseinander. Machen Sie einen großen Schritt nach vorne, wobei Sie sicherstellen, dass das Knie des vorderen Beins im rechten Winkel über Ihrem Knöchel liegt. Das hintere Bein sollte ausgestreckt sein. ",
        name="Ausfallschritte",
        videoPath="assets/videos/Ausfallschritte.mp4",
        dauer=60,
        imagePath="assets/images/Ausfallschritte.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/rzGOuLXiFCk"
    ),
    UebungList(
        looping=True,
        timer=False,
        execution="Kniebeugung mit Stuhl: Setzen Sie sich auf einen stabilen Stuhl. Strecken Sie Ihr linkes Bein langsam aus. Das Knie verändert seine Höhe nicht und bleibt auf seiner Ausgangsposition. Es sollte sich eine waagerechte Linie zwischen Oberschenkel und Schienbein bilden. Senken Sie den Fuß nun anschließend wieder ab. Wiederholen Sie diese Bewegung auf beiden Seiten. Insgesamt sollten sie auf die vorgeschriebene Wiederholungsanzahl kommen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Kniebeugung mit Stuhl",
        videoPath="assets/videos/KniebeugungStuhl.mp4",
        dauer=30,
        imagePath="assets/images/KniebeugungmitStuhl.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/N2zp2n7fJI4"
    ),
    UebungList(
        looping=True,
        timer=True,
        execution="Einbeinstand links: Stellen Sie sich auf Ihren rechten Fuß. Achten Sie darauf, dass Ihr Knie etwas nach außen zeigt. Federn Sie Ihr rechtes Bein leicht ein und versuchen Sie, nur auf dem rechten Fuß zu stehen und sich auszubalancieren. Bewegen Sie Ihr freies Bein nach Möglichkeit ein wenig in alle Richtungen. Sollten Sie Schmerzen spüren, brechen Sie die Übung bitte sofort ab.",
        name="Einbeinstand rechts",
        videoPath="assets/videos/EinbeinstandRechts.mp4",
        dauer=60,
        imagePath="assets/images/EinbeinstandRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/9tgYWwhyhqI"
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht und strecken Sie Ihren linken Arm aus, woraufhin der Arm leicht nach unten geht, sodass der Arm nun schräg nach unten zeigt. Die Handfläche zeigt nach vorne. Ihre rechte Hand geht nun unter dem linken Arm durch und greift den linken Daumen, um ihn sanft zum Körper zu ziehen. Achten Sie darauf, dass Sie nur eine leichte Dehnung spüren und den Daumen nicht zu stark zu sich ziehen.",
        name="Daumendehnung links",
        videoPath="assets/videos/DaumenDehnungLinks.mp4",
        dauer=30,
        imagePath="assets/images/DaumenDehnungLinks.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/jaheeVOXiXI"
    ),
     UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und halten Sie das Handtuch wie gezeigt vor sich. Drücken Sie nun Ihre Hände nach außen, um Spannung auf das Handtuch zu bekommen und halten Sie diese Position.",
        name="Außenrotation Schultern",
        videoPath="assets/videos/AusenrotSchultern.mp4",
        dauer=30,
        imagePath="assets/images/ausenrotSchultern.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/QcWreHBFxg4",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und greifen Sie das Handtuch wie gezeigt über sich. Drücken Sie nun Ihre Hände nach außen, um Spannung auf das Handtuch zu bekommen und lehnen Sie sich nach hinten.",
        name="Aufdehnen mit Handtuch",
        videoPath="assets/videos/AufdehnenHandtuch.mp4",
        dauer=30,
        imagePath="assets/images/aufdehnenmithandtuch.png",
        added=False,
        instruction="",
        required="Handtuch",
        onlineVidePath="https://youtu.be/fPNmJ5lgqwI",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und im Ausfallschritt. Senken Sie nun das linke Knie in richtung Boden und achten Sie darauf, dass Ihr rechtes Knie sich nicht nach vorne bewegt und fixiert bleibt.",
        name="Einbeinkiebeuge rechts",
        videoPath="assets/videos/einbeinkniebeugeR.mp4",
        dauer=30,
        imagePath="assets/images/EinbeinkniebeugeR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/jOxyq5G_EYw",

    ),
     UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und im Ausfallschritt. Senken Sie nun das rechte Knie in richtung Boden und achten Sie darauf, dass Ihr linkes Knie sich nicht nach vorne bewegt und fixiert bleibt.",
        name="Einbeinkiebeuge links",
        videoPath="assets/videos/einbeinkniebeugeL.mp4",
        dauer=30,
        imagePath="assets/images/EinbeinkniebeugeL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/PYYvoqqwpws",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und nehmen Sie Ihre Hände so, als wollten Sie nach einer Stange in der Luft greifen. Ziehen Sie diese fiktive Stange aus der Luft nun mit geradem Rücken auf schulterhöhe nach unten.",
        name="Fiktive Klimmzüge",
        videoPath="assets/videos/fiktiveKlimzuege.mp4",
        dauer=30,
        imagePath="assets/images/fiktiveKlimmzuege.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Lp8ls2Wbc0o",

    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie die Hände wie gezeigt auf kopfhöhe überkreuz. Die Handrücken Ihrer Hände sind nach vorne gerichtet. Führen Sie anschließend eine Abwärtsbewegung mit den Händen durch, bei der sich Ihre Hände wie gezeigt drehen. ",
        name="Funktionelle Armkräftigung",
        videoPath="assets/videos/funktarmkraeftigung.mp4",
        dauer=30,
        imagePath="assets/images/funktarmkraeftigung.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/PEn-PzrGlGw",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie den rechten Fuß wie gezeigt auf den linken Oberschenkel. Versuchen Sie Ihr rechtes Knie soweit wie möglich nach unten zu drücken.",
        name="Piriformisdehnung rechts",
        videoPath="assets/videos/priformisR.mp4",
        dauer=30,
        imagePath="assets/images/PiriformisR.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/n6F5P_gwv_s",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie den linken Fuß wie gezeigt auf den rechten Oberschenkel. Versuchen Sie Ihr linkes Knie soweit wie möglich nach unten zu drücken.",
        name="Piriformisdehnung links",
        videoPath="assets/videos/pririformisL.mp4",
        dauer=30,
        imagePath="assets/images/PiriformisL.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/_S5BlGvFdF0",
    ),
     UebungList(## Muss 2 mal drinn sein weil es sonst einen Buck gibt. Frag nicht warum
        looping=False,
        timer=True,
        execution="Sitzen Sie aufrecht auf einem Stuhl und nehmen Sie den linken Fuß wie gezeigt auf den rechten Oberschenkel. Versuchen Sie Ihr linkes Knie soweit wie möglich nach unten zu drücken.",
        name="Piriformisdehnung links",
        videoPath="assets/videos/pririformisL.mp4",
        dauer=30,
        imagePath="assets/images/PiriformisL.png",
        added=False,
        instruction="",
        required="Stuhl",
        onlineVidePath="https://youtu.be/_S5BlGvFdF0",
    ),
    UebungList( #179 
        looping=False,
        timer=True,
        execution="Führen Sie die Bewegung aus dem Becken heraus aus. Achten Sie dabei auf einen Hüftbreiten Stand und gehen sie leicht in die Knie. Die Hände schlenkern nach vorne",
        name="Rotation Links und Rechts",
        videoPath="assets/videos/RotationLinksRechts.mp4",
        dauer=30,
        imagePath="assets/images/RotationLinksRechts.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/fsY4x8Hc8Eo",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Bitte positionieren Sie Ihre Hände auf Bauchhöhe, wobei Ihre Arme leicht gebeugt sind. Führen Sie die Bewegung dabei aus dem Becken heraus.",
        name="Rotation unten",
        videoPath="assets/videos/RotationUnten.mp4",
        dauer=30,
        imagePath="assets/images/RotationUnten.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/z4IpH1yQcAA",
    ),
    UebungList( #181
        looping=False,
        timer=True,
        execution="Bitte positionieren Sie Ihre Hände auf Brustbeinhöhe, wobei Ihre Arme leicht gebeugt sind. Führen Sie die Bewegung dabei aus dem Becken heraus.",
        name="Rotation Mitte",
        videoPath="assets/videos/RotationMitte.mp4",
        dauer=30,
        imagePath="assets/images/RotationMitte.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/HjG3_AO5Rcc",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Bitte positionieren Sie Ihre Hände auf Kinnhöhe, wobei Ihre Arme leicht gebeugt sind. Führen Sie die Bewegung dabei aus dem Becken heraus.",
        name="Rotation Oben",
        videoPath="assets/videos/RotationOben.mp4",
        dauer=30,
        imagePath="assets/images/RotationOben.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/YjaeN0okaQw",
    ),
    UebungList( #183
        looping=False,
        timer=True,
        execution="Führen Sie die dynamische Bewegung aus dem Becken heraus durch, indem Sie abwechselnd die Arme vor und zurück bewegen. Stellen Sie sicher, dass Sie einen hüftbreiten Stand einnehmen und leicht in die Knie gehen.",
        name="Armpendeln",
        videoPath="assets/videos/Armpendeln.mp4",
        dauer=30,
        imagePath="assets/images/Armpendeln.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/5x_m7IQmsQg",
    ),
    UebungList(
        looping=False,
        timer=True,
        execution="Nehmen Sie einen knietiefen Stand ein, der hüftbreit ist. Führen Sie die Bewegung aus dem Becken heraus durch, indem Sie Arme und Kopf mitschwingen lassen.",
        name="Golfschwung",
        videoPath="assets/videos/Golfschwung.mp4",
        dauer=30,
        imagePath="assets/images/Golfschwung.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/H2BSm-wyOQw",
    ),
    UebungList(#185
        looping=False,
        timer=True,
        execution="Führen Sie die Bewegung ohne Kraft aus und halten Sie dabei Ihren Nacken locker.",
        name="Dehnung der Rückenfaszien",
        videoPath="assets/videos/DehungRueckenfastzien.mp4",
        dauer=30,
        imagePath="assets/images/DehnungUFaszien.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/MhbS5T2R5Mg",
    ),
    UebungList(# 186
        looping=False,
        timer=True,
        execution="Schwingen Sie Ihre Arme gerade und entgegengesetzt zu den Beinen mit. Lassen Sie Ihre Arme dabei locker und führen Sie die Bewegung aus dem Becken heraus durch.",
        name="Beinpendeln links",
        videoPath="assets/videos/BeinpendelnL.mp4",
        dauer=30,
        imagePath="assets/images/BeinpendelL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/Fj7pJd6_Tp0",
    ),
    UebungList(# 187
        looping=False,
        timer=True,
        execution="Schwingen Sie Ihre Arme gerade und entgegengesetzt zu den Beinen mit. Lassen Sie Ihre Arme dabei locker und führen Sie die Bewegung aus dem Becken heraus durch.",
        name="Beinpendeln rechts",
        videoPath="assets/videos/BeinpendelnR.mp4",
        dauer=30,
        imagePath="assets/images/BeinpendelR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/knRfu2g_l5M",
    ),
    UebungList(# 188
        looping=False,
        timer=True,
        execution="Stellen Sie sich in den Einbeinstand, während Ihr Bein diagonal nach vorne geht. Ihre Arme sollten entgegengesetzt und ebenfalls diagonal bewegt werden.",
        name="Torisionsbewegung rechts",
        videoPath="assets/videos/TorisionsbewegungR.mp4",
        dauer=30,
        imagePath="assets/images/TorisionsbewegungR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/4EEyTube8hk",
    ),
    UebungList(# 189
        looping=False,
        timer=True,
        execution="Stellen Sie sich in den Einbeinstand, während Ihr Bein diagonal nach vorne geht. Ihre Arme sollten entgegengesetzt und ebenfalls diagonal bewegt werden.",
        name="Torisionsbewegung links",
        videoPath="assets/videos/TorisionsbewegungL.mp4",
        dauer=30,
        imagePath="assets/images/TorisionsbewegungL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/S9Jdugd4z8M",
    ),
    UebungList( #190
        looping=False,
        timer=True,
        execution="Führen Sie die Übung aus, indem Sie Ihren Kopf leicht überstrecken und die Bewegung ähnlich einem Holzhacker ausführen. Achten Sie darauf, dass Sie den Armen hinterherschauen und die auf- und ab-Bewegung mit Schwung ausführen.",
        name="Holzhacker",
        videoPath="assets/videos/Holzhacker.mp4",
        dauer=30,
        imagePath="assets/images/Holzhacker.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/UCiiL9u83CQ",
    ),
    UebungList(#191
        looping=False,
        timer=True,
        execution="Führen Sie die Übung aus, indem Sie Ihren Kopf leicht überstrecken und die Bewegung ähnlich einem Holzhacker ausführen. Achten Sie darauf, dass Sie den Armen hinterherschauen und die auf- und ab-Bewegung mit Schwung ausführen.",
        name="Holzhacker (diagonal)",
        videoPath="assets/videos/HolzhackerDiago.mp4",
        dauer=30,
        imagePath="assets/images/Holzhackerdiago.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/VEos6EHyZ9A",
    ),
    UebungList(#192
        looping=False,
        timer=True,
        execution="Nehmen Sie einen hüftbreiten und knietiefen Stand ein. Führen Sie die Bewegung durch, indem Sie Ihren Kopf jeweils bis zur Ferse drehen, während Ihre Arme locker von links nach rechts pendeln.",
        name="Schultergürtel lockern",
        videoPath="assets/videos/SchulterguertelLockern.mp4",
        dauer=30,
        imagePath="assets/images/SchulterguertelLockern.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/_pvFyvxbYm4",
    ),
    UebungList(#193
        looping=False,
        timer=True,
        execution="Beginnen Sie, indem Sie Ihre Handflächen am Oberschenkel positionieren. Führen Sie dann die Arme seitlich über den Kopf nach oben. Atmen Sie während dieser Aufwärtsbewegung ein und während der Abwärtsbewegung aus.",
        name="Atemübung",
        videoPath="assets/videos/Atemuebung.mp4",
        dauer=30,
        imagePath="assets/images/Atemuebung.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/s7FscrpHqZM",
    ),
    UebungList(#194
        looping=False,
        timer=True,
        execution="Nehmen Sie eine Schrittstellung ein und bewegen Sie Ihre Füße nacheinander nach vorne. Schauen Sie Ihrer Hand bei der Übung hinterher.",
        name="Mobilisation BWS/LWS links",
        videoPath="assets/videos/MobilisationBurstLWSL.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationBWSLWSL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/v0wmjnWR7Js",
    ),
    UebungList(#195
        looping=False,
        timer=True,
        execution="Nehmen Sie eine Schrittstellung ein und bewegen Sie Ihre Füße nacheinander nach vorne. Schauen Sie Ihrer Hand bei der Übung hinterher.",
        name="Mobilisation BWS/LWS rechts",
        videoPath="assets/videos/MobilisationBurstLWSR.mp4",
        dauer=30,
        imagePath="assets/images/MobilisationBWSLWSR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/biiXZCYpZNI",
    ),
    UebungList(# 196
        looping=False,
        timer=True,
        execution="Halten Sie Ihre Arme auf gleicher Höhe und nehmen Sie eine Schrittstellung ein. Führen Sie die Bewegung aus der Hüfte heraus durch und achten Sie darauf, dass ein rechter Winkel im Ellenbogen erhalten bleibt.",
        name="Ganzkörperkräftigung rechts",
        videoPath="assets/videos/RumpfkraeftigungR.mp4",
        dauer=30,
        imagePath="assets/images/RumpfkraeftigungR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/jjMiI7J5v0c",
    ),
    UebungList(#197
        looping=False,
        timer=True,
        execution="Halten Sie Ihre Arme auf gleicher Höhe und nehmen Sie eine Schrittstellung ein. Führen Sie die Bewegung aus der Hüfte heraus durch und achten Sie darauf, dass ein rechter Winkel im Ellenbogen erhalten bleibt.",
        name="Ganzkörperkräftigung links",
        videoPath="assets/videos/RumpfkraeftigungL.mp4",
        dauer=30,
        imagePath="assets/images/RumpfkraeftigungL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/zmOnCBSKBWc",
    ),
    UebungList(# 198
        looping=False,
        timer=True,
        execution="Halten Sie Ihren Rücken gerade und führen Sie die Bewegung aus dem Becken heraus durch. Bringen Sie dabei die Schulterblätter zusammen nach hinten. Sollten Sie Unwohlsein in der Lendenwirbelsäule verspüren, überspringen Sie bitte diese Übung.",
        name="Rückenstrecker",
        videoPath="assets/videos/Rueckenstrecker.mp4",
        dauer=30,
        imagePath="assets/images/Rueckenstrecker.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/PerP-mYHVH8",
    ),
    UebungList(#199
        looping=False,
        timer=True,
        execution="Stellen Sie sicher, dass Ihre Schulterblätter bei der Bewegung nach hinten zusammengeführt werden und spannen Sie dabei Ihren Bauch an. Die Daumen sollten auf Augenhöhe bleiben , während ein rechter Winkel zwischen Ober- und Unterarm besteht.",
        name="Butterfly",
        videoPath="assets/videos/Butterfly.mp4",
        dauer=30,
        imagePath="assets/images/Butterfly.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/mwuGTCcd0ss",
    ),
    UebungList(# 200
        looping=False,
        timer=True,
        execution="Halten Sie Ihren Rücken gerade und richten Sie Ihren Blick zum Boden. Ihre Arme sollten immer leicht gebeugt sein, und Ihre Schulterblätter sich annähern. Die Daumen zeigen dabei zur Brust.",
        name="Kräftigung BWS",
        videoPath="assets/videos/BWSKraeftigung.mp4",
        dauer=30,
        imagePath="assets/images/BWSKraeftigung.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/7k4chSjI2jk",
    ),
    UebungList(# 201
        looping=False,
        timer=True,
        execution="Führen Sie die Bewegung aus, indem Sie Ihre Schulter zum Knie bringen. Positionieren Sie Ihre Hände am Oberschenkel und nehmen Sie einen schulterbreiten, knietiefen Stand ein.",
        name="Schultern lockern",
        videoPath="assets/videos/Schulterlockerung.mp4",
        dauer=30,
        imagePath="assets/images/Schulterguertellockerung.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="https://youtu.be/-TfWd6SkuPo",
    ),
    UebungList(# 202
        looping=False,
        timer=True,
        execution="Gehen Sie in den Vierfüßlerstand. Positionieren Sie Ihre Hände auf Höhe der Schultern und Ihre Knie hüftbreit auseinander. Achten Sie darauf, den Bauch während der gesamten Übung anzuspannen.",
        name="Versteckter Liegestütz vorwärts",
        videoPath="assets/videos/verLiegestuetzVorwaerts.mp4",
        dauer=30,
        imagePath="assets/images/verLiegestuetzVorwaerts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="",
    ),
    UebungList(# 203
        looping=False,
        timer=True,
        execution="Gehen Sie in den Vierfüßlerstand. Positionieren Sie Ihre Hände auf Höhe der Schultern und Ihre Knie hüftbreit auseinander. Achten Sie darauf, den Bauch während der gesamten Übung anzuspannen.",
        name="Versteckter Liegestütz rückwärts",
        videoPath="assets/videos/verLiegestuetzRueckwaerts.mp4",
        dauer=30,
        imagePath="assets/images/verLiegestuetzRueckwaerts.png",
        added=False,
        instruction="",
        required="Matte",
        onlineVidePath="",
    ),
    UebungList(# 204
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren rechten Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Rückenstrecker im Einbeinstand rechts",
        videoPath="assets/videos/rueckenstreckerEinbeinR.mp4",
        dauer=30,
        imagePath="assets/images/rueckenstreckerEinbeinR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 205
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren linken Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Rückenstrecker im Einbeinstand links",
        videoPath="assets/videos/rueckenstreckerEinbeinL.mp4",
        dauer=30,
        imagePath="assets/images/rueckenstreckerEinbeinL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 206
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren rechten Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Brustwirbelsäule im Einbeistand rechts",
        videoPath="assets/videos/bwsEinbeinR.mp4",
        dauer=30,
        imagePath="assets/images/bwsEinbeinR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 207
        looping=False,
        timer=True,
        execution="Positionieren Sie Ihren linken Fuß fest am Boden und fixieren Sie Ihn während der Übung dort. Halten Sie Ihr Knie auf Höhe des Sprunggelenks, um eine optimale Ausrichtung zu erreichen. Achten Sie darauf, Ihren Bauch während der gesamten Übung anzuspannen.",
        name="Brustwirbelsäule im Einbeistand links",
        videoPath="assets/videos/bwsEinbeinL.mp4",
        dauer=30,
        imagePath="assets/images/bwsEinbeinL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 208
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und Drehen Sie die Daumen nach außen. Bringen Sie außerdem Ihre Schulterblätter zusammen und versuchen Sie während der Übung die Balance zu halten.",
        name="Kräftigung Hüfte im Einbeistand rechts",
        videoPath="assets/videos/kraeftigungHuefteEinbeinR.mp4",
        dauer=30,
        imagePath="assets/images/kraeftigungHuefteEinbeinR.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 209
        looping=False,
        timer=True,
        execution="Stehen Sie aufrecht und Drehen Sie die Daumen nach außen. Bringen Sie außerdem Ihre Schulterblätter zusammen und versuchen Sie während der Übung die Balance zu halten.",
        name="Kräftigung Hüfte im Einbeistand links",
        videoPath="assets/videos/kraeftigungHuefteEinbeinL.mp4",
        dauer=30,
        imagePath="assets/images/kraeftigungHuefteEinbeinL.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
    UebungList(# 210
        looping=False,
        timer=True,
        execution="Gehen Sie in den Vierfüßler Stand auf einer Matte. Ihr Rücken muss gerade sein. Strecken Sie nun abwechselnd das rechte Bein und den linken Arm und das linke Bein und den rechten Arm aus. Strecken Sie so weit, dass sich eine Waagerechte zwischen Rücken, Arm und Bein bildet.",
        name="Kräftigung im Viefüßlerstand (schwer)",
        videoPath="assets/videos/kraeftigungVierfueßlerstandS.mp4",
        dauer=30,
        imagePath="assets/images/kraeftigungVierfueßlerstandS.png",
        added=False,
        instruction="",
        required="",
        onlineVidePath="",
    ),
]

@login_required(login_url="login")
def admin_power(request):
    ##Update Executions
    # id = 1
    # all_exercises = models.Uebungen_Models.objects.all()
    # print("Test")
    # print(len(uebungen))
    # print(len(all_exercises))
    # for i in uebungen:
    #     exercise = models.Uebungen_Models.objects.get(id=id)
    #     exercise.execution = i.execution
    #     exercise.save()
    #     id += 1
        
    # print("done")
        
    ##Create new Exercises
    # for i in additionalUebungList2:
    #             Uebungen_Models.objects.create(
    #                 looping=i.looping,
    #                 timer=i.timer,
    #                 execution=i.execution,
    #                 name=i.name,
    #                 videoPath=i.videoPath,
    #                 dauer=i.dauer,
    #                 imagePath=i.imagePath,
    #                 added=i.added,
    #                 instruction=i.instruction,
    #                 required=i.required,
    #                 onlineVideoPath = i.onlineVidePath

    #             )
    # inizialize_first_second()

    # for i in signals.uebungen:
    #             Uebungen_Models.objects.create(
    #                 looping=i.looping,
    #                 timer=i.timer,
    #                 execution=i.execution,
    #                 name=i.name,
    #                 videoPath=i.videoPath,
    #                 dauer=i.dauer,
    #                 imagePath=i.imagePath,
    #                 added=i.added,
    #                 instruction=i.instruction,
    #                 required=i.required,
    #                 onlineVideoPath = i.onlineVidePath

    #             )

    # for i in models.LaxoutUser.objects.all():
    #     laxout_tree = models.LaxTree.objects.create()
    #     i.lax_tree_id = laxout_tree.id
    #     i.save()

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


@login_required(login_url="login")
def chats(request):
    users = models.LaxoutUser.objects.filter(created_by=request.user.id)

    return render(request, "laxout_app/chats.html", {"users": users})


@login_required(login_url="login")
def personal_chat(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)
    personal_chat = models.ChatDataModel.objects.filter(created_by=id)
    print(f"Länge des Chats{len(personal_chat)}")
    return render(
        request,
        "laxout_app/personal-chat.html",
        {"user": user, "personal_chat": personal_chat},
    )


@login_required(login_url="login")
def post_message(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)
    message = request.POST.get("message")
    is_sender = request.POST.get("is_sender")
    user.user_has_seen_chat = False
    user.save()
    models.ChatDataModel.objects.create(
        message=message, is_sender=False, created_by=id, admin_id=request.user.id
    )
    return HttpResponse("OK")


@login_required(login_url="login")
def admin_has_seen(request, id=None):
    user = models.LaxoutUser.objects.get(id=id)
    user.admin_has_seen_chat = True
    user.save()
    return HttpResponse("OK")
