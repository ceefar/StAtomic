# dc.py imports
from unicodedata import category
import discord
from discord.utils import get
from discord.ext import commands, tasks
# for cycling lists
from itertools import cycle

# add discord token as variable 'dctoken' here
#dctoken = ""

# general vars
playa = cycle(["Your Mother","Your Father"]) 

# setup intents, define command prefix for bot , intents needed for on join/on remove
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", description="The description", intents=intents)

# a temp dict of dicts that will act like the db and ig when implementing can upload to it at intervals/daily
# would mean would need sumnt for, if user not in the temp list (and need their info) then grab it from db
# ig would also be good to pull the most active users locally too every day
# stores dictionaries (i think anyway, is what im planning)
temp_user_dict_for_db = {}


# ---- general noob crap ----

@bot.event
async def  on_ready():
    print("Ready !")
    change_status.start()

@bot.command()
async def ping(ctx):
    await ctx.send('**pong**')

@bot.command()
async def message(ctx, user:discord.Member, *, message=None):
    message="Damn Son"
    await user.send(message=message)


# ---- general testing bot crap ----

@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(playa)))


# ---- general testing commands crap ----

# create channel of your name (test af)
@bot.command()
async def createmychannel(ctx):
    guild = ctx.guild

    mbed = discord.Embed(
    title="Success",
    description = "Your Channel Has Been Created"
    )

    if ctx.author.guild_permissions.manage_channels:
        await guild.create_text_channel(name='{}'.format(ctx.author.name)) #category=972790226504282133 < doesnt work tho btw, probably wrong category tho or id type idk
        await ctx.send(embed=mbed)

# delete channel by id
@bot.command()
async def deletechannel(ctx, channel:discord.TextChannel):
    mbed = discord.Embed(
    title="Success",
    description = "Channel: {} has been deleted".format(channel)
    )
    if ctx.author.guild_permissions.manage_channels:
        await ctx.send(embed=mbed)
        await channel.delete()


# ---- general testing events crap ----

# ---- on member join ----
@bot.event
async def on_member_join(member):
    """ event to run (which will create new channel, do permissions, inform that user via dm and msg their personal channel etc """

    # set guild (server) to that of the current member
    guild = member.guild

    # get general channel id, post arrival message to general channel, and send a basic private message as text
    general_channel = bot.get_channel(972790226504282135)
    await general_channel.send(f"{member} has arrived!")
    await member.send('Some Info Will Be Here - Plus Your Private Channel Link?!') 
    
    # create this user their own text channel of their name with number id, change its colour and grab the id
    users_role = await guild.create_role(name='{}'.format(f"{member}_role"))
    await users_role.edit(color=discord.Color(0xe6bc00))
    await member.add_roles(users_role)
    # create a category for which the channel will be placed in 
    users_category = await guild.create_category(name='{}'.format(f"{member.name[:4]}'s space"))  # if -1 == s/S then no ['s] (lol but its true tho)

    # gives only you the permissions to see your own channel
    # it is made hidden for default roles but viewable for the (new) member being referenced (obvs mods can see it too tho)
    overwrites = {
    guild.default_role: discord.PermissionOverwrite(view_channel=False),
    users_role: discord.PermissionOverwrite(view_channel=True)
    }

    # create their new channel with the new category and role overrides, also grab the id
    users_channel = await guild.create_text_channel(name='{}'.format(member), category=users_category, overwrites=overwrites)
    users_channel_id = users_channel.id

    users_webhook = await users_channel.create_webhook(name="{}hook".format(member)) 

    # create a basic embed message for dm
    private_mbed = discord.Embed(
    title="Welcome",
    description = "Your Channel <#{}> Has Been Created In The Category {} With The Role @{}".format(users_channel_id, users_category.name.title(), users_role)
    )
    # dm the embed to the new user
    await member.send(embed=private_mbed)

    # create embed for their new channel
    channel_mbed = discord.Embed(
    title="Info",
    description = "This is your sef space (aka private channel), noone else can see it (except the mods obvs), and the bot will send your stuff here (using a private webhook), again dw no other users can see this except you so go crazy"
    )
    # send this embed to the users new channel
    await users_channel.send(embed=channel_mbed)

    # test prints for db
    print(f"{member = }")
    print(f"{users_role = }")
    print(f"{users_category = }")
    print(f"{users_channel = }")
    print(f"{users_channel_id = }")
    print(f"{users_webhook = }")
    print(f"{users_webhook.url = }")
    print(f"{users_webhook.token = }")
    print(f"{member.roles = }")

    # THIS IS DUMB, JUST USE LOCAL DB FOR NOW (dumb because when app closes dicts go)
    # upload to the local "db"
    # the global data type is a list, within this list we're storing a dictionary for each user
    # that dictionary itself is a value pair with the key being the users name
    # other stuff to include like last message (as a tracker of activity) but not doing rn
    temp_user_dict_for_db[member.name] = {"user_name":member.name, "user_id":member.id, "user_category_id":users_category.id,
                                "user_category_name":users_category.name, "user_role_name":users_role.name, "user_role_id":users_role.id,
                                "user_channel_name":users_channel.name, "user_channel_id":users_channel_id, "user_webhook_id":users_webhook.id,
                                "user_webhook_url":users_webhook.url, "user_webhook_token":users_webhook.token,
                                "users_role_object":users_role, "users_channel_object":users_channel}


