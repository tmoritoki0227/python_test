# DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.  
#from distutils.version import LooseVersion, StrictVersion
# from packaging.version import LooseVersion, StrictVersion
import json
import requests 
from requests.auth import HTTPBasicAuth
from distutils.version import StrictVersion
   
print ("aaa")
a = 0
print(a)
# https://orebibou.com/ja/home/201703/20170330_001/
# https://jitaku.work/it/language/python/python-version-comparison/
#print(StrictVersion('11.0') > StrictVersion('10.4.2'))

# *.1.0
# 1.*.0
# 1.*.*
import re

# rを付けることを推奨。
# バックスラッシュをそのままで分かりやすいため。
content = '*.1.1' 
pattern = '([0-9]+|\*{1})\.[0-9]\.[0-9]'

result = re.match(pattern, content)

if result:
  print ("match")

else:
  print ("not match")

stringValue = '1.45.*'
# stringValue = '12.45.89'
# https://qiita.com/luohao0404/items/7135b2b96f9b0b196bf3
pattern = re.compile(r'(?P<major>[0-9]+|\*).(?P<minor>[0-9]+|\*).(?P<micro>[0-9]+|\*)')
# ansible-galaxy collection install cisco.ios:1.0.0 -f
# https://docs.ansible.com/ansible/2.9_ja/galaxy/user_guide.html#id16
# https://docs.ansible.com/ansible/2.9_ja/galaxy/user_guide.html#id8
# https://y0m0r.hateblo.jp/entry/20140918/1411053589
match = pattern.search(stringValue)

if match:
    print('major:' + match.group('major').strip());
    print('minor:' + match.group('minor').strip());
    print('micro:' + match.group('micro').strip());
else:
    print('みつかりませんでした')

url = 'https://moritoki.jfrog.io/artifactory/api/storage/xraysample-local/release/'
# ユーザー名を指定
username = 'tmoritoki0227@gmail.com'
# パスワードを指定
password = 'cmVmdGtuOjAxOjE3MTM5NjM4ODI6SG5RV3ZGMXdjeXhieklLc1loNDdsNHdMeTF2'

# GET送信のケース
response = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password),timeout=3)
res_json = json.loads(response.text)
print (res_json)
version = res_json['children']


print (version)
print (version[0])
ver: list = []
for item in version:
     print(item['uri'])
     ver.append(item['uri'].replace('/', ''))

print (ver)
ver.sort(key=StrictVersion)
print (ver)
# print sorted(ver, key=StrictVersion)

aaa= ['1.0', '1.0.1', '1.0.2', '1.1', '1.1.1', '1.1.2', '11.0.0', '2.0.0']
print (aaa)
aaa.sort(key=StrictVersion)
print (aaa)

# aaa= '1.0.1'
ver2: list = []
for a in aaa:
  match = re.match(r'1\.[0-9]+\.[0-9]+', a)

  if match:
      # print ("match")
      # print (match.group())
      ver2.append(match.group())
  # else:
      # print('みつかりませんでした')

print (ver2)
print ("ver2=" + str(ver2))

print("-------------------------------------------------------------------------------")
import os # 環境変数取得に必要
# print(os.environ) # 環境変数全部表示

# 環境変数取得
sd_collection: str = os.getenv('SD_COLLECTION')
# SD_COLLECTION="/aaa/release/1.0.0 , /bbb/release/1.*.0, /ccc/release/1.0.*, /ddd/release/1.*.*, /aaa/test/3.0.0"
# export SD_COLLECTION="/aaa/release/1.0.0 , /bbb/release/1.*.0, /ccc/release/1.0.*, /ddd/release/1.*.*, /aaa/test/3.0.0"

# collectionをカンマで区切って配列に格納。splitは分割メソッド。stripは前後の空白削除
collections: list = sd_collection.split(',')
print("collections = " + str(collections))

