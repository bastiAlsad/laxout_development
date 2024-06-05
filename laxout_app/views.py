from django.shortcuts import render
from string import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from . import forms
#Test

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
        print(str(user.last_login.date) + "Last Login date")
        if days_between_today_and_date(user.last_login) < 14:
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
                <p>Sie können die App 2 Wochen kostenlos und unverbindlich benutzen. Nach der 2 wöchigen Testphase werden wir Sie fragen, ob Sie die App für einmalig 29€ weiternutzen möchten.</p>
                <p>Wenn Sie darauf nicht antworten, oder Sie sich gegen die weitere Nutzung entscheiden, werden wir Ihre Daten löschen und Ihr Zugang wird ungültig. </p>
                <p>Drücken Sie nun bitte auf den <a href="${link}" style=" color: blue;">Loslegen</a> Button, um mit Ihrem Training beginnen!</p>
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
    # billing_model, created = models.BillingCount.objects.get_or_create(id=1)
    # billing_count = str(billing_model.billing_count)
    # new_billing_count = billing_model.billing_count+1
    # billing_model.billing_count = new_billing_count
    # billing_model.save()
    # current_billing_id = ""
    # how_many_zeros = 12-len(billing_count)

    # for i in range(how_many_zeros):
    #     current_billing_id+= "0"
    # current_billing_id+= billing_count
    # #Produktion
    # #/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/ 
    # #Dev
    # #D:/DEV/laxout_backend_development/laxout/laxout_app/leistungsnachweise/
    # print(f"Current billing Id {current_billing_id}")
    # input_pdf_path = "/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_vorlage.pdf"  # Passe den Pfad zur vorhandenen PDF-Datei an D:/DEV/laxout_backend_development/laxout/laxout_app/leistungsnachweise/leistungsnachweis
    # output_pdf_path = f"/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_{current_billing_id}.pdf"  # Passe den Pfad für die neu erstellte PDF-Datei an
    # pdf.modifyPdf(input_pdf_path,output_pdf_path,current_billing_id)

    # # Pfad zur PDF-Datei
    # pdf_attachment_path = f"/home/dashboardlaxout/backup_laxout/laxout_app/leistungsnachweise/leistungsnachweis_{current_billing_id}.pdf"

    # # Hinzufügen der PDF-Datei als Anhang
    # with open(pdf_attachment_path, 'rb') as pdf_attachment:
    #     part = MIMEApplication(pdf_attachment.read(), 'pdf')
    #     part.add_header('Content-Disposition', f'attachment; filename= {pdf_attachment_path}')
    #     msg.attach(part)

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
            email = form.cleaned_data.get("email_adress")
            note = request.POST.get("selected_illness")
            insteance.note = note
            insteance.save()
            # lax_ai.train_model(request.user.id)
            # predicted_exercises_ids = lax_ai.predict_exercise(note)

            exercises = []
            print(f"note{note}")

            ai_training_data = models.AiTrainingDataGlobal.objects.filter(illness=note).last()

            # , created_by=request.user.id

            if ai_training_data != None:
                list_order_objects = (
                    models.Laxout_Exercise_Order_For_User.objects.filter(
                        laxout_user_id=ai_training_data.id
                    )
                )
                # print("LIST Skipped LENGTH {}".format(skipped_exercises))
                sorted_list = sorted(
                    list_order_objects, key=lambda x: x.order
                )  # Werden der größe nach Sotiert
                # print("Sorted List {}".format(sorted_list))
                related_exercises_rigth_order = []

                for i in sorted_list:
                    related_exercises_rigth_order.append(
                        models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
                    )

                

                for i in related_exercises_rigth_order:
                    user_instance = insteance
                    # es wird geschaut, ob es schon eine Reihenfolge gibt
                        
                    exercise_to_add = Laxout_Exercise.objects.create(
                            execution=Uebungen_Models.objects.get(id=i.appId).execution,
                            name=Uebungen_Models.objects.get(id=i.appId).name,
                            dauer=Uebungen_Models.objects.get(id=i.appId).dauer,
                            videoPath=Uebungen_Models.objects.get(id=i.appId).videoPath,
                            looping=Uebungen_Models.objects.get(id=i.appId).looping,
                            added=False,
                            instruction="",
                            timer=Uebungen_Models.objects.get(id=i.appId).timer,
                            required=Uebungen_Models.objects.get(id=i.appId).required,
                            imagePath=Uebungen_Models.objects.get(id=i.appId).imagePath,
                            appId=Uebungen_Models.objects.get(id=i.appId).id,
                            onlineVideoPath=Uebungen_Models.objects.get(
                                id=i.appId
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
        ilness_list_obj = models.AiTrainingDataGlobal.objects.all()
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


    current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )  # es wird geschaut, ob es schon eine Reihenfolge gibt

    print(f"ids der geradigen order:")
    for i in current_order_objects:
        print(i.laxout_exercise_id)


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

        print(f"ID der hinzugefügten Übung {exercise_to_add.id}")

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


#from . import signals


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


additionalUebungList2 = [  
    
]


uebungen_to_append00 = []  # Nacken
uebungen_to_append01 = []
uebungen_to_append02 = []
uebungen_to_append07 = []
uebungen_to_append10 = []  # Schultern
uebungen_to_append11 = []
uebungen_to_append12 = []
uebungen_to_append17 = []
uebungen_to_append20 = []  # Mittlerer Rücken
uebungen_to_append21 = []
uebungen_to_append22 = []
uebungen_to_append27 = []
uebungen_to_append30 = []  # Bauch Rumpf
uebungen_to_append31 = []
uebungen_to_append32 = []
uebungen_to_append37 = []
uebungen_to_append40 = []  # Unterer Rücken
uebungen_to_append41 = []
uebungen_to_append42 = []
uebungen_to_append47 = []
uebungen_to_append50 = []  # Beine Füße
uebungen_to_append51 = []
uebungen_to_append52 = []
uebungen_to_append57 = []
uebungen_to_append60 = []  # Arme Hände
uebungen_to_append61 = []
uebungen_to_append62 = []
uebungen_to_append67 = [254, 255, 256, 257]




def inizialize_first_second(debugValue):# Falls die Ids in der Datenbank durch löschungen verzogen werden kommt ein debugValue hinzu, der die Ids anpasst ab Übung 210 wird der wert relevant (387)
    for i in uebungen_to_append00:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append01:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append02:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=0))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append07:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append10:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append11:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append12:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append17:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=1))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append20:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append21:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append22:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append27:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=2))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append30:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append31:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append32:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append37:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=3))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append40:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append41:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append42:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append47:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=4))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append50:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append51:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append52:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append57:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=5))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()
    for i in uebungen_to_append60:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=0))
        instance_exercise.save()
    for i in uebungen_to_append61:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=1))
        instance_exercise.save()
    for i in uebungen_to_append62:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=2))
        instance_exercise.save()
    for i in uebungen_to_append67:
        instance_exercise = models.Uebungen_Models.objects.get(id=i+debugValue)
        instance_exercise.first.add(models.First.objects.create(first=6))
        instance_exercise.second.add(models.Second.objects.create(second=7))
        instance_exercise.save()



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
        
    #Create new Exercises
    for i in additionalUebungList2:
                Uebungen_Models.objects.create(
                    looping=i.looping,
                    timer=i.timer,
                    execution=i.execution,
                    name=i.name,
                    videoPath=i.videoPath,
                    dauer=i.dauer,
                    imagePath=i.imagePath,
                    added=i.added,
                    instruction=i.instruction,
                    required=i.required,
                    onlineVideoPath = i.onlineVidePath

                )
    inizialize_first_second(0)#auf pythonanywhere ist dieser wert aktuell 387 erklärung bei 'def' inizialize..

    # models.Uebungen_Models.objects.all().delete()
    # models.First.objects.all().delete()
    # models.Second.objects.all().delete()

    # from . import signals
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
    # inizialize_first_second()

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


