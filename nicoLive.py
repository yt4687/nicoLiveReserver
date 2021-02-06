
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
  
    def __init__(self, set_caststart_time, set_cast_hours, data_ini_file):

        # 取得する日付
        self.date_time = set_caststart_time

        # 放送時間の長さ
        self.hours = set_cast_hours

        # 設定読み込み (読み込む設定の量が多いので読み込み位置を変更した)
        config_ini = os.path.dirname(os.path.abspath(sys.argv[0])) + '/nicoLiveReserver.ini'
        config = configparser.ConfigParser()
        config.read(config_ini, encoding='UTF-8')
        #print('config_ini['+config_ini)

        # 生放送用の設定ファイルを読み込み
        Livedata = configparser.ConfigParser()
        Livedata.read(data_ini_file, encoding='UTF-8')
        
        #ニコニコセッション関係
        self.nicologin_mail = config.get('Default', 'nicologin_mail')
        self.nicologin_password = config.get('Default', 'nicologin_password')

        # 生放送関係
        self.Livetitle = Livedata.get('nicoLive', 'title')
        self.Livedescription = Livedata.get('nicoLive', 'description')
        self.Livecategory = Livedata.get('nicoLive', 'category')
        self.LiveoptionalCategories = Livedata.get('nicoLive', 'optionalCategories')
        self.Livetags = Livedata.get('nicoLive', 'tags')
        self.LiveisTagOwnerLock = Livedata.get('nicoLive', 'isTagOwnerLock')
        self.LivecommunityId = Livedata.get('nicoLive', 'communityId')
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
        
        # コミュニティIDを手動でセットしたいとき用
        

        # タイトル内の日付文字を置換
        if self.Livetitle.rfind('{date}') != -1:
            self.Livetitle = self.Livetitle.replace('{date}', self.date_time.strftime('%Y年%m月%d日'))
        elif self.Livetitle.rfind('{date2}') != -1:
            self.Livetitle = self.Livetitle.replace('{date2}', self.date_time.strftime('%Y/%m/%d'))
        
        # タイトル内の時間文字を置換
        if self.Livetitle.rfind('{time}') != -1:
            self.Livetitle = self.Livetitle.replace('{time}', self.date_time.strftime('%H:%M～'))


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
            "reservationBeginTime": self.date_time.strftime('%Y-%m-%d')+"T"+self.date_time.strftime('%H:%M:00')+"+09:00",
            "durationMinutes": self.hours,
            "isTimeshiftEnabled": self.LiveisTimeshiftEnabled,
            "isUadEnabled": self.LiveisUadEnabled,
            "isIchibaEnabled": self.LiveisIchibaEnabled,
            "isOfficialIchibaOnly": self.LiveisOfficialIchibaOnly,
            "maxQuality": self.LivemaxQuality,
            "isQuotable": self.LiveisQuotable,
            "isAutoCommentFilterEnabled": self.LiveisAutoCommentFilterEnabled,
        }

        # サブカテゴリがある時は追加する
        if self.LiveoptionalCategories == ('凸待ち' or '顔出し' or 'クルーズ待ち' or '生ゲームで遊ぶ'):
            payload["optionalCategories"] = self.LiveoptionalCategories
        
        #print(payload)
        
        response = requests.post(url, json.dumps(payload), headers = headers)      
        
        return response.json()
        

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
    
    Live_error_table = {
        'INVALID_PARAMETER': {'message': 'パラメーターエラー。出る場合は ini の間違いを確認し、間違いがない場合は開発者まで報告ください'},
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
