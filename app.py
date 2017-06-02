import itchat
from itchat.content import TEXT, FRIENDS

FIRST_REPLY='您好%s，欢迎申请加入留德中国人工智能学会！请您先做个自我介绍，随后我会将您加入到群聊中。'
FALSE_INTRO='为了保证群聊质量，请您认真做一下自我介绍。'
GOODBYE='好的%s！我已把您加到群聊。请遵守群规，不要发广告及无关内容。谢谢！'
users = []  # type: List[str]


@itchat.msg_register(FRIENDS)
def text_reply(msg):
    users.append(msg.FromUserName)
    return FIRST_REPLY % msg.User.NickName


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    if msg.FromUserName not in users:
        users.append(msg.FromUserName)
        return FIRST_REPLY % msg.User.NickName
    elif len(msg.Content) < 5 or '我' not in msg.Content:
        return FALSE_INTRO
    else:
        chatroom_id = itchat.search_chatrooms(name='留德中国人工智能')[0].UserName
        itchat.add_member_into_chatroom(chatroomUserName=chatroom_id, useInvitation=True, memberList=[msg.User])
        return GOODBYE % msg.User.NickName


itchat.auto_login(hotReload=True, enableCmdQR=True)
itchat.run()