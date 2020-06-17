import re

REGEX = r"(\w+)" \
        r"(?:(" \
            r">=|<=|=|!=|>|<" \
        r")(" \
            r"[\w%]+|" \
            "\\\"(?:\\\\.|[^\"\\\\\\n])*\\\"+" \
        r"))?"

def lex(exp: str):
    for match in re.finditer(REGEX, exp):
        print(match.group(0))

# if __name__ == '__main__':
#     list(lex("art  time<=yesterday genre=roc% rating>3"))
print(REGEX)