@login_required(login_url="login")
def edit_plans(request):
    plans_list = models.AiTrainingDataGlobal.objects.all()
    print(f"plans_list{plans_list}")
    return render(
        request,
        "laxout_app/plaene.html",
        {
            "plans_list": plans_list,
        },
    )


@login_required(login_url="login")
def delete_plan(request, id=None):
    if id != None:
        print("id nicht none")
        plan_to_delete = models.AiTrainingDataGlobal.objects.get(id=id)
        if plan_to_delete.created_by == request.user.id:
            print("gelöscht")
            plan_to_delete.delete()
    return render(request, "laxout_app/plaene.html")


@login_required(login_url="login")
def edit_plan(request, id=None):

    plan = models.AiTrainingDataGlobal.objects.get(id=id)

    related_exercises = plan.related_exercises.all()

    related_exercises = []

    current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )  # es wird geschaut, ob es schon eine Reihenfolge gibt

    print(f"ids der geradigen order:")
    for i in current_order_objects:
        print(i.laxout_exercise_id)

    if len(current_order_objects) == 0 and len(related_exercises) != 0:
        print("There was a diffenrence")
        order = 1
        for i in related_exercises:
            models.Laxout_Exercise_Order_For_User.objects.create(
                laxout_user_id=id, laxout_exercise_id=i.id, order=order
            )

            order += 1
        print("length")
        print(len(models.Laxout_Exercise_Order_For_User.objects.all()))

    print("LENGTH ORDER OBJECTS{}".format(len(current_order_objects)))

    list_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
        laxout_user_id=id
    )
    # print("LIST Skipped LENGTH {}".format(skipped_exercises))
    sorted_list = sorted(
        list_order_objects, key=lambda x: x.order
    )  # Werden der größe nach Sotiert
    # print("Sorted List {}".format(sorted_list))
    related_exercises_rigth_order = []

    for i in sorted_list:
        related_exercises_rigth_order.append(
            models.Laxout_Exercise.objects.get(id=i.laxout_exercise_id)
        )

    return render(
        request,
        "laxout_app/edit_plan.html",
        {"related_exercises": related_exercises_rigth_order, "plan": plan},
    )



