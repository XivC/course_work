from attr import dataclass
from django.db import connection

"""
This service provide ability to call postgresql stored functions
Now supports only single-row functions
"""


@dataclass
class FunctionCaller:
    function: str
    args: list

    def __call__(self):
        sql = f'SELECT {self.function}({self.args_to_string(self.args)});'
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchone()

    def args_to_string(self, args):
        if not args:
            return ''

        stringifies = []
        for arg in args:

            if arg is None:
                str_arg = 'null::INTEGER'
            elif type(arg) == int:
                str_arg = self.arg_to_int(arg)
            elif type(arg) == str:
                str_arg = self.arg_to_str(arg)
            elif hasattr(arg, '__iter__'):
                str_arg = self.args_to_array(arg)
            else:
                raise Exception(f'Argument of type {type(arg)} is not supported')
            stringifies.append(str_arg)

        return ','.join(stringifies)  # remove trailing comma

    def arg_to_str(self, arg):
        return f"'{arg}'"

    def arg_to_int(self, arg):
        return f"{arg}"

    def args_to_array(self, args):
        return f'ARRAY [{self.args_to_string(args)}]'