# for でcollectionを１つずつ処理していく
for collection in collections:
  print ("------------------------loopスタート-------------------------")
  collection_parts = collection.strip().split('/') # 空白除去して/で分割
  print ("collection_parts = " + str(collection_parts))

  # name 取得
  name = collection_parts[1]
  print ("name = " + str(name))
  
  # version取得
  user_specified_version = str(collection_parts[3]) # 1.0.0が欲しい。a[3]に入っている
  print ("user_specified_version = " + str(user_specified_version) )
  
  # バージョン一覧取得.api実行
  response = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))
  print(response.status_code)
  # Response オブジェクトの raise_for_status メソッドをコールすることで 400-599 の時に HTTPError を raise します。
  response.raise_for_status()

  # リトライ１
  # https://gammasoft.jp/support/solutions-of-requests-get-failed/
  # リトライ２
  # https://qiita.com/azumagoro/items/3402facf0bcfecea0f06

# メソッドなので先頭あたりにもっていく
# わかりずらいが１＋３回やってる　1回＋0<3 1<3 2<3 の３回
# def get_retry(url, retry_times, errs):
#     for t in range(retry_times + 1):  # 0 1 2 3
#         r = requests.get(url,timeout=3) # 
#         if t < retry_times: # 
#             if r.status_code in errs:
#                 time.sleep(2)
#                 continue # 失敗したらfor繰り返し
#         return r
# try:
  # res = get_retry("https://httpbin.org/status/503", 3, [500, 502, 503])
  # print(res.status_code)
  # response.raise_for_status() # Response オブジェクトの raise_for_status メソッドをコールすることで 400-599 の時に HTTPError を raise します。
# except requests.exceptions.RequestException as e:
  # print("Artifactoryのapi実行に失敗しました : ",e)
