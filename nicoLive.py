
from datetime import datetime, timedelta
import json
import os
import pickle
from pprint import pprint
import re
import requests
import sys
import websocket
import configparser

class nicoLive:

    # 実況 ID とチャンネル/コミュニティ ID の対照表 公式チャンネルは誤動作防止のためにコメントアウト
    jikkyo_id_table = {
        #'jk1': {'type': 'channel', 'id': 'ch2646436', 'name': 'NHK総合'},
        #'jk2': {'type': 'channel', 'id': 'ch2646437', 'name': 'NHKEテレ'},
        #'jk4': {'type': 'channel', 'id': 'ch2646438', 'name': '日本テレビ'},
        #'jk5': {'type': 'channel', 'id': 'ch2646439', 'name': 'テレビ朝日'},
        #'jk6': {'type': 'channel', 'id': 'ch2646440', 'name': 'TBSテレビ'},
        #'jk7': {'type': 'channel', 'id': 'ch2646441', 'name': 'テレビ東京'},
        #'jk8': {'type': 'channel', 'id': 'ch2646442', 'name': 'フジテレビ'},
        #'jk9': {'type': 'channel', 'id': 'ch2646485', 'name': 'TOKYO MX'},
        'jk10': {'type': 'community', 'id': 'co5253063', 'name': 'テレ玉'},
        'jk11': {'type': 'community', 'id': 'co5215296', 'name': 'tvk'},
        'jk101': {'type': 'community', 'id': 'co5214081', 'name': 'NHK BS1'},
        'jk103': {'type': 'community', 'id': 'co5175227', 'name': 'NHK BSプレミアム'},
        'jk141': {'type': 'community', 'id': 'co5175341', 'name': 'BS日テレ'},
        'jk151': {'type': 'community', 'id': 'co5175345', 'name': 'BS朝日'},
        'jk161': {'type': 'community', 'id': 'co5176119', 'name': 'BS-TBS'},
        'jk171': {'type': 'community', 'id': 'co5176122', 'name': 'BSテレ東'},
        'jk181': {'type': 'community', 'id': 'co5176125', 'name': 'BSフジ'},
        'jk191': {'type': 'community', 'id': 'co5251972', 'name': 'WOWOW PRIME'},
        'jk192': {'type': 'community', 'id': 'co5251976', 'name': 'WOWOW LIVE'},
        'jk193': {'type': 'community', 'id': 'co5251983', 'name': 'WOWOW CINEMA'},
        #'jk211': {'type': 'channel',   'id': 'ch2646846', 'name': 'BS11'},
        'jk222': {'type': 'community', 'id': 'co5193029', 'name': 'BS12'},
        'jk333': {'type': 'community', 'id': 'co5245469', 'name': 'AT-X'},
    }
    

    def __init__(self, jikkyo_id, set_caststart_time, set_cast_hours):

        # 実況 ID
        self.jikkyo_id = jikkyo_id

        # 取得する日付
        self.date_time = set_caststart_time

        # 放送時間の長さ
        self.hours = set_cast_hours

        # 設定読み込み (読み込む設定の量が多いので読み込み位置を変更した)
        config_ini = os.path.dirname(os.path.abspath(sys.argv[0])) + '/nicoLiveReserver.ini'
        config = configparser.ConfigParser()
        config.read(config_ini, encoding='UTF-8')
        config = configparser.ConfigParser()
        config.read(config_ini, encoding='UTF-8')
        
        #ニコニコセッション関係
        self.nicologin_mail = config.get('Default', 'nicologin_mail')
        self.nicologin_password = config.get('Default', 'nicologin_password')

        #生放送関係
        self.Livetitle = config.get('nicoLive', 'title')
        self.Livedescription = config.get('nicoLive', 'description')
        self.Livecategory = config.get('nicoLive', 'category')
        self.LiveoptionalCategories = config.get('nicoLive', 'optionalCategories')
        self.Livetags = config.get('nicoLive', 'tags')
        self.LiveisTagOwnerLock = config.get('nicoLive', 'isTagOwnerLock')
        self.LiveisMemberOnly = config.get('nicoLive', 'isMemberOnly')
        self.LiveisTimeshiftEnabled = config.get('nicoLive', 'isTimeshiftEnabled')
        self.LiveisUadEnabled = config.get('nicoLive', 'isUadEnabled')
        self.LiveisIchibaEnabled = config.get('nicoLive', 'isIchibaEnabled')
        self.LiveisOfficialIchibaOnly = config.get('nicoLive', 'isOfficialIchibaOnly')
        self.LivemaxQuality = config.get('nicoLive', 'maxQuality')
        self.LiveisQuotable = config.get('nicoLive', 'isQuotable')
        self.LiveisAutoCommentFilterEnabled = config.get('nicoLive', 'isAutoCommentFilterEnabled')
        
        # コミュニティIDを手動で使いたいとき用
        self.LivecommunityId = config.get('nicoLive', 'communityId')

        # タイトル内の日付文字を置換
        if self.Livetitle.rfind('date') != -1:
            self.Livetitle = self.Livetitle.replace('date', self.date_time.strftime('%Y年%m月%d日'))
        elif self.Livetitle.rfind('date2') != -1:
            self.Livetitle = self.Livetitle.replace('date2', self.date_time.strftime('%Y/%m/%d'))

    def setbroadcast(self, create):

        user_session = self.__login()
        url = 'http://live2.nicovideo.jp/unama/api/v2/programs'

        if self.jikkyo_id == 'jk2021':
            jikkyo_comm = self.LivecommunityId
        else: 
            jikkyo_comm = self.__getRealNicoJikkyoID(self.jikkyo_id)
            jikkyo_comm = jikkyo_comm['id']
        
        headers = {
            'Content-Type': 'application/json',
            'X-niconico-session' : user_session,
            'Accept' : 'application/json'
        }

        payload = {
            "title":self.Livetitle,
            "description":self.Livedescription,
            "category":self.Livecategory,
            #"tags":[self.Livetags], # 修正中
            "isTagOwnerLock": bool(self.LiveisTagOwnerLock),
            "isMemberOnly": bool(self.LiveisMemberOnly),
            "communityId": jikkyo_comm,
            "reservationBeginTime": self.date_time.strftime('%Y-%m-%d')+"T"+self.date_time.strftime('%H:%M:00')+"+09:00",
            "durationMinutes": self.hours,
            "isTimeshiftEnabled": bool(self.LiveisTimeshiftEnabled),
            "isUadEnabled": bool(self.LiveisUadEnabled),
            "isIchibaEnabled": bool(self.LiveisIchibaEnabled),
            "maxQuality": self.LivemaxQuality,
            "isQuotable": bool(self.LiveisQuotable),
            "isAutoCommentFilterEnabled": bool(self.LiveisAutoCommentFilterEnabled),
        }

        #print(payload)

        response = requests.post(url, json.dumps(payload), headers = headers)
        #print(response)
        

        return response.json()
        

    # 実況 ID リストを取得
    @staticmethod
    def getJikkyoIDList():
        return nicoLive.jikkyo_id_table.keys()


    # 実況チャンネル名を取得
    @staticmethod
    def getJikkyoChannelName(jikkyo_id):
        if jikkyo_id in nicoLive.jikkyo_id_table:
            return nicoLive.jikkyo_id_table[jikkyo_id]['name']
        else:
            return None


    # ニコニコにログインする
    def __login(self, force = False):

        cookie_dump = os.path.dirname(os.path.abspath(sys.argv[0])) + '/cookie.dump'

        # ログイン済み & 強制ログインでないなら以前取得した Cookieを再利用
        if os.path.exists(cookie_dump) and force == False:

            with open(cookie_dump, 'rb') as f:
                cookies = pickle.load(f)
                return cookies.get('user_session')

        else:

            # ログインを実行
            url = 'https://account.nicovideo.jp/api/v1/login'
            post = { 'mail': self.nicologin_mail, 'password': self.nicologin_password }
            session = requests.session()
            session.post(url, post)

            # Cookie を保存
            with open(cookie_dump, 'wb') as f:
                pickle.dump(session.cookies, f)
            
            return session.cookies.get('user_session')


    # スクリーンネームの実況 ID から、実際のニコニコチャンネル/コミュニティの ID と種別を取得する
    def __getRealNicoJikkyoID(self, jikkyo_id):
        if jikkyo_id in nicoLive.jikkyo_id_table:
            return nicoLive.jikkyo_id_table[jikkyo_id]
        else:
            return None

    # 実況チャンネル名を取得
    @staticmethod
    def getLiveerrormsg(error_code):
        if error_code in nicoLive.Live_error_table:
            return nicoLive.Live_error_table[error_code]['message']
        else:
            return None
    
    Live_error_table = {
        'INVALID_TAGS': {'message': '無効なタグ指定があります。'},
        'OVERLAP_MAINTENANCE': {'message': '番組放送時間にメンテナンス時間が重複しています'},
        'AUTHENTICATION_FAILED': {'message': 'niconicoセッションが無効です。IDとパスワードを確認してください'},
        'NO_COMMUNITY_OWNED': {'message': '指定されたコミュニティでの放送権がありません'},
        'COMMUNITY_NOT_FOUND': {'message': '指定されたコミュニティが存在しません'},
        'PENALIZED_COMMUNITY': {'message': '放送ペナルティを受けたコミュニティでは放送できません'},
        'OVERLAP_COMMUNITY': {'message': '同一コミュニティで他に重複した別ユーザの放送の予定があります'},
        'NOT_PREMIUM_USER': {'message': 'プレミアムユーザではありません'},
        'PENALIZED_USER': {'message': '配信ペナルティを受けています'},
        'OVERLAP_PROGRAM_PROVIDER': {'message': '該当時間に別の同ユーザの放送予定があります'},
        'NO_PERMISSION': {'message': '許可のない操作をしようとした'},
        'UNDER_MANTENANCE': {'message': 'メンテナンス中です'},
        'SERVICE_ERROR': {'message': '一時的なサーバ不調によりリクエストに失敗しました(リトライすると直る可能性もありますし、障害の可能性もあります)'},
    }

# 例外定義
class ResponseError(Exception):
    pass
class FormatError(Exception):
    pass
class LoginError(Exception):
    pass
class SessionError(Exception):
    pass
class JikkyoIDError(Exception):
    pass
class LiveIDError(Exception):
    pass
