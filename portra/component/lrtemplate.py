import uuid

class LRTemplate:
    def __init__(self, name, settings):
        self.settings = settings
        self.value = {
            'uuid': escape(str(uuid.uuid4())),
            'settings': self.settings
        }
        self.s = {
            'id': escape(str(uuid.uuid4())),
            'internalName': escape(name),
            'title': escape(name),
            'type': escape('Develop'),
            'value': self.value,
            'version': 0
        }

    def dump(self):
        return 's = {\n' + self.write(self.s, 1) + '\n}'

    def write(self, vals, indent):
        output = []
        for key, value in sorted(vals.items()):
            if not type(value) is dict:
                s = '\t' * indent + key + ' = ' + str(value) + ','
                output.append(s)
            else:
                s = '\t' * indent + key + ' = {\n' + self.write(value , indent + 1) + '\n' + '\t' * indent + '},'
                output.append(s)
        return '\n'.join(output)

def escape(string):
    return '\"' + string + '\"'
