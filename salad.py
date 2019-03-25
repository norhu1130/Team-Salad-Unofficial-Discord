# -*- coding: utf-8 -*- 

import asyncio, discord, datetime, re, sys, os, random, requests, json, urllib.request, psutil, ctypes, oauth2, setting
from bs4 import BeautifulSoup as bs4
from unter_translate import *
from naver_api import *
from msg_log import *
from mysql import *
from preta import *

Setting = setting.Settings()
Copyright = Setting.copy
app = discord.Client()
a = 0

async def unknown_error(message, e):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000)) 
    embed = discord.Embed(title="죄송합니다. 원인을 알 수 없는 애러가 발생했습니다.", description="애러가 계속 발생 할 경우, 아래에 있는 오류코드를 가지고 문의 해 주시기 바랍니다.\nOfficial Support Server : https://invite.gg/rutapbot", color=Setting.error_embed_color)
    embed.set_footer(text = randcode)
    await app.send_message(message.channel, embed=embed)
    await app.send_message(app.get_channel(Setting.error_notice_channel), "```Markdown\n# Unknown error\n* Server : %s(%s)\n* Channel : %s(%s)\n* Author : %s(%s)\n* Code : %s\n- errinfo : %s```" % (message.server, message.server.id, message.channel, message.channel.id, message.author, message.author.id, randcode, e))

async def http_error(message, e):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000)) 
    embed = discord.Embed(title="죄송합니다. 예기치 못한 애러가 발생했습니다.", description="봇이 메시지 관련한 충분한 권한을 가지고 있는지 다시 한 번 확인 해 주시기 바랍니다.\nOfficial Support Server : https://invite.gg/rutapbot", color=Setting.error_embed_color)
    embed.set_footer(text = randcode)
    await app.send_message(message.author, embed=embed)
    await app.send_message(app.get_channel(Setting.error_notice_channel), "```Markdown\n# Discord HTTP error\n* Server : %s(%s)\n* Channel : %s(%s)\n* Author : %s(%s)\n* Code : %s\n- errinfo : %s```" % (message.server, message.server.id, message.channel, message.channel.id, message.author, message.author.id, randcode, e))

async def custom_error(message, e, description):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000)) 
    embed = discord.Embed(title="죄송합니다. 원인을 알 수 없는 애러가 발생했습니다.", description="%s\nOfficial Support Server : https://invite.gg/rutapbot" % (description), color=Setting.error_embed_color)
    embed.set_footer(text = randcode)
    await app.send_message(message.channel, embed=embed)
    await app.send_message(app.get_channel(Setting.error_notice_channel), "```Markdown\n# Custom error\n* Server : %s(%s)\n* Channel : %s(%s)\n* Author : %s(%s)\n* Code : %s\n- errinfo : %s```" % (message.server, message.server.id, message.channel, message.channel.id, message.author, message.author.id, randcode, e))

async def music_play(message, app, filename, length):
    try:
        if os.path.isfile("Server_%s/playing.log" % (message.server.id)):
            return None
        else:
            f = open("Server_%s/playing.log" % (message.server.id), 'w')
            f.close()
            voice = app.voice_client_in(message.server)
            player = voice.create_ffmpeg_player("sound/%s" % (filename), use_avconv=False)
            player.start()
            await asyncio.sleep(length)
            try:
                os.remove("Server_%s/playing.log" % (message.server.id))
            except:
                pass
    except:
        return None

@app.event
async def on_ready():
    try:
        rpc = open("rpc.setting", 'r').read()
        await app.change_presence(game=discord.Game(name=rpc, type=0))
        print("rpc.setting 파일을 찾았습니다.\n봇이 \"%s\"을(를) 플레이 하게 됩니다.\n\n==============================\n" % (rpc))
    except Exception as e:
        print("rpc.setting 파일을 발견하지 못하였습니다.\n%s\n\n==============================\n" % (e))

    print("Bot is Ready!\n\n==============================\n\n[봇 정보]\n%s (%s)\n\n==============================\n\n" % (app.user.name, app.user.id))

    mysql_add_table_content("saladstatus", "status", "1")

    while a < 1:
        now = datetime.datetime.now()
        embed=discord.Embed(title="I'm online!", description="%s/%s/%s | %s:%s" % (str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute)), color=Setting.embed_color)
        embed.set_footer(text = "Ver. %s | %s" % (Setting.version, Copyright))
        online_notice = await app.send_message(app.get_channel(Setting.online_notice_channel), embed=embed)
        await asyncio.sleep(300)
        await app.delete_message(online_notice)

@app.event
async def on_member_join(member):
    try:
        msg = open("Server_%s/welcome_msg.setting" % (member.server.id), 'r').read()
        channel = open("Server_%s/welcome_channel.setting" % (member.server.id), 'r').read()
        await app.send_message(app.get_channel(channel), "<@%s>, %s" % (member.id, msg))
    except:
        pass

@app.event
async def on_member_remove(member):
    try:
        msg = open("Server_%s/bye_msg.setting" % (member.server.id), 'r').read()
        channel = open("Server_%s/bye_channel.setting" % (member.server.id), 'r').read()
        await app.send_message(app.get_channel(channel), "`%s%s`, %s" % (member.name, "#"+member.discriminator, msg))
    except:
        pass

