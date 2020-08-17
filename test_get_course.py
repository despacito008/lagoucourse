import pprint
from lagoucourse.download.course import *
from lagoucourse.constant.setting import *

course_list = get_course_list(HEADER, COURSE_URL, INSPECT_COURSE_USL)


pprint.pprint(course_list)
