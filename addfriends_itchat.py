from collections import defaultdict
from enum import Enum

import itchat
from itchat.content import TEXT, FRIENDS

GROUP_NAME = '中德人工智能协会'
TRIGGER_WORDS = ['我要进AI群', '我想进AI群', '拉进AI群']
WARN_FWD = '注意，你的自我介绍将发送给其他群成员。'
AFTER_ADD = '若要申请进群请回复 我想进AI群'
FIRST_REPLY = '您好%s，欢迎申请加入%s！请您先做个自我介绍，随后我会将您加入到群聊中。' + WARN_FWD
INTRO_FAILED = '为了保证群聊质量，请您认真做一下自我介绍。' + WARN_FWD
GOODBYE = '好的%s！我已向您发送了群聊邀请，请做确认。' \
          '%s是中国驻德使馆教育处认可的组织。' \
          '请保持良好的社区氛围，多发原创内容增进讨论, 严禁发广告及无关内容。' \
          '如果您希望运维，投稿，赞助或合作，我们热烈欢迎！请与我私信联系，谢谢！' \
          '最后，请牢记我们的域名 aichina.de 祝您在群里结识更多的朋友！'
GROUP_INTRO = '请大家热烈欢迎即将加入群的%s, ta是：%s'


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
    if len(intro) < 20:
        return False
    keywds = ['hi', 'hello', 'hallo', '大家好',
              '我是', '我叫', '我']
    for wd in keywds:
        if wd.lower() in intro:
            return True
    return False


def send_group_invitation(msg) -> None:
    chatroom_id = itchat.search_chatrooms(name=GROUP_NAME)[0].UserName
    itchat.add_member_into_chatroom(chatroomUserName=chatroom_id, useInvitation=True, memberList=[msg.User])


def intro_upcomming_member(user: str, intro: str) -> None:
    chatroom_id = itchat.search_chatrooms(name=GROUP_NAME)[0].UserName
    itchat.send_msg(msg=GROUP_INTRO % (user, intro), toUserName=chatroom_id)


@itchat.msg_register(FRIENDS)
def add_friends(msg):
    itchat.add_friend(**msg['Text'])


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    if check_trigger_words(msg.Content):
        if users[msg.FromUserName] == FriendStatus.INVITE_SENT:
            # the user sent trigger words again but the invitation already sent
            send_group_invitation(msg)
            itchat.send_msg(msg=GOODBYE % (msg.User.NickName, GROUP_NAME), toUserName=msg.FromUserName)
        else:
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


itchat.auto_login(enableCmdQR=2)
itchat.run()
