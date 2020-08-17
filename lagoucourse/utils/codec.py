
import re

def replace_windows_path_invalid_char(s):
    """
    将 windows 路径中的非法字符改为目标字符，比如以下字符串:
     - 这是个?*非法目录
     - apllo:ff
    它们是不能作为 windows 目录进行创建和读写的，使用该函数可以对其中的非法字符进行替换，从而使其合法。
    """
    return re.sub('[\/:*?"<>|]', '-',s)

def format_size(bytes):
    """
    字节bytes转化K\M\G
    """
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)