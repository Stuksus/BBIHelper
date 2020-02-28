import random
import vk_api
import requests
import traceback


def write_msg(session, user_id, message, ):  # Write message to user
    rand = random.randint(-9223372036854775807, 9223372036854775807)
    session.method('messages.send', {'peer_id': user_id, 'random_id': rand, 'message': str(message)})


def Auth(token="token",
         scope="manage"):  # Auth like group
    return vk_api.VkApi(token=token, scope=scope)


def getLongPoll(session, idGroup='idgroup'):  # create or update LongPoll server
    return session.method("groups.getLongPollServer", {"group_id": idGroup})


def getMembersOfPoll(session, owner_id, poll_id, friends_count=99):
    return session.method("polls.getById", {"owner_id": owner_id, "poll_id": poll_id, "friends_count": friends_count})


def getMembersOfGroup(session, peer_id, group_id):
    return session.method("messages.getConversationMembers", {"peer_id": peer_id, "group_id": group_id})


def getNameById(session, userIds):
    teg = ''
    data = session.method('users.get', {"user_ids": userIds})[0]
    teg += data['first_name'] + " " + data['last_name']
    return teg


while True:
    try:
        vkSession = vk_api.VkApi('+' + "number", "password", scope="wall")
        vkSession.auth()

        vk = Auth()
        LongPoll = getLongPoll(vk)


        def sendNullMembers(sessionP, sessionG, ownerId, pollId, peerId, groupId):
            membersOfGroup = getMembersOfGroup(sessionG, peerId, groupId)
            idsGroup = []
            for id in membersOfGroup["items"]:
                if id["member_id"] > 0:
                    idsGroup.append(id["member_id"])
            nullVote = []
            try:
                ids = []
                for id in getMembersOfPoll(sessionP, ownerId, pollId)["friends"]:
                    ids.append(id["id"])
            except:
                nullVote = idsGroup

            if nullVote == []:
                for i in ids:
                    idsGroup.remove(i)
            message = 'ВАЖНЫЙ ОПРОС!! Если вы нашли себя в этом списке, значит вы еще не голосовали! Ай яй яй \n'

            for i in idsGroup:
                name = getNameById(vk, i)
                message += "[id" + str(i) + "|" + str(name) + "]" + ", "
            res = write_msg(sessionG, peerId, message)


        while True:
            response = requests.get(LongPoll["server"] + "?act=a_check&key=" + LongPoll['key'] + "&ts=" + LongPoll[
                'ts'] + "&wait=25").json()
            if str(response).find('failed') < 0:
                updates = response['updates']
                if updates:
                    for element in updates:
                        if element['object']['text'].find("club186392580") >= 0:
                            if element['object']['fwd_messages'] != []:
                                if element['object']['fwd_messages'][0]['attachments'][0]['type'] == 'poll':
                                    groupId = element['group_id']
                                    peerId = element['object']['peer_id']
                                    pollInfo = element['object']['fwd_messages'][0]['attachments'][0]['poll']
                                    ownerId = pollInfo['owner_id']
                                    pollId = pollInfo['id']

                            else:
                                if element['object']['attachments'] != []:
                                    if element['object']['attachments'][0]['type'] == 'poll':
                                        groupId = element['group_id']
                                        peerId = element['object']['peer_id']
                                        pollInfo = element['object']['attachments'][0]['poll']
                                        ownerId = pollInfo['owner_id']
                                        pollId = pollInfo['id']
                            sendNullMembers(vkSession, vk, ownerId, pollId, peerId, groupId)
                LongPoll['ts'] = response['ts']


    except:
        vk2 = Auth()
        var = traceback.format_exc()
        write_msg(vk2, logId, var)