@login_required(login_url="login")
def add_exercises_plan(request, id=None, first=0, second=0):
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
            new_dauer = models.Uebungen_Models.objects.get(id=new_id).dauer

        programm_instance = models.AiTrainingDataGlobal.objects.get(id=id)
        current_exercises = programm_instance.related_exercises.all()

        current_order_objects = models.Laxout_Exercise_Order_For_User.objects.filter(
            laxout_user_id=id
        )
        if len(current_order_objects) == 0 and len(current_exercises) != 0:
            print("There was a diffenrence")
            order = 1
            for i in current_exercises:
                models.Laxout_Exercise_Order_For_User.objects.create(
                    laxout_user_id=id, laxout_exercise_id=i.id, order=order
                )
                order += 1

        exercise_to_add = models.Laxout_Exercise.objects.create(
            execution=new_execution,
            name=models.Uebungen_Models.objects.get(id=new_id).name,
            dauer=new_dauer,
            videoPath=models.Uebungen_Models.objects.get(id=new_id).videoPath,
            looping=models.Uebungen_Models.objects.get(id=new_id).looping,
            added=False,
            instruction="",
            timer=models.Uebungen_Models.objects.get(id=new_id).timer,
            required=models.Uebungen_Models.objects.get(id=new_id).required,
            imagePath=models.Uebungen_Models.objects.get(id=new_id).imagePath,
            appId=new_id,
            onlineVideoPath=models.Uebungen_Models.objects.get(
                id=new_id
            ).onlineVideoPath,
        )
        order_new_exercise = len(current_order_objects) + 1

        print(f"ID der hinzugefügten Übung {exercise_to_add.id}")

        models.Laxout_Exercise_Order_For_User.objects.create(
            laxout_user_id=id,
            laxout_exercise_id=exercise_to_add.id,
            order=order_new_exercise,
        )

        print(exercise_to_add.dauer)
        exercise_to_add.save()

        if request.user.id == programm_instance.created_by:
            programm_instance.related_exercises.add(exercise_to_add)
            programm_instance.save()

    workout_list = get_workout_list(0, 0)

    return render(
        request,
        "laxout_app/add_exercises.html",
        {"workouts": workout_list, "userId": id},
    )