# HTTP 500 Internal Server Error
# HTTP 503 Service Unavailable
# HTTP 502 Bad Gateway


  # res_json = json.loads(response.text)
  # print (res_json)
  # キーchildrenの値を取得
  children_info = res_json['children']
  print ("children_info = " + str(children_info) )

  # キーuriの値を取得
  available_version: list = []
  for c in children_info:
      # print(c['uri'])
      available_version.append(c['uri'].replace('/', ''))

  print ("available_version前 = " + str(available_version))
  available_version.sort(key=StrictVersion) # 並び替えだが、最初から昇順ぽく並んでいるので変化が見られない
  print ("available_version後 = " + str(available_version))

  # 最新バージョン取得
  # どうすればいよいか？１番後ろの要素が１番新しい
  # 1.0.0 → releaseでそのまま1.0.0取得
  # 1.4.0 → releaseで1.4.0なので、存在しないのでエラー
  # 1.*.0 → releaseで1.4.0なので、存在しないのでエラー
  # 1.0.* → releaseで1.0.2取得
  # 1.*.* → releaseで1.2.2取得 
  # 3.0.0 → testでそのまま3.0.0取得  
  # 
  # *が含まれる場合
  # *が含まれない場合
  ## バージョン取得処理なし
  #　match = re.match(r'[0-9]\.[0-9]+\.[0-9]+', a) # rって何？raw 文字列を使用すると \ を 1 つの文字として扱います
  # \エスケープ文字 これが無効になる？　ドットは正規表現で何かにマッチする一文字・通常はただのドット。
  # 今回はただのドットして扱いたいのエスケープしているはず
  # rおかしくない？
  
  #user_specified_version = '1.0.0'
  #user_specified_version = '1.0.*'
  #user_specified_version = '1.*.1'
  #user_specified_version = '1.*.*'
  # rおかしくない？


  # どこに＊があるか判定するif処理
  if re.match(r'[0-9]+\.[0-9]+\.[0-9]+', user_specified_version): # 全部数字でマッチングしたら
    print ("ALL数字でマッチンぐしたよ")
    print ("user_specified_version = " + str(user_specified_version) )
    install_version = user_specified_version

  # pattern = re.compile(r'(?P<major>[0-9]+|\*).(?P<minor>[0-9]+|\*).(?P<micro>[0-9]+|\*)')
  elif re.match(r'[0-9]+\.[0-9]+\.\*', user_specified_version): # '1.0.*'
  # elif re.match(r'(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.\*', user_specified_version): # '1.0.*'
    print ("最後に＊ありでマッチンぐしたよ")
    print ("user_specified_version = " + str(user_specified_version) )
    #  ['1.0.0', '1.0.1', '1.0.2', '1.1.0', '1.1.1', '1.2.1', '1.2.2', '2.0.0', '2.0.10'] の中から
    #  ['1.0.0', '1.0.1', '1.0.2'] を抽出し'1.0.2'となる必要がある。
    # if re.match(r'[0-9]+\.[0-9]+\.[0-9]+', user_specified_version):
    
    # 左と中が数字、右は何でもOKのものを抽出したい
    print ("available_version = " + str(available_version))
    #match_version = [v for v in available_version if re.match(r'[0-9]+\.[0-9]+\.\*', v)]

    # ★ここが問題、ここの正規表現をどうやってつくる？
    # user_specified_versionをドットで分割するか？
    user_specified_version_parts = user_specified_version.split('.') # ドットで分割して前２つの数字を取得
    print("user_specified_version_parts = " + str(user_specified_version_parts))
    # マッチチングした文字をとれるはず
    # match_version = [v for v in available_version if re.match(r'1\.0\.[0-9]+', v)]
    # match_version = [v for v in available_version if re.match(r"user_specified_version_parts[0]\.user_specified_version_parts[1]\.[0-9]+", v)]
    # ptn = user_specified_version_parts[0] + r'\.' +user_specified_version_parts[1] + r'\.[0-9]+'
    match_version = [v for v in available_version if re.match(user_specified_version_parts[0] + r'\.' + user_specified_version_parts[1] + r'\.[0-9]+', v)]
    # match_version = [v for v in available_version if re.match(ptn, v)]
    #match_version = [v for v in available_version if re.match(r'1\.0\.[0-9]+', v)]
    # match_version: list = []
    # for ver in available_version:
    #   print (ver)
    #   if re.match(r'1+\.0+\.[0-9]+', ver):
    #     match_version.append("a")
    print("match_version = " + str(match_version))
    match_version.sort(key=StrictVersion) # match_versionの中身がソートされて保存もされる
    print("match_version_sorted = " + str(match_version))
    #match_version_sort = match_version.sort(key=StrictVersion) 
    #print("match_version_sort = " + str(match_version_sort))

    install_version = match_version[-1] # 配列最後を取得。１番大きいもの
    print("install_version = " + str(install_version))



  elif re.match(r'[0-9]+\.\*.[0-9]+', user_specified_version): # '1.*.1'
    print ("真ん中に＊ありでマッチンぐしたよ")
    print ("user_specified_version = " + str(user_specified_version) )
    #  ['1.0.0', '1.0.1', '1.0.2', '1.1.0', '1.1.1', '1.2.1', '1.2.2', '2.0.0', '2.0.10'] の中から
    #  ['1.0.1', '1.1.1', '1.2.1'] を抽出し'1.2.1'となる必要がある。

    # 左と右が数字、中は何でもOKのものを抽出したい
    print ("available_version = " + str(available_version))

    user_specified_version_parts = user_specified_version.split('.') # ドットで分割して前と後ろの２つの数字を取得
    print("user_specified_version_parts = " + str(user_specified_version_parts))
    print ("pattern => " + user_specified_version_parts[0] + r'\.[0-9]+' + user_specified_version_parts[2])
    match_version = [v for v in available_version if re.match(user_specified_version_parts[0] + r'\.[0-9]+\.' + user_specified_version_parts[2], v)]

    print("match_version = " + str(match_version))
    match_version.sort(key=StrictVersion) # match_versionの中身がソートされて保存もされる
    print("match_version_sorted = " + str(match_version))

    install_version = match_version[-1] # 配列最後を取得。１番大きいもの
    print("install_version = " + str(install_version))

  elif re.match(r'[0-9]+\.\*\.\*', user_specified_version): # '1.*.*'
    print ("真ん中、最後に＊ありでマッチンぐしたよ")
    print ("user_specified_version = " + str(user_specified_version) )

    #  ['1.0.0', '1.0.1', '1.0.2', '1.1.0', '1.1.1', '1.2.1', '1.2.2', '2.0.0', '2.0.10'] の中から
    #  ['1.0.0', '1.0.1', '1.0.2', '1.1.0', '1.1.1', '1.2.1', '1.2.2'] を抽出し'1.2.2'となる必要がある。

    # 左が数字、中、右は何でもOKのものを抽出したい
    print ("available_version = " + str(available_version))

    user_specified_version_parts = user_specified_version.split('.') # ドットで分割して前と後ろの２つの数字を取得
    print("user_specified_version_parts = " + str(user_specified_version_parts))
    match_version = [v for v in available_version if re.match(user_specified_version_parts[0] + r'\.[0-9]+' + r'\.[0-9]+', v)]

    print("match_version = " + str(match_version))
    match_version.sort(key=StrictVersion) # match_versionの中身がソートされて保存もされる
    print("match_version_sorted = " + str(match_version))

    install_version = match_version[-1] # 配列最後を取得。１番大きいもの
    print("install_version = " + str(install_version))


  else:
    print ("バージョンの指定が不正です" + str(user_specified_version) )
  # ＊以外の場合はエラーをはく
  # ansible-gallaxyコマンド生成
  
  ansible_gallaxy_command = "ansible-gallaxy install " + str(name) + "-" + str(install_version) + ".tar.gz"
  print ("ansible_gallaxy_command = " + str(ansible_gallaxy_command))
  # 生成したコマンド実行

