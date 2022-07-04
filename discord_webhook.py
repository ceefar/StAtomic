from dhooks import Webhook, File

hook = Webhook("https://discord.com/api/webhooks/972807254757740594/ZPyet8Dn7A02xK49YGNoZXvRsKO7mwsX2lMyWQa4MDceLUUM4sEhv-AXpS2b2rFb7zoM")

def push_image_to_dc(imgpath:str):
    hook.send("check out this picture", file=imgpath)

def push_img_to_dc():
    discord_pic = File("imgs\\filter_view\\1_parent_test.png")
    hook.send("check out this picture", file=discord_pic)