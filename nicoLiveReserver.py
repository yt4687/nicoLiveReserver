#!/usr/bin/python3

import argparse
import configparser
import dateutil.parser
import json
import os
from pprint import pprint
import shutil
import sys
import datetime as dt
import configparser
import time as timeim

import nicoLive

# バージョン情報
__version__ = '3.0.0'

def main():

    # 引数解析
    parser = argparse.ArgumentParser(description = 'ニコニコ生放送の枠をCLIベースで取得するツール', formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument('-d','--Date', help = '予約をする日付 (ex: 2020/12/19)')
    parser.add_argument('-t','--Time', help = '予約を開始する時間 (ex: 04:00)')
    parser.add_argument('-ch','--jkchannel', help = '予約する実況コミュニティを指定します。')
    parser.add_argument('-ho','--hours', help = '放送する時間（時）、チャンネル以外では最大放送時間が6時間までなので6時間以降は分割されます (ex: 24)')
    parser.add_argument('-m','--minutes', action='store_true', help = '放送する時間（分）配信時間を30分に設定、または30分追加するときに使います')
    parser.add_argument('-a','--autset', action='store_true', help = 'iniに指定された項目を使って予約を行います')
    parser.add_argument('-v', '--version', action='version', help = 'バージョン情報を表示する', version='nicoLiveReserver version ' + __version__)
    args = parser.parse_args()

    if args.autset == False:
        # 引数
        jikkyo_id = args.jkchannel
        date_time = dateutil.parser.parse(args.Date.rstrip() +' ' + args.Time.rstrip()) #日付と時刻を連結する
        hours = args.hours
        minutes = args.minutes

        # 予約可能期間外かチェック
        now = dt.datetime.now()
        up_time = now + dt.timedelta(days = 8)

        if date_time > up_time :
            raise Exception(f"{date_time.strftime('%Y/%m/%d')}は予約可能時間外のため予約できません。予約可能な期間は予約日から1週間です")
        if date_time <now :
            raise Exception(f"{date_time.strftime('%Y/%m/%d')}はすでに過ぎた日付です。予約可能な期間は予約日から1週間です")
    
        if hours == None and minutes == None:
            raise Exception("放送時間が指定されていません")

    # 設定ファイルの存在を確認
    config_ini = os.path.dirname(os.path.abspath(sys.argv[0])) + '/nicoLiveReserver.ini'
    if not os.path.exists(config_ini):
        raise Exception('nicoLiveReserver.ini が存在しません。nicoLiveReserver.example.ini からコピーし、\n適宜設定を変更して nicoLiveReserver と同じ場所に配置してください。')

    # 設定読み込み (読み込む設定の量が多いので読み込み位置を変更した)
    config_ini = os.path.dirname(os.path.abspath(sys.argv[0])) + '/nicoLiveReserver.ini'
    config = configparser.ConfigParser()
    config.read(config_ini, encoding='UTF-8')

    #ニコニコセッション関係
    nicologin_mail = config.get('Default', 'nicologin_mail')
    nicologin_password = config.get('Default', 'nicologin_password')

    # autosettingが適用された
    if args.autset == True:
        datec = config.get('AutoSetting', 'datec')
        jikkyo_id = config.get('AutoSetting', 'jkch')
        time = config.get('AutoSetting', 'time')
        days = config.get('AutoSetting', 'Reservedays')
        now = dt.date.today() + dt.timedelta(days = int(datec))
        date_time =  dt.datetime.strptime((now.strftime('%Y/%m/%d') + ' ' + time), '%Y/%m/%d %H:%M')
        hours = int(days)*24
        minutes = False
    
    def post(set_caststart_time, set_end_time, set_cast_hours):

        # インスタンスを作成
        jkcomment = nicoLive.nicoLive(nicologin_mail, nicologin_password, set_start_time, set_end_time, set_cast_hours, jikkyo_id)
        print(f"{set_caststart_time.strftime('%Y/%m/%d %H:%M')} に {nicoLive.nicoLive.getJikkyoChannelName(jikkyo_id)} コミュニティの放送予定を作成します")
        
        try:
            result = jkcomment.setbroadcast('create')
        except (nicoLive.ResponseError, nicoLive.SessionError) as ex:
            print(f"エラー: {ex.args[0]}")
            print('=' * shutil.get_terminal_size().columns)
            return

        if result['meta']['status'] == 201:
            print(f"生放送の予約に成功しました。生放送idは{result['data']['id']}です")
            print(f"URL [https://live2.nicovideo.jp/watch/{result['data']['id']}]")
        else:
            error_code = result['meta']['errorCode']
            e_message = jkcomment.getLiveerrormsg(error_code)
            print(f"生放送の予約に失敗しました。status：{result['meta']['status']} [errorCode：{result['meta']['errorCode']}]")
            print('失敗理由：' + e_message)

    # 枠取りをするときに使う変数
    set_program_count = 0 # 初期値（この値には6時間分の番組のカウントを入れる）
    set_program_count_hasu = 0 # 初期値（6時間までの番組を入れる）

    # チャンネル以外では一度に取れるのが6時間までなので、6時間ごとに分割
    if int(hours) > 5:
       answer = divmod(int(hours), 6)
       set_program_count = answer[0]
       set_program_count_hasu = answer[1] *60 # 分単位に変換
       if minutes == True: # 30分が指定されていた場合
           set_program_count_hasu += 30
    else:
       set_program_count_hasu = int(hours) * 60 # 分単位に変換する
       if minutes == True: # 30分が指定されていた場合
           set_program_count_hasu += 30

    finish_count = 0
    set_start_time = date_time

    while finish_count < set_program_count:
        set_cast_hours =  360 # 放送予定時間を6時間にセット
        set_end_time = set_start_time + dt.timedelta(hours = 6) # 次の放送開始時間をセット
        post(set_start_time, set_end_time, set_cast_hours)

        set_start_time = set_end_time # 次の放送開始時間をセット
        finish_count += 1
        timeim.sleep(0.3)

    if set_program_count_hasu > 0:
        set_cast_hours =  set_program_count_hasu # 放送予定時間をセット
        set_end_time = set_start_time + dt.timedelta(minutes = set_cast_hours) # 次の放送開始時間をセット
        post(set_start_time, set_end_time, set_cast_hours)

if __name__ == '__main__':
    main()