# 次の配列の処理へ

# 考慮
## 例外処理
## 成功失敗判定

print ("end")
## 失敗時のログ出力
## sdコマンド作成



user_specified_version = '1.0.0'
user_specified_version = '1.0.*'
user_specified_version = '1.*.1'
user_specified_version = '1.*.*'

# pattern = re.compile(r'(?P<major>[0-9]+|\*).(?P<minor>[0-9]+|\*).(?P<micro>[0-9]+|\*)')
match = re.match(r'(?P<major>.+)\.(?P<minor>.+)\.(?P<micro>.+)', user_specified_version)
if match:
    print('major:' + match.group('major').strip());
    print('minor:' + match.group('minor').strip());
    print('micro:' + match.group('micro').strip());
else:
    print('みつかりませんでした')


majaor_version = match.group('major').strip()
minor_version = match.group('minor').strip()
micro_version = match.group('micro').strip()

print('majaor_version = ' + majaor_version)
print('minor_version = ' + minor_version)
print('micro_version = ' + micro_version)

if re.match(r'[0-9]+', majaor_version) and re.match(r'[0-9]+', minor_version) and re.match(r'[0-9]+', micro_version):
  print ("ALL数字でマッチンぐしたよ")
  # print ("user_specified_version = " + str(user_specified_version) )

elif re.match(r'[0-9]+', majaor_version) and re.match(r'[0-9]+', minor_version) and re.match(r'\*', micro_version):
# elif re.match(r'[0-9]+\.[0-9]+\.\*', user_specified_version): # '1.0.*'
# # elif re.match(r'(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.\*', user_specified_version): # '1.0.*'
  print ("最後に＊ありでマッチンぐしたよ")
#   #print ("user_specified_version = " + str(user_specified_version) )

elif re.match(r'[0-9]+', majaor_version) and re.match(r'\*', minor_version) and re.match(r'[0-9]+', micro_version):
  print ("真ん中に＊ありでマッチンぐしたよ")

elif re.match(r'[0-9]+', majaor_version) and re.match(r'\*', minor_version) and re.match(r'\*', micro_version):
  print ("真ん中、最後に＊ありでマッチンぐしたよ")

else:
  print ("バージョンの指定が不正です" + str(user_specified_version) )