from PIL import Image, ImageDraw, ImageFont


def draw_base_rectangle_text_img():

    # base dimensions
    width = 500
    height = 500

    # font
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=28)
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=20)
    #font = ImageFont.truetype("PermanentMarker-Regular.ttf", size=20)

    # setting up a rectangle test
    w, h = 50 , 50
    # x0 y0, x1 y1
    shape = [(450, 450), (w - 10, h - 10)]

    # new img object
    img = Image.new('RGB', (width, height), color='#8ecae6')

    # --- rectangle ----

    # draw a rectangle test
    #imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    imgDraw = ImageDraw.Draw(img)
    imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    img.save('imgs/result.png')

    # ---- rectangle ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    message1 = "Hello boss!"
    textWidth, textHeight = imgDraw.textsize(message1, font=fontTitle)
    xText1 = (width - textWidth) / 2
    yText1 = (height - textHeight) / 8   # < TOP POSITION

    # configure first subtask text and location 
    message2 = "SubTask Title n Ting!"
    textWidth2, textHeight2 = imgDraw.textsize(message2, font=font)
    xText2 = (width - textWidth2) / 2
    yText2 = ((height - textHeight2) / 8) + (textHeight2 * 2)

    # configure first subtask text and location 
    message3 = "Im The Last Line Wuutttt!"
    textWidth3, textHeight3 = imgDraw.textsize(message3, font=font)
    xText3 = (width - textWidth3) / 2
    yText3 = ((height - textHeight3) / 8) + (textHeight3 * 4)

    # draw the text
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xText1, yText1), message1, font=fontTitle, fill="#ffb703")
    imgDraw.text((xText2, yText2), message2, font=font, fill="#ffb703")
    imgDraw.text((xText3, yText3), message3, font=font, fill="#ffb703")

    # save the result
    img.save('imgs/result.png')



def draw_improved_rectangle_text_img(imgpath = 'imgs/task-subtask.png', usertitle="Im The Main Task", userSubTask1="First SubTask Say Wutttt", userSubTask2="Second SubTask In This Biatchhhh"):
    """ setting up for right aligned and maybe a bit smaller but will come back to improve tbf just need a basic ting rn"""

    # base dimensions
    width = 500
    height = 500

    # font
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=28)
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=20)

    # setting up a rectangle test
    w, h = 50 , 50
    # x0 y0, x1 y1
    shape = [(450, 450), (w - 10, h - 10)]

    # new img object
    img = Image.new('RGB', (width, height), color='#8ecae6')

    # --- rectangle ----

    # draw a rectangle test
    #imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    imgDraw = ImageDraw.Draw(img)
    imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    img.save(imgpath)

    # ---- rectangle ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    message1 = usertitle
    textWidth, textHeight = imgDraw.textsize(message1, font=fontTitle)
    xText1 = 100
    yText1 = (height - textHeight) / 8   # < TOP POSITION

    # configure first subtask text and location 
    message2 = userSubTask1
    textWidth2, textHeight2 = imgDraw.textsize(message2, font=font)
    xText2 = 100
    yText2 = ((height - textHeight2) / 8) + (textHeight2 * 2)

    # configure first subtask text and location 
    message3 = userSubTask2
    textWidth3, textHeight3 = imgDraw.textsize(message3, font=font)
    xText3 = 100
    yText3 = ((height - textHeight3) / 8) + (textHeight3 * 4)

    # draw the text
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xText1, yText1), message1, font=fontTitle, fill="#ffb703")
    imgDraw.text((xText2, yText2), message2, font=font, fill="#ffb703")
    imgDraw.text((xText3, yText3), message3, font=font, fill="#ffb703")

    # save the result
    img.save(imgpath)



