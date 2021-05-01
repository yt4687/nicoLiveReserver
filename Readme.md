[![](https://img.shields.io/badge/Origin-tsukumijima-28a745?style=for-the-badge)](https://github.com/tsukumijima/JKCommentCrawler)
![GitHub](https://img.shields.io/github/license/yt4687/Tomoyo-nicoLiveReserver-?style=for-the-badge)
![GitHub](https://img.shields.io/badge/Python-3.8-3376AB?style=for-the-badge&logo=Python)
![](https://img.shields.io/badge/OS-Windows-0078D6?style=for-the-badge&logo=Windows)
[![](https://img.shields.io/badge/Using-niconico-231815?style=for-the-badge&logo=niconico)](https://nicovideo.jp)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/yt4687/nicoLiveReserver?style=for-the-badge)](https://github.com/yt4687/nicoLiveReserver/releases)

# nicoLiveReserver
ニコニコ生放送の放送枠の予約をCLIから行うツールです。  


新ニコニコ実況移行後に廃止されたチャンネルの非公式実況コミュニティが手動でしている実況枠の作成を自動化できたらいいなという思いで作りました。


使う際は[https://commons.nicovideo.jp/material/nc235573](https://commons.nicovideo.jp/material/nc235573)に利用登録していただけると嬉しいです。

## 注意

- このツールの利用には基本的にニコニコのプレミアムアカウントが必要です。  
  - 生放送を行うためにはプレミアムアカウントが必須です。  
- 生放送を行う際にはニコニコ側のユーザー生放送の制限がかかります。  
  - ユーザー生放送の最大配信時間は6時間まで（これ以上の時間を指定するときは後述）
  - 同一時間に同じユーザーで複数の配信はできない。
  - そのほかユーザー生放送作成画面でできない設定はこのツールでもできないので注意してください。
- このツールはニコニコ動画のサーバと通信します。負荷をかける改造は慎むようにお願いします。  
- このツールは配信時間が６時間を超える放送時間を設定した場合、自動で分割して設定された時間分の番組を作成します。  
(例、24時間分作成するときは、ユーザー生放送は1回6時間までの制限なので、4本に分割されて作成されます)  


## インストール

[ここ](https://github.com/yt4687/nicoLiveReserver/releases)からダウンロードします。ダウンロードできたら解凍し、適当なフォルダに配置します。  

あるいは、GitHub の画面内にある緑色の［Code］ボタンをクリックすると［Download Zip］ボタンが表示されるので、ボタンをクリックしてダウンロードすることもできます。 

### 設定

nicoLiveReserver を使う前には設定が必要です。まずは nicoLiveReserver.example.ini を nicoLiveReserver.ini にコピーします。

その後、nicoLiveReserver.ini を編集します。  
編集箇所は ニコニコにログインするメールアドレス・ニコニコにログインするパスワードです。  
設定項目は間違えるとニコニコ側からエラーが返されるので注意してください。必要に応じて例があります。  

ニコニコにログインするメールアドレス / パスワードも指定します。前述の通り、基本的にプレミアムアカウントのログイン情報が必要です。  
次に自動実行するときに必要な設定項目を設定します。予約したいチャンネルに書き換えてください。  
(赤線の場所は必ず自分のものや世や牛たいチャンネルに書き換えてください、ほかはそのままで問題ないです)  
![スクリーンショット 2021-05-01 201028](https://user-images.githubusercontent.com/35659282/116780715-55cb7180-aab9-11eb-8eff-81aa89e87c7e.png)


設定項目は間違えるとニコニコ側からエラーが返されるので注意してください。必要に応じて例があります。 

これで設定は完了です。

### 実行方法

nicoLiveReserver は Python スクリプトですが、わざわざ環境をセットアップするのも少し手間かなと思ったので、単一の実行ファイルにまとめたものも同梱しています。  

Python から普通に実行する場合は、別途依存ライブラリのインストールが必要です。  
`pip install -r requirements.txt` ( pip が Python2 の事を指すシステムの場合は pip3 ) と実行し、依存ライブラリをインストールします。  
Python 3.8 で検証しています。Python 2 系は論外として、3.8 未満のバージョンでは動かないかもしれません。

## 使い方
基本の使い方は以下のようになります。  

・登録時
ダウンロードしたフォルダ内の「スケジューラ登録バッチ」をクリックして起動  
![image](https://user-images.githubusercontent.com/35659282/116780432-bce82680-aab7-11eb-8f70-75d0815d697f.png)  
起動すると実行する時間の入力する部分があるので入力して「Enter」を押下(例では18:00に設定)  
![image](https://user-images.githubusercontent.com/35659282/116780451-e43ef380-aab7-11eb-9e46-3054fe6dfff1.png)  
この画面になったら設定完了です、画面は閉じてください  
![image](https://user-images.githubusercontent.com/35659282/116780475-0fc1de00-aab8-11eb-85a7-0728dfebf341.png)  
登録が終わった後、「初期実行バッチ」を実行して準備完了です。翌日以降指定された時間に予約を自動で行います。    
![image](https://user-images.githubusercontent.com/35659282/116780942-a42d4000-aaba-11eb-9170-aa7bb9328e2c.png)  
  
  
・削除するとき  
「スケジューラ削除」をクリックして起動  
![image](https://user-images.githubusercontent.com/35659282/116780559-8363eb00-aab8-11eb-8744-e7a23b5dc0bc.png)  
この画面が出たら正常に削除が完了しています、画面を閉じて下さい  
![image](https://user-images.githubusercontent.com/35659282/116780615-c1610f00-aab8-11eb-913a-fbc64a98f955.png)

## 上級編 手動で実行する場合の項目。
配信時間は、オプションで設定し必要に合わせて組み合わせて使えます。  
予約時刻は、必ず5分単位で設定してください。エラーで予約できません。  

```
optional arguments:
  -h, --help            show this help message and exit
  -d DATE, --Date DATE  予約をする日付 (ex: 2020/12/19)
  -t TIME, --Time TIME  予約を開始する時間 (ex: 04:00)
  -ch JKCHANNEL, --jkchannel JKCHANNEL
                        予約する実況コミュニティを指定します。
  -ho HOURS, --hours HOURS
                        放送する時間（時）、チャンネル以外では最大放送時間が6時間までなので6時間以降は分割されます (ex: 24)
  -m, --minutes         放送する時間（分）配信時間を30分に設定、または30分追加するときに使います
  -a, --autset          iniに保存された設定を使って予約します
  -v, --version         バージョン情報を表示する
```
```
-ch で予約する実況チャンネルを指定できます。
-ho で1時間単位の配信時間の設定ができます。  
-m で配信時間を30分追加または設定ができます。  
（ニコニコ側の使用で30分単位しか使えないので、-m オプションで設定できる数字は30のみです。現状わざと明示的に入れるようにしています）
-ini 生放送を予約するときに使う設定ファイルを切り替えられます。必ず同じフォルダ内に入れてファイル名と拡張子のみを入力するようにしてください。(省略可)
```
具体例  
```
./nicoLiveReserver.exe 2021/01/31 04:00 -ch jk101 -ho 1 -m 30
```
`-ch jk101`には予約したい実況チャンネルが入ります。（指定可能なチャンネルは下記）
`2021/01/31` には予約したい日の日付が、04:00には配信を開始したい時間が入ります。  
`-ho 1` は配信したい時間数を入力 `-m 30` は配信時間を30分、または30分追加するときに入力します。  

jk101 に配信時間を30分にしたいときはこうなります。  
```
./nicoLiveReserver.exe -ch jk101 2021/01/31 04:00 -m 30
```
jk101 に配信時間を1時間にしたいときはこうなります。
```
./nicoLiveReserver.exe -ch jk101 2021/01/31 04:00 -ho 1
```
jk101 に配信時間を1時間30分にしたいときはこうなります。
```
./nicoLiveReserver.exe -ch jk101 2021/01/31 04:00 -ho 1 -m 30
```


指定可能なチャンネル一覧
```
        jk10: テレ玉
        jk11: tvk
	jk12: チバテレビ
        jk101: NHK BS1
        jk103: NHK BSプレミアム
        jk141: BS日テレ
        jk151: BS朝日
        jk161: BS-TBS
        jk171: BSテレ東
        jk181: BSフジ
        jk191: WOWOW PRIME
        jk192: WOWOW LIVE
        jk193: WOWOW CINEMA
        jk222: BS12
	jk236: BSアニマックス
        jk333: AT-X
```


不具合報告は [Issues](https://github.com/yt4687/nicoLiveReserver/issues) までお願いします。

## License
[MIT License](LICENSE.txt)

