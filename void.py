#OTkwODY5ODM4ODQ1MDY3Mjg0.GeMGYO.iNXSfdQyIkNOYKBPl_sh2vVSZXQKB940gKE-wc
from multiprocessing import context
from turtle import position
import discord
from discord.ext import commands
import random
import httpx
import sys
import os
import json
import datetime
import aiohttp
import asyncio
os.system("pip3 install jishaku")
import jishaku
os.system("pip3 install googletrans==3.1.0a0")
from googletrans import Translator
os.system("pip3 install discord.py[voice]")

def cls():
    os.system("clear")

token = "OTkwODY5ODM4ODQ1MDY3Mjg0.GeMGYO.iNXSfdQyIkNOYKBPl_sh2vVSZXQKB940gKE-wc"
prefix = ".", ""
fansrole = 997165469855399997
vannotifchnnl = "997165667914633286"
guild = "Storm"
failemo = "<a:void_bot_failed:997853182183080067>"
guildid = 962851677118038087
vanitycode = "stormop"
owner = 962141696055988244
owner2 = 841240166659653632
owner3 = 743767021681901648
tick = "<a:void_bot_success:997853448823390271>"
vcname = "discord.gg/stormop"
team = "</3"
vanity = "/darkclan"
console = "void-console"
power = 998089354553593906
roleidtogive = 997165469855399997
p4pmode = False
annc = 997165610406514760
npr = "no prefix"
void = "Xany#5677"
voidid = 962141696055988244
intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix=prefix,case_insensitive=False,strip_after_prefix=True,intents=intents)
client.remove_command('help')
client.load_extension('jishaku')

print("Starting..")

@client.command(aliases=["h"])
async def help(ctx):
    bra = ctx.message.author
    breh = bra.avatar_url
    void = discord.Embed(title="Storm", description=f"**Help**\nMy prefix for this server is `{prefix}`\n\n<a:voidblack:997820209928876032> Enabled Features\n<a:Kamui:970455256511172638> 24/7\n<:rix_rich:998139731508473997> Vanity notifier\n<:SAD_booster1:983679863523266560> Boost Greet\n\n**Commands**\n>`jsk,official,help,ar,rr,status,nuke,unbanall,snipe,kick,ban,shiftroles,roleall,unlock,lock,avatar,purge,info,ss,membercount,nick,auditlog,joinvc,settings,esay,say,ping,hide,slowmode,unhide,translate,timer`\n\n**Language:** Python | **Creator:** - Xany#5677\n[Support Server](https://discord.gg/stormop)")
    void.set_thumbnail(url=breh)
    void.set_footer(text=f"{vanitycode} | Developer: Void", icon_url=breh)
    await ctx.reply(embed=void)

@client.event
async def on_ready():
    vcname = discord.utils.get(client.get_all_channels(), name="discord.gg/stormop")
    print("Void Online | Xany\n" * 5)
    os.system("clear")
    print(f"--- Connected ---\nGuild: {guild}\nDeveloper: Xany\nVanitycode: {vanitycode}\nP4P mode: {p4pmode}\n-----------------")
    await client.change_presence(activity=discord.Streaming(name="Ur Mom", url="https://www.twitch.tv/void"))
    print("\nStatus Activated")
    print(f"\nJoined {vcname}\n\nStorm")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return None
    else:
        k = discord.Embed(description=error)
        await ctx.send(embed=k, mention_author=True)

@client.command()
async def servericon(ctx):
    url = ctx.guild.icon_url
    name = ctx.guild.name
    leogay = ctx.author
    breh = ctx.message.author
    radhe = breh.avatar_url
    idk = discord.Embed(title=name,description=f"[GIF DOWNLOAD]({url})")
    idk.set_image(url=url)
    idk.set_footer(text=f"requested by {leogay.name}#{leogay.discriminator}", icon_url=radhe)
    await ctx.reply(embed=idk, mention_author=False)

