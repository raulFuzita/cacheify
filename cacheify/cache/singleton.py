class Singleton(type):
    """
    A metaclass for creating singleton classes. A singleton is a class that allows only a single instance of itself to be created.
    This pattern is useful when exactly one object is needed to coordinate actions across the system. 
    Every singleton class should inherit from this class by specifying 'metaclass=Singleton'.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if cls not in cls._instances:
            cls._instances[cls] = {}
        if key not in cls._instances[cls]:
            cls._instances[cls][key] = super().__call__(*args, **kwargs)
        return cls._instances[cls][key]