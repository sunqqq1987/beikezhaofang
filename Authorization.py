import hashlib
import base64    
# 获取Authorization
# 来源https://github.com/ShiJianYingxiang/origin/blob/master/fang_beike/fang_beike/spiders/ershou_viewer.py
# url没用
def generateAuthorization(self, url, url_parm):
  secret_key = "d5e343d453aecca8b14b2dc687c381ca"
  secret_id = "20180111_android"
  # 提取URL内参数
  # url_parm = {i.split("=")[0]: i.split("=")[1] for i in url.split("?")[1].split("&")}
  # 参数排序
  url_parm_sort = sorted(url_parm.items(), key=lambda x: x[0], reverse=False)
  p2 = secret_key + "".join([i[0] + "=" + i[1] for i in url_parm_sort])
  v3 = hashlib.sha1(p2.encode('utf-8')).hexdigest()
  v4 = secret_id + ":" + v3
  v5 = base64.b64encode(v4.encode("utf-8"))
  return v5.decode()