@client.command(aliases=["ar"])
@commands.has_permissions(administrator=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if role.name == "₍⑅ᐢ..ᐢ₎ ・trainees・・꒱꒱":
        return None
    else:
        await member.add_roles(role)
        await ctx.reply(f"Added {role} to {member.mention}")

@client.command(aliases=["av"])
async def avatar(ctx, user:discord.Member=None):
    if not user:
        user = ctx.author
        av = user.avatar_url
        void = discord.Embed(description="Avatar of {}".format(user.mention))
        void.set_image(url=av)
        await ctx.reply(embed=void, mention_author=False)

@client.command(aliases=["rr"])
@commands.has_permissions(administrator=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if role.name == "₍⑅ᐢ..ᐢ₎ ・trainees・・꒱꒱":
        return None
    else:
        await member.remove_roles(role)
        await ctx.reply(f"Removed {role} from {member.mention}")

@client.command()
@commands.has_permissions(manage_roles=True)
async def official(member):
    ofr = 997794531602878516
    await member.add_roles(ofr)

@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user : discord.Member, *, reason="No reason provided"):
    await user.ban(reason=reason)
    ban = discord.Embed(title=f"Banned {user.name}", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await ctx.message.delete()
    await ctx.channel.send(embed=ban)
    await user.send(embed=ban)

@client.command(pass_context=True)
async def nick(ctx, user: discord.Member = None, *, nick: str = None):
    idk = ctx.guild.get_role("998089354553593906")
    m = ctx.message.author
    if m.guild_permissions.administrator or idk in m.roles:
        if not user:
            await ctx.reply(f"Missing Arguments\n\n>.nick <user> <nickname>")
        elif not nick:
            await ctx("Missing arguments\n\n> .nick <user> <nickname>")
        else:
            try:
                await user.edit(nick=nick)
                void = discord.Embed(description="Changed {}'s nickname to {}".format(user, nick))
                await ctx.reply(embed=void)
            except Exception as e:
                await ctx.reply("An unknow error occured **|** {}".format(e))

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
    await user.kick(reason=reason)
    kick = discord.Embed(title=f"Kicked {user.name}", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await ctx.message.delete()
    await ctx.channel.send(embed=kick)
    await user.send(embed=kick)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messges = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply('Channel locked :lock:')

    @lock.error
    async def lock_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.reply(f"{error}")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel=None):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messges = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.reply('Channel unlocked :unlock:')

    @unlock.error
    async def unlock_error(ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.reply(f"{error}")

@client.command(aliases=["mc"])
async def membercount(ctx):
    leogay = ctx.guild.member_count
    timestamp = datetime.datetime.utcnow()
    author = ctx.message.author
    carhigh = author.avatar_url
    idk = discord.Embed(title="Members", description=f"Member Count: {leogay}")
    idk.set_footer(text=f"Void :P | {vanitycode}", icon_url=carhigh)
    await ctx.reply(embed=idk, mention_author=False)

@client.command(aliases=["set"])
@commands.has_permissions(administrator=True)
async def settings(ctx):
    ok = ctx.message.author
    lmak = ok.avatar_url
    lel = discord.Embed(title="Settings", description=f"Void\n\n Server Name: {guild}\nVanity Code: {vanitycode}\nTag: {vanity}\nTeam Role: {team}\nP4P Mode: {p4pmode}\nNo Prefix Role: {npr}\nOwner ID: {void}\nVc to Join: {vcname}\n\n Some of the variables are not shown. Ask Owner: {void}")
    lel.set_footer(text="Storm | Settings", icon_url=lmak)
    await ctx.reply(embed=lel, mention_author=False)

@client.event
async def on_member_join(member: discord.Member):
    guild = member.guild
    chat = guild.get_channel(997763041217216542)
    await chat.send(f"**{member.mention}, Welcome to /stormop<a:X6_PinkButterfly:972369169985208340>**")

@client.command()
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    await ctx.channel.set_permissions(ctx.guild.defalt_role, view_channel=False)
    await ctx.send(f'{tick} **|** This channel is now hidden')

@client.command()
async def say(ctx, *, msg=None):
    if ctx.author.id == 962141696055988244:
        await ctx.message.delete()
        await ctx.send(msg)
    else:
        return None

@client.command(aliases=["cooldown", "setdelay"])
@commands.has_permissions(manage_channels=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.reply(f"Set channel delay to {seconds} seconds.")

@client.command()
@commands.has_permissions(manage_channels=True)
async def unhide(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
    await ctx.send(f'{tick} **|** This channel is now unhidden')

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content
    await asyncio.sleep(60)
    del snipe_message_author[message.channel.id]
    del snipe_message_content[message.channel.id]

@client.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        em = discord.Embed(title="Sniped Message")
        em.add_field(name="**__Content__**", value=snipe_message_content[channel.id])
        em.set_footer(text=f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.reply(embed=em, mention_author=False)
    except KeyError:
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")

@client.command(aliases=["ts"])
async def translate(ctx, lang, *, thing):
    translator = Translator()
    translation = translator.translate(thing, dest=lang)
    await ctx.reply(translation.text)

    @translate.error
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter required Args. \n\n> translate <language> <text>")

@client.command()
@commands.cooldown(1, 25, commands.BucketType.user)
async def timer(ctx, want:int):
    ok = ctx.message.author
    okk = ok.avatar_url
    em = discord.Embed(description=f"Timer started for {want} seconds")
    em.set_thumbnail(url=okk)
    await ctx.reply(embed=em, mention_author=False)
    await asyncio.sleep(want)
    await ctx.reply(f"Your timer for {want}s has been ended")

@client.command(pass_context=True)
async def status(ctx, member: discord.Member=None):
    kk = ctx.message.author
    ok = kk.avatar_url
    guild = ctx.author.guild
    if member is None:
        member = ctx.message.author
        if member.status == discord.Status.online:
            idk = discord.Embed(title=f"{vanitycode}", description=f"[>] Status - Online")
            idk.set_footer(text=member, icon_url=ok)
            await ctx.send(embed=idk)
        elif member.status == discord.Status.offline:
            naukrani = discord.Embed(title=f"{vanitycode}", description=f"[>] Status - Offline")
            naukrani.set_footer(text=member, icon_url=ok)
            await ctx.send(embed=naukrani)
        elif member.status == discord.Status.idle:
            lmak = discord.Embed(title=f"{vanitycode}", description=f"[>] Staus - Idle")
            lmak.set_footer(text=member, icon_url=ok)
            await ctx.send(embed=lmak)
        elif member.status == discord.Status.dnd:
            lmok = discord.Embed(title=f"{vanitycode}", description=f"[>] Status - Do Not Disturb")
            lmok.set_footer(text=member, icon_url=ok)
            await ctx.send(embed=lmok)
        else:
            err = discord.Embed(title=f"{vanitycode}", description=f"I was unable to detect user status")
            err.set_footer(text=member, icon_url=ok)
            await ctx.send(embed=err)

@client.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    saved = [ctx.channel.category, ctx.channel.position]
    await ctx.channel.clone()
    await ctx.channel.delete()
    nuked = saved[0].text_channels[-1]
    await nuked.edit(position=saved[-1])
    await nuked.send(f"`This channel was nuked by {ctx.author.name}#{ctx.author.discriminator}`")

@client.command()
async def sup(ctx):
    role = client.guilds[0].get_role("997794531602878516")
    file = open('role_members.txt', 'r')
    member_list = [str(member.id) for member in client.get_all_channels()
    if not str(member.status) == "offline" and f'/{vanitycode}' in member.activity]
    for line in file.readlines():
        if line[:-1] not in member_list:
            member = await client.guilds[0].get_member(int(line))
            await member.remove_roles(role)
            a_file = open('role_member.txt', 'a')
            for member_id in member_list:
                await client.guilds[0].get_member(int(member_id)).add_roles(role)
                file.write(member_id + '\n')
                sup.start()

@client.event
async def on_message(message):
    await client.process_commands(message)
    member = message.author
    if "MessageType.premium_guild" in str(message.type):
        await message.channel.send(f"Thanks for boosting us {member.mention} <3")

@client.command()
async def info(ctx):
    void=discord.Embed(title="Information about {}".format(client.user), description="This Bot is a Private Bot\nLanguage: Python<:void_python:999732162406404096>\nVersion: 2.7.16\nDeveloper: Xany#5677")
    void.set_thumbnail(url=ctx.author.avatar_url)
    void.set_footer(text=f"Void :P | {vanity}")
    await ctx.reply(embed=void, mention_author=False)

@client.command(aliases=["esay"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 6, commands.BucketType.user)
async def embedsay(ctx, channel, *, msg):
    guild = ctx.author.guild
    if channel is None:
        channel = ctx.channel
    else:
        esay = discord.Embed(title=guild.name, description=msg)
        esay.set_thumbnail(url=ctx.guild.icon_url)
        await channel.send(embed=esay)

@client.event
async def on_invite_update(invite):
    guild = invite.guild
    logs = await guild.audit_logs(limit=1,after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.invite_update).flatten()
    logs = logs[0]
    if logs.user.id == owner or owner2 or owner3:
        pass
    else:
        await logs.user.ban(reason="Changing vanity | Void Anti-Vanity Stealer")

@client.command(aliases=["screenshot"])
@commands.guild_only()
@commands.cooldown(1,8,commands.BucketType.user)
async def ss(ctx, *, ssig):
    idk = ctx.message.content.lower()
    if "porn" in idk or "sex" in idk or "xx" in idk or "xham" in idk or "hellmom" in idk or "xvid" in idk or "miakhal" in idk or "cum" in idk or "orgasm" in idk or "slut" in idk or "naked" in idk or "brazzers" in idk or "nig" in idk or "fuck" in idk or "horny" in idk:
        await ctx.reply("18+ websites aren't allowed", mention_author=False)
    elif "jerk" in idk or "redgif" in idk or "hentai" in idk:
        await ctx.reply("18+ websites aren't allowed", mention_author=False)
    elif "bit.ly" in idk or "shorturl" in idk or "cutt.ly" in idk:
        await ctx.reply("url shorterners aren't allowed.", mention_author=False)
    elif "https" in idk or "http" in idk:
        void = discord.Embed(title=f"{guild}")
        void.set_footer(text="Screenshot")
        void.set_image(url=f"https://image.thum.io/get/{ssig}")
        await ctx.reply(embed=void, mention_author=False)
    else:
        void2 = discord.Embed(title=f"{guild}")
        void2.set_footer(text="Screenshot")
        void2.set_image(url=f"https://image.thum.io/get/{ssig}")
        await ctx.reply(embed=void2, mention_author=False)

@client.command(aliases=["vc"])
@commands.cooldown(1,30,commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
@commands.guild_only()
async def joinvc(ctx):
    channel = discord.utils.get(client.get_all_channels(), name="discord.gg/stormop")
    await channel.connect()
    await ctx.reply(f"{tick} | Successfully connected to <#{channel.id}>")

@client.command()
async def ping(ctx):
    void = discord.Embed(description="My Ping is: {}".format(round(client.latency * 1000)))
    void.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.reply(embed=void, mention_author=False)

def restart_bot():
    os.execv(sys.executable,['python'] + sys.argv)

@client.command()
@commands.has_permissions(administrator=True)
async def restart(ctx):
    await ctx.reply("Restarting......")
    restart_bot()

@client.command()
@commands.has_permissions(view_audit_log=True)
@commands.cooldown(1,12,commands.BucketType.user)
@commands.guild_only()
async def auditlog(ctx, lmt:int):
    if lmt >= 31:
        await ctx.reply("Action rejected, you aren't allowed to fetch more than `30` entries", mention_author=False)
        return
    idk = []
    str = ""
    async for entry in ctx.guild.audit_logs(limit=lmt):
        idk.append(f'''User: `{entry.user}`
        Action: `{entry.action}`
        Target: `{entry.target}`
        Reason: `{entry.reason}`\n\n''')
        for n in idk:
            str += n
            str=str.replace("AuditLogAction", "")
            void=discord.Embed(title=f"{guild}", description=f">>> {str}")
            void.set_footer(text=f"{vanity} | Audit Log Actions", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=void, mention_author=False)

@client.command()
async def logout(ctx):
    await ctx.reply("Logging out...")
    await client.logout()

@client.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    vc = guild.get_role(997854163314671687)
    if not before.channel and after.channel:
        await member.add_roles(vc, reason="Joined VC")
    elif before.channel and not after.channel:
        await member.remove_roles(vc, reason="Left VC")

@client.command(pass_context=True, aliases=["clear"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send('{} | Successfully cleared/purged {} messages.'.format(tick,limit))
    await ctx.message.delete()

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"{failemo} | Uses ~ `{prefix}purge <number of messages>`", mention_author=False)
        if isinstance(error, commands.MissingPermissions):
            await ctx.reply(f"{failemo} | You are missing Manage Messages permission(s) to run this command.", mention_author=False)


@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
@commands.cooldown(1,5,commands.BucketType.user)
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.reply('**Unbanning {} members**'.format(len(banlist)))
    for users in banlist:
        await ctx.guild.unban(user=users.user, reason=f"By {ctx.author}")

@client.event
async def on_member_update(before,after):
    if str(before.raw_status) == "offline":
        return
    else:
        try:
            bst = after.activities[0].name
            ast = before.activities[0].name
            if vanity in bst:
                if not vanity in ast:
                    channel = client.get_channel(997763041217216542)
                    role = after.guild.get_role(997794531602878516)
                    await after.add_roles(role, reason="Added Vanity In Status")
                    await channel.send(f"Thanks for adding our vanity in ur status<a:Mega_void_flush:999376310507933797><33")
                elif vanity in ast:
                    if not vanity in bst:
                        channel = client.get_channel(997763041217216542)
                        role = after.guild.get_role(997794531602878516)
                        if role in after.roles:
                            await after.remove_roles(role, reason="Removed Vanity from status")
                            await channel.send(f"Removed our vanity from status gay.")
        except:
            pass

@client.command()
async def shiftroles(ctx, leogay:discord.Member, lmak:discord.Member):
    role = ctx.guild.get_role(998089354553593906)
    if leogay.id == lmak.id:
        await ctx.reply("Action rejected cant shift roles to the same user.", mention_author=False, delete_after=2)
        return
    elif leogay.id == ctx.message.author.id or lmak.id == ctx.message.author.id:
        await ctx.reply("Action rejected, cant execute on yourself.", mention_author=False, delete_after=3)
        return
    elif leogay.id == voidid or lmak.id == voidid:
        await ctx.reply("unauthorized", mention_author=False, delete_after=3)
        return
    elif role in ctx.message.author.roles:
        xd = await ctx.reply("shifting roles...", mention_author=False)
        for rol in leogay.roles:
            if role.id == 998089354553593906:
                continue
            try:
                await lmak.add_roles(rol, reason=f"Action issued by {ctx.message.author} After user [ roles shift ]")
            except:
                continue
            for rol in leogay.roles:
                if role.id == 997794531602878516:
                    continue
                await xd.edit(f"{tick} | Successfully shifted roles from {leogay.mention} to {lmak.mention}", mention_author=False, delete_after=3)


@client.command(aliases=["roleeveryone"])
@commands.cooldown(1, 120, commands.BucketType.user)
@commands.guild_only()
async def roleall(ctx,*,reason):
    if reason == " ":
        reason = None
    else:
        reason = " ".join(reason)
        void = discord.Embed(description=f"Adding <@{fansrole}> to Everyone in the server, Reason: `{reason}`")
        responsible = f"Role all | Action done by {ctx.message.author.name}#{ctx.author.discriminator}"
        role = discord.utils.get(ctx.guild.roles, id=fansrole)
        mem = await ctx.guild.chunk()
        membercount = 0
        pr = ctx.guild.get_role(998089354553593906)
        if pr in ctx.message.roles:
            await ctx.reply(f"Assigning <@{fansrole}> to everyone in the server....", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,replied_user=False))
            for user in mem:
                if role in user.roles:
                    continue
                else:
                    membercount += 1
                    try:
                        await user.add_roles(role, reason=responsible)
                    except:
                        pass
            if membercount == 0:
                return await ctx.reply(f"Everyone alr has <@{fansrole}> role", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,replied_user=False))
            await ctx.reply(f"{tick} | Successfully added <@{fansrole}> to {membercount} members", allowed_mentions=discord.AllowedMentions(everyone=False,roles=False,replied_user=False))
            return
        else:
            await ctx.reply("unauthorized", mention_author=False, delete_after=3)

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
@commands.guild_only()
async def unbnall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    idk = 'Void | Unbanning {} members'.format(len(banlist))
    if ctx.author == guild.owner:
        void=discord.Embed()
        void.set_author(name="Void Security")
        void.set_thumbnail(url="https://cdn.discordapp.com/avatars/969287286388826162/a_d7ab74c2b8f26d77b88ca77da767d15e.gif?size=1024")
        void.set_footer(text="Void | Mass Unban")
        void.add_field(name=f"{tick}SUCCESS", value=f'```{idk}```')
        await ctx.reply(embed=void)
        for users in banlist:
            await ctx.guild.unban(user=users.user,reason="Void Security | Action issued by Server Owner")
    else:
        leogay = discord.Embed()
        leogay.set_author(name="Void Security")
        leogay.set_thumbnail(url="https://cdn.discordapp.com/avatars/969287286388826162/a_d7ab74c2b8f26d77b88ca77da767d15e.gif?size=1024")
        leogay.set_footer(text="This message will be self destructed in a few seconds.")
        leogay.add_field(name=f"{failemo}FAILED", value=f'```"You must be owner to use this command."```')
        await ctx.reply(embed=leogay, delete_after=4)

@client.command()
async def badges(ctx, member: discord.Member=None):
    user = member or ctx.author
    with open("badges.json", "r") as f:
        idk = json.load(f)
    if str(user.id) not in idk:
        await ctx.reply(f"{failemo} | {user} Have no bot badges", mention_author=False)
    elif str(user.id) in idk:
        void = discord.Embed(description="", color=0x2f3136)
        void.set_footer(text=user, icon_url=user.avatar)
        void.set_author(name=f"Badges!", icon_url=client.user.avatar)
        for bd in idk[str(user.id)]:
            void.description += f"{bd}\n"
            await ctx.reply(embed=void, mention_author=False)

@client.command()
@commands.has_permissions(administrator=True)
async def addbadge(ctx, user:discord.Member,*,badge):
    with open("badges.json", "r") as f:
        idk = json.load(f)
    if str(user.id) not in idk:
        idk[str(user.id)] = []
        idk[str(user.id)].append(f"{badge}")
        await ctx.reply(f"{tick} | Added {badge} to {user}.", mention_author=False)
    elif str(user.id) in idk:
        idk[str(user.id)].append(f"{badge}")
        await ctx.reply(f"{tick} | Added {badge} to {user}.", mention_author=False)
        with open("badges.json", "w") as f:
            json.dump(idk, f, indent=4)



client.run(token, reconnect=True)