@app.event
async def on_message(message):
    now = datetime.datetime.now()

    try:
        log_msg(message.server, message.server.id, message.channel, message.channel.id, message.author.name, "#"+message.author.discriminator, message.author.id, message.content)
    except Exception as e:
        print("msg log error : %s" % (e))

    if message.channel.id == "559188829513449491": # "uptime-checking" Channel
        if message.author.id == "554300338274959360":
            if "I'll check the status of Bot Online." in message.content:
                await app.send_message(message.channel, "Team Salad Online")

    if message.channel.id == "559188543038160906": # "team-salad-yt-notice" Channel
        if message.author.id == "159985870458322944":
            split = message.content.split("|")
            channel_name = str(split[0])
            video_id = str(split[1])

            f = open("yt_notice_channel.setting", 'r')
            lists = f.read()
            f.close()

            lists = lists.split("\n")

            f = open("yt_notice_channel_num.setting", 'r')
            num = f.read()
            f.close()

            count = 0
            result = False

            while not result:
                try:
                    channel_id = str(lists[count])
                    await app.send_message(app.get_channel(channel_id), "방금 `%s` 채널에 영상이 업로드 되었습니다! %s" % (channel_name, video_id))
                except:
                    pass
                if count == int(num) - 1:
                    result = True
                else:
                    count = count + 1

    if message.channel.id == "559188590748368897": # "team-salad-twitch-notice" Channel
        if message.author.id == "159985870458322944":
            split = message.content.split("|")
            channel_name = str(split[0])
            video_id = str(split[1])

            f = open("twitch_notice_channel.setting", 'r')
            lists = f.read()
            f.close()

            lists = lists.split("\n")

            f = open("twitch_notice_channel_num.setting", 'r')
            num = f.read()
            f.close()

            count = 0
            result = False

            while not result:
                try:
                    channel_id = str(lists[count])
                    await app.send_message(app.get_channel(channel_id), "방금 `%s` 트위치 채널에서 방송이 진행중입니다!\n%s" % (channel_name, video_id))
                except:
                    pass
                if count == int(num) - 1:
                    result = True
                else:
                    count = count + 1

    if message.author.bot:
        return None

    if message.channel.is_private:
        await app.send_message(message.channel, "<@%s>, DM에서는 명령어를 사용 할 수 없습니다!" % (message.author.id))
        return None

    try:
        try:
            msgarrived = float(str(time.time())[:-3])
            msgtime = timeform(message.timestamp)
            msgdelay = msgarrived - msgtime - 32400
            ping = int(msgdelay * 1000)

            mysql_add_table_content("saladstatus", "ping", ping)
            mysql_add_table_content("saladstatus", "status", "1")

            if os.path.isfile("Server_%s/maple_ver.setting" % (message.server.id)):
                try:
                    prefix = open("Server_%s/prefix.setting" % (message.server.id), 'r').read()
                except:
                    prefix = Setting.prefix
                    open("Server_%s/prefix.setting" % (message.server.id), 'w').write(prefix)

                if "salad admin notice" in message.content:
                    if message.author.id in Setting.bot_admin:
                        q = message.content
                        check = q.replace("salad admin notice", "")
                        if check == None or check == "" or check == " ":
                            await app.send_message(message.channel, "<@%s>, 공지 항목란이 비어있습니다!" % (message.author.id))
                        else:
                            servers = open("Servers.log", 'r').read()
                            await app.send_message(message.channel, "<@%s>, `%s`개의 서버에 다음과 같은 공지가 보내집니다. `취소` 또는 `수락`을 입력하여 주세요.\n\n```%s```" % (message.author.id, servers, q))
                            new_message = await app.wait_for_message(author=message.author)
                            if new_message.content == "수락":
                                embed=discord.Embed(title="공지 시스템", color=Setting.embed_color)
                                embed.add_field(name="공지 발신 준비중!", value="<@" + message.author.id + ">", inline=False)
                                embed.set_author(name="by 매리(#4633)", icon_url="https://cdn.discordapp.com/avatars/351613953769603073/b4805197b14b4366c3aaebaf79109fa8.webp")
                                embed.set_footer(text="Notice Module by Mary | Ver. %s | %s" % (Setting.version, Copyright))
                                mssg = await app.send_message(message.channel, embed=embed)
                                allowprefix = ["notice", "공지", "알림"]
                                disallowprefix = ["밴", "경고", "제재", "길드", "ban", "worry", "warn", "guild"]
                                nfct = True
                                nfctname = "Team-화공-공지-자동생성됨"
                                a = []
                                b = []
                                e = []
                                ec = {}
                                embed=discord.Embed(title="공지 시스템", color=Setting.embed_color)
                                embed.add_field(name="공지 발신중!", value="<@" + message.author.id + ">", inline=False)
                                embed.set_author(name="by 매리(#4633)", icon_url="https://cdn.discordapp.com/avatars/351613953769603073/b4805197b14b4366c3aaebaf79109fa8.webp")
                                embed.set_footer(text="Notice Module by Mary | Ver. %s | %s" % (Setting.version, Copyright))
                                await app.edit_message(mssg, embed=embed)
                                for server in app.servers:
                                    for channel in server.channels:
                                        for tag in allowprefix:
                                            if tag in channel.name:
                                                dtat = True
                                                for distag in disallowprefix:
                                                    if distag in channel.name:
                                                        dtat = False
                                                if dtat:
                                                    if not server.id in a:
                                                        try:
                                                            await app.send_message(channel, q)
                                                        except discord.HTTPException:
                                                            e.append(str(channel.id))
                                                            ec[channel.id] = "HTTPException"
                                                        except discord.Forbidden:
                                                            e.append(str(channel.id))
                                                            ec[channel.id] = "Forbidden"
                                                        except discord.NotFound:
                                                            e.append(str(channel.id))
                                                            ec[channel.id] = "NotFound"
                                                        except discord.InvalidArgument:
                                                            e.append(str(channel.id))
                                                            ec[channel.id] = "InvalidArgument"
                                                        else:
                                                            a.append(str(server.id))
                                                            b.append(str(channel.id))
                                asdf = "```\n"
                                for server in app.servers:
                                    if not server.id in a:
                                        if nfct:
                                            try:
                                                ch = await app.create_channel(server, nfctname)
                                                await app.send_message(ch, "__**공지채널을 발견하지 못하여 공지채널을 자동으로 생성하였습니다.**__\n자세한 내용은 봇 관리자에게 문의해주세요 : https://invite.gg/rutapbot")
                                                await app.send_message(ch, q)
                                            except:
                                                asdf = asdf + str(server.name) + "[채널 생성 실패]\n"
                                            else:
                                                asdf = asdf + str(server.name) + "[채널 생성 및 재발송 성공]\n"
                                        else:
                                            asdf = asdf + str(server.name) + "\n"
                                asdf = asdf + "```"
                                embed=discord.Embed(title="공지 시스템", color=Setting.embed_color)
                                embed.add_field(name="공지 발신완료!", value="<@" + message.author.id + ">", inline=False)
                                bs = "```\n"
                                es = "```\n"
                                for bf in b:
                                    bn = app.get_channel(bf).name
                                    bs = bs + str(bn) + "\n"
                                for ef in e:
                                    en = app.get_channel(ef).name
                                    es = es + str(app.get_channel(ef).server.name) + "(#" + str(en) + ") : " + ec[ef] + "\n"
                                bs = bs + "```"
                                es = es + "```"
                                if bs == "``````":
                                    bs = "``` ```"
                                if es == "``````":
                                    es = "``` ```"
                                if asdf == "``````":
                                    asdf = "``` ```"
                                sucess = bs
                                missing = es
                                notfound = asdf
                                embed.add_field(name="공지 발신 성공 채널:", value=sucess, inline=False)
                                embed.add_field(name="공지 발신 실패 채널:", value=missing, inline=False)
                                embed.add_field(name="공지 채널 없는 서버:", value=notfound, inline=False)
                                embed.set_author(name="by 매리(#4633)", icon_url="https://cdn.discordapp.com/avatars/351613953769603073/b4805197b14b4366c3aaebaf79109fa8.webp")
                                embed.set_footer(text="Notice Module by Mary | Ver. %s | %s" % (Setting.version, Copyright))
                                await app.edit_message(mssg, embed=embed)
                            else:
                                await app.send_message(message.channel, "<@%s>, 취소되었습니다." % (message.author.id))
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 봇 관리자가 아닙니다!' % (message.author.id))

                if message.content == "salad admin info":
                    if message.author.id in Setting.bot_admin:
                        stat = setting.MEMORYSTATUSEX()
                        ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                        cpu = psutil.cpu_percent()
                        mem = stat.dwMemoryLoad
                        servers = open("servers.rtl", 'r').read()
                        embed = discord.Embed(title="정보", description=None, color=Setting.embed_color)
                        embed.add_field(name="봇 정보", value="`%s`/`%s`개의 서버에서 사용중" % (len(app.servers), servers), inline=False)
                        embed.add_field(name="하드웨어 정보", value="CPU : `%s/100` 사용중\nRAM : `%s/100` 사용중\n\n**보안을 위하여 모델명은 노출하지 않습니다**" % (cpu, mem), inline=False)
                        await app.send_message(message.channel, embed=embed)
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 봇 관리자가 아닙니다!' % (message.author.id))

                if message.content.startswith("salad admin game"):
                    if message.author.id in Setting.bot_admin:
                        q = message.content.replace("salad admin game ", "")
                        f = open("rpc.setting", 'w')
                        old = f.read()
                        f.close()
                        open("rpc.setting", 'w').write(q)
                        await app.change_presence(game=discord.Game(name=q, type=0))
                        await app.send_message(message.channel, '<@%s>, 플레이중인 게임을 `%s`에서 `%s`으로 변경하였습니다!' % (message.author.id, old, q))
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 봇 관리자가 아닙니다!' % (message.author.id))

                if message.content == "salad admin shutdown":
                    if message.author.id in Setting.bot_admin:
                        await app.change_presence(game=discord.Game(name="Offline", type=0))
                        await app.send_message(message.channel, '<@%s>, 5분 이내에 오프라인으로 전환됩니다. (디스코드 API 딜레이)' % (message.author.id))
                        mysql_add_table_content("saladstatus", "status", "0")
                        exit()
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 봇 관리자가 아닙니다!' % (message.author.id))

                if message.content.startswith("salad admin url short"):
                    if message.author.id in Setting.bot_admin:
                        q = message.content.replace("salad admin url short", '')
                        await app.send_message(message.channel, await url_short(message, q))
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 봇 관리자가 아닙니다!' % (message.author.id))

                if message.content == prefix + "도움말":
                    embed = discord.Embed(title="팀 샐러드 봇 도움말", description="`<>` : 필수입력\n`[]` : 선택입력\n`A|B` : A와 B중 택 1", color=Setting.embed_color)
                    embed.add_field(name="카테고리 : `일반`", value="`%s정보` - 봇에 대한 정보를 출력합니다!\n`%s카페 <팬카페공지|방송공지|전체글>` - 해당 게시판의 최근 5개(전체글은 8개)의 글을 불러옵니다!\n`%s카페 대문` - 카페 대문을 보여줍니다!\n`%s번역 <도움말|...> <...>` - `%s번역 도움말`을 확인해주세요." % (prefix, prefix, prefix, prefix, prefix), inline=False)
                    embed.add_field(name="카테고리 : `음성`", value="`%s접속` - 참가해있는 음성 채널에 봇을 초대합니다.\n`%s나가기` - 봇이 음성 채널에서 나갑니다.\n`%s정지` - 음악 정지를 위해 봇이 음성채널에 재입장 합니다." % (prefix, prefix, prefix), inline = False)
                    embed.add_field(name="카테고리 : `재미`", value="`사과야 ~` - 마플 AI를 사용할 수 있습니다. 자세한 내용은 `사과야 도와줘` 참고.\n`운터야 ~` - 운터 AI를 사용 할 수 있습니다. 자세한 내용은 `운터야 도와줘` 참고.\n`%s운세 [도움말]` - 운세를 볼 수 있습니다. 1일 1회로 제한됩니다." % (prefix), inline = False)
                    embed.add_field(name="카테고리 : `설정 (관리자 권한 필요)`", value="`%s음성알림 <켜기|끄기>` - 봇이 음성채널에 접속&퇴장시 `이예에에에에!!!!` 와 `안해`를 외칠지 결정합니다.\n`%s방송알림 <트위치|유튜브|도움말>` - `%s방송알림 도움말`을 참고하여 주세요.\n`%s환영말 <끄기|할말>` - 유저가 서버에 입장하면 환영말을 띄웁니다!\n`%s떠나는말 <끄기|할말>` - 유저가 서버에 퇴장하면 떠나보내는 말을 띄웁니다!\n`%s접두사 <...>` - 접두사가 타 봇과 겹치는 경우, 수정이 가능합니다." % (prefix, prefix, prefix, prefix, prefix, prefix), inline = False)
                    embed.add_field(name="카테고리 : `봇 관리자`", value="`salad admin shutdown` - 봇의 가동을 중지시킵니다.\n`salad admin game <...>` - 봇이 플레이중인 게임을 바꿀 수 있습니다.\n`salad admin notice <...>` - 공지를 보낼 수 있습니다.\n`salad admin url short <...>` - url 단축을 사용할 수 있습니다.\n`salad admin info` - 봇과 관련한 정보를 표시합니다.", inline = False)
                    embed.add_field(name="카테고리 : `팀 샐러드`", value="팀 샐러드 유튜브 : http://me2.do/FwVM95S2\n팀 샐러드 팬카페 : http://me2.do/5vDU2PWk", inline = False)
                    embed.add_field(name="카테고리 : `팀 화공`", value="공식 지원서버 : https://invite.gg/rutapbot\n공식 홈페이지 : https://rutapofficial.xyz", inline = False)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)

                if message.content == prefix + '정보':
                    embed = discord.Embed(title="팀 샐러드 봇 정보", description=None, color=Setting.embed_color)
                    embed.add_field(name="카테고리 : `소개`", value="http://me2.do/FwVM9RwO", inline = False)
                    embed.add_field(name="카테고리 : `개발자`", value="화향, Hyuns Production", inline = False)
                    embed.add_field(name="카테고리 : `저작권`", value="봇 프로필 : `꼬욤`님 ( http://me2.do/5bGmzBfb )\n입장 메시지 GIF : `운터신 숭배자 키리엘`님 ( http://me2.do/GXNexdv6 )\n퇴장 메시지 일러스트 : `하ru`님 ( http://me2.do/FrFrgcVR )\n사운드 소스 : `팀 샐러드` ( http://me2.do/FwVM95S2 )\n카페 대문 일러스트는 원작자가 소유합니다.\n**기타 이곳에 나열되지 않은 작품은 모두 `Team. 화공`에서 저작권을 소유합니다.**", inline = False)
                    embed.add_field(name="카테고리 : `오픈소스 라이선스`", value="https://weart.ist/dpnk (`BSD 3-Clause License`)\nThis bot use Naver API. : http://me2.do/x2ipxUY8\nThis bot use Twitter API. : http://me2.do/5QfjInVH", inline = False)
                    embed.add_field(name="카테고리 : `Github`", value="http://me2.do/5BrFBPWs", inline = False)
                    embed.add_field(name="카테고리 : `팀 샐러드`", value="팀 샐러드 유튜브 : http://me2.do/FwVM95S2\n팀 샐러드 팬카페 : http://me2.do/5vDU2PWk", inline = False)
                    embed.add_field(name="카테고리 : `팀 화공`", value="공식 지원서버 : https://invite.gg/rutapbot\n공식 홈페이지 : https://rutapofficial.xyz", inline = False)
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, embed=embed)

                if message.content.startswith(prefix + '접두사'):
                    if message.author.server_permissions.administrator or message.author.id in Setting.bot_admin:
                        q = message.content.replace(prefix + '접두사', '')
                        q = q.replace('\n', '')
                        q = q.replace('\t', '')
                        q = q.replace(' ', '')
                        q = q[:1]
                        open("Server_%s/prefix.setting" % (message.server.id), 'w').write(q)
                        embed = discord.Embed(title="완료!", description="해당 서버에 대한 접두사가 `%s`에서 `%s`(으)로 변경되었습니다!" % (prefix, q), color=Setting.embed_color)
                        embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                        await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 서버 관리자가 아닙니다!' % (message.author.id))

                if message.content.startswith(prefix + "운세"):
                    q = message.content.replace("운세", "")
                    if "도움말" in q:
                        embed = discord.Embed(title="운세 도움말!", description=None, color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `설명`", value="꾸몽님의 신년운세 영상을 기반으로 제작되었습니다. 1일 1회만 조회가 가능합니다.", inline = False)
                        embed.add_field(name="카테고리 : `운세`", value="`대대길` > `대길` > `중길` > `소길` > `평` > `흉` > `소흉` > `대흉` > `대대흉`", inline = False)
                        embed.add_field(name="카테고리 : `관련영상`", value="신년운세 [Minecraft] : https://youtu.be/aN3AcNFrbTA", inline = False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                    else:
                        if os.path.isfile("fortune/%s_%s_%s_%s_complete.log" % (now.year, now.month, now.day, message.author.id)):
                            await app.send_message(message.channel, '<@%s>, 오늘은 이미 운세를 조회하셨습니다! 내일 다시 와주세요!' % (message.author.id))
                            return None
                        else:
                            result = random.randint(1, 9)
                            if result == 1:
                                result = ":pig: :fireworks: **대대길** :fireworks: :pig:\n`축하합니다 이예에에에에ㅔㅔㅔㅔ!!!`"
                            elif result == 2:
                                result = ":fireworks: :fireworks: **대길** :fireworks: :fireworks:\n`축하합니다!`"
                            elif result == 3:
                                result = ":fireworks: **중길** :fireworks:\n`이정도면 괜찮아요!`"
                            elif result == 4:
                                result = ":fireworks: **소길**\n`아직까진 괜찮아요!`"
                            elif result == 5:
                                result = "**평**\n`무난하네요!`"
                            elif result == 6:
                                result = ":nauseated_face: **흉** :nauseated_face:\n`그리 심각하진 않아요...아직은...`"
                            elif result == 7:
                                result = ":skull: **소흉** :skull:\n`심각하진 않아요...`"
                            elif result == 8:
                                result = ":nauseated_face: :skull: **대흉** :skull: :nauseated_face:\n`.....`"
                            elif result == 9:
                                result = ":skull_crossbones: :boom: **대대흉** :boom: :skull_crossbones:\n`망 했 어 요...`"
                            else:
                                await custom_error(message, "unknown result in fortune :: %s" % (result), "예상치 못한 애러입니다. 저희팀에 문의하여 주세요.")
                                return None

                        embed = discord.Embed(title="오늘의 운세!", description=result, color=Setting.embed_color)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        open("fortune/%s_%s_%s_%s_complete.log" % (now.year, now.month, now.day, message.author.id), 'w').close()

                if message.content.startswith(prefix + '환영말'):
                    if message.author.server_permissions.administrator or message.author.id in Setting.bot_admin:
                        q = message.content.replace(prefix + '환영말', '')
                        if "끄기" in q:
                            try:
                                os.remove("Server_%s/welcome_msg.setting" % (message.server.id))
                                os.remove("Server_%s/welcome_channel.setting" % (message.server.id))
                            except:
                                pass
                            embed = discord.Embed(title="완료!", description="앞으로 유저 입장시, 아무 환영말도 띄우지 않습니다!", color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                        else:
                            f = open("Server_%s/welcome_msg.setting" % (message.server.id), 'w')
                            f.write(q)
                            f.close()
                            f = open("Server_%s/welcome_channel.setting" % (message.server.id), 'w')
                            f.write(message.server.id)
                            f.close()
                            embed = discord.Embed(title="완료!", description="앞으로 유저 입장시, 아래와 같은 환영말이 뜹니다!\n`(유저언급), %s`" % (q), color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 서버 관리자가 아닙니다!' % (message.author.id))

                if message.content.startswith(prefix + '떠나는말'):
                    if message.author.server_permissions.administrator or message.author.id in Setting.bot_admin:
                        q = message.content.replace(prefix + '떠나는말', '')
                        if "끄기" in q:
                            try:
                                os.remove("Server_%s/bye_msg.setting" % (message.server.id))
                                os.remove("Server_%s/bye_channel.setting" % (message.server.id))
                            except:
                                pass
                            embed = discord.Embed(title="완료!", description="앞으로 유저 퇴장시, 아무 환영말도 띄우지 않습니다!", color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                        else:
                            f = open("Server_%s/bye_msg.setting" % (message.server.id), 'w')
                            f.write(q)
                            f.close()
                            f = open("Server_%s/bye_channel.setting" % (message.server.id), 'w')
                            f.write(message.server.id)
                            f.close()
                            embed = discord.Embed(title="완료!", description="앞으로 유저 퇴장시, 아래와 같은 환영말이 뜹니다!\n`(유저 닉네임), %s`" % (q), color=Setting.embed_color)
                            embed.set_footer(text="Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                            await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                    else:
                        await app.send_message(message.channel, '<@%s>, 당신은 서버 관리자가 아닙니다!' % (message.author.id))

                if message.content.startswith(prefix + '번역'):
                    r = message.content.replace(prefix + "번역", "")
                    if "도움말" in r:
                        embed = discord.Embed(title="\"번역\" 도움말", description=None, color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `설명`", value="파파고의 NMT(통계기반 번역시스템)을 이용한 번역을 할 수 있습니다.\n다만, 운터어 번역은 네이버에서 제공하는 기능이 아닌, **저희가 직접 작업한 기능으로, 불안정 할 수 있습니다.**", inline = False)
                        embed.add_field(name="카테고리 : `명령어`", value="`%s번역 <출발언어> <도착언어> <번역하고 싶은 내용>` - 번역을 하실 수 있습니다." % (prefix), inline = False)
                        embed.add_field(name="카테고리 : `[번역] 출발언어`", value="`자동감지`, `한국어`, `일본어`, `영어`, `운터어", inline = False)
                        embed.add_field(name="카테고리 : `[번역] 도착언어`", value="`한국어`, `일본어`, `영어`, `운터어`", inline = False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                    else:
                        split = r.split(" ")

                        start = str(split[1])
                        end = str(split[2])
                        
                        q = r.replace(start, "")
                        q = q.replace(end, "")

                        if "한" in start:
                            start_q = "ko"
                        elif "일" in start:
                            start_q = "jp"
                        elif "영" in start:
                            start_q = "en"
                        elif "운터" in start:
                            start_q = "unter"
                        elif "언어" in start or "자동" in start:
                            result = await papago_detectlangs(message, q)
                            if "ko" in result or "en" in result or "jp" in result:
                                start_q = result
                                if "ko" in result:
                                    start = "한국어 (자동감지됨)"
                                elif "en" in result:
                                    start = "영어 (자동감지됨)"
                                else:
                                    start = "일본어 (자동감지됨)"
                            else:
                                await app.send_message(message.channel, '<@%s>, 올바르지 않은 입력값이 존재합니다!' % (message.author.id))
                        else:
                            await app.send_message(message.channel, '<@%s>, 올바르지 않은 입력값이 존재합니다!' % (message.author.id))
                            return None

                        if "한" in end:
                            end_q = "ko"
                        elif "일" in end:
                            end_q = "jp"
                        elif "영" in end:
                            end_q = "en"
                        elif "운터" in end:
                            if start_q == "ko":
                                end_q = "unter"
                            else:
                                await app.send_message(message.channel, '<@%s>, 운터어의 경우, `한국어 -> 운터어`와 `운터어 -> 한국어`만 지원합니다!' % (message.author.id))
                                return None
                        else:
                            await app.send_message(message.channel, '<@%s>, 올바르지 않은 입력값이 존재합니다!' % (message.author.id))
                            return None

                        if start_q == "unter":
                            if end_q == "ko":
                                pass
                            else:
                                await app.send_message(message.channel, '<@%s>, 운터어의 경우, `한국어 -> 운터어`와 `운터어 -> 한국어`만 지원합니다!' % (message.author.id))
                                return None

                        if str(q.replace("\t", "")) == None:
                            await app.send_message(message.channel, '<@%s>, 올바르지 않은 입력값이 존재합니다!' % (message.author.id))
                            return None

                        if end_q == "unter" or start_q == "unter":
                            if start_q == "unter":
                                result = translate_unter_to_ko(q)
                            elif end_q == "unter":
                                result = translate_ko_to_unter(q)
                            else:
                                await custom_error(message, "unknown result in translate :: %s -> %s (q : %s)" % (start_q, end_q, q), "예상치 못한 애러입니다. 저희팀에 문의하여 주세요.")
                        else:
                            result = await papago_smt(message, q, start_q, end_q)

                        if not result:
                            return None
                        else:
                            embed = discord.Embed(title="번역결과", description=None, color=Setting.embed_color)
                            embed.add_field(name="원문", value=q, inline = False)
                            embed.add_field(name="출발언어", value=start, inline = True)
                            embed.add_field(name="도착언어", value=end, inline = True)
                            embed.add_field(name="결과", value=result, inline = False)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)

                if message.content.startswith(prefix + "방송알림"):
                    r = message.content.replace(prefix + "방송알림", '')
                    if "도움말" in r:
                        embed = discord.Embed(title="\"방송알림\" 도움말", description=None, color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `설명`", value="팀 샐러드 멤버가 방송을 키거나, 유튜브에 영상을 업로드 할 시, 채널에 알림을 발송합니다.", inline = False)
                        embed.add_field(name="카테고리 : `명령어`", value="`%s방송알림 트위치` - 하단에 있는 멤버가 방송을 키면 이 채널에 알림을 보냅니다.\n`%s방송알림 유튜브` - 하단에 있는 멤버가 영상을 올리면 이 채널에 알림을 보냅니다.\n`%s방송알림 끄기` - 해당 채널에 설정된 모든 알림을 해제합니다." % (prefix, prefix, prefix), inline = False)
                        embed.add_field(name="카테고리 : `[알림] 유튜브`", value="TEAM Salad : http://me2.do/FwVM95S2\n꾸몽 : http://me2.do/G35MwHN6\n카운터 : http://me2.do/Gym2oiIz\n마플 마인크래프트 채널 : http://me2.do/5h0PKIpt\n메타 TV : http://me2.do/GMEhypTE", inline = False)
                        embed.add_field(name="카테고리 : `[알림] 트위치`", value="정메타 : http://me2.do/5ZGF9UoZ\nFGcounter : http://me2.do/x5hTZknR\n아이리스 : http://me2.do/F1025Nz5\n마인애플 : http://me2.do/51J4pwMG\nGGUMONG : http://me2.do/GBqUuJQk\n유성짱짱123 : http://me2.do/x2a1NTvf\n파크모 : http://me2.do/F0kLGVKb", inline = False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                    elif "트위치" in r:
                        f = open("twitch_notice_channel_num.setting", 'r')
                        old_num = f.read()
                        f.close()
                        new_num = int(old_num) + 1
                        f = open("twitch_notice_channel_num.setting", 'w')
                        f.write(str(new_num))
                        f.close()

                        f = open("twitch_notice_channel.setting", 'r')
                        old_ch = f.read()
                        f.close()
                        new_ch = "%s\n%s" %  (old_ch, message.channel.id)
                        f = open("twitch_notice_channel.setting", 'w')
                        f.write(new_ch)
                        f.close()

                        embed = discord.Embed(title="완료!", description="앞으로 하단에 있는 스트리머가 방송을 키면 알림을 발송합니다!", color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `[알림] 트위치`", value="정메타 : http://me2.do/5ZGF9UoZ\nFGcounter : http://me2.do/x5hTZknR\n아이리스 : http://me2.do/F1025Nz5\n마인애플 : http://me2.do/51J4pwMG\nGGUMONG : http://me2.do/GBqUuJQk\n유성짱짱123 : http://me2.do/x2a1NTvf\n파크모 : http://me2.do/F0kLGVKb", inline = False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                    elif "유튜브" in r:
                        f = open("yt_notice_channel_num.setting", 'r')
                        old_num = f.read()
                        f.close()
                        new_num = int(old_num) + 1
                        f = open("yt_notice_channel_num.setting", 'w')
                        f.write(str(new_num))
                        f.close()

                        f = open("yt_notice_channel.setting", 'r')
                        old_ch = f.read()
                        f.close()
                        new_ch = "%s\n%s" %  (old_ch, message.channel.id)
                        f = open("yt_notice_channel.setting", 'w')
                        f.write(new_ch)
                        f.close()

                        embed = discord.Embed(title="완료!", description="앞으로 하단에 있는 멤버가 영상을 올리면 알림을 발송합니다!", color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `[알림] 유튜브`", value="TEAM Salad : http://me2.do/FwVM95S2\n꾸몽 : http://me2.do/G35MwHN6\n카운터 : http://me2.do/Gym2oiIz\n마플 마인크래프트 채널 : http://me2.do/5h0PKIpt\n메타 TV : http://me2.do/GMEhypTE", inline = False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                    elif "끄기" in r:
                        f = open("yt_notice_channel.setting", 'r')
                        yt = f.read()
                        f.close()

                        f = open("twitch_notice_channel.setting", 'r')
                        tc = f.read()
                        f.close()

                        if message.channel.id in yt:
                            new_yt = yt.replace("\n%s" % (message.channel.id), "")
                            f = open("yt_notice_channel.setting", 'w')
                            f.write(new_yt)
                            f.close()

                            f = open("yt_notice_channel_num.setting", 'r')
                            old_num = f.read()
                            f.close()
                            new_num = int(old_num) - 1
                            f = open("yt_notice_channel_num.setting", 'w')
                            f.write(str(new_num))
                            f.close()

                        if message.channel.id in tc:
                            new_tc = tc.replace("\n%s" % (message.channel.id), "")
                            f = open("twitch_notice_channel.setting", 'w')
                            f.write(new_tc)
                            f.close()

                            f = open("twitch_notice_channel_num.setting", 'r')
                            old_num = f.read()
                            f.close()
                            new_num = int(old_num) - 1
                            f = open("twitch_notice_channel_num.setting", 'w')
                            f.write(str(new_num))
                            f.close()

                            embed = discord.Embed(title="완료!", description="앞으로 `유튜브/트위치`와 관련한 모든 알림을 받지 않습니다!", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, "<@%s>," % (message.author.id), embed=embed)
                    else:
                        await app.send_message(message.channel, '<@%s>, 올바르지 않은 값이 입력되었습니다! `%s방송알림 도움말`을 입력하여 확인해주세요!' % (message.author.id, prefix))

                if message.content.startswith(prefix + '음성알림'):
                    if message.author.server_permissions.administrator or message.author.id in Setting.bot_admin:
                        q = message.content.replace('음성알림', '')
                        if "켜기" in q:
                            open("Server_%s/voice_notice.setting" % (message.server.id), 'w').write("1")
                            embed = discord.Embed(title="완료!", description="앞으로 봇이 음성채널에 접속&퇴장시 `이예에에에에!!!!` 와 `안해`를 외치게 됩니다!", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                        elif "끄기" in q:
                            open("Server_%s/voice_notice.setting" % (message.server.id), 'w').write("0")
                            embed = discord.Embed(title="완료!", description="앞으로 봇이 음성채널에 접속&퇴장시 `이예에에에에!!!!` 와 `안해`를 외치지 않게 됩니다!", color=Setting.embed_color)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, embed=embed)
                        else:
                            await app.send_message(message.channel, '<@%s>, 올바르지 않은 입력값입니다!' % (message.author.id))
                    else:
                        await app.send_message(message.channel, "<@%s>, 당신은 관리자가 아닙니다!" % (message.author.id))

                if message.content == prefix + "카페 대문":
                    data = requests.get("https://cafe.naver.com/MyCafeIntro.nhn?clubid=29567614")
                    status = data.status_code
                    if status != 200:
                        await custom_error(message, status, "일시적인 서비스 다운으로 추측 됩니다. 잠시 후 다시 시도해 주세요.")
                    else:
                        soup = bs4(data.text, "html.parser")
                        posts = soup.find_all('div', {'style' : 'text-align: center;'})

                        embed = discord.Embed(title="이번 주 카페 대문", color=Setting.embed_color)

                        original = str(posts[0])
                        original = original.split(" ")
                        original = str(original[10])
                        original = original.replace("""src="https://""", "")
                        original = original.replace('"', "")
                        file = "https://%s" % (original)

                        original = str(posts[1])
                        original = re.sub("""&nbsp;|amp;|\t|<div style="text-align: center;">|<span style="font-size: 10pt;">|<b>|</b>|<b style="font-size: 10pt;">|</div>|</span>""", '', original)
                        original = original.replace("이번주 추천 그림", "")
                        title = original

                        original = str(posts[2])
                        original = re.sub("""&nbsp;|amp;|\t|<div style="text-align: center;">|<span style="font-size: 10pt;">|</div>|</span>|<a class="m-tcol-c url-txt" href="|</a>""", '', original)
                        original = original.replace(""""<font color="#666666" face="돋움"><span style="display: inline-block; margin-top: 3px; font-size: 11px; overflow-wrap: break-word; text-align: -webkit-right;">""", '')
                        original = re.findall(r'\d+', original)

                        complete = False
                        count = 1
                        while not complete:
                            if len(str(original[count])) < 5:
                                count = count + 1
                                pass
                            else:
                                complete = True
                                id = original[count]
                                print(id)

                        link = "https://cafe.naver.com/teamsalad/%s" % (id)
                        print(link)

                        url = await url_short(message, link)

                        if url == False:
                            return None
                        else:
                            embed.add_field(name=title, value="링크 : %s" % (url), inline = False)
                            embed.set_image(url=file)
                            embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                            await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)

                if message.content == prefix + "카페 전체글" or message.content == prefix + "카페 최신글":
                    data = requests.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=29567614&search.boardtype=L")
                    status = data.status_code
                    if status != 200:
                        await custom_error(message, status, "일시적인 서비스 다운으로 추측 됩니다. 잠시 후 다시 시도해 주세요.")
                    else:
                        soup = bs4(data.text, "html.parser")
                        posts = soup.find_all('a', {'class' : 'article'})
                        result = False
                        position = 0
                        while not result:
                            if "article_noti" in str(posts[position]):
                                position = position + 1
                                pass
                            else:
                                result = True
                                complete = False
                                count = 1

                        embed = discord.Embed(title="팬카페 최근 게시물", color=Setting.embed_color)

                        while not complete:
                            original = str(posts[position])
                            original = re.sub("""&nbsp;|\n|\t|<a class="article" href="/|</a>|amp;""", '', original)
                            original = original.replace("""onclick="clickcr(this, 'cfa.atitle','','',event);">""", "")
                            original = original.replace("""<span class="head">""", "")
                            original = original.replace("</span>", "")
                            original = original.replace("<span class=ico-q>", "")
                            split = original.split()
                            link = "https://cafe.naver.com/%s" % (str(split[0]))
                            url = await url_short(message, link)
                            title = str(split[1:])
                            title = re.sub(""""|'|,|[|]""", '', title)
                            position = position + 1
                            count = count + 1
                            if url == False:
                                complete = True
                                return None
                            else:
                                embed.add_field(name=title, value="링크 : %s" % (url), inline = False)
                                if count == 9:
                                    complete = True

                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                    
                if message.content == prefix + "카페 방송공지":
                    data = requests.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=29567614&search.menuid=25&search.boardtype=L")
                    status = data.status_code
                    if status != 200:
                        await custom_error(message, status, "일시적인 서비스 다운으로 추측 됩니다. 잠시 후 다시 시도해 주세요.")
                    else:
                        soup = bs4(data.text, "html.parser")
                        posts = soup.find_all('a', {'class' : 'article'})
                        result = False
                        position = 0
                        while not result:
                            if "article_noti" in str(posts[position]):
                                position = position + 1
                                pass
                            else:
                                result = True
                                complete = False
                                count = 1

                        embed = discord.Embed(title="\"방송공지\" 게시판 최근 게시물", color=Setting.embed_color)

                        while not complete:
                            original = str(posts[position])
                            original = re.sub("""&nbsp;|\n|\t|<a class="article" href="/|</a>|amp;""", '', original)
                            original = original.replace("""" onclick="clickcr(this, 'gnr.title','','',event);">""", "")
                            original = original.replace("""<span class="head">""", "")
                            original = original.replace("</span>", "")
                            split = original.split()
                            link = "https://cafe.naver.com/%s" % (str(split[0]))
                            url = await url_short(message, link)
                            title = str(split[1:])
                            title = re.sub(""""|'|,|[|]""", '', title)
                            position = position + 1
                            count = count + 1
                            if url == False:
                                complete = True
                                return None
                            else:
                                embed.add_field(name=title, value="링크 : %s" % (url), inline = False)
                                if count == 6:
                                    complete = True

                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)

                if message.content == prefix + "카페 팬카페공지":
                    data = requests.get("https://cafe.naver.com/ArticleList.nhn?search.clubid=29567614&search.menuid=24&search.boardtype=L")
                    status = data.status_code
                    if status != 200:
                        await custom_error(message, status, "일시적인 서비스 다운으로 추측 됩니다. 잠시 후 다시 시도해 주세요.")
                    else:
                        soup = bs4(data.text, "html.parser")
                        posts = soup.find_all('a', {'class' : 'article'})
                        result = False
                        position = 0
                        while not result:
                            if "article_noti" in str(posts[position]):
                                position = position + 1
                                pass
                            else:
                                result = True
                                complete = False
                                count = 1

                        embed = discord.Embed(title="\"팬카페공지\" 게시판 최근 게시물", color=Setting.embed_color)

                        while not complete:
                            original = str(posts[position])
                            original = re.sub("""&nbsp;|\n|\t|<a class="article" href="/|</a>|amp;""", '', original)
                            original = original.replace("""" onclick="clickcr(this, 'gnr.title','','',event);">""", "")
                            split = original.split()
                            link = "https://cafe.naver.com/%s" % (str(split[0]))
                            url = await url_short(message, link)
                            title = str(split[1:])
                            title = re.sub(""""|'|,|[|]""", '', title)
                            position = position + 1
                            count = count + 1
                            if url == False:
                                complete = True
                                return None
                            else:
                                embed.add_field(name=title, value="링크 : %s" % (url), inline = False)
                                if count == 6:
                                    complete = True

                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, '<@%s>,' % (message.author.id), embed=embed)
                                
                if message.content == prefix + "접속":
                    if not message.author.voice_channel:
                        await app.send_message(message.channel, '당신은 음성채널에 있지 않습니다!')
                        return None

                    try:
                        voice = await app.join_voice_channel(message.author.voice_channel)
                    except Exception as e:
                        await custom_error(message, e, "봇이 이미 음성채널에 있는 것 같습니다!\n봇이 음성채널에 없음에도 불구하고 해당 애러가 발생하면 저희 팀에게 알려주세요!")
                        return None

                    embed = discord.Embed(title="여기를 눌러 원작자의 게시글로 갈 수 있습니다!", url="https://cafe.naver.com/teamsalad/32122", color=Setting.embed_color)
                    embed.set_image(url="https://cdn.discordapp.com/attachments/544850440450473994/544869673867542528/eeeeeeeehhhhhhh_unter.gif")
                    embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                    await app.send_message(message.channel, '<@%s>, <#%s> 에 성공적으로 접속했다 이예에에에에ㅔㅔㅔ!!!!' % (message.author.id, message.author.voice_channel.id), embed=embed)
                    result = open("Server_%s/voice_notice.setting" % (message.server.id), 'r').read()
                    if result == "1":
                        await music_play(message, app, "eeeeehhhhhhhhhh.mp3", 4)
                    else:
                        return None

                if message.content == prefix + "나가기":
                    try:
                        voice = app.voice_client_in(message.server)
                        embed = discord.Embed(title="여기를 눌러 원작자의 게시글로 갈 수 있습니다!", url="https://cafe.naver.com/teamsalad/17636", color=Setting.embed_color)
                        embed.set_image(url="https://cdn.discordapp.com/attachments/544850440450473994/544850464538230787/nope.jpg")
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, "<@%s>, 안 해" % (message.author.id), embed=embed)
                        result = open("Server_%s/voice_notice.setting" % (message.server.id), 'r').read()
                        if result == "1":
                            await music_play(message, app, "exit.m4a", 3)
                        else:
                            return None
                        await voice.disconnect()
                        try:
                            os.remove("Server_%s/playing.log" % (message.server.id))
                        except:
                            pass
                    except Exception as e:
                        await custom_error(message, e, "봇이 음성채널에 들어가 있지 않는거 같습니다!\n봇이 음성채널에 있음에도 불구하고 해당 애러가 발생하면 저희 팀에게 알려주세요!")
                        return None

                if message.content == prefix + "정지":
                    if not message.author.voice_channel:
                        await app.send_message(message.channel, '당신은 음성채널에 있지 않습니다!')
                        return None

                    try:
                        voice = app.voice_client_in(message.server)
                        await voice.disconnect()
                        os.remove("Server_%s/playing.log" % (message.server.id))
                        await app.join_voice_channel(message.author.voice_channel)
                        await app.send_message(message.channel, '<@%s>, 음악이 정지되었습니다!' % (message.author.id))
                    except:
                        pass

                if message.content.startswith('사과야'):
                    q = message.content.replace("사과야", "")
                    if q.endswith("도와줘"):
                        embed = discord.Embed(title="마플 AI 도움말", description=None, color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `모드변경`", value="모드는 총 `일반`, `청사과`, `스웩`으로, `사과야 [모드명] 바꿔줘`로 수정이 가능합니다.", inline = False)
                        embed.add_field(name="카테고리 : `명령어`", value="기본 명령어는 `사과야` 이며, 꾸몽님께서 올리신 **`마플 인공지능`** 영상을 베이스로 제작되었습니다.", inline = False)
                        embed.add_field(name="카테고리 : `관련링크`", value="인공지능 마플Ver [Minecraft] : https://youtu.be/riM4UCxpJE4", inline = False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        return None
                        
                    if "바꿔" in q:
                        q = q.replace("바꿔", "")
                        if "일반" in q:
                            open("Server_%s/maple_ver.setting" % (message.server.id), 'w').write("1")
                            await app.send_message(message.channel, '<@%s>, 일반 모드로 변경하였습니다!' % (message.author.id))
                            return None
                        elif "청사과" in q:
                            open("Server_%s/maple_ver.setting" % (message.server.id), 'w').write("2")
                            await app.send_message(message.channel, '<@%s>, 청사과 모드로 변경하였습니다!' % (message.author.id))
                            return None
                        elif "스웩" in q:
                            open("Server_%s/maple_ver.setting" % (message.server.id), 'w').write("3")
                            await app.send_message(message.channel, '<@%s>, 스웩모드로 변경하였습니다!' % (message.author.id))
                            return None
                        else:
                            await app.send_message(message.channel, '<@%s>, 올바른 버전명이 아닙니다!' % (message.author.id))
                            return None
                    
                    ver = open("Server_%s/maple_ver.setting" % (message.server.id), 'r').read()
                    if ver == "1":
                        if "날씨" in q:
                            response = random.randint(1,2)
                            if response == 1:
                                await app.send_message(message.channel, '<@%s>, 하늘이... 깜깜해요!' % (message.author.id))
                                await music_play(message, app, "Maple AI/1_night_sky.mp3", 1)
                            else:
                                await app.send_message(message.channel, '<@%s>, 날씨가... 어떻죠?' % (message.author.id))
                                await music_play(message, app, "Maple AI/1_unknown_weather.mp3", 1)
                        elif "운세" in q:
                            await music_play(message, app, "Maple AI/1_fortune.mp3", 15)
                            await app.send_message(message.channel, '<@%s>, 오늘의 운세는 말입니다...' % (message.author.id))
                        else:
                            await music_play(message, app, "Maple AI/1_reply.mp3", 0.3)
                            await app.send_message(message.channel, '<@%s>, 녜?' % (message.author.id))
                    elif ver == "2":
                        if "대답" in q or "길게" in q:
                            await music_play(message, app, "Maple AI/2_reply_long.mp3", 14)
                            await app.send_message(message.channel, '<@%s>, 네에에-' % (message.author.id))
                        else:
                            await music_play(message, app, "Maple AI/2_reply.mp3", 14)
                            await app.send_message(message.channel, '<@%s>, 네' % (message.author.id))
                    elif ver == "3":
                        if "내일" in q and "점심" in q:
                            await app.send_message(message.channel, '<@%s>, 내일 점심 그...' % (message.author.id))
                            await music_play(message, app, "Maple AI/3_lunch.mp3", 6)
                        elif "실시간 교통상황" in q:

                            async def play(message):
                                await app.send_message(message.channel, '<@%s>, 실시간 교통상황이 뭔데?' % (message.author.id))
                                await asyncio.sleep(1.5)
                                await app.send_message(message.channel, '<@%s>, 네비게이션 그 씨끄러워가꼬...' % (message.author.id))

                            await play(message)
                            await music_play(message, app, "Maple AI/3_live_traffic.mp3", 3)
                            await asyncio.sleep(0.2)
                            response = random.randint(1, 15)
                            if response == 1:
                                await app.send_message(message.channel, '<@%s>, 뭐꼬 야 내 영역에 침범할래?????' % (message.author.id))
                                await music_play(message, app, "Maple AI/3_virus_hidden_fix.mp3", 3)
                        elif "편의점" in q and "길" in q:
                            await app.send_message(message.channel, '<@%s>, 편의점 이 앞에 집앞에 있다 아이가' % (message.author.id))
                            await music_play(message, app, "Maple AI/3_convient_market.mp3", 6)
                        elif "부산" in q:
                            await app.send_message(message.channel, '<@%s>, 잘 따라해래이 경상북도' % (message.author.id))
                            await music_play(message, app, "Maple AI/3_busan.mp3", 2)
                        elif "재밌는" in q:
                            await app.send_message(message.channel, '<@%s>, 나 재밌는얘기 그 잘~ 알지...' % (message.author.id))
                            await music_play(message, app, "Maple AI/3_gag.mp3", 14)
                        elif "종료" in q:
                            await app.send_message(message.channel, '<@%s>, 마 다시는 내앞에 나타나지 마라' % (message.author.id))
                            await music_play(message, app, "Maple AI/3_off.mp3", 14)
                            try:
                                voice = app.voice_client_in(message.server)
                                await voice.disconnect()
                                os.remove("Server_%s/playing.log" % (message.server.id))
                            except:
                                pass
                        else:
                            response = random.randint(1,3)
                            if response == 1:
                                await app.send_message(message.channel, '<@%s>, 마 뭐꼬' % (message.author.id))
                                await music_play(message, app, "Maple AI/3_reply_1.mp3", 1)
                            elif response == 2:
                                await app.send_message(message.channel, '<@%s>, 뭐꼬' % (message.author.id))
                                await music_play(message, app, "Maple AI/3_reply_2.mp3", 0.2)
                            else:
                                await app.send_message(message.channel, '<@%s>, 와 부르노?' % (message.author.id))
                                await music_play(message, app, "Maple AI/3_reply_3_1.mp3", 1)
                                await app.send_message(message.channel, '<@%s>, 아 퍼뜩 말해라 와 부르노?' % (message.author.id))
                                await music_play(message, app, "Maple AI/3_reply_3_2.mp3", 1)
                    else:
                        await app.send_message(message.channel, '<@%s>, 버전 정보를 불러오지 못했습니다!\n`사과야 (버전명) 바꿔줘`로 다시 세팅 해 주세요!' % (message.author.id))

                if message.content.startswith('운터야'):
                    q = message.content.replace("운터야", "")

                    if q.endswith("도와줘"):
                        embed = discord.Embed(title="운터 AI 도움말", description=None, color=Setting.embed_color)
                        embed.add_field(name="카테고리 : `명령어`", value="기본 명령어는 `운터야` 이며, 꾸몽님께서 올리신 **`운터 인공지능`** 영상을 베이스로 제작되었습니다.", inline=False)
                        embed.add_field(name="카테고리 : `관련링크`", value="인공지능 운터Ver [Minecraft] : https://youtu.be/hahT9edqmsA", inline=False)
                        embed.set_footer(text="Ver. %s | %s" % (Setting.version, Copyright))
                        await app.send_message(message.channel, embed=embed)
                        return None

                    if "난 질문" in q and "했" in q:
                        await app.send_message(message.channel, '<@%s>, 응...응...응' % (message.author.id))
                        await music_play(message, app, "unter AI/yes yes yes.mp3", 2)
                    elif "대답" in q and "길게" in q:
                        await app.send_message(message.channel, '<@%s>, 우웅...' % (message.author.id))
                        await music_play(message, app, "unter AI/yeees.mp3", 1)
                    elif "내가" in q and "충전" in q:
                        await app.send_message(message.channel, '<@%s>, 응...' % (message.author.id))
                        await music_play(message, app, "unter AI/yes%s.mp3" % (random.randint(1, 5)), 0.3)
                        await asyncio.sleep(0.2)
                        await app.send_message(message.channel, '<@%s>, (시스템 종료)' % (message.author.id))
                        await music_play(message, app, "unter AI/system shutdown.mp3", 3)
                        await asyncio.sleep(0.2)
                        await app.send_message(message.channel, '<@%s>, 스마트폰이 종료되었습니다.' % (message.author.id))
                        await music_play(message, app, "unter AI/hah smart is shutdown.mp3", 1)
                        try:
                            voice = app.voice_client_in(message.server)
                            await voice.disconnect()
                            os.remove("Server_%s/playing.log" % (message.server.id))
                        except:
                            pass
                    else:
                        await app.send_message(message.channel, '<@%s>, 응...' % (message.author.id))
                        await music_play(message, app, "unter AI/yes%s.mp3" % (random.randint(1, 5)), 0.3)
                    
                if message.content == '주민마을발견':
                    try:
                        voice = await app.join_voice_channel(message.author.voice_channel)
                    except Exception as e:
                        pass
                    await app.send_message(message.channel, '<@%s>, 이스터에그 발견! 주민마을이다ㅏㅏ 이예ㅖㅖ' % (message.author.id))
                    await music_play(message, app, "tnt.mp3", 231)
            else:
                try:
                    os.makedirs("Server_%s" % (message.server.id))
                except:
                    pass

                open("Server_%s/maple_ver.setting" % (message.server.id), 'w').close()
                f = open("Servers.log", 'r')
                old = f.read()
                f.close()
                new = str(int(old) + 1)
                f = open("Servers.log", 'w')
                f.write(new)
                f.close()
                open("Server_%s/voice_notice.setting" % (message.server.id), 'w').write("1")
                open("Server_%s/prefix.setting" % (message.server.id), 'w').write(Setting.prefix)
                embed = discord.Embed(title="환영합니다!", description="해당 서버에 팀샐봇이 자동적으로 활성화 되었습니다! 팀샐봇 관련한 모든 기능을 사용하실 수 있습니다!", color=Setting.embed_color)
                embed.add_field(name="카테고리 : `안내`", value="기본 접두사는 ``%s`` 이며, ``%s도움말``로 기본 명령어를 확인하세요!" % (Setting.prefix, Setting.prefix))
                embed.add_field(name="카테고리 : `링크`", value="개인정보 처리방침 : https://rutapofficial.xyz/post/18/\n이용약관 : https://rutapofficial.xyz/post/21/")
                embed.add_field(name="카테고리 : `팀 화공`", value="공식 지원서버 : https://invite.gg/rutapbot\n공식 홈페이지 : https://rutapofficial.xyz", inline = False)
                embed.set_footer(text = "Server ID : %s | Ver. %s | %s" % (message.server.id, Setting.version, Copyright))
                await app.send_message(message.channel, embed=embed)
        except discord.HTTPException as e:
                await http_error(message, e)
    except Exception as e:
        try:
            await unknown_error(message, e)
        except discord.HTTPException as e:
            return None # 위에서 HTTPException 잡아서 출력하니까 여기서 HTTPException 애러나는데 왜나는지 모르겠음

app.run(Setting.token)
