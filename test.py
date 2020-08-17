import requests
import json
from lagoucourse.decrypt.aliplayer_decrypt import *
from lagoucourse.constant.setting import *
API_TEMPLATE = "https://gate.lagou.com/v1/neirong/kaiwu/getLessonPlayHistory?lessonId={0}&isVideo=true"

page = requests.Session()
page.headers = HEADER
response = page.get("https://gate.lagou.com/v1/neirong/kaiwu/getLessonPlayHistory?lessonId=3798&isVideo=true").text
response_json = json.loads(response)
print(response_json)

aliPlayAuth = response_json['content']['mediaPlayInfoVo']['aliPlayAuth']
authKeyToEncryptData(aliPlayAuth)
strify = stringify(authKeyToEncryptData(aliPlayAuth))
playAuth = json.loads(strify)

publicParam = {
    **PUBLIC_PARAMS,
    "AccessKeyId": playAuth['AccessKeyId'],
    "Timestamp": generateTimestamp(),
    "SignatureNonce": generateRandom()
}
privateParam = {
    **PRIVATE_PARAMS,
    "AuthInfo": playAuth['AuthInfo'],
    "SecurityToken": playAuth['SecurityToken'],
    "VideoId": playAuth['VideoMeta']['VideoId']
}

allParams = getAllParams(publicParam, privateParam)
cqs = getQueryStr(allParams)
stringToSign = "GET" + "&" + percentEncode("/") + "&" + percentEncode(cqs)
signature = hmacSHA1Signature(playAuth['AccessKeySecret'], stringToSign)
queryString = cqs + "&Signature=" + signature
api = "https://vod.cn-shanghai.aliyuncs.com/?" + queryString

print(api)

print("=====================================")
print(page.get(api).json())