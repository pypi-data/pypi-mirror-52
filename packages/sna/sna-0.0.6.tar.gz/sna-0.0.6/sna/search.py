import os
import re
import io


class Search(object):
    def __init__(self, parent):
        self.parent = parent
        self.through = self

    def __getattr__(self, key):
        if key not in self.__dict__:
            print("warning you dont choose valid unit")
            return None

    def characters(self):
        self.parent.target_seperators("")
        return self.parent

    def words(self):
        sentence_words = [".", "!", "?"]
        self.parent.target_seperators(
            " ", ",", "\n", *sentence_words
        )
        return self.parent

    def sentence(self):
        self.parent.target_seperators(".", "!", "?")
        return self.parent

    def lines(self):
        paragraph_words = ["\n\n"]
        self.parent.target_seperators(
            "\n", "\r", "\r\n", *paragraph_words
        )
        return self.parent

    def paragraphs(self):
        self.parent.target_seperators("\n\n")
        return self.parent


class Sna(object):
    def __init__(self):
        self.filename = None
        self.entities = dict()
        self.usable_entities = dict()
        self.split_words = None
        self.inplace = False
        self.selected_classes = list()
        self.through = None

    def search(self, *args):
        if len(args) == 0:
            self.usable_entities = self.entities.copy()
        else:
            for arg in args:
                if arg in self.entities:
                    self.usable_entities[
                        arg
                    ] = self.entities[arg]

        through = Search(self)
        return through

    def __call__(self, regex):
        def decorator(cls):
            compilation = re.compile(regex)
            if cls.__name__ not in self.entities:
                self.entities[cls.__name__] = list()

            for rule in self.entities[cls.__name__]:
                if (
                    compilation == rule[0]
                    and cls is rule[1]
                ):
                    return cls

            self.entities[cls.__name__].append(
                (compilation, cls)
            )
            return cls

        return decorator

    def __getattr__(self, key):

        if key in self.__dict__.keys():
            return self.__dict__[key]
        else:

            def parameter_harvester(*args, **kwargs):
                for cls in self.selected_classes:
                    func = getattr(cls, key)
                    func(*args, **kwargs)
                self.selected_classes = list()
                self.usable_entities = dict()

            return parameter_harvester

    def target_seperators(self, *args):
        self.split_words = args
        return self

    def on(self, string=None, filepath=None):
        new_file = str()
        if self.split_words is None:
            self.lines()

        if filepath is not None:
            if os.path.isfile(filepath):
                filepath = os.path.abspath(filepath)
                with open(filepath, "r") as f:
                    content = f.read()
        elif string is not None and isinstance(
            string, str
        ):
            content = string
        else:
            raise Exception(
                "string or filepath must be provided"
            )

        target = str()

        for char in content:
            target = target + char
            if char in self.split_words:
                for (
                    cls_name,
                    rules,
                ) in self.usable_entities.items():

                    for compilation, cls in rules:
                        match = compilation.match(target)
                        if match is not None:
                            self.selected_classes.append(
                                cls(match)
                            )
                target = str()
        return self
