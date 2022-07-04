import os
from dhooks import Webhook, File


#dcwebhook = ""

hook = Webhook(dcwebhook)

image1 = "imgs/mood/mood-swings.png"
image2 = "imgs/other/abstract-blur-supermarket.jpg"

def push_image_to_dc(imgpath:str):
    imgpath = imgpath.replace("\\","/")
    hook.send("Here's Your Image", file=File(imgpath))

def push_test_img_to_dc():
    discord_pic = File("imgs/filter_view/1_parent_test.png")
    hook.send("check out this picture", file=discord_pic)

def push_msg_to_dc(msg):
    hook.send(msg)

