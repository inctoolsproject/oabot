import errno
import os
import sys
import tempfile

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import requests, json

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi("nfyIfQMOsUJ0948KJkMbQAEdro5hsDXfW8QqSFHiVjcheRZP/g3yDojeRP+PXpElmAS/BLWvZdln2gFN8aPYI1HWTZaPEur1IVoHp+Qv/CAFPnHRd/Zs73HEQHEGJnJ3vz2XqJSPyuvROg5UfGHkAgdB04t89/1O/w1cDnyilFU=")
# Channel Secret
handler = WebhookHandler("736dcf921090876bb87b6fc52cff9996")
#===========[ NOTE SAVER ]=======================
notes = {}

# Post Request
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Terima kasih telah mengundang saya ke dalan group\nKetik !help untuk melihat event, team formation, dan fitur lainnya")) 
    
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text #simplify for receove message
    sender = event.source.user_id #get user_id
    gid = event.source.sender_id #get group_id
    
#=====[ LEAVE GROUP OR ROOM ]==========
    # if text == "!me":
    #     if isinstance(event.source, SourceUser):
    #         profile = line_bot_api.get_profile(event.source.user_id)
    #         line_bot_api.reply_message(
    #             event.reply_token, [
    #                 TextSendMessage(text="Nama: " + profile.display_name),
    #                 TextSendMessage(text="Status bio: " + profile.status_message)
    #             ]
    #         )
        # elif isinstance(event.source, SourceUser):
        #     profile = line_bot_api.get_profile(event.source.sender_id)
        #     line_bot_api.reply_message(
        #         event.reply_token, [
        #             TextSendMessage(text="Nama: " + profile.display_name),
        #             TextSendMessage(text="Status bio: " + profile.status_message)
        #         ]
        #     )
        # else:
        #     line_bot_api.reply_message(
        #         event.reply_token,
        #         TextSendMessage(text="Bot can"t use profile in group chat"))

    if text == "!coss-bye":
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Bye semuanya :D"))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Bye semuanya :D"))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Command ini tidak bisa dipakai dalam private chat :("))
#=====[ TES MESSAGE ]=============
    if text == "redtube on":
        angka = random.randint(1, 200)
        r = requests.get("https://api.boteater.vip/redtube?page={}".format(angka))
        data=r.text
        data=json.loads(data)
        for anu in data["result"]:
            line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=anu["dl"], preview_image_url=anu["img"]))
    elif text == "xvideos on":
        angka = random.randint(1, 200)
        r = requests.get("https://api.boteater.vip/xvideos?page={}".format(angka))
        data=r.text
        data=json.loads(data)
        for anu in data["result"]:
            line_bot_api.reply_message(event.reply_token,VideoSendMessage(original_content_url=anu["dl"], preview_image_url=anu["img"]))
#=====[ TES MESSAGE ]=============
    elif text == "confirm":
        confirm_template = ConfirmTemplate(text="Bot nya bagus?", actions=[
            MessageTemplateAction(label="Yes", text="Yes!"),
            MessageTemplateAction(label="No", text="No!"),
        ])
        template_message = TemplateSendMessage(
            alt_text="Confirm alt text", template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)

#=====[ SEARCH ID LINE ]=============
    elif "/idline: " in event.message.text:
        skss = event.message.text.replace("/idline: ", "")
        sasa = "http://line.me/R/ti/p/~" + skss
        text_message = TextSendMessage(text=sasa)
        line_bot_api.reply_message(event.reply_token, text_message)
        return 0

    # elif "!contoh idline"

    # elif "/apakah " in event.message.text:
    #     quo = ("Iya","Tidak","Gak tau","Bisa jadi","Mungkin iya","Mungkin tidak")
    #     jwb = random.choice(quo)
    #     text_message = TextSendMessage(text=jwb)
    #     line_bot_api.reply_message(event.reply_token, text_message)
    #     return 0

    # elif (text == "999+") or (text == "999++"):
    #     message = TextSendMessage(text="ckk by")
    #     line_bot_api.reply_message(event.reply_token, message)

    # elif (text == "Bot") or (text == "bot"):
       #  message = TextSendMessage(text="Siapa bot? ke bot an lu")
      #   line_bot_api.reply_message(event.reply_token, message)

   #  elif (text == "Tes") or (text == "tes") or (text == "Test") or (text == "test"):
        # message = TextSendMessage(text="suk beybeh")
       #  line_bot_api.reply_message(event.reply_token, message)

    # elif (text == "@") or (text == "Yud") or (text == "yud") or (text == "yudha"):
    #     message = TextSendMessage(text="Apa manggil-manggil cogan")
    #     line_bot_api.reply_message(event.reply_token, message)

    # elif text == ".":
    #     message = TextSendMessage(text="Titik titik amat so high lu")
    #     line_bot_api.reply_message(event.reply_token, message)

    # elif (text == "Bah") or (text == "bah"):
    #     message = TextSendMessage(text="Beh")
    #     line_bot_api.reply_message(event.reply_token, message)

