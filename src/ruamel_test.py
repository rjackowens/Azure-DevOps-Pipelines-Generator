import sys
from ruamel.yaml import YAML

data = {"resources":{"repositories": [{"repository": "remote"}], "type": "git", "name": "DevOps/CICD.Scripts", "ref": "refs/heads/master"}, "created":"2/28"}

def indent_type(s):
    levels = []
    ret_val = ''
    for line in s.splitlines(True):
        ls = line.lstrip()
        indent = len(line) - len(ls)
        if 'created' in ls:
            levels.append(indent)
        ret_val += '  ' * len(levels) + line
    return ret_val

yaml = YAML()
yaml.explicit_start = True
yaml.dump(data, sys.stdout, transform=indent_type)
# yaml.indent(indent=4)
# yaml.dump(data, sys.stdout)



# def sequence_indent_four(s):
#     # this will fail on direclty nested lists: {1; [[2, 3], 4]}
#     levels = []
#     ret_val = ''
#     for line in s.splitlines(True):
#         ls = line.lstrip()
#         indent = len(line) - len(ls)
#         if not ls.startswith('- '):
#             if not levels or indent > levels[-1]:
#                 levels.append(indent)
#             elif levels:
#                 if indent < levels[-1]:
#                     levels = levels[:-1]
#             # same -> do nothing
#         else:
#             if levels:
#                 if indent <= levels[-1]:
#                     while levels and indent <= levels[-1]:
#                         levels = levels[:-1]
#         ret_val += '  ' * len(levels) + line
#     return ret_val

# yaml = YAML()
# yaml.explicit_start = True
# yaml.dump(data, sys.stdout, transform=sequence_indent_four)
