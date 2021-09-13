import sys
import re
import os
import enchant


class CodeAnalyzer:
    def __init__(self):
        self.list_index = []
        self.list_error = []
        self.errors = ()

    def open_file(self, input_file):
        with open(input_file) as f:
            for index, line in enumerate(f, start=1):
                if line == '\n':
                    continue
                else:
                    self.list_index.append(index)
                    self.list_error.append(line)

    def line_length(self):
        for index, el in zip(self.list_index, self.list_error):
            if len(el) > 79:
                self.errors += ((index, "S001 Too long"),)

    def indentation(self):
        for index, el in zip(self.list_index, self.list_error):
            count = 0
            for x in list(el):
                if x == ' ':
                    count += 1
                elif x.isalpha() or x == '#':
                    break
            if count in [x*4 for x in range(10)]:
                continue
            else:
                self.errors += ((index, 'S002 Indentation is not a multiple of four'),)

    def semicolon(self):
        for index, el in zip(self.list_index, self.list_error):
            try:
                first, second = el.split('#')
                if re.findall(';$', first.strip()):
                    self.errors += ((index, 'S003 Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)'),)
                elif ";" in second:
                    continue
            except ValueError:
                if re.findall(';$', el):
                    self.errors += ((index, 'S003 Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)'),)

    def space_before_comment(self):
        for index, el in zip(self.list_index, self.list_error):
            if el[0] == "#":
                continue
            elif '#' in el:
                if re.findall(r'\s{2}#', el):
                    continue
                else:
                    self.errors += ((index, 'S004 Less than two spaces before inline comments'),)

    def todo(self):
        for index, el in zip(self.list_index, self.list_error):
            if re.findall(r'# [Tt][Oo][Dd][Oo]\s?\w*', el):
                self.errors += ((index, 'S005 TODO found'),)

    def two_blank_lines(self):
        idx = 0
        for index, el in (zip(self.list_index, self.list_error)):
            if index == idx + 4:
                self.errors += ((index, 'S006 More than two blank lines preceding a code line'),)
            else:
                idx = index

    def spaces_after_def_class(self):
        for index, el in zip(self.list_index, self.list_error):
            if re.findall(r'class\s{2,}\w+|def\s{2,}\w+', el):
                self.errors += ((index, f"S007 Too many spaces after '{el.split()[0]}'"),)

    def class_camelcase(self):
        d = enchant.Dict("en_US")
        for index, el in zip(self.list_index, self.list_error):
            if re.match(r'class', el):
                new_statement = ""
                class_name, statement = el.split()
                for letter in statement:
                    if letter.isalpha():
                        new_statement  = ''.join(' ' + letter if letter.isupper() else letter for letter in statement)
                list_words = re.findall('[A-Z][^A-Z]*', new_statement.strip(':'))
                if el.islower():
                    self.errors += ((index, f"S008 Class name '{statement.strip(':')}' should be written in CamelCase"),)
                for word in list_words:
                    if not d.check(word):
                        self.errors += ((index, f"S008 Class name '{statement.strip(':')}' should be written in CamelCase"),)

    def def_snake_case(self):
        for index, el in zip(self.list_index, self.list_error):
            if re.findall(r'def', el):
                function_split = el.split()
                if function_split[1][0].istitle():
                    self.errors += ((index, f"S009 Function name '{function_split[1].strip('():')}' should use snake_case"),)

    def args_snake_case(self):
        for index, el in zip(self.list_index, self.list_error):
            func = re.findall(r'def\s\w+\d?\(.*?\)', el)
            to_strip = str(re.findall(r'def\s\w+\d?[(]', el))
            func_args = str(''.join(func).strip(to_strip)).split(',')
            for el in func_args:
                try:
                    arg_name, value = el.split('=')
                    if not arg_name.islower():
                        self.errors += ((index, f"S010 Argument name '{arg_name.strip()}' should be written in snake_case"),)
                except ValueError:
                    continue

    def variable_snake_case(self):
        # print(self.list_error)
        for index, el in zip(self.list_index, self.list_error):
            if not re.match(r'\s+?def\s{1}', el):
                if el[0:4] == 4 * ' ' or el[0:8] == 8 * ' ':
                    try:
                        variable_name, value = el.split('=')
                        if not variable_name.islower():
                            self.errors += ((index, f"S011 Variable '{variable_name.strip()}' in function should be snake_case"),)
                    except ValueError:
                        continue

    def if_mutable(self):
        mutable_elements = ['[]', '{}']
        for index, el in zip(self.list_index, self.list_error):
            func = re.findall(r'def\s\w+\d?\(.*?\)', el)
            to_strip = str(re.findall(r'def\s\w+\d?[(]', el))
            func_args = str(''.join(func).strip(to_strip)).split(',')
            for el in func_args:
                try:
                    arg_name, value = el.split('=')
                    if value.strip(')') in mutable_elements:
                        self.errors += ((index, f"S012 The default argument value is mutable"),)
                except ValueError:
                    continue

    def run_checks(self):
        self.line_length()
        self.indentation()
        self.semicolon()
        self.space_before_comment()
        self.todo()
        self.two_blank_lines()
        self.spaces_after_def_class()
        self.class_camelcase()
        self.def_snake_case()
        self.args_snake_case()
        self.variable_snake_case()
        self.if_mutable()

    def print_result(self, args):
        for index, el in sorted(self.errors):
            print(f'{args}: Line {index}:', el.strip())

    @staticmethod
    def path_validation(path):
        try:
            return path
        except FileNotFoundError:
            os.chdir('..')
            return os.getcwd()+path


def main():
    args = sys.argv
    path = args[1]
    path_moved_up = CodeAnalyzer.path_validation(path)
    try:
        for file in os.listdir(path_moved_up):
            if file.endswith('.py'):
                code_analyzer = CodeAnalyzer()
                real_path = f'{path_moved_up}\\{file}'
                code_analyzer.open_file(real_path)
                code_analyzer.run_checks()
                code_analyzer.print_result(f'{args[1]}\\{file}')
            else:
                continue
    except NotADirectoryError:
        code_analyzer = CodeAnalyzer()
        code_analyzer.open_file(path_moved_up)
        code_analyzer.run_checks()
        code_analyzer.print_result(args[1])


main()
