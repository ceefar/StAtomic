from PIL import Image, ImageDraw, ImageFont, ImageFilter


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
        xText2 = 80
        #yText2 = (((height-textHeight2) / 10) + textHeight) + ((textHeight2*2) * multiplier) + 10
        

        if last_item_y_pos == 0:
            last_item_y_pos = yText1 + textHeight2 - 10
            pass


        # yText3 = yText1 + textHeight3 + 20
        # yText2 = (textHeight + 50) + (((textHeight2*2) * multiplier) + 10)
        yText2 = last_item_y_pos + textHeight2 + 10
        last_item_y_pos = yText2

        # draw the text
        imgDraw.text((xText2, yText2), message2, font=font, fill="#ce9300")

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


# SUPER SMALL UPDATE, FFS DO ACTUALLY REFACTOR THO NOT JUST 1 JILLION FUCNTIONS WITH ONLY MINOR EDITS TO OTHERS IN FINAL
def draw_dynamic_task_subtask_snapshot_updated(imgname:str, userSubTasksList:list[tuple], usertitle:str) -> str:
    """ setting up for right aligned and maybe a bit smaller but will come back to improve tbf just need a basic ting rn"""

    # path for image storage
    imgpath = f'imgs/{imgname}.png'

    # base dimensions
    width = 500
    height = 500

    # font
    fontTitle = ImageFont.truetype("PottaOne-Regular.ttf", size=22) # Righteous-Regular.ttf # PottaOne-Regular.ttf # SpecialElite-Regular.ttf
    font = ImageFont.truetype("PottaOne-Regular.ttf", size=16)
    fontWatermark = ImageFont.truetype("Righteous-Regular.ttf", size=18)

    # setting up bg rectangle & border
    w, h = 30 , 30 # basically border size so guna test using for title
    # x0 y0, x1 y1
    shape = [(470, 470), (w - 10, h - 10)]

    # new img object
    img = Image.new('RGB', (width, height), color='#8ecae6')

    # --- rectangle ----

    # draw bg rectangle & border
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
    yText1 = h + 10  # h is the border size so this is just outside of the border # (height - textHeight) / 8

    # draw the title
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xText1, yText1), message1, font=fontTitle, fill="#ffb703")

    # save the result
    img.save(imgpath)

    # ---- subtasks ----

    # FOR MULTI LINE TEXT AND TEXT TRANSPARENCY! (want transp for watermark but cba to do rn)
    # https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

    # how many subtasks there are (as may want to limit?)
    amountOfSubTasks = len(userSubTasksList)

    multiplier = 0
    last_item_y_pos = 0
    for subTask in userSubTasksList:

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # configure subtask text and location
        multiplier += 0.6 
        message2 = subTask[0]
        _, textHeight2 = imgDraw.textsize(message2, font=font)
        xText2 = 80
        #yText2 = (((height-textHeight2) / 10) + textHeight) + ((textHeight2*2) * multiplier) + 10
        

        if last_item_y_pos == 0:
            last_item_y_pos = yText1 + textHeight2
            pass


        # yText3 = yText1 + textHeight3 + 20
        # yText2 = (textHeight + 50) + (((textHeight2*2) * multiplier) + 10)
        yText2 = last_item_y_pos + textHeight2 + 10
        last_item_y_pos = yText2

        # draw the text
        if subTask[1] == "in_progress":
            imgDraw.text((xText2, yText2), message2, font=font, fill="#ffb703") # ce9300 darker shade of og title color
        else:
            # green for completed
            imgDraw.text((xText2, yText2), message2, font=font, fill="#32CD32") #32CD32 #4ee44e

        # save the result
        img.save(imgpath)


        # ---- pasting tick into sub tasks ----

        # note we are still in for loop so if condition is necessary to avoid printing green tick on every subtask line
        if subTask[1] == "completed":
             # path, r, g, b
            subi = ['imgs/icons/check_box_fill1.png ',50,205,50]
        elif subTask[1] == "in_progress":
            # path, r, g, b  #206,147,0 (og text colour) #255,87,51 (dark orange) #164,117,0 (darker orangey brown)
            # imgs/icons/arrow_right_alt_fill1.png
            # imgs/icons/remove_fill1.png
            # imgs/icons/subdirectory_arrow_right_fill1.png
            # imgs/icons/check_indeterminate_small_fill1.png
            # imgs/icons/keyboard_double_arrow_right_fill1.png
            # imgs/icons/expand_less_fill1.png
            # imgs/icons/arrow_drop_up_fill1.png
            #
            # imgs/icons/check_box_outline_blank_fill1.png
            # imgs/icons/check_box_fill1.png 
            subi = ['imgs/icons/check_box_outline_blank_fill1.png',255,87,51] 
               
        #load icon img (svg not supported btw)
        subimg = Image.open(subi[0]) 
        # resize it to the same size as the height (its a square) 
        subimg = subimg.resize((textHeight2, textHeight2))
        # convert to rgba for masking (so it is transparent where there is no fill)
        subimg = subimg.convert("RGBA")
        # paste on top of current img (everything we have so far) with color, co-ordinates, then the img mask 
        # - literally created coloured box then masks img over the top, pretty neat
        img.paste((subi[1],subi[2],subi[3]), (45, int(yText2)+3), subimg) 
        # save the result
        img.save(imgpath)

        # note we are still in for loop so if condition is necessary to avoid printing green tick on every subtask line
        #if subTask[1] == "completed":
        #    #load icon img (svg not supported btw)
        #    tickimg = Image.open('imgs/icons/task_alt_fill1.png') 
        #    # resize it to the same size as the height (its a square) 
        #    tickimg = tickimg.resize((textHeight2, textHeight2))
        #    # convert to rgba for masking (so it is transparent where there is no fill)
        #    tickimg = tickimg.convert("RGBA")
        #    # paste on top of current img (everything we have so far) with color, co-ordinates, then the img mask 
        #    # - literally created coloured box then masks img over the top, pretty neat
        #    img.paste((50,205,50), (45, int(yText2)+3), tickimg) 
        #    # save the result
        #    img.save(imgpath)
    


    # ---- watermark text ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    watermark = "St.Atomic"
    watermarkWidth, watermarkHeight = imgDraw.textsize(watermark, font=fontWatermark)
    xwaterText = (width - watermarkWidth) - 40
    ywaterText = (height - watermarkHeight) - 40  

    # draw the title
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xwaterText, ywaterText), watermark, font=fontWatermark, fill=(255,87,51))

    # save the result
    img.save(imgpath)


    # ---- watermark icon img ----

    #load icon img (svg not supported btw)
    waterimg = Image.open('imgs/icons/inventory_fill1.png') 
    # resize it to the same size as the height (its a square) 
    waterimg = waterimg.resize((int(watermarkHeight*2), int(watermarkHeight*2)))
    # convert to rgba for masking (so it is transparent where there is no fill)
    waterimg = waterimg.convert("RGBA")
    # paste on top of current img (everything we have so far) with color, co-ordinates, then the img mask 
    # - literally created coloured box then masks img over the top, pretty neat
    img.paste((255,87,51), ((xwaterText - (watermarkHeight*2) - 5), ywaterText-12), waterimg) 
    # save the result
    img.save(imgpath)



    # return the path to the created image
    return(imgpath)




if __name__ == "__main__":
    pass
    #draw_task_snapshot_test_af("ceefar")
    #draw_base_rectangle_text_img()
    #draw_improved_rectangle_text_img()
    #draw_dynamic_task_subtask_snapshot("ceefar", ["The First Child Shizzle", "Im The Second In Dis Biatch", "The Third Mofo", "A Fourth You Say!?", "Number 5 Wudup?"] , "Im The Bestest Task")

    