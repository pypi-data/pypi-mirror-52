class SimpleTestCache(object):
    primers = None

    def __init__(self):
        self.primers = {}

    def register_primer(self, name, cls):
        self.primers[name] = cls

    def primer(self, name):
        return self.primers[name]

    def no_primers_defined(self):
        return not bool(self.primers)


