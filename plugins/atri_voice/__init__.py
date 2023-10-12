from typing import Tuple, Any
from nonebot.params import RegexGroup
from nonebot.plugin import PluginMetadata, on_regex
from nonebot.adapters.onebot.v11 import MessageSegment, ActionFailed,Bot,MessageEvent
from BertVITS2 import Trans_GS
from config import BotSelfConfig
from .katakana import katakana

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-atri",
    description="ATRI VITS 模型拟声",
    usage="ATRI\n" +
          "- 说(日语)\n",
    extra={
        "unique_name": "Gal-Voice",
        "example": "说お兄ちゃん大好き",
        "author": "KOG <1458038842@qq.com>",
        "version": "0.0.1",
    },
)

import os
# api for other plugins
def gs_func(msg):
    Trans_GS(msg,0,'voice.wav')
    voice=f'file:///'+os.getcwd()+'/voice.wav'
    return MessageSegment.record(voice)


Priority = 5

gp=False
send_id=1458038842
g_p_regex = "^(群聊|私聊)(.+)$"
g_p_cmd = on_regex(g_p_regex, block=True, priority=Priority)

def atoi(s):
    s = s[::-1]
    num = 0
    for i, v in enumerate(s):
        for j in range(0, 10):
            if v == str(j):
                num += j * (10 ** i)
    return num

@g_p_cmd.handle()
async def _(event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    g_p,id = matched[0],matched[1]
    user_id = event.get_user_id()
    if user_id not in BotSelfConfig.superusers:
        await g_p_cmd.finish('权限不足')
    global gp
    global send_id
    send_id=atoi(id)
    if(g_p=='群聊'):
        gp=True
        # print("切换至群聊对象{0}".format(send_id))
        await g_p_cmd.finish("切换至群聊对象{0}".format(send_id))
    else:
        gp=False
        # print("切换至私聊对象{0}".format(send_id))
        await g_p_cmd.finish("切换至私聊对象{0}".format(send_id))


gs_regex = "^(?:温迪|)(发送|说|文件)(.+)$"

gs_cmd = on_regex(gs_regex, block=True, priority=Priority)



@gs_cmd.handle()
async def _(bot:Bot,event: MessageEvent,matched: Tuple[Any, ...] = RegexGroup()):
    cmd,msg = matched[0],matched[1]
    if cmd=='发送':
        user_id = event.get_user_id()
        if user_id not in BotSelfConfig.superusers:
            await gs_cmd.finish('权限不足')
        try:
            if(gp):
                await bot.send_group_msg(group_id=send_id,message=gs_func(msg=msg))
            else:
                await bot.send_private_msg(user_id=send_id,message=gs_func(msg=msg))
            await gs_cmd.finish('发送成功')
        except ActionFailed as e:
            await gs_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
    elif cmd=='说':
        try:
            await gs_cmd.finish(message=gs_func(msg=msg))
        except ActionFailed as e:
            await gs_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
    else:
        try:
            gs_func(msg=msg)
            uid=event.get_user_id()
            gid=getattr(event, 'group_id', None)
            if gid!=None:
                voice=os.getcwd()+'/voice.wav'
                await bot.call_api('upload_group_file',group_id=gid,file=voice,name=msg+'.wav')
            else:
                voice=os.getcwd()+'/voice.wav'
                await bot.call_api('upload_private_file',user_id=uid,file=voice,name=msg+'.wav')
        except ActionFailed as e:
            await gs_cmd.finish('API调用失败：' + str(e) + '。请检查输入字符是否匹配语言。')
