class FrameRegistry:
    objects = {

    }

    def __new__(cls, *args, **kwargs):
        """ Create as a singleton. """
        if not hasattr(cls, "instance"):
            cls.instance = object.__new__(cls)
        return cls.instance

    def __setitem__(self, key, value):
        self.objects[key] = value

    def __getitem__(self, item):
        if item in self.objects:
            return self.objects[item]
        else:
            return False

    def register_ob(self, name, obj):
        self.objects[name] = obj

    def pull(self, obj):
        return self.objects[obj]


_registry_ob = FrameRegistry()


def register(f):
    def wr_regis(*args, **kwargs):
        _registry_ob.register_ob(f.__name__, f)
        x = f(*args, **kwargs)
        return x
    return wr_regis


def pull(o):
    r = _registry_ob.pull(o)
    return r
