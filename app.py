from collections import defaultdict
from enum import Enum

import itchat
from itchat.content import TEXT, FRIENDS

GROUP_NAME = '中德人工智能协会'
TRIGGER_WORDS = '我要进AI群'
FIRST_REPLY = '您好%s，欢迎申请加入留德中国人工智能学会！请您先做个自我介绍，随后我会将您加入到群聊中。'
INTRO_FAILED = '为了保证群聊质量，请您认真做一下自我介绍。'
GOODBYE = '好的%s！我已把您加到群聊。请遵守群规，不要发广告及无关内容。谢谢！'


class FriendStatus(Enum):
    UNKNOWN = 'unknown friend'
    SELF_INTRO = 'do self-intro'
    INVITE_SENT = 'send the invitation'


users = defaultdict(lambda: FriendStatus.UNKNOWN)


def check_self_intro(intro: str) -> bool:
    return len(intro) > 5 and '我' in intro


def send_group_invitation(msg) -> None:
    chatroom_id = itchat.search_chatrooms(name=GROUP_NAME)[0].UserName
    itchat.add_member_into_chatroom(chatroomUserName=chatroom_id, useInvitation=True, memberList=[msg.User])


@itchat.msg_register(FRIENDS)
def add_friends(msg):
    itchat.add_friend(**msg['Text'])


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    if TRIGGER_WORDS in msg.Content:
        if users[msg.FromUserName] == FriendStatus.INVITE_SENT:
            # the user sent trigger words again but the invitation already sent
            send_group_invitation(msg)
            return GOODBYE % msg.User.NickName
        else:
            users[msg.FromUserName] = FriendStatus.SELF_INTRO
            return FIRST_REPLY % msg.User.NickName
    if users[msg.FromUserName] == FriendStatus.SELF_INTRO:
        if check_self_intro(msg.Content):
            users[msg.FromUserName] = FriendStatus.INVITE_SENT
            send_group_invitation(msg)
            return GOODBYE % msg.User.NickName
        else:
            return INTRO_FAILED


itchat.auto_login(hotReload=True)
itchat.run()
