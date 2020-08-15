import discord
from discord.ext import commands
import sqlite3
from coffeehouse.lydia import LydiaAI
import time

class Lydia(commands.Cog):

    def __init__(self,client):
        self.lydia = LydiaAI("69e6f26aba27d05e14c6a48e38008bc0794e24c1d25591db00575e9ce93c577ca934724981a540c319c7da3209ca4c0f910098c14ad6b5e27902c346c9f5cf7f")
        self.client = client
        self.conn = sqlite3.connect('./lydia_sessions.sqlite3')
        self.cur = self.conn.cursor()

    @commands.command(aliases=["lydia"])
    async def ai(self, ctx, *, quest):
        self.cur.execute(f'SELECT * FROM sessions WHERE user_id="{ctx.author.id}"')
        query = self.cur.fetchone()

        if query == None:
            session = self.lydia.create_session()
            self.cur.execute(f"INSERT INTO sessions VALUES ('{ctx.author.id}','{session.id}','{session.expires}')")
            self.conn.commit()

            await ctx.send(session.think_thought(quest))
        else:
            #give it a 50 second margin to avoid possible errors
            if query[2]-50 < int(time.time()):
                self.cur.execute(f'DELETE FROM sessions WHERE session_id = "{query[1]}"')
                session = self.lydia.create_session()
                self.cur.execute(f"INSERT INTO sessions VALUES ('{ctx.author.id}','{session.id}','{session.expires}')")
                self.conn.commit()


                reply = session.think_thought(quest)
                await ctx.send(reply)
                #or alternatively
                #await ctx.send(session.think_thought(quest))
            else:
                reply = self.lydia.think_thought(query[1], quest)
                await ctx.send(reply)
                #or alternatively
                #await ctx.send(session.think_thought(quest))

        #remember to comment this out if you use the alternatives above
        print(f"[<]{ctx.message.author}: {quest}\n[>]{reply}")


def setup(client):
    client.add_cog(Lydia(client))
