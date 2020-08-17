from typing import Dict
import requests
from dataclasses import dataclass, field
import json


@dataclass
class Course:
    brief:str 
    duration:str
    hasBuy: bool
    href:str
    id: int
    image: str
    originalPrice: str
    price: str
    promotionType: int
    pruchasedCount: str
    remainSeconds: int
    secKillTag: str
    tag: str
    teacherName: str
    teacherTitle: str
    title: str
    inspect:Dict = field(default_factory=dict)

def get_course_list(header, course_url,inspect_course_url):
    page = requests.Session()
    page.headers = header
    resp = page.get(course_url).text
    resp_json = json.loads(resp)
    ret = list()
    for course_json in resp_json['content']['courseCardList'][0]['courseList']:
        course = Course(**course_json)
        in_resp = page.get(inspect_course_url.format(course.id)).text
        in_resp_json = json.loads(in_resp)
        if not in_resp_json['content']['hasBuy']:
            continue
        course.inspect = in_resp_json['content']
        ret.append(course)
    return ret


