import os
import sys
import re
import json
import time
import requests
from typing import Iterable
from lagoucourse.download.course import *
from lagoucourse.decrypt.aliplayer_decrypt import *
from lagoucourse.constant.setting import *
from lagoucourse.utils.codec import *
import urllib
import urllib.request


start_time = time.time()

course_list = get_course_list(HEADER, COURSE_URL, INSPECT_COURSE_USL)

def download_report_hook(blocknum, blocksize, totalsize):
    speed = (blocknum * blocksize) / (time.time() - start_time)
    # speed_str = " Speed: %.2f" % speed
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize
     
    # 设置下载进度条
    f = sys.stdout
    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    f.write(percent_str.ljust(8, ' ') + '[' + s + ']' + speed_str)
    f.flush()
    # time.sleep(0.1)
    f.write('\r')

def auto_retry_down(url,filename):
    try:
        urllib.request.urlretrieve(url,filename,download_report_hook)
    except urllib.error.ContentTooShortError:
        print(f'download {url} Network conditions is not good.Reloading...')
        auto_retry_down(url,filename)

def get_original_list(header, course_list, vod_meta_url, vod_url):
    page = requests.Session()
    page.headers = header
    ret = dict()
    for course in course_list:
        ret[course.title] = list()
        page.headers['referer'] = course.href
        for lesson in course.inspect['courseSectionList']:
            for in_lesson in lesson['courseLessons']:
                time.sleep(1)
                print(f"开始获取课节{in_lesson}")
                resp = page.get(vod_meta_url.format(in_lesson['id'])).text
                resp_json = json.loads(resp)
                mp = resp_json.get('content',{}).get('mediaPlayInfoVo',{})
                if not mp:
                    print(f"跳过{mp}...")
                    continue
                aliPlayAuth = mp.get('aliPlayAuth',{})
                if not aliPlayAuth:
                    print(f"跳过{mp}...")
                    continue
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
                stringToSign ="GET" + "&" + percentEncode("/") + "&" + percentEncode(cqs)
                signature = hmacSHA1Signature(playAuth['AccessKeySecret'], stringToSign)
                queryString = cqs + "&Signature=" + signature
                api = "https://vod.cn-shanghai.aliyuncs.com/?" + queryString
                # print(api)
                api_result = page.get(api).json()
                if not isinstance(api_result.get('PlayInfoList',{}).get('PlayInfo'),Iterable):
                    continue
                for index,play_item in enumerate(api_result.get('PlayInfoList',{}).get('PlayInfo')):    
                    ret[course.title].append((in_lesson['theme'],api))
                    dirname = replace_windows_path_invalid_char(course.title)
                    if not os.path.exists(f"D:\\backup\\lagou\\{dirname}"):
                        os.makedirs(f"D:\\backup\\lagou\\{dirname}",exist_ok=True)
                    print(f"正在下载D:\\backup\\lagou\\{dirname}\\{in_lesson['theme']}")
                    downloadFileName = replace_windows_path_invalid_char(in_lesson['theme'].replace(" ","") + "_" + str(index) + ".mp4")
                    auto_retry_down(play_item['PlayURL'],f"D:\\backup\\lagou\\{dirname}\\{downloadFileName}")

get_original_list(HEADER, course_list, VOD_META_URL, VOD_URL)
print(f"总耗时:{time.time()-start_time}s")

