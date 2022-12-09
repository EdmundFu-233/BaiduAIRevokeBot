# -*- coding:UTF-8 -*-
####AIRevokeBotVer1.0####
import requests
import base64
from botoy import GroupMsg,Action,S,Botoy
from botoy import decorators as deco
from botoy.collection import MsgTypes
from botoy.decorators import these_msgtypes,from_these_groups
from botoy.contrib import plugin_receiver
from urllib.parse import quote
import ast
@plugin_receiver.group
@deco.ignore_botself
@from_these_groups(    )           #这里为你需要监听的群聊
@these_msgtypes(MsgTypes.TextMsg,               #接收信息类型
                MsgTypes.AtMsg,
                MsgTypes.PicMsg,
                MsgTypes.ReplyMsg,
                MsgTypes.ReplyMsgA
                )
def main(ctx:GroupMsg):
    msg = ctx.Content.strip()
    if 'Content' in msg:
        msgPre = ast.literal_eval(ctx.Content)
        msg = msgPre.get('Content').strip()
    if 'Content' not in msg and 'GroupPic' in msg:
        return
    print(msg)
    url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=" + get_access_token()
        
    payload='text=' + quote(msg,encoding='utf-8')
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    responsejson = response.json()
    conclusion = responsejson.get('conclusionType')
    if conclusion == 2 :                #判断是否合规
        responseData = responsejson.get('data')
        Action(ctx.CurrentQQ).revokeGroupMsg(
            group=ctx.FromGroupId,
            msgSeq=ctx.MsgSeq,
            msgRandom=ctx.MsgRandom,
            )
        Action(ctx.CurrentQQ).shutUserUp(
            groupID=ctx.FromGroupId,
            userid=ctx.FromUserId,
            ShutTime=2                              #这里是你需要禁言的时长，单位为分钟
            )
        S.bind(ctx).text("根据百度AI返回结果，此发言不合规，已自动撤回。" + "百度认为不合规理由为: " 
        + str(responseData[0].get('msg') + " 这次判断的把握为: " + str(responseData[0].get('hits')[0].get('probability'))))
        S.bind(ctx).text("Base64后的原文： " + str(base64.b64encode(msg.encode('utf-8'))),'utf-8')
        print("sensetive msg discover")


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"            #下方为你的KEY，请去百度AI开放平台申请
    params = {"grant_type": "client_credentials", "client_id": "XXXXXXXX", "client_secret": "XXXXXXXXX"}
    return str(requests.post(url, params=params).json().get("access_token"))
bot_qq = 123456             #你的BOT的QQ号
bot = Botoy(
    qq = bot_qq,
)
if __name__ == "__main__":
    bot.run()