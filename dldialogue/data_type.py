class SingleOption:
    def __init__(self, value, name=None):
        self.value = value
        if name:
            self.name = name
        else:
            self.name = value.capitalize()

    def __str__(self):
        return self.value

class OptionType:
    def __init__(self, **kwargs):
        self.default = None
        self.options = []

        if "default" in kwargs:
            self.default = kwargs["default"]
        if "options" in kwargs:
            self.options = kwargs["options"]
            
        self.value = self.default

    def __str__(self):
        return self.value

class StringType:
    def __init__(self, **kwargs):
        self.default = None

        if "default" in kwargs:
            self.default = kwargs["default"]
        
        self.value = self.default
    
    def __str__(self):
        return self.value

class BooleanType:
    def __init__(self, **kwargs):
        self.default = False

        if "default" in kwargs:
            self.default = kwargs["default"]

        self.value = self.default
    
    def __str__(self):
        return self.value

class FloatType:
    def __init__(self, **kwargs):
        self.default = 0
        self.min = -10
        self.max = 10
        self.increment = 1

        if "default" in kwargs:
            self.default = kwargs["default"]
        if "min" in kwargs:
            self.min = kwargs["min"]
        if "max" in kwargs:
            self.max = kwargs["max"]
        if "increment" in kwargs:
            self.increment = kwargs["increment"]

        self.value = self.default

    def __str__(self):
        return self.value
