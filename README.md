//  Read Me
//  AkitosHomeWork
//
//  Created by 蔡 易達 on 2022/5/30.
//  Copyright © 2022年 蔡 易達. All rights reserved.
//====================spkuji_api.py====================//

以Python+Flask Server的方式架設於GCP(Google Cloud Platform)實現抓取日本スポーツくじ的最新得獎頁面、抓取以下5種類的得獎號碼：

”BIG　くじ” 
”MEGA BIG　くじ” 
”100円BIG　くじ” 
”BIG1000　くじ” 
”mini BIG くじ”

抓取後以JSON格式回傳給Request的一方、實現api接口

目標頁面：
https://store.toto-dream.com/dcs/subos/screen/pi05/spin014/PGSPIN01401LnkHoldCntLotResultLstBIG.form 

API響應端口 ：
http://35.200.24.201:5000/loto_api/get

====================spkuji_api.py====================//


