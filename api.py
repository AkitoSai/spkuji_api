from flask import Flask, jsonify
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/spkuji_api/', methods=['GET'])
def hello_api():
    return jsonify('Welcom,Sport Kuji API')

# API 主端口
@app.route('/spkuji_api/get', methods=['GET'])
def loto_api():

    # 設定爬蟲對象頁面的 url 並將頁面 xml 內容抓取至 spkuji
    url = 'https://store.toto-dream.com/dcs/subos/screen/pi05/spin014/PGSPIN01401LnkHoldCntLotResultLstBIG.form'
    response = requests.get(url)
    spkuji = BeautifulSoup(response.text, 'lxml')

    # 從 spkuji 找到5個獎項的名稱的 table
    kuji_titles_mb2 = spkuji.find_all('table', class_='kobetsu-format1 mb2')
    kuji_titles_mb10 = spkuji.find_all('table', class_='kobetsu-format1 mb10')

    # 獎項的名稱的放進名為 kuji_titles 的 Array
    kuji_titles = []
    
    for i in range(0,len(kuji_titles_mb2)):
        kuji_titles.append(kuji_titles_mb2[i])

    for i in range(0,len(kuji_titles_mb10)):
        kuji_titles.append(kuji_titles_mb10[i])


    #轉換成為 api 響應的結果 kujiResulrsArray
    kujiResulrsArray = []

    for i in range(0,len(kuji_titles)):
    
        #獲取各種類的名稱 sub_title
        sub_title = kuji_titles[i].find('td').text
    
        #找到各自對應 img 的 alt 值用來做分辨
        image_alt = kuji_titles[i].select('img')[0].get('alt')
    
        # 找到各自對應的 div 區塊並抓取內容
        if (image_alt == 'BIG') or (image_alt == 'MEGABig') or (image_alt == 'HyakuenBig') or (image_alt == 'BIG1000') or (image_alt == 'mini BIG'):
        
            datas = None
        
            if image_alt == 'BIG':
                datas = spkuji.find('div', class_='kujikekkaNumber kujikekkaBig mb5')
            elif image_alt == 'MEGABig':
                datas = spkuji.find('div', class_='kujikekkaNumber kujikekkaMegaBig mb5')
            elif image_alt == 'HyakuenBig':
                datas = spkuji.find('div', class_='kujikekkaNumber kujikekkaHyakuenBig mb5')
            elif image_alt == 'BIG1000':
                datas = spkuji.find('div', class_='kujikekkaNumber kujikekkaBig1000 mb5')
            elif image_alt == 'mini BIG':
                datas = spkuji.find('div', class_='kujikekkaNumber kujikekkaminiBig mb5')

            #從符合的 div 中抓取 class為“adjustment” 的 tables
            tables = datas.find_all('table', class_='adjustment')
    

            if (datas != None) and (len(tables)>0):
        
                numbers = ''
            
                for j in range(1,len(tables)):
                
                    tds = tables[j].find_all('td')
                    for k in range(0,len(tds)):
                        numbers += tds[k].text
                
                    if j < len(tables)-1:
                        numbers += " "
        
                #找到各自對應 img 的 src 圖片連結
                image_url = kuji_titles[i].select('img')[0].get('src')
            
                #把各種類的名稱(subtitle) 得獎號碼(numbers) 圖片url(image_url) 放進lotoDic
                lotoDic = {"subtitle":sub_title,"numbers":numbers,"imgurl":image_url}
    
            kujiResulrsArray.append(lotoDic)

    #組成 API 響應的 JSON 格式並回傳
    response_json = {"title" : "スポーツくじ","results":kujiResulrsArray}

    return jsonify(response_json)

if __name__ == '__main__':
    app.run(debug=True)

