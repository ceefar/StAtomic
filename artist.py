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
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=22)
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=16)

    # setting up a rectangle test
    w, h = 30 , 30
    # x0 y0, x1 y1
    shape = [(470, 470), (w - 10, h - 10)]

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
    last_item_y_pos = 0
    for subTask in userSubTasksList:

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # configure subtask text and location
        multiplier += 0.6 
        message2 = subTask
        _, textHeight2 = imgDraw.textsize(message2, font=font)
        xText2 = 60
        #yText2 = (((height-textHeight2) / 10) + textHeight) + ((textHeight2*2) * multiplier) + 10
        

        if last_item_y_pos == 0:
            last_item_y_pos = yText1 + textHeight2 - 10
            pass


        # yText3 = yText1 + textHeight3 + 20
        # yText2 = (textHeight + 50) + (((textHeight2*2) * multiplier) + 10)
        yText2 = last_item_y_pos + textHeight2 + 10
        last_item_y_pos = yText2

        # draw the text
        imgDraw.text((xText2, yText2), message2, font=font, fill="#ffb703")

        # save the result
        img.save(imgpath)
    
    # return the path to the created image
    return(imgpath)




################# NEW TEST AF - NEED TO DO PROPERLY BUT RUSHING RN FOR PoC ########################


def draw_task_snapshot_test_af(todoTaskID:int, userTagsList:list, title:str, details:str = "") -> str:
    """ new, basic test for filter view page """

    # todoTaskID, title, detail, tagsList, taskStatus, createdDate, days_since_created, IF VALID : updatedDate, days_since_updated

    # path for image storage
    imgpath = f'imgs/filter_view/{todoTaskID}_test.png'

    # base dimensions
    width = 500
    height = 500

    # font
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=20)
    fontSubTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=16)
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=14)

    # setting up a rectangle test
    w, h = 30 , 30
    # x0 y0, x1 y1
    shape = [(470, 470), (w - 10, h - 10)]

    # new img object
    img = Image.new('RGB', (width, height), color='#8ecae6')

    # --- rectangle/bg ----

    # draw a rectangle test
    #imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    imgDraw = ImageDraw.Draw(img)
    imgDraw.rectangle(shape, fill ="#023047", outline ="#ffb703")
    img.save(imgpath)

    # ---- title ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    message1 = title
    textWidth, textHeight = imgDraw.textsize(message1, font=fontTitle)
    xText1 = 60
    yText1 = (height - textHeight) / 8   # < TOP POSITION

    # draw the text
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xText1, yText1), message1, font=fontTitle, fill="#ffb703")

    # save the result
    img.save(imgpath)





    ######## NEW ########

    # ---- details ----
    if details:

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # configure the title text and location
        message3 = details
        textWidth3, textHeight3 = imgDraw.textsize(message3, font=fontSubTitle)
        #### NEED HERE - if textwidth larger than rectangle width then split the line!
        xText3 = 60
        yText3 = yText1 + textHeight3 + 20   # under title?

        # draw the text
        #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
        imgDraw.text((xText3, yText3), message3, font=fontTitle, fill="#ffb703")

        # save the result
        img.save(imgpath)


    # ---- tags ----

    # how many subtasks there are (as may want to limit?)
    amountOfSubTasks = len(userTagsList)

    multiplier = 0
    for subTask in userTagsList:

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # configure subtask text and location
        multiplier += 0.6 
        message2 = subTask
        textWidth2, textHeight2 = imgDraw.textsize(message2, font=font)
        xText2 = 20
        #yText2 = (((height-textHeight2) / 10) + textHeight) + ((textHeight2*2) * multiplier) + 10
        yText2 = (textHeight + 50) + (((textHeight2*2) * multiplier) + 50)

        # draw the text
        imgDraw.rectangle((xText2, yText2+5, (xText2 + textWidth2)+5, (yText2 + textHeight2)+5), fill='#ffb703')
        imgDraw.text((xText2+2.5, yText2+2.5), message2, font=font, fill="#023047")

        # save the result
        img.save(imgpath)
    
    # return the path to the created image
    return(imgpath)



def draw_task_snapshot_parentchild_test_af(todoTaskID:int, userTagsList:list, title:str, details:str = "") -> str:
    pass




if __name__ == "__main__":
    pass
    #draw_task_snapshot_test_af("ceefar")
    #draw_base_rectangle_text_img()
    #draw_improved_rectangle_text_img()
    #draw_dynamic_task_subtask_snapshot("ceefar", ["The First Child Shizzle", "Im The Second In Dis Biatch", "The Third Mofo", "A Fourth You Say!?", "Number 5 Wudup?"] , "Im The Bestest Task")

    