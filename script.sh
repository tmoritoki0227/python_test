#!/bin/bash

export SD_COLLECTION="/aaa/release/1.0.0 , /bbb/release/1.*.0, /ccc/release/1.0.*, /ddd/release/1.*.*, /aaa/test/3.0.0"

echo $SD_COLLECTION

# カンマを空白に置換して配列格納。空白だと配列にしてくれるため
lists=(${SD_COLLECTION//,/ }) # ${変数名//置換前文字列/置換後文字列}


echo ${lists[@]} # 全部表示
# echo ${list[1]} # 1つ
# for i in ${array[@]}; do
#     echo $i
# done
for list in ${lists[@]}; do
    echo "list=$list"
    path=(${list//\// }) # スラッシュを空白に置換して配列格納。空白だと配列にしてくれるため
    # echo ${version[@]}
    # echo ${version[2]} # 2にバージョンがあるため
    # [0] aaa 
    # [1] release
    # [2] 1.0.0
    name=${path[0]}
    version=${path[2]}

    # ここでsdコマンドを呼ぶ

    echo "ansible-gallaxy install ${name}-${version}.tar.gz" 
done


lists=("/aaa/release/1.0.0" "/bbb/release/1.*.0")
echo ${lists[@]}

