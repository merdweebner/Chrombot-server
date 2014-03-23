class UrlsManager(object):
    """docstring for UrlsManager"""
    def __init__(self):
        super(UrlsManager, self).__init__()

        self.highArray = []
        self.normalArray = []
        self.lowArray = []

    def add(self, obj):
        # priors = ['high', 'normal', 'low']
        # positions = ['head', 'tail']
        target_array = self.normalArray
        if obj.get('priority') == 'high':
            target_array = self.highArray
        elif obj.get('priority') == 'low':
            target_array = self.lowArray
        
        if obj.get('position') == 'head':
            target_array.insert(0, obj)
        else:
            target_array.append(obj)

    def pop(self):
        target = self.highArray or self.normalArray or self.lowArray
        if target:
            ret = target[0]
            target.remove(ret)
            return ret
        else:
            return {}

    def getN(self, numbers):
        dest = self.highArray[0:numbers]
        self.highArray[0:numbers] = []
        if len(dest) < numbers:
            dest.append(self.normalArray[0: numbers - len(dest)])
            self.normalArray[0: numbers - len(dest)] = []
        if len(dest) < numbers:
            dest.append(self.lowArray[0: numbers - len(dest)])
            self.lowArray[0: numbers - len(dest)] = []

        return dest

gUrls = UrlsManager()
        
