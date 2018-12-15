from wxpy import ensure_one

from . import  spider

def get_no_forward(MsgType, sender,member):
    # 获取不能转发的消息

    type_list = {47:'表情消息', 57:'视频/语音聊天'}

    # 判断是否为群内消息,当时群消息时,此代码返回对应的通知内容
    if member and MsgType in type_list:
        return '禀报小主,有群消息了!\n 群名称:{}\n发信人:{}\n他发来了一封{}'.format(
            sender,member.name,type_list.get(MsgType))

    # 当上面的代码没有执行时,代表为好友消息,返回对应的通知内容
    if MsgType in type_list:
        return '禀报小主,有新消息了!\n 发信人:{}\n他发来了一封{}'.format(
            sender,type_list.get(MsgType))

    # 当类型为可转发的类型,返回None
    return None


# 获取可转发的数据
def get_forward(MsgType, sender,member):

    type_list = {3:'图片消息', 43:'视频消息', 34:'语音消息'}

    # 判断消息是否为内置的可转发的数据,且不是群聊消息时,返回特定通知内容
    if MsgType in type_list and not member:
        return '禀报小主,有新消息了!\n 发信人:{}\n他发来了一封{}'.format(sender,type_list.get(MsgType))

    # 判断消息是否为内置的可转发的数据,且是群聊消息时,返回特定通知内容
    if MsgType in type_list and member:
        return '禀报小主,有群消息了!\n群名称:{}\n发信人:{}\n他发来了一封{}'.format(
            sender,member.name,type_list.get(MsgType))

# 回复好友消息
def replay_message(message,friends):
    # 将管理员消息按照#分割,0 为好友名称 1 为消息内容
    rep = message.split('#')

    # 判断是否为查询快递命令
    if '@快递' in rep[0]:
        express = spider.GetExpress(''.join(rep[1:]))
        return express.get_express()
    # 获取好友名称,将@替换掉
    reply_name = rep[0].replace('@', '')

    # 查找人员,返回对应的对象
    replay = friends.search(reply_name)

    # 如果有数据,表示有该好友
    if replay:
        # 获取好友对象
        replay = ensure_one(replay)
        # 放置有多个#在文本中,所有用空字符组合一下消息
        reply_msg = ''.join(rep[1:])
        # 将回复的消息发送给好友
        replay.send_msg(reply_msg)
        # 返回管理员通知消息
        return '禀报小主,信息已成功回复!'

    # 当没有找到还有时,返回通知消息
    else:
        return '禀报小主,小的翻遍花名册,查无此人,请问小主是否记错名字了呢!'

# 回复群主消息
def replay_group_message(message,groups):
    # 将管理员消息按照#分割,0 为群聊名称 1 为消息内容
    rep = message.split('#')
    # 获取群聊名称,将-替换掉
    group_name = rep[0].replace('-', '')
    # 查找群,返回对应的对象
    replay_group = groups.search(group_name)
    if replay_group:
        replay_group = replay_group[0]
        reply_msg = ''.join(rep[1:])
        replay_group.send_msg(reply_msg)
        return '禀报小主,信息已成功回复!'
    else:
        return '禀报小主,小的翻遍花名册,查无此人,请问小主是否记错名字了呢!'