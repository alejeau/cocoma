# Test of Python's class methods


class StaticClass:
    @classmethod
    def cm(cls):
        cls.sm()

    @staticmethod
    def sm():
        print("toto")


StaticClass.cm()