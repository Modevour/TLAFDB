#!/bin/bash
#方法一、在onion.txt中放入明网或其他途径找到的v3洋葱域名即可爬取全部v3洋葱域名
cat onion.txt | while read line || [[ -n ${line} ]]  #针对while read line无法读取最后一行的问题要加[[ -n ${line} ]]
do
  #${#line}——计算字符串长度
if [ ${#line} -gt 60 ];then
    echo $line
    curl --socks5-hostname  127.0.0.1:9150 --connect-timeout 30 $line| grep -E -o '[0-9a-zA_Z]+\.onion' | sort | uniq | sort -R >> v3onion.txt
fi
done