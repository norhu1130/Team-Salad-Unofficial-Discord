import os, discord, asyncio, json, urllib, datetime, random, sys, urllib.request, setting

Setting = setting.Settings()
app = discord.Client()

async def ncustom_error(message, e, description):
    now = datetime.datetime.now()
    randcode = "ERR :: %s%s%s%s" % (now.month, random.randint(1,10000000), now.day, random.randint(1,10000)) 
    embed = discord.Embed(title="죄송합니다. 원인을 알 수 없는 애러가 발생했습니다.", description="%s\nOfficial Support Server : https://invite.gg/rutapbot" % (description), color=Setting.error_embed_color)
    embed.set_footer(text = randcode)
    await app.send_message(message.channel, embed=embed)
    await app.send_message(app.get_channel(Setting.error_notice_channel), "```Markdown\n# Custom error\n* Server : %s(%s)\n* Channel : %s(%s)\n* Author : %s(%s)\n* Code : %s\n- errinfo : %s```" % (message.server, message.server.id, message.channel, message.channel.id, message.author, message.author.id, randcode, e))

async def url_short(message, q):
    data = "url=%s" % (urllib.parse.quote(q))
    request = urllib.request.Request("https://openapi.naver.com/v1/util/shorturl")
    request.add_header("X-Naver-Client-Id", Setting.naver_api_id)
    request.add_header("X-Naver-Client-Secret", Setting.naver_api_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        response = response_body.decode('utf-8')
        url = json.loads(response)["result"]["url"]
        return url
    else:
        await ncustom_error(message, rescode, "url 단축사이트의 일시적인 다운으로 파악됩니다. 잠시 후 다시 시도하여 주세요.")
        return False

async def papago_smt(message, q, start, end):
    encText = urllib.parse.quote(q)
    data = "source=%s&target=%s&text=%s" % (start, end, encText)
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", Setting.naver_api_id)
    request.add_header("X-Naver-Client-Secret", Setting.naver_api_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        response = response_body.decode('utf-8')
        result = json.loads(response)["message"]["result"]["translatedText"]
        return result
    else:
        await ncustom_error(message, rescode, "API의 일시적인 다운으로 파악됩니다. 잠시 후 다시 시도하여 주세요.")
        return False

async def papago_detectlangs(message, q):
    encQuery = urllib.parse.quote(q)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", Setting.naver_api_id)
    request.add_header("X-Naver-Client-Secret", Setting.naver_api_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        response = response_body.decode('utf-8')
        result = json.loads(response)["langCode"]
        return result
    else:
        await ncustom_error(message, rescode, "API의 일시적인 다운으로 파악됩니다. 잠시 후 다시 시도하여 주세요.")
        return False