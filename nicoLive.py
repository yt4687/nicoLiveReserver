
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

    jikkyo_id_table = {
        #'jk1': {'type': 'channel', 'id': 'ch2646436', 'name': 'NHK総合'},
        #'jk2': {'type': 'channel', 'id': 'ch2646437', 'name': 'NHKEテレ'},
        #'jk4': {'type': 'channel', 'id': 'ch2646438', 'name': '日本テレビ'},
        #'jk5': {'type': 'channel', 'id': 'ch2646439', 'name': 'テレビ朝日'},
        #'jk6': {'type': 'channel', 'id': 'ch2646440', 'name': 'TBSテレビ'},
        #'jk7': {'type': 'channel', 'id': 'ch2646441', 'name': 'テレビ東京'},
        #'jk8': {'type': 'channel', 'id': 'ch2646442', 'name': 'フジテレビ'},
        #'jk9': {'type': 'channel', 'id': 'ch2646485', 'name': 'TOKYO MX'},
        'jk10': {'type': 'community', 'id': 'co5253063', 'name': 'テレ玉', 'tag': ',{"label":"テレ玉","isLocked":true}'},
        'jk11': {'type': 'community', 'id': 'co5215296', 'name': 'tvk', 'tag': ',{"label":"ｔｖｋ","isLocked":true},{"label":"TVK","isLocked":true}'},
        'jk12': {'type': 'community', 'id': 'co5359761', 'name': '千葉テレビ', 'tag': ',{"label":"千葉テレビ","isLocked":true},{"label":"チバテレビ","isLocked":true}'},
        'jk101': {'type': 'community', 'id': 'co5214081', 'name': 'NHK BS1', 'tag': ',{"label":"NHK_BS1","isLocked":true}'},
        'jk103': {'type': 'community', 'id': 'co5175227', 'name': 'NHK BSプレミアム', 'tag':',{"label":"NHK_BSP","isLocked":true},{"label":"NHK_BSプレミアム","isLocked":true}' },
        'jk141': {'type': 'community', 'id': 'co5175341', 'name': 'BS日テレ', 'tag': ',{"label":"BS日テレ","isLocked":true}'},
        'jk151': {'type': 'community', 'id': 'co5175345', 'name': 'BS朝日', 'tag': ',{"label":"BS朝日","isLocked":true}'},
        'jk161': {'type': 'community', 'id': 'co5176119', 'name': 'BS-TBS', 'tag': ',{"label":"BS朝日","isLocked":true}'},
        'jk171': {'type': 'community', 'id': 'co5176122', 'name': 'BSテレ東', 'tag': ',{"label":"BS-TBS","isLocked":true}'},
        'jk181': {'type': 'community', 'id': 'co5176125', 'name': 'BSフジ', 'tag': ',{"label":"BSフジ","isLocked":true}'},
        'jk191': {'type': 'community', 'id': 'co5251972', 'name': 'WOWOW PRIME', 'tag': ',{"label":"WOWOW_Prime","isLocked":true},{"label":"WOWOWプライム","isLocked":true}'},
        'jk192': {'type': 'community', 'id': 'co5251976', 'name': 'WOWOW LIVE', 'tag': ',{"label":"WOWOW_Live","isLocked":true},{"label":"WOWOWライブ","isLocked":true}'},
        'jk193': {'type': 'community', 'id': 'co5251983', 'name': 'WOWOW CINEMA', 'tag': ',{"label":"WOWOW_Cinema","isLocked":true},{"label":"WOWOWシネマ","isLocked":true}'},
        #'jk211': {'type': 'channel',   'id': 'ch2646846', 'name': 'BS11'},
        'jk222': {'type': 'community', 'id': 'co5193029', 'name': 'BS12', 'tag': ',{"label":"BS12","isLocked":true},{"label":"Twellv","isLocked":true}'},
        'jk236': {'type': 'community', 'id': 'co5296297', 'name': 'BSアニマックス', 'tag': ',{"label":"BSANIMAX","isLocked":true},{"label":"BSアニマックス","isLocked":true}'},
        'jk333': {'type': 'community', 'id': 'co5245469', 'name': 'AT-X', 'tag': ',{"label":"AT-X","isLocked":true}'},
    }
    # エラーコード一覧
    Live_error_table = {
        'INVALID_PARAMETER': {'message': 'パラメーターエラー。出る場合は ini の間違いを確認し、間違いがない場合は開発者まで報告ください'},
        'INVALID_TAGS': {'message': '無効なタグ指定があります。'},
        'OVERLAP_MAINTENANCE': {'message': '番組放送時間にメンテナンス時間が重複しています'},
        'AUTHENTICATION_FAILED': {'message': 'セッションが無効です。IDとパスワードを確認してください'},
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


     
    def __init__(self, nicologin_mail, nicologin_password, set_start_time, set_end_time, set_cast_hours, jikkyo_id):

        # 取得する日付
        self.start_time = set_start_time

        # 終了する日付
        self.end_time = set_end_time

        # 放送時間の長さ
        self.hours = set_cast_hours

        #ニコニコセッション関係
        self.nicologin_mail = nicologin_mail
        self.nicologin_password = nicologin_password

        # 生放送用の設定ファイルを読み込み
        Livedata = configparser.ConfigParser()
        Livedata.read('Preset.ini', encoding='UTF-8')

        # 生放送関係
        self.Livetitle = Livedata.get('nicoLive', 'title')
        self.Livedescription = Livedata.get('nicoLive', 'description')
        self.Livecategory = Livedata.get('nicoLive', 'category')
        self.Livetags = Livedata.get('nicoLive', 'tags')
        self.LiveisTagOwnerLock = Livedata.get('nicoLive', 'isTagOwnerLock')
        self.LivecommunityId = nicoLive.jikkyo_id_table[jikkyo_id]['id']
        self.LiveisMemberOnly = Livedata.get('nicoLive', 'isMemberOnly')
        self.LiveisTimeshiftEnabled = Livedata.get('nicoLive', 'isTimeshiftEnabled')
        self.LiveisUadEnabled = Livedata.get('nicoLive', 'isUadEnabled')
        self.LiveisIchibaEnabled = Livedata.get('nicoLive', 'isIchibaEnabled')
        self.LiveisOfficialIchibaOnly = Livedata.get('nicoLive', 'isOfficialIchibaOnly')
        self.LivemaxQuality = Livedata.get('nicoLive', 'maxQuality')
        self.LiveisQuotable = Livedata.get('nicoLive', 'isQuotable')
        self.LiveisAutoCommentFilterEnabled = Livedata.get('nicoLive', 'isAutoCommentFilterEnabled')

        # テキストになってるTrue Falseをboolへ変換（もっとスマートに書きたい）
        if self.LiveisTagOwnerLock == str('true'):
            self.LiveisTagOwnerLock = True
        else:
            self.LiveisTagOwnerLock = False

        if self.LiveisMemberOnly == str('true'):
            self.LiveisMemberOnly = True
        else:
            self.LiveisMemberOnly = False
        
        if self.LiveisTimeshiftEnabled == str('true'):
            self.LiveisTimeshiftEnabled = True
        else:
            self.LiveisTimeshiftEnabled = False
        
        if self.LiveisUadEnabled == str('true'):
            self.LiveisUadEnabled = True
        else:
            self.LiveisUadEnabled = False
        
        if self.LiveisIchibaEnabled == str('true'):
            self.LiveisIchibaEnabled = True
        else:
            self.LiveisIchibaEnabled = False
        
        if self.LiveisOfficialIchibaOnly == str('true'):
            self.LiveisOfficialIchibaOnly = True
        else:
            self.LiveisOfficialIchibaOnly = False
        
        if self.LiveisQuotable == str('true'):
            self.LiveisQuotable = True
        else:
            self.LiveisQuotable = False

        if self.LiveisAutoCommentFilterEnabled == str('true'):
            self.LiveisAutoCommentFilterEnabled = True
        else:
            self.LiveisAutoCommentFilterEnabled = False

        # タイトル内のチャンネル文字を置換
        if self.Livetitle.rfind('{JKch}') != -1:
            self.Livetitle = self.Livetitle.replace('{JKch}', nicoLive.jikkyo_id_table[jikkyo_id]['name'])

        # タイトル内の日付をセット
        self.Livetitle = self.Livetitle.replace('{date}', self.start_time.strftime('%Y年%m月%d日'))
        
        # タイトル内の時間をセット
        self.Livetitle = self.Livetitle.replace('{time}', self.start_time.strftime('%H:%M～'))+self.end_time.strftime('%H:%M')

        # タグにチャンネル固有のものを追加
        self.Livetags = self.Livetags + nicoLive.jikkyo_id_table[jikkyo_id]['tag']


    def setbroadcast(self, create):

        user_session = self.__login()
        url = 'http://live2.nicovideo.jp/unama/api/v2/programs'
        
        headers = {
            'Content-Type': 'application/json',
            'X-niconico-session' : user_session,
            'Accept' : 'application/json'
        }

        # タグを投稿できる状態に処理
        Livetags = '['+self.Livetags+']'
        Livetags = json.loads(str(Livetags))

        payload = {
            "title":self.Livetitle,
            "description":self.Livedescription,
            "category":self.Livecategory,
            "tags": Livetags,
            "isTagOwnerLock": self.LiveisTagOwnerLock,
            "isMemberOnly": self.LiveisMemberOnly,
            "communityId": self.LivecommunityId,
            "reservationBeginTime": self.start_time.strftime('%Y-%m-%d')+"T"+self.start_time.strftime('%H:%M:00')+"+09:00",
            "durationMinutes": self.hours,
            "isTimeshiftEnabled": self.LiveisTimeshiftEnabled,
            "isUadEnabled": self.LiveisUadEnabled,
            "isIchibaEnabled": self.LiveisIchibaEnabled,
            "isOfficialIchibaOnly": self.LiveisOfficialIchibaOnly,
            "maxQuality": self.LivemaxQuality,
            "isQuotable": self.LiveisQuotable,
            "isAutoCommentFilterEnabled": self.LiveisAutoCommentFilterEnabled,
        }
        
        #print(payload)
        
        response = requests.post(url, json.dumps(payload), headers = headers)      
        
        return response.json()
        
    # 実況チャンネル名を取得
    @staticmethod
    def getJikkyoChannelName(jikkyo_id):
        if jikkyo_id in nicoLive.jikkyo_id_table:
            return nicoLive.jikkyo_id_table[jikkyo_id]['name']
        else:
            return '指定された'
    
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
    
    # エラーコードの説明を返す
    @staticmethod
    def getLiveerrormsg(error_code):
        if error_code in nicoLive.Live_error_table:
            return nicoLive.Live_error_table[error_code]['message']
        else:
            return None
    
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
