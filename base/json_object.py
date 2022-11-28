import json
# 序列化
def serialize_instance(obj):
	d = {'__classname__': type(obj).__name__}
	d.update(vars(obj))
	return d
# 反序列化
def unserialize_object(d):
	clsname = d.pop('__classname__', None)
	if clsname:
		# 需要改进的地方，定义类；也可以通过getattr创建对象
		cls = corpora.Dictionary  # 测试用的类，可更改为其他类
		obj = cls.__new__(cls)
		for key, value in d.items():
			setattr(obj, key, value)
			return obj
	else:
		return d
def bejson(f):
    json.dump(dictionary, f, default=serialize_instance, indent=4)
def beobject(f):
	dictionary = json.load(f, object_hook=unserialize_object)