[![](https://img.shields.io/badge/Origin-tsukumijima-28a745?style=for-the-badge)](https://github.com/tsukumijima/JKCommentCrawler)
![GitHub](https://img.shields.io/github/license/yt4687/Tomoyo-nicoLiveReserver-?style=for-the-badge)
![GitHub](https://img.shields.io/badge/Python-3.8-3376AB?style=for-the-badge&logo=Python)
![](https://img.shields.io/badge/OS-Windows-0078D6?style=for-the-badge&logo=Windows)
[![](https://img.shields.io/badge/Using-niconico-231815?style=for-the-badge&logo=niconico)](https://nicovideo.jp)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/yt4687/nicoLiveReserver?style=for-the-badge)](https://github.com/yt4687/nicoLiveReserver/releases)

# nicoLiveReserver
ニコニコ生放送の放送枠の予約をCLIから行うツールです。  

**v2から汎用化のため実況コミュニティ向けの機能を一部省略しました。設定されていた内容はプリセットという形で残してあるのでプリセットフォルダ内にある必要な設定済みチャンネル設定ファイルををnicoLiveReserver.exeのあるフォルダにコピーして使ってください。**  


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


## インストール

[ここ](https://github.com/yt4687/nicoLiveReserver/releases)からダウンロードします。ダウンロードできたら解凍し、適当なフォルダに配置します。  

あるいは、GitHub の画面内にある緑色の［Code］ボタンをクリックすると［Download Zip］ボタンが表示されるので、ボタンをクリックしてダウンロードすることもできます。 

### 設定

nicoLiveReserver を使う前には設定が必要です。まずは nicoLiveReserver.example.ini を nicoLiveReserver.ini にコピーしましょう。

その後、nicoLiveReserver.ini を編集します。  
編集箇所は ニコニコにログインするメールアドレス・ニコニコにログインするパスワードです。  
設定項目は間違えるとニコニコ側からエラーが返されるので注意してください。必要に応じて例があります。  

ニコニコにログインするメールアドレス / パスワードも指定します。前述の通り、基本的にプレミアムアカウントのログイン情報が必要です。

次に、data.example.ini を data.ini または必要に応じて好きな名前に変更します。（このファイルが標準設定になります）  
その後、nicoLiveReserver.ini を編集します。  
最低限編集が必要なのは、タイトル、説明欄、タグ、コミュニティIDです。  
コミュニティIDがないと予約が行えません。  
設定項目は間違えるとニコニコ側からエラーが返されるので注意してください。必要に応じて例があります。 

これで設定は完了です。

### 実行方法

nicoLiveReserver は Python スクリプトですが、わざわざ環境をセットアップするのも少し手間かなと思ったので、単一の実行ファイルにまとめたものも同梱しています。  
こちらのバイナリを使ったほうが手軽ですが、一方で特に Windows の場合、Python から普通に実行するときと比べ起動に数秒時間がかかるというデメリットもあります。  

Python から普通に実行する場合は、別途依存ライブラリのインストールが必要です。  
`pip install -r requirements.txt` ( pip が Python2 の事を指すシステムの場合は pip3 ) と実行し、依存ライブラリをインストールします。  
Python 3.8 で検証しています。Python 2 系は論外として、3.8 未満のバージョンでは動かないかもしれません。

## 使い方

基本の使い方は以下のようになります。  
ここでは exe 版を使っているものとして説明します。他の実行方法でも拡張子が変わったりなかったりするだけで使い方は同じです。  
このツールの設定項目は、実況チャンネル、配信日付、配信時間、配信時間になります。  

このツールは配信時間が６時間を超える放送時間を設定した場合、自動で分割して設定された時間分の番組を作成します。  
(例、24時間分作成するときは、ユーザー生放送は1回6時間までの制限なので、4本に分割されて作成されます)  
予約時刻は、必ず5分単位で設定してください。エラーで予約できません。  
ini が指定されない場合は data.ini を標準で参照します。

配信時間は、オプションで設定し必要に合わせて組み合わせて使えます。  
```
positional arguments:
  Date                  予約をする日付 (ex: 2020/12/19)
  Time                  予約を開始する時間 (ex: 04:00)

optional arguments:
  -h, --help            show this help message and exit
  -ho HOURS, --hours HOURS
                        放送する時間（時）、チャンネル以外では最大放送時間が6時間までなので6時間以降は分割されます (ex: 24)
  -m MINUTES, --minutes MINUTES
                        放送する時間（分）、配信時間を30分、または30分追加するときに使います (ex. 30)
  -ini INIFILE, --inifile INIFILE
                        読み込む設定ファイルを指定。指定されない時は data.ini を読みます (ex. NHKBS1.ini)
  -v, --version         バージョン情報を表示する
```
```
-ho で1時間単位の配信時間の設定ができます。  
-m で配信時間を30分追加または設定ができます。  
（ニコニコ側の使用で30分単位しか使えないので、-m オプションで設定できる数字は30のみです。現状わざと明示的に入れるようにしています）
-ini 生放送を予約するときに使う設定ファイルを切り替えられます。必ず同じフォルダ内に入れてファイル名と拡張子のみを入力するようにしてください。(省略可)
```
具体例  
```
./nicoLiveReserver.exe 2021/01/31 04:00 -ho 1 -m 30 -ini data2.ini
```
`2021/01/31` には予約したい日の日付が、04:00には配信を開始したい時間が入ります。  
`-ho 1` は配信したい時間数を入力 `-m 30` は配信時間を30分、または30分追加するときに入力します。  
`-ini data2.ini` には参照させる ini ファイルを入力します（省略した場合には data.ini を参照します）  


配信時間を30分にしたいときはこうなります。
```
./nicoLiveReserver.exe 2021/01/31 04:00 -m 30
```
配信時間を1時間にしたいときはこうなります。
```
./nicoLiveReserver.exe 2021/01/31 04:00 -ho 1
```
配信時間を1時間30分にしたいときはこうなります。
```
./nicoLiveReserver.exe 2021/01/31 04:00 -ho 1 -m 30
```
ini を指定する場合
data2.ini というiniファイルを指定して、配信時間を1時間にしたいときはこうなります。
```
./nicoLiveReserver.exe 2021/01/31 04:00 -ho 1 -ini data2.ini
```
data2.ini というiniファイルを指定して、配信時間を1時間30分にしたいときはこうなります。
```
./nicoLiveReserver.exe 2021/01/31 04:00 -ho 1 -m 30 -ini data2.ini
```

不具合報告は [Issues](https://github.com/yt4687/nicoLiveReserver/issues) までお願いします。

## License
[MIT License](LICENSE.txt)

