import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import turtle
import random


class Emailer:
    def __init__(self):
        self.sender_email = ""
        self.sender_app_password = ""
        self.receiver_email = ""
        self.subject = "Check out Your Certificate Now!"
        self.body = "Your certificate has arrived"

        self.csv_path = ""
        self.df = None
        self.template_path = ""
        self.pdf_name = ""

        self.name_x_pos = 0
        self.name_y_pos = 0
        self.cid_x_pos = 0
        self.cid_y_pos = 0

        self.font = None
        self.font1 = None
        self.font2 = None
        self.font3 = None

    def set_paths(self, template_path, csv_path):
        self.template_path = template_path
        self.csv_path = csv_path
        self.df = pd.read_csv(self.csv_path)

    def set_sender(self, sender_email, sender_app_password):
        self.sender_email = sender_email
        self.sender_app_password = sender_app_password

    def set_positions(self, name_pos_tuple: tuple, id_pos_tuple: tuple):
        self.name_x_pos, self.name_y_pos = name_pos_tuple
        self.cid_x_pos, self.cid_y_pos = id_pos_tuple

    def set_fonts(self, font_list: list, size_list: list):
        self.font = ImageFont.truetype(font=font_list[0], size=size_list[0])
        self.font1 = ImageFont.truetype(font=font_list[1], size=size_list[1])
        self.font2 = ImageFont.truetype(font=font_list[2], size=size_list[2])
        self.font3 = ImageFont.truetype(font=font_list[3], size=size_list[3])

    def start_preview(self):
        # Customize the positioning based on your template
        ran_temp = random.randint(1000, 9999)
        row_temp = None
        self.create_columns()
        for _, x in self.df.iterrows():
            row_temp = x
            break
        template = Image.open(self.template_path)
        draw = ImageDraw.Draw(template)
        x_2, y_2 = 818, 549  # coordinates event
        x_3, y_3 = 480, 565  # coordinates date

        # Accessing data using correct column names
        certificate_text_temp = f"{row_temp['Roll Number']}-{row_temp['Name (On Certificate)']}"
        draw.text((self.name_x_pos, self.name_y_pos), certificate_text_temp, font=self.font, fill='black')
        draw.text((self.cid_x_pos, self.cid_y_pos), str(ran_temp), font=self.font1, fill='black')
        draw.text((x_2, y_2), row_temp['event'], font=self.font2, fill='black')
        draw.text((x_3, y_3), "12-12-23", font=self.font3, fill='black')

        pdf_name_temp = f'{row_temp["Roll Number"]}-{row_temp["Name (On Certificate)"]}.png'
        pdf_path = "previewed_certificate" + '/' + pdf_name_temp
        template.save(pdf_path, 'png')

        self.show_preview(pdf_path)

        del (row_temp, x_2, y_2, x_3, y_3, ran_temp, pdf_name_temp, pdf_path, certificate_text_temp)

    @staticmethod
    def show_preview(pdf_path):
        s = turtle.Screen()
        s.bgpic(pdf_path)
        s.mainloop()

    def set_email_message(self):
        # Setting the message for mail
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = self.receiver_email
        message['Subject'] = self.subject
        message.attach(MIMEText(self.body, 'plain'))
        return message

    def new_mail(self, index, row, ran):
        # Customize the positioning based on your template
        self.df.at[index, 'certificateID'] = ran
        template = Image.open(self.template_path)
        draw = ImageDraw.Draw(template)
        x2, y2 = 818, 549  # coordinates event
        x3, y3 = 480, 565  # coordinates date

        # Accessing data using correct column names
        certificate_text = f"{row['Roll Number']}-{row['Name (On Certificate)']}"
        draw.text((self.name_x_pos, self.name_y_pos), certificate_text, font=self.font, fill='black')
        draw.text((self.cid_x_pos, self.cid_y_pos), str(ran), font=self.font1, fill='black')
        draw.text((x2, y2), row['event'], font=self.font2, fill='black')
        draw.text((x3, y3), "12-12-23", font=self.font3, fill='black')

        self.pdf_name = f'{row["Roll Number"]}-{row["Name (On Certificate)"]}.pdf'
        pdf_path = "downloaded_certificates/" + '/' + self.pdf_name
        template.save(pdf_path, 'PDF')
        self.attach_pdf_to_message(pdf_path)

    def attach_pdf_to_message(self, pdf_path):
        with open(pdf_path, 'rb') as attachment_file:
            pdf_attachment = MIMEApplication(attachment_file.read(), _subtype="pdf")
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=self.pdf_name)
            message = self.set_email_message()
            message.attach(pdf_attachment)

            self.login_to_email(message)

    def login_to_email(self, message):
        # Login and Send Email.
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(self.sender_email, self.sender_app_password)
            smtp.sendmail(self.sender_email, self.receiver_email, message.as_string())

    def create_columns(self):
        # Adding column 'certificateID' to CSV
        try:
            self.df["certificateID"]
        except KeyError:
            self.df["certificateID"] = [""] * len(self.df)

        # Adding column 'email_sent' to CSV
        try:
            self.df["email_sent"]
        except KeyError:
            self.df['email_sent'] = [""] * len(self.df)

        # Adding column 'event' to CSV
        self.df["event"] = ["NSS"] * len(self.df)  # NOQA

        # Adding column 'event_type' to CSV
        self.df["event_type"] = ["Hackathon"] * len(self.df)

    def send_mail(self):
        ran = random.randint(1000, 9999)

        self.create_columns()

        flag = False
        if all(self.df["email_sent"] == "success"):
            print("All emails were  already sent successfully!")
            return
            # flag = True

        for index, row in self.df.iterrows():
            if row["email_sent"] != "success":
                self.receiver_email = row["Email"]
                self.new_mail(index, row, ran)

                # Update Excel Status
                self.df.at[index, 'email_sent'] = 'success'
                ran += 1
                print(f"Email Sent Successfully for {self.receiver_email}")
        self.df.to_csv(self.csv_path, index=False)
        if not flag:
            print("All Mails Sent Successfully !")
