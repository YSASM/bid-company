import hashlib
def get_md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()