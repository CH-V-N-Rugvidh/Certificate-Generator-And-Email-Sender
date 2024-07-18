from pathlib import Path
import positions
import email_sender

from tkinter import Tk, Canvas, Button, PhotoImage  # Entry, Text
import tkinter
from tkinter import filedialog

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")

name_x: int
name_y: int
cid_x: int
cid_y: int
template_path: str
csv_path: str
pos = positions.Positions()


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def get_template_path():
    template_path1 = tkinter.filedialog.askopenfilename(initialdir="/", title="Select a Template",
                                                        filetypes=(("png", "*.png"), ("jpg", "*.jpg"),
                                                                   ("jpeg", "*.jpeg"), ("All Files", "*.*")))
    # If no path is selected, then do not replace the label's text with empty.
    if template_path1 != "":
        entry_1.configure(text=template_path1.replace("\\", "/"))
        globals()['template_path'] = template_path1.replace("\\", "/")


def get_csv():
    csv_path1 = tkinter.filedialog.askopenfilename(initialdir="/", title="Select the CSV File",
                                                   filetypes=(("csv", "*.csv"), ("All Files", "*.*")))
    # If no path is selected, then do not replace the label's text with empty.
    if csv_path1 != "":
        entry_2.configure(text=csv_path1.replace("\\", "/"))
        globals()['csv_path'] = csv_path1.replace("\\", "/")


def get_certificate_id_pos():
    try:
        i, j = pos.get_certificate_id_pos(template_path)
        globals()["cid_x"] = i
        globals()["cid_y"] = j
    except NameError:
        print("No Template Selected...")


def get_name_position():
    try:
        i, j = pos.get_name_pos(template_path)
        globals()['name_x'] = i
        globals()['name_y'] = j
    except NameError:
        print("No Template Selected...")


def preview():
    try:
        emailer = email_sender.Emailer()
        emailer.set_paths(template_path, csv_path)
        emailer.set_positions((name_x, name_y), (cid_x, cid_y))
        emailer.set_fonts(["tahoma.ttf", "tahoma.ttf", "tahoma.ttf", "tahoma.ttf"], [40, 10, 30, 20])
        emailer.start_preview()

    except NameError:
        print("Some of the fields are missing...")


def launch():
    try:
        emailer = email_sender.Emailer()
        emailer.set_paths(template_path, csv_path)
        emailer.set_sender("rudvid09@gmail.com", "wrop rqdo clfa yadx")  # NOQA
        emailer.set_positions((name_x, name_y), (cid_x, cid_y))
        emailer.set_fonts(["tahoma.ttf", "tahoma.ttf", "tahoma.ttf", "tahoma.ttf"], [40, 10, 30, 20])
        emailer.send_mail()

    except NameError:
        print("Some of the fields are missing...")


window = Tk()
window.geometry("778x436")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=436,
    width=778,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    391.0,
    218.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    749.0,
    404.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    8.06,
    8,
    image=image_image_3
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=get_template_path,
    relief="flat",
    bg="white"
)
button_1.place(
    x=334.0,
    y=177.0,
    width=87.00000762939453,
    height=34.684200286865234
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=get_csv,
    relief="flat",
    bg="white"
)
button_2.place(
    x=655.0,
    y=177.0,
    width=87.0,
    height=34.68000030517578
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=get_certificate_id_pos,
    relief="flat",
    bg="white"
)
button_3.place(
    x=234.0,
    y=251.0,
    width=136,
    height=52
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=launch,
    relief="flat",
)
button_4.place(
    x=337.0,
    y=360,
    width=135,
    height=52
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=get_name_position,
    relief="flat",
    bg="white"
)
button_5.place(
    x=500,
    y=251.0,
    width=136,
    height=50
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_6 = Button(
    image=button_image_6,
    text="Preview",
    borderwidth=0,
    highlightthickness=0,
    command=preview,
    relief="flat",
    bg="Blue"
)
button_6.place(
    x=337,
    y=305,
    width=135,
    height=52
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    238.0,
    195.0,
    image=entry_image_1
)
entry_1 = tkinter.Label(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=154.0,
    y=185.0,
    # width=168.0,
    width=173,
    height=18.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    564.0,
    195.0,
    image=entry_image_2
)
entry_2 = tkinter.Label(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=480.0,
    y=185.0,
    width=168.0,
    height=18.0
)

canvas.create_text(
    61.0,
    51.0,
    anchor="nw",
    text="Hello There , Kindly Read the Instructions given Below",
    fill="#E823EC",
    font=("Inter ExtraBold", 14 * -1)
)

canvas.create_text(
    61.0,
    81.0,
    anchor="nw",
    text="1.Upload Certificate Template",
    fill="#000000",
    font=("Inter SemiBold", 12 * -1)
)

canvas.create_text(
    315.0,
    81.0,
    anchor="nw",
    text="2.Upload A .CSV File",
    fill="#000000",
    font=("Inter SemiBold", 12 * -1)
)

canvas.create_text(
    61.0,
    112.0,
    anchor="nw",
    text="3.Set Desired Positions",
    fill="#000000",
    font=("Inter SemiBold", 12 * -1)
)

canvas.create_text(
    315.0,
    112.0,
    anchor="nw",
    text="4.Select their position",
    fill="#000000",
    font=("Inter SemiBold", 12 * -1)
)

canvas.create_text(
    61.0,
    143.0,
    anchor="nw",
    text="5.Press Launch",
    fill="#000000",
    font=("Inter SemiBold", 12 * -1)
)

canvas.create_text(
    70.0,
    185.0,
    anchor="nw",
    text="Template:",
    fill="#000000",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_text(
    420.0,
    261.0,
    anchor="nw",
    text="Name:",
    fill="#000000",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_text(
    70.0,
    263.0,
    anchor="nw",
    text="ROLL/CertificateID:",
    fill="#000000",
    font=("Inter SemiBold", 16 * -1)
)

canvas.create_text(
    420.0,
    185.0,
    anchor="nw",
    text="CSV:",
    fill="#000000",
    font=("Inter", 16 * -1)
)

canvas.create_text(
    270,
    315,
    anchor="nw",
    text="Preview: ",
    fill="#000000",
    font=("Inter SemiBold", 16 * -1)
)

window.resizable(False, False)
window.mainloop()
