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



# ---- NEW [TEST] SHOPPING LIST ARTIST ----


def draw_dynamic_shopping_list(imgname:str, listItems:list, listTitle:str) -> str:
    """ does multi line only up to 22 list items currently and list item over 26 chars will likely break but is gravy for now """

    # path for image storage
    imgpath = f'imgs/{imgname}.png'

    # base bg dimensions
    # FIXME - MAKE THIS DYNAMIC NOW!
    #   - hmm its a bg tho so how, would have to stick extra img or if is longer use a different img?
    width = 500
    height = 393 

    # define fonts 
    fontTitle = ImageFont.truetype("imgs/font_files/AmaticSC-Bold.ttf", size=38) # AmaticSC-Bold.ttf
    font = ImageFont.truetype("imgs/font_files/Caveat-SemiBold.ttf", size=20) # Caveat-SemiBold.ttf # GloriaHallelujah-Regular.ttf # PatrickHand-Regular.ttf

    # open new img object of paper bg
    img = Image.open('imgs/other/lined_paper_one.jpg')

    # resize the image and save it as our bg
    resized_img = img.resize((width, height))
    resized_img.save(imgpath)

    # ---- title ----

    # setup base object from original resized img background and open it for drawing 
    img = Image.open(imgpath)
    imgDraw = ImageDraw.Draw(img)

    # configure the title text position, and grab its dimensions based on its font incase we need them
    shopTitle = listTitle
    titleWidth, titleHeight = imgDraw.textsize(shopTitle, font=fontTitle)
    xTitlePos = 70
    yTitlePos = 10

    # draw the title on the bg img
    imgDraw.text((xTitlePos, yTitlePos), shopTitle, font=fontTitle, fill="#7C0D0E") # 0D7C7B deep red

    # save the result
    img.save(imgpath)

    # ---- list items ----

    # how many subtasks there are (as may want to limit?)
    amountOfListItems = len(listItems)
    print(f"{amountOfListItems = }")

    # var used for creating new spacing for each line
    last_item_y_pos = 0
    # var used for cropping & 2nd column x positioning, need to know what is the longest line on the page
    longest_list_item = 0
    # vars for setting list items x position in second loop (dont want this to change)
    secondloop = False
    longest_li_second_loop = longest_list_item
    # runs (draws) for each item in the list
    for i, item in enumerate(listItems):

        # FIXME 
        # do this shit proper so dont have this slice thing based on longer list items
        # and obvs also need to do proper sized img n shit blah blah blah is fine for now just add this slice chars thing tbf

        # temporary slice long lines if there are two columns on the page since could break formatting
        if len(item) > 28 and amountOfListItems > 11:
            item = item[:28]

        # setup base object
        imgDraw = ImageDraw.Draw(img)

        # to set the new x pos for the second loop once and not have it change
        if amountOfListItems > 11 and i > 10 and secondloop == False:
            longest_li_second_loop = longest_list_item + 70
            secondloop = True

        # configure list items x position, and grab its dimensions based on its font incase we need them
        listItem = item
        liWidth, liHeight = imgDraw.textsize(listItem, font=font)
        if i <= 10:
            xLiTextPos = 70
        else:
            xLiTextPos = longest_li_second_loop + 30

        # if list item is the longest save it outside of loop, this is used to crop
        if liWidth > longest_list_item:
            longest_list_item = liWidth
        
        # should reset for the second loop
        if i == 11:
            last_item_y_pos = 0

        # if first iteration only
        if last_item_y_pos == 0:
            # slightly different as need to set the first position as it is the hinge for the remaining list items
            last_item_y_pos = yTitlePos + 20.5 
            print(f"{last_item_y_pos = }")

        # after this every line is just added a set amount (dont use liHeight as this changes duhhh)
        yLiTextPos = last_item_y_pos + 27.5
        last_item_y_pos = yLiTextPos
        print(f"{last_item_y_pos = }")

        # draw the list item text
        imgDraw.text((xLiTextPos, yLiTextPos), listItem, font=font, fill="#191970") # 191970 midnight blue

        # save the result
        img.save(imgpath)
        

    # crop if only 1 column (11 items or less)
    if amountOfListItems <= 11:
        # find what is longer, the longest list item or the title, and use that as the base width for our crop calculation
        longest = longest_list_item if longest_list_item > titleWidth else titleWidth
        # set width here within if statement as width will be accurate for use in watermark print either way (if more or less than 11)
        width = longest + xTitlePos + 40
        # left pos of crop, top pos of crop, width of final img, height of final img
        img = img.crop((0, 0, width , height))
    


    # ---- watermark text & icon img ----

    # setup base object
    imgDraw = ImageDraw.Draw(img)

    # configure the title text and location
    fontWatermark = ImageFont.truetype("Righteous-Regular.ttf", size=18)
    #watermark = "St.Atomic"
    watermark = "80HD"
    watermarkWidth, watermarkHeight = imgDraw.textsize(watermark, font=fontWatermark)
    xwaterText = (width - watermarkWidth) - 10
    ywaterText = (height - watermarkHeight) - 15  

    # draw the title
    #imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 0)) fb8500
    imgDraw.text((xwaterText, ywaterText), watermark, font=fontWatermark, fill=(255,87,51))

    # save the result
    img.save(imgpath)

    #load icon img (svg not supported btw)
    brainwaterimg = Image.open("imgs/icons/mental-health.png") # mental-health lightbulb artificial-intelligence
    # resize it to the same size as the height (its a square) 
    brainwaterimg = brainwaterimg.resize((int(watermarkHeight*2.5), int(watermarkHeight*2.5)))
    # convert to rgba for masking (so it is transparent where there is no fill)
    brainwaterimg = brainwaterimg.convert("RGBA")
    # paste on top of current img (everything we have so far) with color, co-ordinates, then the img mask 
    # - the mask is just itself with its full colour (i assume as like a jpg, then masks out the rest)
    img.paste(brainwaterimg, ((xwaterText - (watermarkHeight*2) - 12), ywaterText-12), brainwaterimg) 
    # save the result
    img.save(imgpath)



    # update the file name and save the result
    imgpath = imgpath.lower().replace(" ","_")
    img.save(imgpath)

    # return the path to the created image
    return(imgpath)





if __name__ == "__main__":
    #draw_task_snapshot_test_af("ceefar")
    #draw_base_rectangle_text_img()
    #draw_improved_rectangle_text_img()
    #draw_dynamic_task_subtask_snapshot("ceefar", ["The First Child Shizzle", "Im The Second In Dis Biatch", "The Third Mofo", "A Fourth You Say!?", "Number 5 Wudup?"] , "Im The Bestest Task")
    draw_dynamic_shopping_list("shoptest", ["item1","item2","item3","item4","item5","item6","im a really long list item","item8","item9","item10","im a kinda long list item","item12","im a little teapot","short and stout","here is my handle","here is my spout"], "Long Shopping List")
    draw_dynamic_shopping_list("shoptest1col", ["item1","item2","item3","item4","item5","item6","im a really really really really really long list item","item8","item9","item10","im a kinda long list item"], "Short  Shopping List")
    draw_dynamic_shopping_list("shoptest2col", ["item1","item2","item3","item4","item5","item6","im a really really really really really long list item","item8","item9","item10","im a kinda long list item","im a little teapot","short and stout","here is my handle","here is my spout","when you tip me over","thats not very cash money of you"], "Budget Shopping List")