def draw_dynamic_task_subtask_snapshot(imgname:str, userSubTasksList:list, usertitle:str) -> str:
    """ setting up for right aligned and maybe a bit smaller but will come back to improve tbf just need a basic ting rn"""

    # path for image storage
    imgpath = f'imgs/{imgname}.png'

    # base dimensions
    width = 500
    height = 500

    # font
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=24)
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=18)

    # setting up a rectangle test
    w, h = 50 , 50
    # x0 y0, x1 y1
    shape = [(450, 450), (w - 10, h - 10)]

    # new img object
    img = Image.new('RGB', (width, height), color='#8ecae6')

    # --- rectangle ----

    # draw a rectangle test
    #imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    imgDraw = ImageDraw.Draw(img)
    imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    img.save(imgpath)

    # ---- title ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    message1 = usertitle
    textWidth, textHeight = imgDraw.textsize(message1, font=fontTitle)
    xText1 = 60
    yText1 = (height - textHeight) / 8   # < TOP POSITION

    # draw the text
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xText1, yText1), message1, font=fontTitle, fill="#ffb703")

    # save the result
    img.save(imgpath)

    # ---- subtasks ----

    # how many subtasks there are (as may want to limit?)
    amountOfSubTasks = len(userSubTasksList)

    multiplier = 0
    for subTask in userSubTasksList:

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # configure subtask text and location
        multiplier += 0.6 
        message2 = subTask
        _, textHeight2 = imgDraw.textsize(message2, font=font)
        xText2 = 60
        #yText2 = (((height-textHeight2) / 10) + textHeight) + ((textHeight2*2) * multiplier) + 10
        yText2 = (textHeight + 50) + (((textHeight2*2) * multiplier) + 10)

        # draw the text
        imgDraw.text((xText2, yText2), message2, font=font, fill="#ffb703")

        # save the result
        img.save(imgpath)
    
    # return the path to the created image
    return(imgpath)




################# NEW TEST AF - NEED TO DO PROPERLY BUT RUSHING RN FOR PoC ########################


def draw_task_snapshot_test_af(imgname:str, userSubTasksList:list, usertitle:str) -> str:
    """ setting up for right aligned and maybe a bit smaller but will come back to improve tbf just need a basic ting rn"""

    # path for image storage
    imgpath = f'imgs/{imgname}.png'

    # base dimensions
    width = 500
    height = 500

    # font
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=24)
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=18)

    # setting up a rectangle test
    w, h = 50 , 50
    # x0 y0, x1 y1
    shape = [(450, 450), (w - 10, h - 10)]

    # new img object
    img = Image.new('RGB', (width, height), color='#8ecae6')

    # --- rectangle ----

    # draw a rectangle test
    #imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    imgDraw = ImageDraw.Draw(img)
    imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    img.save(imgpath)

    # ---- title ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    message1 = usertitle
    textWidth, textHeight = imgDraw.textsize(message1, font=fontTitle)
    xText1 = 60
    yText1 = (height - textHeight) / 8   # < TOP POSITION

    # draw the text
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xText1, yText1), message1, font=fontTitle, fill="#ffb703")

    # save the result
    img.save(imgpath)

    # ---- subtasks ----

    # how many subtasks there are (as may want to limit?)
    amountOfSubTasks = len(userSubTasksList)

    multiplier = 0
    for subTask in userSubTasksList:

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # configure subtask text and location
        multiplier += 0.6 
        message2 = subTask
        _, textHeight2 = imgDraw.textsize(message2, font=font)
        xText2 = 60
        #yText2 = (((height-textHeight2) / 10) + textHeight) + ((textHeight2*2) * multiplier) + 10
        yText2 = (textHeight + 50) + (((textHeight2*2) * multiplier) + 10)

        # draw the text
        imgDraw.text((xText2, yText2), message2, font=font, fill="#ffb703")

        # save the result
        img.save(imgpath)
    
    # return the path to the created image
    return(imgpath)




if __name__ == "__main__":
    draw_base_rectangle_text_img()
    draw_improved_rectangle_text_img()
    draw_dynamic_task_subtask_snapshot("ceefar", ["The First Child Shizzle", "Im The Second In Dis Biatch", "The Third Mofo", "A Fourth You Say!?", "Number 5 Wudup?"] , "Im The Bestest Task")

    