#=====[ TEMPLATE MESSAGE ]=============
    # elif text == "/tools":
    #     buttons_template = TemplateSendMessage(
    #         alt_text="Tools message",
    #         template=ButtonsTemplate(
    #             title="[ TOOLS MESSAGE ]",
    #             text= "Tap the Button",
    #             actions=[
    #                 MessageTemplateAction(
    #                     label="App Cloner",
    #                     text="/app clone"
    #                 ),
    #                 MessageTemplateAction(
    #                     label="Cek ID Line",
    #                     text="!contoh idline"
    #                 ),
    #                 MessageTemplateAction(
    #                     label="Your profile",
    #                     text="/me"
    #                 )
    #             ]
    #         )
    #     )
        
    #     line_bot_api.reply_message(event.reply_token, buttons_template)
    elif (text == "!help") or (text == "help") or (text == "Help"):
        message = TemplateSendMessage(
            alt_text ="Help message",
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = "https://i.ibb.co/HPcmhCY/1551283598926.jpg",
                        title = "COSS Menu",
                        text = "Silahkan pilih\nTekan tombol dibawah ini",
                        actions = [
                            MessageTemplateAction(
                                label = "Random COSS anime music",
                                text = "!random-anime-music"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://i.ibb.co/HPcmhCY/1551283598926.jpg",
                        title = "COSS Menu 2",
                        text = "Silahkan pilih, tekan tombol dibawah ini",
                        actions = [
                            MessageTemplateAction(
                                label = "Keluarkan bot",
                                text = "!coss-Bye"
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)


    elif (text == "!About us") or (text == "!about us") or (text == "About us") or (text == "about us"):
        buttons_template = TemplateSendMessage(
            alt_text =" Help message",
            template = ButtonsTemplate(
                title = "LIST HELP",
                text = "silahkan pilih, tekan tombol dibawah ini",
                actions = [
                    MessageTemplateAction(
                        label = "Comming soon",
                        text = "!commingsoon"
                    ),
                    MessageTemplateAction(
                        label = "Management COSS",
                        text = "!managementcoss"
                    ),
                    MessageTemplateAction(
                        label = "About Coss",
                        text = "!aboutcoss"
                    ) 
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif "!commingsoon" in event.message.text:
        token = event.reply_token
        text_message = TextSendMessage(text = "Comming Soon...")
        line_bot_api.reply_message(token, text_message)
#=== [SEGAME TEAM] ===
    elif (text == "!aboutcoss") or (text == "About Coss") or (text == "about coss") or (text == "coss family") or (text == "Coss Family") or (text == "COSS"):
        token = event.reply_token
        buttons_template = TemplateSendMessage(
            alt_text = "COSS",
            template = ButtonsTemplate(
                title = "Community Of Smule Singers",
                text = ".....",
                actions = [
                    MessageTemplateAction(
                        label = "Terima Kasih",
                        text = "#"
                    )
                ]
            )
        )
        line_bot_api.reply_message(token, buttons_template)


    if event.message.text == "!mlbb team":
        message_2 = TemplateSendMessage(
            alt_text = "SeGame MLBB Team",
            template = ButtonsTemplate(
                title = "   Mobile Legend Team",
                text = "Klik dibawah ini\nUntuk melihat informasi team kami",
                thumbnail_image_url = "https://cdn.pbrd.co/images/HYh1DgJ.png",
                actions = [
                    MessageTemplateAction(
                        label = "Next Generation",
                        text = "!next generation team"
                    ),
                    MessageTemplateAction(
                        label = "The Raven",
                        text = "!the raven team"
                    ),
                    MessageTemplateAction(
                        label = "Hunger Strike",
                        text = "!hunger strike team"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message_2)

    elif (text == "!the raven team") or (text == "the raven team") or (text == "The raven team"):
        message = TemplateSendMessage(
            thumbnail_image_url = "http://www.segameesports.com/assets/img/games/ML-Logo.png",
            alt_text = "THE RAVEN TEAM",
            template = CarouselTemplate(
                columns = [
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgronQ.png",
                        title = "zato",
                        text = "The Raven Leader\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgronQ.png"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgsdV0.png",
                        title = "Umbu Jahat",
                        text = "The Raven Member\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgsdV0.png"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgsyPK.png",
                        title = "RDecimo",
                        text = "The Raven Member\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgsyPK.png"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgqEFk.jpg",
                        title = "Mons°Wijay",
                        text = "The Raven Member\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgqEFk.jpg"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgtnPq.png",
                        title = "RAMA #46",
                        text = "The Raven Member\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgtnPq.png"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgumHa.png",
                        title = "mau ga jadi pacarku?",
                        text = "The Raven Member\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgumHa.png"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url = "https://cdn.pbrd.co/images/HYgumHa.png",
                        title = "Sibor",
                        text = "The Raven Member\nKlik dibawah ini untuk melihat profile",
                        actions = [
                            URITemplateAction(
                                label = "CEK PROFILE",
                                uri = "https://cdn.pbrd.co/images/HYgumHa.png"
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

    elif (text == "!next generation team") or (text == "!the raven team") or (text == "!hunger strike team"):
        token = event.reply_token
        text_message = TextSendMessage(text = "Comming Soon")
        line_bot_api.reply_message(token, text_message)
#=====[ CAROUSEL MESSAGE ]==========
    elif text == "/musik":
        buttons_template = TemplateSendMessage(
            alt_text="Enjoy whit music",
            template=ButtonsTemplate(
                title="[ GENDRE MUSIC ]",
                text= "Tap the Button",
                actions=[
                    MessageTemplateAction(
                        label="Music Indonesia",
                        text="/Mindo"
                    ),
                    MessageTemplateAction(
                        label="Music Barat",
                        text="/Mbarat"
                    ),
                    MessageTemplateAction(
                        label="Music Kpop",
                        text="/Mkpop"
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, buttons_template)
#=====[ CAROUSEL MESSAGE ]==========
    elif (text == "!managementcoss") or (text == "Managementcoss") or (text == "managementcoss"):
        message = TemplateSendMessage(
            alt_text="MANAGEMENT COSS",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/0J8m0Bv/Meiya.jpg",
                        title="Owner COSS",
                        text="@COSS_JustMeiya",
                        actions=[
                            URITemplateAction(
                                label="Meiya",
                                uri="https://line.me/ti/p/~justmeiya"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/tzbrRYB/Qian.jpg",
                        title="Founder COSS",
                        text="@__COSSQIAN",
                        actions=[
                            URITemplateAction(
                                label="Qian",
                                uri="https://line.me/ti/p/~qian_bi"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/7jQ7DRG/Need.jpg",
                        title="Co Founder COSS",
                        text="@COSS_JustNeed",
                        actions=[
                            URITemplateAction(
                                label="Need",
                                uri="https://line.me/ti/p/~NeedMoodBooster"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/RhdrQnN/Mamah.jpg",
                        title="Leader COSS",
                        text="@X1N_RYN_COSS",
                        actions=[
                            URITemplateAction(
                                label="Mamah",
                                uri="https://line.me/ti/p/~azzky41"
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url="https://i.ibb.co/TgGyrVM/Via.jpg",
                        title="Admin COSS",
                        text="@_COSSVIACAVS_",
                        actions=[
                            URITemplateAction(
                                label="Vianita",
                                uri="https://line.me/ti/p/~cibellin"
                            )
                        ]
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)

#============= [GABUNG DISCORD BUTTON TEMPLATE] =============
    if event.message.text == "!gabung discord":
        buttons_template = TemplateSendMessage(
            alt_text="SeGame Official",
            template=ButtonsTemplate(
                title="SeGame Discord",
                text="segame dulu yuk bareng kita",
                thumbnail_image_url="https://i.ibb.co/Yfrjvqs/Se-Game-Discord-Logo.png",
                actions=[
                    URITemplateAction(
                        label="Invite link 1",
                        uri="https://discord.me/SeGame_Esports"
                    ),
                    URITemplateAction(
                        label="Invite link 2",
                        uri="https://discord.gg/vMcMe8f"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

    if event.message.text == "!me":
        profile = line_bot_api.get_profile(event.source.user_id)
        buttons_template = TemplateSendMessage(
            alt_text="Profile Status",
            template=ButtonsTemplate(
                title="" + profile.display_name,
                text="Download photo profile klik dibawah ini",
                thumbnail_image_url="" + profile.picture_url,
                actions=[
                    URITemplateAction(
                        label="DOWNLOAD PHOTO",
                        uri="" + profile.picture_url,
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

#===========[RANDOM ANIME MUSIC]===========#
    if event.message.text == "!random-anime-music":
        request_url = requests.get("https://api.moe.team/animusic")
        data = request_url.text
        data = json.loads(data)
        music = data["data"]
        token = event.reply_token
        message_audio = AudioSendMessage(
            original_content_url = "{}".format(music["audio"]),
            duration = 240000
            ),
        buttons_template = TemplateSendMessage(
            alt_text = "Random anime music",
            template = ButtonsTemplate(
                title = "Judul : {}".format(music["title"]),
                text = "Klik dibawah ini untuk mendengarkan musik",
                thumbnail_image_url = "{}".format(music["image"]),
                actions = [
                    URITemplateAction(
                        label = "DENGARKAN MUSIK",
                        uri = "{}".format(music["audio"])
                        ),
                    MessageTemplateAction(
                        label = "Musik lainnya",
                        text = "!random-anime-music"
                        )
                    ]
                )
            )
        line_bot_api.reply_message(token, buttons_template)
        return 0
#===============================

# [MUSIK COMMAND]

    elif "!musik " in event.message.text:
        query = event.message.text.replace("!musik ","")
        r = requests.get("http://ryns-api.herokuapp.com/joox?q={}".format(query))
        data = r.text
        data = json.loads(data)
        data2 = data["result"]
        jmlh = len(data2)
        datalagu = []
        if jmlh > 10:
            jmlh = 10
        else:
            pass
        for x in range(0,jmlh):
            item = CarouselColumn(
                thumbnail_image_url = "{}".format(str(data2[x]["img"])),
                title = "{}".format(str(data2[x]["title"])),
                text = "{}".format(str(data2[x]["artis"])),
                actions = [
                    URITemplateAction(
                        label = "{}".format(str(data2[x]["title"])),
                        uri = "{}".format(str(data2[x]["url"]))
                    )
                ]
            ),
            datalagu.append(item)
        buttons_template = TemplateSendMessage(
            alt_text = "COSS Musik",
            template = CarouselTemplate(
                columns = [(str(datalagu))]
            )
        )
    line_bot_api.reply_message(event.reply_token, buttons_template)  

   # elif (text == "sebel") or (text == "Sebel"):
   #     message = TemplateSendMessage(
   #         alt_text="NeedBot",
   #         template=ImageCarouselTemplate(
   #             columns=[
   #                 ImageCarouselColumn(
   #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52114135/IOS/sticker_animation@2x.png",
   #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
   #                 )
   #             ]
   #         )
   #     )
   # line_bot_api.reply_message(event.reply_token, message)
    # elif "https://api.boteater.co/joox/single/"
#=====[ FLEX MESSAGE ]==========
    # elif text == "yud test":
    #     message = ImagemapSendMessage(
    #         base_url="https://i.imgur.com/g8P1V9Q.jpg",
    #         alt_text="manyimak corom",
    #         base_size=BaseSize(height=1040, width=1040),
    #         actions=[
    #             URIImagemapAction(
    #                 link_uri="https://line.me/ti/p/%40ajd1759p",
    #                 area=ImagemapArea(
    #                     x=0, y=0, width=520, height=1040
    #                 )
    #             ),
    #             MessageImagemapAction(
    #                 text="yudha ganteng",
    #                 area=ImagemapArea(
    #                     x=520, y=0, width=520, height=1040
    #                 )
    #             )
    #         ]
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)

#=====[ Sticker MESSAGE ]==========
    # elif (text == "oksip") or (text == "Oksip"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002735/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "makasih") or (text == "Makasih"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/153453/IOS/sticker.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "nyimak") or (text == "Nyimak"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/13162615/IOS/sticker.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "ga") or (text == "gak") or (text == "gamau") or (text == "Gamau") or (text == "Ga") or (text == "Gak"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/8683557/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "good night") or (text == "Good night") or (text == "selamat malam") or (text == "Selamat malam"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/8683546/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "hai") or (text == "Hai") or (text == "halo") or (text == "Halo"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002738/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "sabar") or (text == "Sabar"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/22499899/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "wkwk") or (text == "Wkwk"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/27695296/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "hehe") or (text == "Hehe"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52002763/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "siap") or (text == "Siap"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/51626520/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif text == "?":
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/34751035/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "please") or (text == "Please") or (text == "tolong") or (text == "Tolong"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/51626499/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "ok") or (text == "oke") or (text == "Ok") or (text == "Oke"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/51626500/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "hahaha") or (text == "Hahaha") or (text == "Haha")or (text == "haha"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/40381622/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
    # elif (text == "sebel") or (text == "Sebel"):
    #     message = TemplateSendMessage(
    #         alt_text="Yudha public bot",
    #         template=ImageCarouselTemplate(
    #             columns=[
    #                 ImageCarouselColumn(
    #                     image_url="https://stickershop.line-scdn.net/stickershop/v1/sticker/52114135/IOS/sticker_animation@2x.png",
    #                     action=URIAction(uri="http://line.me/ti/p/%40ajd1759p")
    #                 )
    #             ]
    #         )
    #     )
    #     line_bot_api.reply_message(event.reply_token, message)
#=======================================================================================================================
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
