class Objectless:
    def __new__(cls, *args, **kwargs):
        raise RuntimeError("%s should not be instantiated" % cls)
