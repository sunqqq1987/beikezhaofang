    # 获取挂牌信息-贝壳网信息
    def get_guapai_data(self, xiaoqu_id):
        guapai_url = 'https://app.api.ke.com/house/ershoufang/searchv5'
        guapai_data = {
            'fullFilters': '1',
            'containerType': '2',
            'limitCount': '20',
            'condition': xiaoqu_id,
            'cityId': '**********',
            'limitOffset': '0'
        }
        # header抓一下复制进来
        headers = {
            "x-req-id": "**********",
            "Page-Schema": "ershou%2Flist",
            "Referer": "ershoulistsearch",
            "Cookie": "lianjia_udid=********;"
                      "lianjia_ssid=**********;"
                      "lianjia_uuid=**********",
            "Lianjia-City-Id": "**********",
            "User-Agent": "Beike2.31.0;Android MuMu; Android 6.0.1",
            "Lianjia-Channel": "**********",
            "Lianjia-Device-Id": "**********",
            "Lianjia-Version": "2.31.0",
            "Lianjia-Im-Version": "2.34.0",
            "Lianjia-Recommend-Allowable": "1",
            "Authorization": self.generateAuthorization(guapai_url, guapai_data),
            "ip": "**********",
            "wifi_name": "**********",
            "lat": "**********",
            "lng": "**********",
            "Host": "app.api.ke.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        guapai_res = requests.get(guapai_url, headers=headers, params=guapai_data)
        # 获取小区的挂牌信息列表
        guapai_json = json.loads(guapai_res.text)
        if guapai_json['errno'] == 0:
            guapai_info = guapai_json['data']['list']
            for i in guapai_info:
                # 插入数据库的信息列表
                sql_data = []
                if 'houseCode' in i:
                    # house_code
                    house_code = i['houseCode']
                    sql_data.append(house_code)
                    # 标题
                    resblock_name = i['title']
                    sql_data.append(resblock_name)
                    # 描述
                    resblock_desc = i['desc']
                    sql_data.append(resblock_desc)
                    # 总价
                    total_p = i['priceStr']
                    total_p = self.return_no(total_p)
                    sql_data.append(total_p)
                    # 小区
                    communityName = i['communityName']
                    sql_data.append(communityName)
                    # basicList处理
                    for basic_info in i['basicList']:
                        # pass
                        sql_data.append(basic_info['value'])
                    # infoList处理
                    for infoList_info in i['infoList']:
                        infoList_data = infoList_info['value']
                        if infoList_info['name'] == '单价：':
                            # 返回数字
                            infoList_data = self.return_no(infoList_data)
                        sql_data.append(infoList_data)
                    # 构造URL，用于微信推送
                    url = 'https://m.ke.com/tj/ershoufang/' + house_code + '.html'
                    sql_data.append(url)
                    # 数据插入数据库
                    self.insert_guapai(sql_data)
            # 休眠
            sleeptime = random.randint(2, 10)
            time.sleep(sleeptime)
