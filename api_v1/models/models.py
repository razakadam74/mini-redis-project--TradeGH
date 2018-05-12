from .. import redis_store



class StringDAO(object):
    def __init__(self):
        self.counter = 0
        self.strings = []

    def get(self, id):
        for string in self.strings:
            if string['id'] == id:
                return string
        api.abort(404, "String {} doesn't exist".format(id))

    def create(self, data):
        string = data
        string['id'] = self.counter = self.counter + 1
        self.strings.append(string)
        return string

    def update(self, id, data):
        string = self.get(id)
        string.update(data)
        return string

    def delete(self, id):
        string = self.get(id)
        self.strings.remove(string)

