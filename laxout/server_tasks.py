from laxout_app import models
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.utils import timezone

sender = "laxoutapp@gmail.com"
reciever = "b.t.friedrich@web.de"
password = "aliy rfnz mtmx xwif"
subject = "Erinnerung an ihr Workout"
body = "Hallo, \nhaben Sie heute schon Ihr Workout gemacht ? Wenn nicht dann wird es höchste Zeit ! Machen Sie das Physio-Workout in der App und werden Sie belohnt. Mit freunlichen Grüßen Das Laxout-Team"

message = MIMEMultipart()
message["From"] = sender
message["To"] = reciever
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))


def add_within_range(number, addend, range_start=1, range_end=7):
    result = (number + addend - range_start) % (
        range_end - range_start + 1
    ) + range_start
    return result


def send_emails():
    try:
        todays_weekday = timezone.datetime.now().weekday()
        print(f"todays weekday {todays_weekday}")
        all_users = models.LaxoutUser.objects.all()
        users_to_send_email = []
        users_send_weekday = 0
        users_send_weekday2 = 0
        users_send_weekday3 = 0
        

        for i in all_users:
            users_creation_weekday = i.creation_date.weekday()
            if i.instruction_in_int == 1:
                if users_creation_weekday == 7:
                    users_send_weekday = 1
                else:
                    users_send_weekday = users_creation_weekday + 1
                if users_send_weekday == todays_weekday:
                    users_to_send_email.append(i)

            if i.instruction_in_int == 2:
                if users_creation_weekday == 7:
                    users_send_weekday = 1
                    users_send_weekday2 = 4

                else:
                    users_send_weekday = users_creation_weekday + 1
                    users_send_weekday2 = add_within_range(
                        users_creation_weekday + 1, 3
                    )
                if (
                    users_send_weekday == todays_weekday
                    or users_send_weekday2 == todays_weekday
                ):
                    users_to_send_email.append(i)

            if i.instruction_in_int == 3:
                if users_creation_weekday == 7:
                    users_send_weekday = 1
                    users_send_weekday2 = 3
                    users_send_weekday3 = 6

                else:
                    users_send_weekday = users_creation_weekday + 1
                    users_send_weekday2 = add_within_range(
                        users_creation_weekday + 1, 3
                    )
                    users_send_weekday3 = add_within_range(users_send_weekday2, 3)
                if (
                    users_send_weekday == todays_weekday
                    or users_send_weekday2 == todays_weekday
                    or users_send_weekday3 == todays_weekday
                ):
                    users_to_send_email.append(i)
            print(users_creation_weekday)
        
        print(users_send_weekday)
        print(users_send_weekday2)
        print(users_send_weekday3)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        print("Logged in ...")
        text = message.as_string()
        all_users_adresses = []
        for i in users_to_send_email:
            if i.email_adress != "":
                all_users_adresses.append(i.email_adress)
        for i in all_users_adresses:
            server.sendmail(sender, i, text)
        print("Emails have been sent")
        server.quit()
    except Exception as e:
        print("An error occurred:", e)


def manage_lax_trees():
    all_users =  models.LaxoutUser.objects.all()
    all_trees =  models.LaxTree.objects.all()
    for i in all_trees:
        if i.condition >= 14.3:
            i.condition -= 14.3
        else:
            i.condition = 0
        i.save()
    for i in all_users:
        users_lax_tree = models.LaxTree.objects.get(id=i.lax_tree_id)
        to_add = users_lax_tree.condition * 1.5
        i.laxout_credits += to_add
        i.save()
    print("managed")


manage_lax_trees()
send_emails()
