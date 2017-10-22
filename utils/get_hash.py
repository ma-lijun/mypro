from hashlib import sha1


def get_hash(str, salt=None):
    # 加盐增加字符串的复杂度
    str = '^#' + str + '@#$'
    if salt:
        str = str + salt
    # 获取一个字符串的hash值
    sh = sha1()
    sh.update(str.encode('utf-8'))
    print(sh.hexdigest(),'2')
    return sh.hexdigest()
