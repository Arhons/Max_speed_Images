from api import *

# importing the tkinter module and PIL
# that is pillow module
from tkinter import *
from PIL import ImageTk, Image
 
def prev_point():
    i = lb_points.curselection()
    if i:
        i = i[0]
        lb_points.select_clear(i)
        if i == 0:
            i = lb_points.size()

        lb_points.select_set(i - 1)
        select_point(None)

def next_point():
    i = lb_points.curselection()
    if i:
        i = i[0]
        lb_points.select_clear(i)
        if i == lb_points.size() - 1:
            i = -1
        lb_points.select_set(i + 1)
        select_point(None)


def search():
    city = ent_city.get()
    get_images(city)
    fill_cities()

def fill_cities():
    lb_cities.delete(0, lb_cities.size() - 1)
    for i, city in enumerate(os.listdir(PATH)):
        lb_cities.insert(i, city)

def fill_points(city):
    lb_points.delete(0, lb_points.size() - 1)
    for i, point in enumerate(os.listdir(f'{PATH}/{city}')):
        lb_points.insert(i, point)

def fill_images(city, point):
    img1 = ImageTk.PhotoImage(Image.open(f"{PATH}/{city}/{point}/000.jpg").resize((300, 300)))
    img2 = ImageTk.PhotoImage(Image.open(f"{PATH}/{city}/{point}/090.jpg").resize((300, 300)))
    img3 = ImageTk.PhotoImage(Image.open(f"{PATH}/{city}/{point}/180.jpg").resize((300, 300)))
    img4 = ImageTk.PhotoImage(Image.open(f"{PATH}/{city}/{point}/270.jpg").resize((300, 300)))

    for label, img in zip((lb_image1, lb_image2, lb_image3, lb_image4), (img1, img2, img3, img4)):
        label.configure(image=img)
        label.image = img

def clear_images():
    for label in (lb_image1, lb_image2, lb_image3, lb_image4):
        label.configure(image=None)
        label.image = None

def select_city(event):
    i = lb_cities.curselection()
    if i:
        city = lb_cities.get(i[0])
        lb_city['text'] = city
        fill_points(city)
        lb_point['text'] = ''
        clear_images()

def select_point(event):
    city = lb_city['text']
    i = lb_points.curselection()
    if i:
        point = lb_points.get(i[0])
        lb_point['text'] = point
        fill_images(city, point)



# Calling the Tk (The initial constructor of tkinter)
root = Tk()
 
# We will make the title of our app as Image Viewer
root.title("Image Viewer")
 
# The geometry of the box which will be displayed
# on the screen
root.geometry("950x700")

frm_images = Frame(root)
lb_image1 = Label(frm_images)
lb_image2 = Label(frm_images)
lb_image3 = Label(frm_images)
lb_image4 = Label(frm_images)
 
# We have to show the box so this below line is needed
lb_image1.grid(row=0, column=0)
lb_image2.grid(row=0, column=1)
lb_image3.grid(row=1, column=0)
lb_image4.grid(row=1, column=1)

frm_images.grid(row=1, column=1)

frm_entry = Frame(master=root)
ent_city = Entry(master=frm_entry, width=25)
ent_city.grid(row=0, column=0)

button_search = Button(frm_entry, text="Search", command=search)
button_search.grid(row=0, column=1)
frm_entry.grid(row=0, column=0, columnspan=3)

lb_city = Label(frm_entry, text='')
lb_city.grid(row=0, column=2)
lb_point = Label(frm_entry, text='')
lb_point.grid(row=0, column=3)

frm_points = Frame(root)
lb_cities = Listbox(frm_points, selectmode=SINGLE, width=20, height=10)
lb_cities.pack()
lb_cities.bind("<<ListboxSelect>>", select_city)

lb_points = Listbox(frm_points, selectmode=SINGLE, width=20, height=10)
lb_points.pack()

frm_points.grid(row=1, column=0)
lb_points.bind("<<ListboxSelect>>", select_point)

frm_buttons = Frame(root)
button_prev = Button(frm_buttons, text="< Prev", command=prev_point)
button_prev.grid(row=0, column=0)

button_next = Button(frm_buttons, text="Next >", command=next_point)
button_next.grid(row=0, column=1)
frm_buttons.grid(row=2, column=1)


fill_cities()
lb_cities.select_set(0)
select_city(0)
 


 

 
