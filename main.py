import PIL.Image
import cv2
import os
from tkinter import *
import time


# from colorama import init
# from colorit import *
# from termcolor import colored

# init()
# init_colorit()

# ascii characters used to build the output text
# stringofasci = "Ñ@#W$9876543210?!abc;:+=-,._       "
# stringofasci = '  .,:;i1tfLCG08@'
stringofasci = '  `:-=+*#%@'
# stringofasci=stringofasci[::-1]
ASCII_CHARS = list(stringofasci)
# print(len(ASCII_CHARS))
# ASCII_CHARS = [ '`' , '.',':',';','!','*','&','O','R','B','@']


# resize image according to a new width
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 2
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return (resized_image)


# convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    return (grayscale_image)


# convert pixels to a string of ascii characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 28] for pixel in pixels])
    return (characters)

row_count = 0
# colors = ['red' , 'white' ,'green' ,'blue']
list_of_words = ['','.']


# class CustomText(Text):
#     '''A text widget with a new method, highlight_pattern()
#
#     example:
#
#     text = CustomText()
#     text.tag_configure("red", foreground="#ff0000")
#     text.highlight_pattern("this should be red", "red")
#
#     The highlight_pattern method is a simplified python
#     version of the tcl code at http://wiki.tcl.tk/3246
#     '''
#     def __init__(self, *args, **kwargs):
#         Text.__init__(self, *args, **kwargs)
#
#     def highlight_pattern(self, pattern, tag, start="1.0", end="end",
#                           regexp=False):
#         '''Apply the given tag to all text that matches the given pattern
#
#         If 'regexp' is set to True, pattern will be treated as a regular
#         expression according to Tcl's regular expression syntax.
#         '''
#
#         start = self.index(start)
#         end = self.index(end)
#         self.mark_set("matchStart", start)
#         self.mark_set("matchEnd", start)
#         self.mark_set("searchLimit", end)
#
#         count = IntVar()
#         while True:
#             index = self.search(pattern, "matchEnd","searchLimit",
#                                 count=count, regexp=regexp)
#             if index == "": break
#             if count.get() == 0: break # degenerate pattern which matches zero-length strings
#             self.mark_set("matchStart", index)
#             self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
#             self.tag_add(tag, "matchStart", "matchEnd")

# def check():
#     mytext.tag_remove('found', '1.0', END)
#
#     for word in list_of_words:
#         idx = '1.0'
#         while idx:
#             idx = mytext.search(word, idx, nocase=1, stopindex=END)
#             if idx:
#                 lastidx = '%s+%dc' % (idx, len(word))
#                 mytext.tag_add('found', idx, lastidx)
#                 idx = lastidx
#
#     mytext.tag_config('found', foreground='white')

def main( new_width=100):
    global ascii_image
    vid = cv2.VideoCapture(0)
    while (True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        frame = cv2.flip(frame, 1)
        frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        image = PIL.Image.fromarray(frame)
        # cv2.imshow('Preview', frame)


        # convert image to ascii
        new_image_data = pixels_to_ascii(resize_image(image))

        # format
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(
            [new_image_data[index:(index + new_width)] for index in range(0, pixel_count, new_width)])






        # print result
        # print(colored(ascii_image, 'green'))
        # print(ascii_image)
        # check()
        mytext.delete("1.0", "end")  # if you want to remove the old data
        mytext.insert(END,ascii_image)
        # # start = mytext.search(' ', '1.0', stopindex=END)
        # mytext.tag_add("change" , '1.0' , '1.5')
        # mytext.config("change" , foreground = 'green')
        # mytext.update()
        # check()
        find()


        root.update()
        # print((color(ascii_image , Colors.white)))

        # time.sleep(0.5)
        # os.system('cls')
        rows_full = row_count + 2
        # print("\033[F" * rows_full)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def color_change(cl):
    mytext.configure(background="black", foreground=cl)


def write_in_text():
    t, s = str(time.time()).split('.')
    filename = t + ".txt"
    text_file = open(filename, "w")

    # write string to file
    text_file.write(ascii_image)

    # close file
    text_file.close()

def find():
    # remove tag 'found' from index 1 to END
    mytext.tag_remove('found', '1.0', END)

    # returns to widget currently in focus
    s = edit.get()
    if s:
        idx = '1.0'
        while 1:
            # searches for desired string from index 1
            idx = mytext.search(s, idx, nocase=1,
                              stopindex=END)
            if not idx: break

            # last index sum of current index and
            # length of text
            # print('found')
            lastidx = '%s+%dc' % (idx, len(s))

            # overwrite 'Found' at idx
            mytext.tag_add('found', idx, lastidx)
            idx = lastidx

        # mark located string as red
        mytext.tag_config('found', foreground='yellow')
        mytext.update()
    # edit.focus_set()
# run program
root= Tk()

root.geometry("830x760")

# root.configure(bg='white')
fram = Frame(root)

# adding label to search box
Label(fram, text='insert char to change color:').pack(side='top')
# adding of single line text box
edit = Entry(fram)

# adding of search button
# butt = Button(fram, text='Find' , command = find)


mytext = Text(root, height = 860, width =    620 )
Bblue = Button(root, text ="Bluecolor", command = lambda: [color_change('blue')])
Bwhite = Button(root, text ="whitecolor", command = lambda : [color_change('white')])
Bred = Button(root, text ="redcolor", command = lambda : [color_change('red')])
Bgreen = Button(root, text ="greencolor", command = lambda : [color_change('green')])
capt = Button(root, text ="Capture_In_text", command = lambda : [write_in_text()])



# text = CustomText()
# text.tag_configure("red", foreground="#ff0000")
# text.highlight_pattern("this should be red", "red")
mytext.configure(background="black", foreground='red')
# mytext.tag_configure("whitec", foreground="white")
# mytext.highlight_pattern("word", "red")
# mytext.tag_config(" ", foreground = "blue")
# configuring a tag called start
# mytext.tag_add("start" , '1.0' , 'end')
# mytext.tag_config("start", background="black",
#                 foreground="red")

capt.config(height=3,
width=80 , fg = 'blue' , bg = 'white')
Bblue.pack(side = 'top')
Bwhite.pack(side = 'top')
Bgreen.pack(side = 'top')
Bred.pack(side = 'top')
capt.pack(side = 'top')
fram.pack(side='top')
# butt.pack(side='top')
edit.pack(side='top', fill=BOTH, expand=1)
# edit.focus_set()
# text.pack()
mytext.pack(side = 'right')
ascii_image = ""

# setting focus

main()