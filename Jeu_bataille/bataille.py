import discord
from discord.ext import commands
from time import sleep
from PIL import Image
import randomaaa

from Carte import *

intents = discord.Intents.default()
intents.members = True
intents.guilds=True

bot = commands.AutoShardedBot(command_prefix=["carte.","-"], intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print('[BOT] Connecté !')
    print("\t ",bot.user.name)
    print("\t ",bot.user.id)
    await bot.change_presence(activity=discord.Game(name=f"-bataille"))


def affiche(liste):
    for i in liste:
        print(i.nom,i.couleur)

def pasting(c1,c2,b=None):
    if b:
        img=Image.open("fond-bataille.png")
    else:
        img=Image.open("fond.png")
    img2 = Image.open(f"./cartes/{c1}.png") 
    img.paste(img2, (0, 0))
    img3 = Image.open(f"./cartes/{c2}.png") 
    img.paste(img3, (264, 0))
    img.save("jeu.png")

async def cas_bataille(ctx,liste,p1,p2,ps1,ps2):
    await ctx.send("BATAILLE !")
    if len(p1)==0:
        return ([],p2)
    elif len(p2)==0:
        return (p1,[])
    c1,c2=p1.pop(0),p2.pop(0)
    liste.append(c1)
    liste.append(c2)
    ca=f"{c1.nom}-{c1.couleur}"
    cb=f"{c2.nom}-{c2.couleur}"
    pasting(ca,cb,True)
    with open("jeu.png", "rb") as fh:
        f = discord.File(fh, filename="jeu.png")
    await ctx.send(file=f)
    #await ctx.send(f"Seconde carte de {ps1} : {c1.nom} de {c1.couleur}\nSeconde carte de {ps2}  : {c2.nom} de {c2.couleur}")
    if c1.valeur>c2.valeur:
        msg=await ctx.send(f"{ps1} remporte cette manche !")
        p1.extend(liste)
        return p1,p2,msg
    elif c2.valeur>c1.valeur:
        msg=await ctx.send(f"{ps2} remporte cette manche !")
        p2.extend(liste)
        return p1,p2,msg
    else:
        if len(p1)>0 and len(p2)>0:
            return await cas_bataille(ctx,liste,p1,p2)
        elif len(p1)==0:
            return ([],p2)
        else:
            return (p1,[])


def react_check(reaction, user, id_joueur2, ctx):
    if (reaction.emoji=="➡️" and not(user.bot) and (user.id==id_joueur2 or user.id==ctx.author.id)):
        return True
    return False



@bot.command()
async def bataille(ctx,skin="default"):
    pseudo1=ctx.author.name
    await ctx.send("La partie va commencer !\nVeuillez mentionner le joueur qui s'oppose à vous.")
    try:
        msg = await bot.wait_for("message", timeout=30)
    except:
        await ctx.send("Partie annulée !")
        return
    sleep(0.5)
    id_joueur2=int(msg.content[2:-1])
    user=bot.get_user(id_joueur2)
    pseudo2=user.name
    await ctx.send(f"{user.mention}, Que la bataille commence !")
    sleep(0.5)
    paquet1,paquet2=melange(paquet())
    await ctx.send(f"{ctx.author.mention}, Vous disposez du paquet Numéro 1\n{user.mention}, Vous disposez du paquet Numéro 2")
    sleep(0.5)
    while len(paquet1)!=0 and len(paquet2)!=0:
        c1=paquet1.pop(0)
        c2=paquet2.pop(0)
        ca=f"{c1.nom}-{c1.couleur}"
        cb=f"{c2.nom}-{c2.couleur}"
        pasting(ca,cb)
        with open("jeu.png", "rb") as fh:
            f = discord.File(fh, filename="jeu.png")
        await ctx.send(file=f)
        #await ctx.send(f"Carte de {pseudo1} : {c1.nom} de {c1.couleur}\nCarte de {pseudo2} : {c2.nom} de {c2.couleur}")
        sleep(0.5)
        if c1.valeur>c2.valeur:
            msg=await ctx.send(f"{pseudo1} remporte cette manche !")
            paquet1.append(c1)
            paquet1.append(c2)
        elif c2.valeur>c1.valeur:
            msg=await ctx.send(f"{pseudo2} remporte cette manche !")
            paquet2.append(c2)
            paquet2.append(c1)
        else:
            liste=[c1,c2]
            paquet1,paquet2,msg= await cas_bataille(ctx,liste,paquet1,paquet2,pseudo1, pseudo2)
        await msg.add_reaction("➡️")
        reaction, user = await bot.wait_for('reaction_add')
        while not react_check(reaction, user, id_joueur2, ctx):
            reaction, user = await bot.wait_for('reaction_add')

    if len(paquet1)==0:
        await ctx.send(f"{user.mention}, TU AS GAGNÉ LA PARTIE !")
    elif len(paquet2)==0:
        await ctx.send(f"{ctx.author.mention}, TU AS GAGNÉ LA PARTIE !")
 

            


#TOKEN
with open("token.txt", "r") as tk:
    token=tk.read()
bot.run(token, bot=True, reconnect=True)