class Part:
    def __init__(self, part_txt=None):
        self.lhs = None
        self.operator = None
        self.rhs = None

        if part_txt is not None:
            self.__parse(part_txt)

    def __parse(self, part_txt):
        pass

def lex(exp: str):
    for part_txt in exp.split(' '):
        if len(part_txt) <= 0:
            continue
        yield __lex_part(part_txt)

def __lex_part(sub_exp: str):
    print(sub_exp)

if __name__ == '__main__':
    list(lex("art  time<=yesterday genre=roc% rating>3"))