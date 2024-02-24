# In einer Datei mit dem Namen "manage_trees_emails.py" im Verzeichnis "management/commands/" deiner Django-App.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.management.base import BaseCommand
from django.utils import timezone
from laxout_app import models


class Command(BaseCommand):
    help = "Manages lax trees and sends emails"

    def handle(self, *args, **kwargs):
        sender = "laxoutapp@gmail.com"
        password = "aliy rfnz mtmx xwif"
        subject = "Erinnerung an Ihr Workout"
        body = "Hallo, \nhaben Sie heute schon Ihr Workout gemacht? Wenn nicht, dann wird es höchste Zeit! Machen Sie das Physio-Workout in der App und werden Sie belohnt. Mit freundlichen Grüßen, Das Laxout-Team"

        message = MIMEMultipart()
        message["From"] = sender
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
                all_users = models.LaxoutUser.objects.all()
                users_to_send_email = []

                for i in all_users:
                    users_creation_weekday = i.creation_date.weekday()

                    if i.instruction_in_int == 1:
                        users_send_weekday = (users_creation_weekday % 7) + 1
                        if users_send_weekday == todays_weekday:
                            users_to_send_email.append(i)

                    elif i.instruction_in_int == 2:
                        users_send_weekday = (users_creation_weekday % 7) + 1
                        users_send_weekday2 = add_within_range(users_send_weekday, 3)
                        if todays_weekday in (users_send_weekday, users_send_weekday2):
                            users_to_send_email.append(i)

                    elif i.instruction_in_int == 3:
                        users_send_weekday = (users_creation_weekday % 7) + 1
                        users_send_weekday2 = add_within_range(users_send_weekday, 3)
                        users_send_weekday3 = add_within_range(users_send_weekday2, 3)
                        if todays_weekday in (
                            users_send_weekday,
                            users_send_weekday2,
                            users_send_weekday3,
                        ):
                            users_to_send_email.append(i)

                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender, password)
                text = message.as_string()
                all_users_adresses = [
                    i.email_adress for i in users_to_send_email if i.email_adress
                ]
                for i in all_users_adresses:
                    print(f"user adresse:{i}")
                for i in all_users_adresses:
                    server.sendmail(sender, i, text)
                server.quit()
                self.stdout.write(self.style.SUCCESS("Emails have been sent"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))

        def manage_lax_trees():
            all_users = models.LaxoutUser.objects.all()
            all_trees = models.LaxTree.objects.all()
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
