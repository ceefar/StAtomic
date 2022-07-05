from dhooks import Webhook, File, Embed

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

def push_embed_to_dc(desc:str = "This is the **description** of the embed! :smiley:", hex_color = 0x5CDBF0,
                        imgiconlink:str = "https://i.imgur.com/rdm3W9t.png", imgbannerlink:str = "https://i.imgur.com/f1LOr4q.png",
                        authr:str = "The Author", field1_name:str="Test Field", field1_value:str = "Value of the field :open_mouth:",
                        field2_name:str = "Another Field", field2_value:str = "1234 :smile:", footer_text:str = "I'm the footer"):

    """ two fields + footer and images, color can be changed in function, supports emoji, note should improve whole function to be more dynamic """

    # main embed object
    embed = Embed(
        description=desc,
        color=0x5CDBF0, # 0xEBA538 0x5CDBF0 - accepts hex or int, literally just the color of the strip to the left of the embed
        timestamp="now"  # "now" sets the timestamp to current time or use format -> "2015-12-31T12:00:00.000Z"
        )
    # define images, must be web links
    image1 = imgiconlink 
    image2 = imgbannerlink
    # embed body
    embed.set_author(name=authr, icon_url=image1)
    embed.add_field(name=field1_name, value=field1_value)
    embed.add_field(name=field2_name, value=field2_value)
    embed.set_footer(text=footer_text, icon_url=image1)
    # set images
    embed.set_thumbnail(image1)
    embed.set_image(image2)
    # send embed via webhook
    hook.send(embed=embed)

