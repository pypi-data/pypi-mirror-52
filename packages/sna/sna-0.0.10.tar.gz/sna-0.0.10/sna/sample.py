from sna.search import Sna

sna = Sna()


@sna("(.*d.*r.*)")
class DR_word(object):
    def __init__(self, match):
        self.content = match.group(1)

    def read(self):
        print(self.content)


@sna("(.*e.*t.*)")
class ET_word(object):
    def __init__(self, match):
        self.content = match.group(1)

    def read(self):
        print(self.content)


# find all patterns
sna.search().through.words().on(
    filepath="sample.txt"
).read()

print(80 * "-")
# Or be specific
sna.search("ET_word").through.words().on(
    filepath="sample.txt"
).read()
