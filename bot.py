# from _typeshed import NoneType
# import discord
from discord.ext import commands
from aternosapi import AternosAPI
from os import getcwd
from json import load

with open(getcwd()+"/credentials.json") as creds:
    credentials = load(creds)

with open(getcwd()+"/servers.json") as srvs:
    servers = load(srvs)

bot = commands.Bot(command_prefix='$')

@bot.command(name="list-servers", pass_context=True, help="Lists available servers")
async def list_servers(ctx):
    resp = []
    for i, server in enumerate(list(servers.keys())):
        resp.append(str(i+1)+": "+server)
    await ctx.send("The registered servers are: \n"+"\n".join(resp))

@bot.command(pass_context=True, help="States the current state of the mentioned server")
async def status(ctx, srv_no):
    try:
        srv_name = list(servers.keys())[int(srv_no)-1]
        api = AternosAPI(credentials["common_cookies"], servers[srv_name]["server_cookie"])
        await ctx.send(srv_name+" server is curently "+api.GetStatus())
        api.driver.quit()
    except IndexError:
        await ctx.send("Such a entry do not exist")

@bot.command(pass_context=True, help="Startes the mentioned server")
async def start(ctx, srv_no):
    try:
        srv_name = list(servers.keys())[int(srv_no)-1]
        api = AternosAPI(credentials["common_cookies"], servers[srv_name]["server_cookie"])
        sresp = api.StartServer()
        if sresp != "something went wrong":
            await ctx.send(srv_name+" "+sresp)
        else :
            await ctx.send(sresp)
        api.driver.quit()
    except IndexError:
        await ctx.send("Such a entry do not exist")
    except TypeError:
        await ctx.send("something went wrong")

@bot.command(pass_context=True, help="Stopes the mentioned server REQUIRED ROLE: MCS manager")
@commands.has_role("MCS manager")
async def stop(ctx, srv_no):
    try:
        srv_name = list(servers.keys())[int(srv_no)-1]
        api = AternosAPI(credentials["common_cookies"], servers[srv_name]["server_cookie"])
        sresp = api.StopServer()
        if sresp != "something went wrong":
            await ctx.send(srv_name+" "+sresp)
        else :
            await ctx.send(sresp)
        api.driver.quit()
    except IndexError:
        await ctx.send("Such a entry do not exist")
    except TypeError:
        await ctx.send("something went wrong")

@bot.command(pass_context=True, help="States the information about the mentioned server")
async def getinfo(ctx, srv_no):
    try:
        srv_name = list(servers.keys())[int(srv_no)-1]
        api = AternosAPI(credentials["common_cookies"], servers[srv_name]["server_cookie"])
        sresp = api.GetServerInfo()
        await ctx.send(sresp["ip"].split(".")[0]+"\nIP: "+sresp["ip"]+"\nPort: "+sresp["port"]+"\nSoftware: "+sresp["software"]+"\nVersion: "+sresp["version"]+"\nPlayers: "+sresp["players"]+"\nStatus: "+sresp["status"])
        api.driver.quit()
    except IndexError:
        await ctx.send("Such a entry do not exist")

# @bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send("You are laking proper roles to run this command")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Such a command do not exist")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a server number e.g. 1")

bot.run(credentials["secret_key"])
