
# xshx add 2024  用元类创建一个单例模式

class SingleMetaBase(type):
    def __call__(cls, *args, **kwargs):
        if hasattr( cls, '_instance'):
            return  getattr( cls, '_instance')
        obj = super().__call__( *args, **kwargs)
        setattr( cls, '_instance', obj)
        return  obj

