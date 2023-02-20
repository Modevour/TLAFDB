# TLAFDB
1、信息收集模块
onionv3.sh——收集暗网中v3洋葱域名shell版本
torcrawler.py——收集暗网中v3洋葱域名py版本以及下载v3洋葱域名对应的网页
2、信息清洗模块
存在真实交易比特币地址筛选：
vaildtransactionbtcfilter.py——筛选信息收集模块得到的暗网网页中存在真实交易比特币地址
镜像地址筛选：
mirroraddressfilter.py——筛选出存在真实交易比特币地址和洋葱域名的关联关系
3、信息分析模块
关键词匹配法和SVM模型（分类对照实验）
PageRank——暗网网页流行度分析
Btclevelrank——存在真实交易比特币地址威胁程度排名

## Results
v3onion.txt——新版V3洋葱域名
vaildtransactionaddress.txt——存在真实交易比特币地址
存在真实交易比特币地址与存在镜像的隐藏服务地址对应表.csv
存在真实交易比特币地址威胁程度排名表.csv

## Contributors
Modevour
