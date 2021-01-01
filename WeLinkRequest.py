# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： WeLinkRequest.py
# Author : v_yanqyu
# Desc: WeLink网络嘉年华
# Date： 2021/1/7 15:05
'''
import json
import os
import random
import string
from urllib.parse import urlencode

import requests
import time
class WeLink():
    def __init__(self,Authorization=None,registerCode=None):
        self.registerCode = registerCode
        self.AuthorizationUrl = "http://mps.chinasoftinc.com:9010/carnival/auth/authCode/welink"
        self.getMaterialListUrl = "http://mps.chinasoftinc.com:9010/carnival/material/getMaterialList"
        self.addLikeUrl ="http://mps.chinasoftinc.com:9010/carnival/comment/addLike"
        self.regesterUrl = "http://mps.chinasoftinc.com:9010/carnival/register"
        self.ShareUrl="http://mps.chinasoftinc.com:9010/carnival/material/materialShareLog"
        self.selectSginScoreUrl ="http://mps.chinasoftinc.com:9010/carnival/integration/selectSginScore"
        self.selectTeamInfoUrl = "http://mps.chinasoftinc.com:9010/carnival/team/selectTeamInfo"
        self.addCommentUrl = "http://mps.chinasoftinc.com:9010/carnival/comment/addComment"
        self.remarkUrl = "https://v1.hitokoto.cn/"
        self.commentListUrl = "http://mps.chinasoftinc.com:9010/carnival/comment/commentList"
        self.addMaterailFileUrl ="http://mps.chinasoftinc.com:9010/carnival/material/addMaterailFile"
        self.getLuckDrawResultUrl = "http://mps.chinasoftinc.com:9010/carnival/luckDrawRecord/getLuckDrawResult"
        self.jsonHeaders = {
            "Host": "mps.chinasoftinc.com:9010",
            "Content-Length": "77",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; SPN-AL00 Build/HUAWEISPN-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.64 Mobile Safari/537.36 HuaWei-AnyOffice/1.0.0/com.huawei.welink",
            "Origin": "http://mps.chinasoftinc.com:9000",
            "Content-Type": "application/json;charset=UTF-8;",
            "Referer": "http://mps.chinasoftinc.com:9000/jnh/",
            "Accept-Encoding": "gzip",
            "Authorization":Authorization,
            "Accept-Language": "zh-CN,zh-CN;q=0.9,en-US;q=0.8",
            "X-Requested-With": "com.huawei.welink",
            "Connection": "keep-alive"
        }
        self.formHeaders= {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; SPN-AL00 Build/HUAWEISPN-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.64 Mobile Safari/537.36 HuaWei-AnyOffice/1.0.0/com.huawei.welink",
        }

        self.materialNumber  ="eyJhc3NldF9pZCI6IjY0ZGRjMzI2NGI2OTAyZjZmYmVhZjg2YmE1Yzk4MzgyIiwiZmlsZU5hbWUiOiLkuIvovb0oMikoMSkubXA0IiwiZmlsZVJlYWxQYXRoIjoiMTAwMC8xMDE5L2I0YTQ1MTJmN2JiNzE2ZGYxNjA4MWFhNWFhMDYzYTA3Lm1wNCIsImZpbGVUeXBlIjoyLCJ1cGxvYWRUaW1lIjoxNjA5OTM1NDMwODU0LCJ1cGxvYWRVc2VySWQiOiIwMDAwMjE4NTkyIiwidXJsIjoiaHR0cHM6Ly9vYnMtbnlnLXRlc3Qub2JzLmNuLW5vcnRoLTEubXlod2Nsb3Vkcy5jb20vMTAwMC8xMDE5L2I0YTQ1MTJmN2JiNzE2ZGYxNjA4MWFhNWFhMDYzYTA3Lm1wNCJ9"

    def getauthCode(self,authCodeUrl):
        """
        :param authCodeUrl: 分享链接换取身份认证
        :return:
        """
        authJson = json.loads(requests.get(authCodeUrl,self.formHeaders).content.decode("utf-8"))
        filename = 'Authorization.txt'
        Authorization = authJson['result']['Authorization']
        with open(filename, 'w', encoding="utf-8") as file_object:
            file_object.write("%s\n" % (Authorization))
        return Authorization

    def getMaterialList(self,type):
        """
        图片/视频获取
        :param  type  1是视频 2是图片
        # 由于检查了cookies之后发现是空也无seesion及其它单点登录认证的迹象的所以推理是Authorization这个字段来效验身份)
        :return:
        """
        try:
            if type == 1:
                data = {"page": {"pageNumbers": 0, "countPerPages": 30},
                        "data": {"folderNumber": "14", "materialType": type, "keyWord": ""}}
            elif type == 2:
                data = {"page": {"pageNumbers": 2, "countPerPages": 10}, "data": {"materialType": 2}}
            responseJson = requests.post(url=self.getMaterialListUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')
            print("拉取到的条数：%s" % (len(json.loads(responseJson)['result']['data'][0])))
            return eval(responseJson)
        except Exception as  OSError:
            print(OSError)

    def addLike(self,responseJson,num):
        """
        点赞（视频或图片都支持）
        responseJson getMaterialList拉到的首页信息清洗下数据
        businessNumber 点赞地址
        businessType 类型 （貌似可以不带）
        :return:
        """
        materialNumber = responseJson['result']['data'][num]['materialNumber']
        data = {"businessNumber": materialNumber, "businessType": "video"}
        materialJson = requests.post(url=self.addLikeUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')  # 这里就不美化样式了
        shareJson = requests.post(url=self.ShareUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')
        print("结果（具体看接口返回）点赞：%s，分享：%s"%(materialJson,shareJson))

    def Regester(self):
        """
        邀请码
        :param registerCode:
        :param mobile:
        :param passWord:
        :param relationUser:
        :return:
        """
        # 随便生成意思下
        sur = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
        name = '豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖'
        nickname = random.choice(sur) +"".join(random.choice(name) for i in range(2))
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151",
                   "152","153", "155", "156", "157", "158", "159", "186", "187", "188"]
        mobile = random.choice(prelist) + "".join(random.choice(string.digits) for i in range(8))
        pwd = "".join(random.choice(string.ascii_letters) + "".join(random.choice(string.digits) for i in range(2) ) for j in  range(5))
        data ={"registerCode": "%s"%(self.registerCode),
               "nickname": nickname,
               "mobile": mobile,
               "passWord": pwd,
               "relationUser": "0000%s"%(self.registerCode)
               }
        print("随机注册信息%s"%(data))
        responseJson = requests.post(url=self.regesterUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')
        print(responseJson)

    def addLikeIt(self,materialNumber):
        """
        定向点赞
        :param materialNumber:
        :return:
        """
        if materialNumber == '':
            materialNumber = self.materialNumber
        else:
            materialNumber = materialNumber
        data = {"businessNumber": materialNumber, "businessType": "video"}
        material = requests.post(url=self.addLikeUrl, json=data, headers=self.jsonHeaders)
        LikeJson = material.content.decode('utf-8')
        print("命中定向点赞：%s"%(LikeJson))

    def addMaterailFile(self,filePath):
        """
        上传图片或视频
        :param filePath
        :return:
        """
        files = {"file": ("%s.jpg"%(filePath), open(filePath, "rb"), "image/png")}
        print("%s.jpg"%(filePath))
        materailFileJson = requests.post(url=self.addMaterailFileUrl, files=files, headers=self.imageupload).content.decode('utf-8')
        print(materailFileJson)

    def selectScore(self):
        """
        查询积分
        :return:
        """
        data = {}
        ScoreJson = requests.post(url=self.selectSginScoreUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')
        TeamScoreJson = requests.post(url=self.selectTeamInfoUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')
        print("个人积分：%s" % (ScoreJson))
        print("团队积分： % s"%(TeamScoreJson))

    def addComment(self,materialNumber=None):
        """
        :param
        添加评论
        :return:
        """
        if materialNumber =='':
            materialNumber = self.materialNumber
        else:
            materialNumber = materialNumber
        remarkJson = requests.get(self.remarkUrl)
        message = json.loads(remarkJson.text)["hitokoto"]
        print("一言API获取到的hitokoto：%s"%(message))
        data = {"businessNumber":self.materialNumber ,"businessType": "video","comContent": message}
        CommitJson = requests.post(url=self.addCommentUrl, json=data, headers=self.jsonHeaders).content.decode('utf-8')
        print("定向评论：%s"%(CommitJson))
        listData = {"page": {"pageNumbers": 1,"countPerPages": 10},"data": {"businessNumber": materialNumber}}
        messageListJson = requests.post(url=self.commentListUrl, json=listData, headers=self.jsonHeaders).content.decode('utf-8')
        messageData = json.loads(messageListJson)["result"]["data"]
        messageTotal = json.loads(messageListJson)["result"]["total"]
        print("该图文或视频一共收到了%s条评论！！！"%(messageTotal))
        for i in range(0,len(messageData)):
            print(messageData[i]['comContent'])

    def getLuckDrawResult(self):
        """
        每日抽奖
        :return:
        """
        json ={}
        drawJson = requests.post(url=self.getLuckDrawResultUrl, json=json, headers=self.jsonHeaders).content.decode('utf-8')
        lotteryIndex = eval(drawJson)["lotteryIndex"]
        relust = {0:'2021玩偶',1:'BRUNO锅',2:'谢谢参与',3:'小米电动滑板车',4:'谢谢参与',5:'华为P40'}
        print("每日转盘抽奖 drawJson：%s,%s ！！！" % (drawJson, relust[lotteryIndex]))
        return lotteryIndex

    def checkAuthor(self):
        """
        检查环境
        :return:
        """
        try:
            AuthorizationFile = "Authorization.txt"
            authCodeFile = "authCodeUrl.txt"
            if not os.path.exists(AuthorizationFile) or not os.path.exists(authCodeFile):
                print("请先手动创建%s,%s便于后期存储换取认证Token" % (authCodeFile, AuthorizationFile))
            else:
                with open(AuthorizationFile, "r") as file:
                    Authorization = file.readline().strip()
                with open(authCodeFile, "r") as file:
                    authCodeUrl = file.readline().strip()
                if Authorization != "" or authCodeFile != "":
                    return WeLink().getauthCode(authCodeUrl)
                else:
                    return Authorization
        except Exception as FileNotFoundError:
            print(FileNotFoundError)

if __name__ == '__main__':
    try:
        lottery =[]
        Authorization = WeLink().checkAuthor()
        if Authorization== None:
            print("Authorization换取认证失败！！！")
        else:
            Code = input("输入1---执行注册邀请码\n"
                         "输入2---查询积分信息 \n"
                         "输入3---每日垃圾抽奖（抽是不可能抽到的 测试9k次lotteryIndex都是4跟2）\n"
                         "输入5---随机刷赞分享\n"
                         "输入6---定向视频图片点赞\n"
                         "输入7---定向评论\n"
                         "输入8---上传图片及视频\n"
                         "请输入需要执行的脚本序列号：")
            if Code == "1":
                WeLink = WeLink(Authorization,input("请输入邀请码："))
                WeLink.Regester()
            elif Code == "2":
                WeLink(Authorization).selectScore()
            elif Code == '3':
                startlottery = int(input("请输入抽奖次数："))
                for i in range(startlottery):
                    lotteryIndex = WeLink(Authorization).getLuckDrawResult()
                    # print(lotteryIndex)
                    if lotteryIndex in (0, 1, 3, 5, 2):
                        relust = {0: '2021玩偶', 1: 'BRUNO锅', 2: '谢谢参与', 3: '小米电动滑板车', 4: '谢谢参与', 5: '华为P40'}
                        # 若中奖了或程序崩溃就记录下
                        lottery.append(relust[lotteryIndex])
                        filename = '%s-抽奖记录.txt' % (time.strftime("%Y-%m-%d"))
                        with open(filename, 'a', encoding="utf-8") as file_object:
                            file_object.write("%s\n" % (relust[lotteryIndex]))
            elif Code == '5':
                MaterList = WeLink(Authorization).getMaterialList(type=1)
                maxmum = 10
                for i in range(0, maxmum):
                    WeLink.addLike(responseJson=MaterList, num=i)
                    print("已完成%s次点赞" % (maxmum))
            elif Code == '6':
                WeLink(Authorization).addLikeIt(input("请输入定向评论的businessNumber："))
            elif Code == '7':
                WeLink(Authorization).addComment(input("请输入定向评论的businessNumber："))
            elif Code == '8':
                WeLink(Authorization).addMaterailFile(input("请输入filePath："))
            else:
                print("没有这个指令！！！")
    except Exception as IndexError:
        print("程序异常崩溃ErrorInfo：%s \n,最终抽奖结果：%s"%(IndexError,lottery))