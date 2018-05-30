import uuid

def escape(string):
    return '\"' + string + '\"'

class LRTemplate:
    """
    Initializes a LRTemplate object with a name and Adobe Lightroom parameters
    passed in as a dictionary.
    """
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

    def __repr__(self):
        return 'LRTemplate(%s)' % self.name

    def __str__(self):
        return self.dump()

    """Outputs this LRTemplate object as a .lrtemplate file."""
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