@login_required(login_url="login")
def edit_plan_exercise(
    request,
    id=None,
):
    if request.method == "POST":
        new_execution = request.POST.get("execution")
        print("new execution:{}".format(new_execution))
        new_dauer = request.POST.get("dauer")  # .objects.get(id=new_id)
        exercise_to_edit_id = request.POST.get("id")
        plan_id = request.POST.get("planId")
        print("plan_id:{}".format(plan_id))
        programm_instance = models.AiTrainingDataGlobal.objects.get(id=plan_id)
        exercise_to_edit = programm_instance.related_exercises.get(
            id=exercise_to_edit_id
        )
        if new_execution:
            exercise_to_edit.execution = new_execution
        if new_dauer:
            exercise_to_edit.dauer = new_dauer
        exercise_to_edit.save()
        programm_instance.save()
    return render(
        request,
        "laxout_app/edit_plan.html",
    )

@login_required(login_url="login")
def delete_plan_exercise(
    request,
    id=None,
):
    if request.method == "POST":
        print("ANGEKOMMEN")
        to_delete_id = request.POST.get("id")
        print(f"to delet id {to_delete_id}")
        instance = models.AiTrainingDataGlobal.objects.get(id=id)
        exercise_to_delete = models.Laxout_Exercise.objects.get(id=to_delete_id)

        if request.user.id == instance.created_by:
            exercise_to_delete.delete()
            instance.save()
            print("to delete id")
            print(to_delete_id)
            to_delete = models.Laxout_Exercise_Order_For_User.objects.get(
                laxout_exercise_id=to_delete_id, laxout_user_id=id
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

    return render(
        request,
        "laxout_app/edit_plan.html",
    )


@login_required(login_url="login")
def create_ai_training_data(request):
    active_admin = models.UserProfile.objects.get(user=request.user)
    active_admin_user = active_admin.user
    if request.method == "POST":
        form = forms.TrainingDataForm(request.POST)
        print("OK")
        if form.is_valid():
            illness = form.cleaned_data.get("illness")
            print(f"illness{illness}")
            models.AiTrainingDataGlobal.objects.get_or_create(
                illness=illness, created_by=request.user.id
            )
            # print(lax_ai.predict_exercise(note))
        return redirect("/home")

    else:
        form = forms.TrainingDataForm
        return render(
            request,
            "laxout_app/create_trainingdata.html",
            {
                "form": form,
                "is_superuser": active_admin_user.is_superuser,
            },
        )


@login_required(login_url="login")
def move_up_plan(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        plan = models.AiTrainingDataGlobal.objects.get(id=id)
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

        context = {"exercises": plan.related_exercises.all()}
        return render(request, "laxout_app/edit_user.html", context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")


@login_required(login_url="login")
def move_down_plan(request, id=None):
    try:
        exercise_id = request.POST.get("exercise_id")
        plan = models.AiTrainingDataGlobal.objects.get(id=id)
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

        context = {"exercises": plan.related_exercises.all()}
        return render(request, "laxout_app/edit_user.html", context)
    except:
        print(Exception)
        return HttpResponse("ERROR INTERNAL 4_0_4")