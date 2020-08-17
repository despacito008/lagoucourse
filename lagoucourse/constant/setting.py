# 用于获取课程链接列表
COURSE_URL = "https://gate.lagou.com/v1/neirong/edu/homepage/getCourseList?deviceSourceCode=2"
# 用于获取课程详细信息
INSPECT_COURSE_USL = "https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId={0}"
# 用于获取视频元信息
VOD_META_URL = "https://gate.lagou.com/v1/neirong/kaiwu/getLessonPlayHistory?lessonId={0}&isVideo=true"
# 用于获取视频链接
VOD_URL = "https://vod.cn-shanghai.aliyuncs.com/?{0}"

# =================== request ...
COOKIE = " 填入自己的 cookie "

HEADER = {
    # "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    "Origin": "https://edu.lagou.com",
    "x-l-req-header":"""{deviceType:1}""",
    "cookie":COOKIE
}

# =================== constant query params
PUBLIC_PARAMS = {
    "SignatureMethod": "HMAC-SHA1",
    "SignatureVersion": "1.0",
    "Format": "JSON",
    "Version": "2017-03-21",
    "AccessKeyId": "",
    "Timestamp": "",
    "SignatureNonce": "",
}

PRIVATE_PARAMS = {
    "Action": "GetPlayInfo",
    "AuthTimeout": "7200",
    "Definition": "240",
    "PlayConfig": "{}",
    "ReAuthInfo": "{}",
    "AuthInfo": "",
    "SecurityToken": "",
    "VideoId": ""
}