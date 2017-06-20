from collections import defaultdict
from enum import Enum

import itchat
from itchat.content import TEXT, FRIENDS

GROUP_NAME = '中德人工智能协会'
MASTER_NAME = '肖涵'
TRIGGER_WORDS = ['我要进AI群', '我想进AI群', '拉进AI群']
WARN_FWD = '注意，你的自我介绍将发送给其他群成员。'
AFTER_ADD = '若要申请进群请回复 我想进AI群'
FIRST_REPLY = '您好%s，欢迎申请加入%s！请您先做个自我介绍，随后我会将您加入到群聊中。\n' \
              '请在5分钟之内完成介绍，否则需要重新输入"我要进AI群"激活入群步骤。\n' \
              '请使用文字自我介绍，并包含"我是"关键字。\n' \
              '此条为机器人发送，所以不需要回复"好的、谢谢、知道了"等客套话。' + WARN_FWD
INTRO_FAILED = '为了保证群聊质量，请您认真做一下自我介绍。注意包含"我是"关键字。' + WARN_FWD
GOODBYE = '好的%s！我已向您发送了群聊邀请，请做确认。' \
          '%s是中国驻德使馆教育处认可的组织。协会主页http://aichina.de\n' \
          '请保持良好的社区氛围，多发原创内容增进讨论, 严禁发广告及无关内容。' \
          '如果您希望运维，投稿，赞助或合作，我们热烈欢迎！请与我私信联系，谢谢！' \
          '最后，请记得按照如下规则修改你在群中的昵称:\n' \
          '公司从业者：姓名-E-单位\n' \
          '大学研究所的教师博后：姓名-R-单位\n' \
          '在读博士生：姓名-D-单位\n' \
          '在读硕士生：姓名-M-单位\n' \
          '在读本科生：姓名-U-单位\n'
GROUP_INTRO = '请大家热烈欢迎即将加入群的%s, ta是：%s'
INTRO_KEYWORDS = ['hi', 'hello', 'hallo', '大家好', '我是', '我叫', '我']


class FriendStatus(Enum):
    UNKNOWN = 'unknown friend'
    SELF_INTRO = 'do self-intro'
    INVITE_SENT = 'send the invitation'


users = defaultdict(lambda: FriendStatus.UNKNOWN)


def check_trigger_words(msg: str) -> bool:
    for t in TRIGGER_WORDS:
        if t.lower() in msg.lower():
            return True
    return False


def check_self_intro(intro: str) -> bool:
    if len(intro) > 10:
        for wd in INTRO_KEYWORDS:
            if wd.lower() in intro.lower():
                return True
    return False


def send_group_invitation(msg) -> None:
    chatroom_id = itchat.search_chatrooms(name=GROUP_NAME)[0].UserName
    itchat.add_member_into_chatroom(chatroomUserName=chatroom_id, useInvitation=True, memberList=[msg.User])


def intro_upcomming_member(user: str, intro: str) -> None:
    chatroom_id = itchat.search_chatrooms(name=GROUP_NAME)[0].UserName
    itchat.send_msg(msg=GROUP_INTRO % (user, intro), toUserName=chatroom_id)


def is_at_me(to_usr: str) -> bool:
    return to_usr == itchat.search_friends(name=MASTER_NAME)[0].UserName


@itchat.msg_register(FRIENDS)
def add_friends(msg):
    itchat.add_friend(**msg['Text'])


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    if is_at_me(msg.ToUserName):
        if users[msg.FromUserName] == FriendStatus.UNKNOWN:
            if check_trigger_words(msg.Content):
                users[msg.FromUserName] = FriendStatus.SELF_INTRO
                itchat.send_msg(msg=FIRST_REPLY % (msg.User.NickName, GROUP_NAME), toUserName=msg.FromUserName)
        elif users[msg.FromUserName] == FriendStatus.SELF_INTRO:
            if check_self_intro(msg.Content):
                users[msg.FromUserName] = FriendStatus.INVITE_SENT
                send_group_invitation(msg)
                intro_upcomming_member(msg.User.NickName, msg.Content)
                itchat.send_msg(msg=GOODBYE % (msg.User.NickName, GROUP_NAME), toUserName=msg.FromUserName)
            else:
                itchat.send_msg(msg=INTRO_FAILED, toUserName=msg.FromUserName)
        elif users[msg.FromUserName] == FriendStatus.INVITE_SENT and check_trigger_words(msg.Content):
            # the user sent trigger words again but the invitation already sent
            send_group_invitation(msg)
            itchat.send_msg(msg=GOODBYE % (msg.User.NickName, GROUP_NAME), toUserName=msg.FromUserName)


itchat.auto_login(hotReload=True)
itchat.run()
