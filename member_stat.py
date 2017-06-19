import json
import re
from collections import Counter

import itchat

GROUP_NAME = '中德人工智能协会'

itchat.auto_login(hotReload=True)

itchat.run(blockThread=False)

all_members = itchat.update_chatroom(itchat.search_chatrooms(name=GROUP_NAME)[0].UserName,
                                     detailedMember=True).MemberList

city_counter = Counter(m.City for m in all_members)
sex_counter = Counter(m.Sex for m in all_members)
signature_counter = Counter(m.Signature for m in all_members)
name_counter = Counter(m.DisplayName for m in all_members)

tmp1 = []
tmp2 = []
for name in name_counter.keys():
    try:
        info = re.split('[-_+＿－]+', name)
        member_type = info[1].upper().strip()
        member_inst = info[-1].upper().strip()
        if member_type in {'M', 'R', 'E', 'D', 'U'}:
            tmp1.append(member_type)
        tmp2.append(member_inst)
    except:
        pass

type_counter = Counter(tmp1)
inst_counter = Counter(tmp2)

results = {
    'cityDist': city_counter,
    'sexDist': sex_counter,
    'signatureDist': signature_counter,
    'nameDist': name_counter,
    'typeDist': type_counter,
    'instDist': inst_counter
}

with open('group_summary.json', 'w') as f:
    f.write(json.dumps(results, ensure_ascii=False))
