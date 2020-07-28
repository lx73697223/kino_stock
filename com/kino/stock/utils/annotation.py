from threading import Thread, Lock


def async_exec(func):
    """
    异步执行方法
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def singleton(func_name=None):
    """
    使用单例模式
    :param func_name: 函数名(计算hash值使用的字符串). 为空时默认一个类只能有一个实例
    """
    singleton_instance = {}
    __lock = Lock()

    def decorator(cls):
        def wrapper(*args, **kw):
            key = str(cls)
            if func_name:
                result = getattr(cls, func_name)(*args, **kw)
                key = "{}.{}".format(key, hash(str(result)))
                # print('--- annotation.singleton. {} ==> {}'.format(func_name, result))

            if key not in singleton_instance:
                with __lock:
                    if key not in singleton_instance:
                        singleton_instance[key] = cls(*args, **kw)
                        print('--- annotation.singleton.', key)
            return singleton_instance[key]
        return wrapper
    return decorator
