import redis

class SessionStore:

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionStore, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        """每一个数据库实例管理一个连接池"""
        pool = redis.ConnectionPool(host='192.168.0.104',port=6379,db=0,password='bright123',decode_responses=True)
        self.r=redis.Redis(connection_pool=pool)


    def set_session(self,session_key,session_value):
        self.r.set(session_key,session_value)

    def get_session(self,session_key):
        return self.r.get(session_key)