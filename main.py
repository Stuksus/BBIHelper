import random
import vk_api
import requests
import traceback



def write_msg(session,user_id, message): #Write message to user
    rand=random.randint(-9223372036854775807,9223372036854775807)
    session.method('messages.send', {'peer_id': user_id,'random_id':rand ,'message': str(message)})

def Auth(token="a8539a058b11bda41c5ca39a2f4799c0a4fcceb1bef882d614b4997ee282574f0a6864bb734a17ddc4e69",scope="manage"): #Auth like group
    return vk_api.VkApi(token =token,scope=scope)

def getLongPoll(session,idGroup=186392580): #create or update LongPoll server
        return session.method("groups.getLongPollServer",{"group_id":idGroup})
def getMembersOfPoll(session,owner_id,poll_id,friends_count=99):
        return session.method("polls.getById",{"owner_id":owner_id,"poll_id":poll_id,"friends_count":friends_count})
def getMembersOfGroup(session,peer_id,group_id):
    return session.method("messages.getConversationMembers",{"peer_id":peer_id,"group_id":group_id})

def getNameById(session,userIds):
    teg=''
    data=session.method('users.get',{"user_ids":userIds})[0]
    teg+=data['first_name']+" "+data['last_name']
    return teg

while True:
    try:
        vkSession = vk_api.VkApi('+'+"79160873425","123123qq",scope="wall")
        vkSession.auth()


        vk=Auth()
        LongPoll=getLongPoll(vk)

        def sendNullMembers(sessionP,sessionG,ownerId,pollId,peerId,groupId):
            membersOfGroup=getMembersOfGroup(sessionG,peerId,groupId)
            idsGroup=[]
            for id in membersOfGroup["items"]:
                if id["member_id"]>0:
                    idsGroup.append(id["member_id"])
            print(idsGroup)
            nullVote=[]
            try:
                ids = []
                for id in getMembersOfPoll(sessionP, ownerId, pollId)["friends"]:
                    ids.append(id["id"])
                print(ids)
            except:
                nullVote=idsGroup

            if nullVote==[]:
                for i in idsGroup:
                    for j in ids:
                        if i!=j:

                            nullVote.append(i)


            print("nullVote")
            print(nullVote)
            message=''
            for i in nullVote:
                name=getNameById(vk,i)
                print(name)
                message+="[id"+str(i)+"|"+str(name)+"]"+", "
            print(message)
            res=write_msg(sessionG,peerId,message)
            print(res)
        while True:
            response =requests.get(LongPoll["server"]+"?act=a_check&key="+LongPoll['key']+"&ts="+LongPoll['ts']+"&wait=25").json()
            if response!="{'failed': 2}":
                updates = response['updates']
                print("all OK")
                if updates:
                    for element in updates:
                        print(element)
                        if element['object']['text'].find("club186392580")>=0:
                            if element['object']['fwd_messages']!=[]:
                                if element['object']['fwd_messages'][0]['attachments'][0]['type']=='poll':
                                    groupId=element['group_id']
                                    peerId=element['object']['peer_id']
                                    pollInfo=element['object']['fwd_messages'][0]['attachments'][0]['poll']
                                    ownerId=pollInfo['owner_id']
                                    pollId=pollInfo['id']
                            else:
                                if element['object']['attachments']!=[]:
                                    if element['object']['attachments'][0]['type']=='poll':
                                        groupId=element['group_id']
                                        peerId=element['object']['peer_id']
                                        print(groupId)
                                        pollInfo=element['object']['attachments'][0]['poll']
                                        ownerId=pollInfo['owner_id']
                                        pollId=pollInfo['id']
                            sendNullMembers(vkSession,vk,ownerId,pollId,peerId,groupId)
                LongPoll['ts'] = response['ts']


    except:
        vk2 = Auth()
        var = traceback.format_exc()
        write_msg(vk2,163298402,var)