# ---- on member leaving ----
@bot.event
async def on_member_remove(member):
    """ basically undoes everything created when a member joins, note should also implement on_raw_member_remove if this doesn't complete """

    # need to remove role, category, channel, webhook (hook might go with the channel tbf but should remove it anyway to be sure)
    # so ig im thinking to use the database but this must be easy enough without doing that
    # ig just use like a global list for now, could always implement that too and say have it upload that stuff every few hours to a db?! (sim idea anyway)

    # role/s
    to_remove_role = temp_user_dict_for_db[member.name]["users_role_object"]
    print(f"{to_remove_role = }")
    await to_remove_role.delete()

    # channel
    to_remove_channel = temp_user_dict_for_db[member.name]["users_channel_object"]
    print(f"{to_remove_channel = }")
    await to_remove_channel.delete()

    # category

    # webhook - do before channel

    # then do to actual db instead



# ---- run the bot ----

bot.run(dctoken)




# FAAAAAAAAAM
# aite first real quick on leave undo all of the shit made and have a mod option to do the same when entering name ig?
# create webhook for the channel
# store the webhook in the database
    # store that webhook in a new table, that links via user id
# grab the webhook before sending stuff to the user omd thats so hard
# gg then its legit done, obvs can and will do more stuff for the bot but at this point...
# move on to new channel idea? (hella simple/brief, more just improvements on mood tracker if anything (sunday start lol))
# then the big refactor!
# - when you do that new project because want new repo without venv as it clogs up the web app way too much






# ---- REFERENCE THINGS ----
"""
# might need for webhooks? idk yet but saving here anyways
# https://discordpy.readthedocs.io/en/latest/api.html?highlight=webhook#discord.Webhook
import aiohttp
from discord import Webhook
async def foo():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('url-here', session=session)
        await webhook.send('Hello World', username='Foo')


# general code
users_channel4 = discord.utils.get(bot.get_all_channels(), guild__name='new.Disaster', name=f"{users_channel}")
users_channel2 = discord.utils.get(member.guild.text_channels, name=f"{users_channel}")
users_channel3 = discord.utils.get(guild.text_channels, name=f"{users_channel}")


# discord py documentation and discord api documentation
https://www.pythondiscord.com/pages/guides/python-guides/discordpy/
https://discordpy.readthedocs.io/en/latest/ext/commands/api.html


# google -> discord.py channel permissions
https://www.codegrepper.com/code-examples/python/channel.permissions+discord.py
https://stackoverflow.com/questions/56300146/change-the-permissions-of-a-discord-text-channel-with-discord-py
https://sysmansquad.com/2021/02/13/create-a-small-discord-py-bot-to-deploy-a-server/


# slash command module
https://pypi.org/project/discord-py-slash-command/
https://discord-interactions.readthedocs.io/en/latest/quickstart.html


# use this for getting their channel name as you can find by name!
# channel = discord.utils.get(member.guild.text_channels, name="welcome")

# sure will use some iteration of this for applying the roles or whatever idk tho maybe dont need roles just straight perms?
# role = get(member.guild.roles, id=role_id)
# await member.add_roles(role)

# also maybe some iteration of this too
# server = ctx.message.server
# perms = discord.Permissions(send_messages=False, read_messages=True)
# await client.create_role(server, name='NoSend', permissions=perms)

"""