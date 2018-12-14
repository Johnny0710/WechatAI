
from wxpy import *

from utils import weather,dispose,wxpy_callback



# 初始化管理员,这个名称为登录的微信好友列表中的名称或备注名
admin_name = '攸小小'

# 初始化机器人,登录微信
bot = Bot(cache_path=True,console_qr=2,qr_path='otherMessage/qr_code.png',qr_callback=wxpy_callback.qr_callback)

# 获取好友列表
my_friends  = bot.friends()
# 获取当前微信号群列表
my_group = bot.groups()
# 获取当前微信公众号列表
my_mps = bot.mps()
# 查找管理员,获取管理员对象
admin = ensure_one( bot.search(admin_name))



# 定义消息处理的函数,使用wxpy提供的装饰器
# 帮助文档:https://wxpy.readthedocs.io/zh/latest/messages.html?highlight=register
@bot.register()
def friend_msg(msg):

    # 获取当前消息的类型
    msg_type = msg.raw['MsgType']
    # 获取当前消息的文本
    message = msg.text
    # 判断发信人是否为管理员
    is_admin = msg.sender.name == admin.name
    # 判断发信人是否为公众号
    is_mp = my_mps.search(msg.sender.name)
    # 在微信中有一部分消息是无法直接通过wxpy转发给其他人的,
    # 这里定义了一个函数来判断当前消息是否符合转发规则
    no_forward = dispose.get_no_forward(msg_type,msg.sender.name,msg.member)

    # 判断no_forward 是否有数据,且是否不是管理员给机器人发送的消息
    if no_forward and not is_admin :
        # 当不是管理员发送的消息时,将提醒管理员有消息了
        admin.send_msg(no_forward)

        # 判断是否为群聊消息,在wxpy中如果是群聊消息 msg.member 显示的是发信人
        # 当判断不是群聊消息时,提醒发信人此消息已告知管理员
        # 2018年12月14日14:38:32
        # 添加判断是否为公众号消息,如果不是公众号提醒发信人已通知管理员
        if not msg.member and not is_mp :
            return '已将消息转发給小主'

    # 判断接收的消息类型是否为文本型,文本型为1 且不是群内的消息以及公众号消息
    if msg_type == 1 and not msg.member and not is_mp :

        # 判断当前文本消息是否为'指令,如果是指令且是管理员发送的,返回如下信息'
        if message == '指令' and msg.sender.name == admin.name:
            return '小主您好,小的目前接受以下几条指令\n' \
                   '1、XX天气  获取某个城市的天气预报\n' \
                   '2、@好友名称#消息内容 给指定的某位好友发送消息,只可以发送文本消息哦\n' \
                   '3、-群名称#消息内容  给指定的群发送消息,只接受文本消息与微信默认表情'

        # 判断当前聊天是否包含天气字眼,如果包含天气字眼返回天气情况
        if '天气' in message and len(message) > 3 :
            return weather.get_city_weather(message.replace('天气', ''))

        # 管理员回复消息,判断管理员发送的消息是否包含@字符,且@字符为第一位时,代表回复好友消息
        if '@' in message and message[0] == '@' and  msg.sender.name == admin.name:
            return dispose.replay_message(message,my_friends)

        # 管理员回复消息,判断管理员发送的消息是否包含-字符,且-字符为第一位时,代表回复群消息
        if '-' in message and message[0] == '-' and msg.sender.name == admin.name:
            return dispose.replay_group_message(message,my_group)

        # 当以上条件都不符合且不是管理员以及公众号消息时,将文本消息发送给管理员
        # 并告知发信人
        if msg.sender.name != admin.name and not is_mp:
            admin.send_msg('有新消息\n{}'.format(msg))
            return '已将消息转发給小主'

    # 判断当前消息是否为文本型 且 是群消息时 通知管理员
    # 群内不进行任何回复,以免造成群内消息过多造成刷屏

    if msg_type == 1 and  msg.member:
        admin.send_msg('有群消息\n群名称:{}\n发信人:{}\n消息内容:{}'.format(
            msg.sender.name,msg.member.name,msg.text
        ))


    # 当消息为文本型以外的消息且为可转发的消息,且不是管理员消息是,将消息转发给管理员
    # 2018年12月14日14:38:32
    # 添加判断是否为公众号消息,如果不是公众号消息回复以下内容
    if msg_type > 1 and not is_admin and not is_mp:
        msg.forward(admin,prefix= dispose.get_forward(msg_type,msg.sender.name,msg.member))
        if not msg.member and not my_mps.search(msg.sender.name):
            return '已将消息转发給小主'

bot.join()