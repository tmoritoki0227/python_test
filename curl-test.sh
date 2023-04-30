#!/bin/bash

# ユーザ指定のバージョンをparseする
user_specified_version="1.0.0"
user_specified_version="1.0.*"
user_specified_version="1.*.*"
user_specified_version="1.*.0"
# https://qiita.com/rockhopper/items/bee538ab4c6aabcd6b0f
# BASH_REMATCHは決まった名前
# if [[ ${user_specified_version} =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
if [[ ${user_specified_version} =~ ^(.+)\.(.+)\.(.+)$ ]]; then
#   echo "ALL数字でマッチンぐしたよ"
  all=${BASH_REMATCH[0]}
  major=${BASH_REMATCH[1]}
  minor=${BASH_REMATCH[2]}
  micro=${BASH_REMATCH[3]} # patchが正しい説

  echo "all=${all}"    # 4.10.1
  echo "major=${major}"  # 4
  echo "minor=${minor}"  # 10
  echo "micro=${micro}"  # 1
fi



# HTTPリクエスト
# curl -s -u tmoritoki0227@gmail.com:cmVmdGtuOjAxOjE3MTM5NjM4ODI6SG5RV3ZGMXdjeXhieklLc1loNDdsNHdMeTF2 -X GET  "https://moritoki.jfrog.io/artifactory/api/storage/xraysample-local/release/"|jq -r '.children[].uri'
url='https://moritoki.jfrog.io/artifactory/api/storage/xraysample-local/release/'
username='tmoritoki0227@gmail.com'
password='cmVmdGtuOjAxOjE3MTM5NjM4ODI6SG5RV3ZGMXdjeXhieklLc1loNDdsNHdMeTF2'

res=$(curl -s -u ${username}:${password} -X GET ${url} -w '\n%{http_code}') # ２行のレスポンスで、１行目がbody、２行目がレスポンスコードになる
# |jq -r '.children[].uri
body=$(echo "$res" | sed '$d') # 最終行削除。１行目取得ではだめなのか？
httpstatus=$(echo "$res" | tail -n 1) # 末尾１行目取得
# echo $body
# echo "body = $body"
# echo $body|jq -r '.children[].uri'
# /1.0.0
# /1.0.1
# /1.0.2
# /1.1.0
# /1.1.1
# /1.2.1
# /1.2.2
# /2.0.0
# /2.0.10
# /3.0.0


aa=$(echo $body|jq -r '.children[].uri') # jqが必要
# echo $aa # ここは文字列。スペース区切り
# /1.0.0 /1.0.1 /1.0.2 /1.1.0 /1.1.1 /1.2.1 /1.2.2 /2.0.0 /2.0.10 /3.0.0
available_version_tmp=($aa) # 文字列から配列へ
echo "available_version_tmp = ${available_version_tmp[@]}"

available_version=()
# 先頭のスラッシュ除去
for v in ${available_version_tmp[@]}; do
    available_version+=(${v//\//}) #  (${SD_COLLECTION//,/ }) # ${変数名//置換前文字列/置換後文字列}
done
echo "available_version = ${available_version[@]}"

echo "httpstatus = $httpstatus"

if [ $httpstatus = 200 ]; then
    # httpリクエストが成功した場合
    match_version=()
    if [[ ${major} =~ ^[0-9]+$ ]] && [[ ${minor} =~ ^[0-9]+$ ]] && [[ ${micro} =~ ^[0-9]+$ ]]; then
        echo "ALL数字でマッチンぐしたよ"
        install_version=${user_specified_version}
        echo "install_version=${install_version}"
    elif [[ ${major} =~ ^[0-9]+$ ]] && [[ ${minor} =~ ^[0-9]+$ ]] && [[ ${micro} =~ ^\*$ ]]; then
        echo "最後に＊ありでマッチンぐしたよ"
        # # if [[ ${user_specified_version} =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)$ ]]; then
        for v in ${available_version[@]}; do
            if [[ ${v} =~ ^${major}\.${minor}+\.[0-9]+$ ]]; then
                match_version+=(${v}) # ユーザ指定の条件にあうものを抽出
            fi
        done
        echo "match_version = ${match_version[@]}" 
        sorted_match_version=( $( printf "%s\n" "${match_version[@]}" | sort -V) ) # 並び替え、昇順になる。元々はファイル中身をソートするコマンド
        echo ${sorted_match_version[@]}
        install_version=${sorted_match_version[${#sorted_match_version[@]}-1]} # １番大きいものを取得
        echo "install_version=${install_version}"
    elif [[ ${major} =~ ^[0-9]+$ ]] && [[ ${minor} =~ ^\*$ ]] && [[ ${micro} =~ ^[0-9]+$ ]]; then
        echo "真ん中に＊ありでマッチンぐしたよ"
        for v in ${available_version[@]}; do
            if [[ ${v} =~ ^${major}\.[0-9]+\.${micro}$ ]]; then
                match_version+=(${v})
            fi
        done
        echo "match_version = ${match_version[@]}"
        sorted_match_version=( $( printf "%s\n" "${match_version[@]}" | sort -V) )
        echo ${sorted_match_version[@]}
        install_version=${sorted_match_version[${#sorted_match_version[@]}-1]} # １番大きいものを取得
        echo "install_version=${install_version}"
    elif [[ ${major} =~ ^[0-9]+$ ]] && [[ ${minor} =~ ^\*$ ]] && [[ ${micro} =~ ^\*$ ]]; then
        echo "真ん中、最後に＊ありでマッチンぐしたよ"
        for v in ${available_version[@]}; do
            if [[ ${v} =~ ^${major}\.[0-9]+\.[0-9]+$ ]]; then
                match_version+=(${v})
            fi
        done
        echo "match_version = ${match_version[@]}"
        sorted_match_version=( $( printf "%s\n" "${match_version[@]}" | sort -V) )
        echo ${sorted_match_version[@]}
        install_version=${sorted_match_version[${#sorted_match_version[@]}-1]} # １番大きいものを取得
        echo "install_version=${install_version}"
    fi

else
    echo a
    # httpリクエストが失敗した場合
    # リトライ（今回は省略）
fi

# ソート
# arr=("3.0.0" "2.0.10" "2.0.0" "1.2.2" "1.2.1" "1.1.1" "1.1.0" "1.0.2" "1.0.1" "1.0.0")
# echo ${arr[@]}
 
# sorted_arr=( $( printf "%s\n" "${arr[@]}" | sort -V) )
# echo ${sorted_arr[@]}

# echo ${sorted_arr[${#sorted_arr[@]}-1]}