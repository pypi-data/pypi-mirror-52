# from tartiflette import Scalar

from typing import Union
from typing_extensions import Literal
from tartiflette.language.ast.base import Node
from tartiflette.constants import UNDEFINED_VALUE
try:
    from bson import ObjectId as ObjectId_
except Exception:
    ObjectId_ = lambda: None


class Json:
    @staticmethod
    def coerce_input(val):
        return val

    @staticmethod
    def coerce_output(val):
        return val

    def parse_literal(self, ast: Node) -> Union[str, Literal[UNDEFINED_VALUE]]:
        return self.coerce_input(ast.value)


class AnyScalar:
    @staticmethod
    def coerce_input(val):
        if val == 'true':
            return True
        elif val == 'false':
            return False
        else:
            try:
                return float(val)
            except Exception:
                return str(val)

    @staticmethod
    def coerce_output(val):
        return val

    def parse_literal(self, ast: Node) -> Union[str, Literal[UNDEFINED_VALUE]]:
        return self.coerce_input(ast.value)


class ObjectId:
    @staticmethod
    def coerce_input(val):
        return ObjectId_(val)

    @staticmethod
    def coerce_output(val):
        return str(val)

    def parse_literal(self, ast: Node) -> Union[str, Literal[UNDEFINED_VALUE]]:
        return self.coerce_input(ast.value)


class ID:
    @staticmethod
    def coerce_input(val):
        return val

    @staticmethod
    def coerce_output(val):
        return val

    def parse_literal(self, ast: Node) -> Union[str, Literal[UNDEFINED_VALUE]]:
        return self.coerce_input(ast.value)

