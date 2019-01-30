import argparse
import re

import pyperclip


class Case:
    def __contains__(self, variable_name):
        raise NotImplementedError

    @staticmethod
    def parse(variable_name):
        raise NotImplementedError

    @staticmethod
    def format(words):
        raise NotImplementedError


class ScreamingSnakeCase(Case):
    PATTERN = r'[\w\d_]+'

    def __contains__(self, variable_name):
        match = re.match(self.PATTERN, variable_name)
        return match is not None and variable_name.isupper()

    @staticmethod
    def parse(variable_name):
        return variable_name.lower().split('_')

    @staticmethod
    def format(words):
        return '_'.join((w.upper() for w in words))


class SnakeCase(Case):
    PATTERN = r'[\w\d_]+'

    def __contains__(self, variable_name):
        match = re.match(self.PATTERN, variable_name)
        return match is not None and variable_name.islower()

    @staticmethod
    def parse(variable_name):
        return variable_name.split('_')

    @staticmethod
    def format(words):
        return '_'.join((w.lower() for w in words))


class CamelCase(Case):
    PATTERN = r'[\w\d]+'

    def __contains__(self, variable_name):
        match = re.match(self.PATTERN, variable_name)
        return match is not None and variable_name[0].isupper()

    @staticmethod
    def parse(variable_name):
        words = []

        for char in variable_name:  # type: str
            if char.isupper():
                words.append(char.lower())

            elif char.isdigit() and not words[-1].isdigit():
                words.append(char)

            else:
                words[-1] += char

        return words

    @staticmethod
    def format(words):
        return ''.join(word.title() for word in words)


CASES = [SnakeCase(), ScreamingSnakeCase(), CamelCase()]


def next_case(variable_name):
    """
    Try calculate next variable case.

    Args:
        variable_name: Some string.

    Returns:
        None - variable name not detected or str - next case of variable.

    """
    if not variable_name:
        return None

    for current_case, new_case in zip(CASES, CASES[1:] + CASES[:1]):
        if variable_name in current_case:
            parsed = current_case.parse(variable_name)
            return new_case.format(parsed)
    else:
        return None


def next_variable_name_to_clipboard(arguments):
    """
    Calculate next variable case and copy to clipboard.

    Args:
        arguments: variable_name

    """
    variable_name = args.variable_name.strip()

    if not variable_name:
        pyperclip.copy('')

    else:
        new_variable_name = next_case(variable_name)

        if new_variable_name is None:
            pyperclip.copy(variable_name)
        else:
            pyperclip.copy(new_variable_name)


def update_file(arguments):
    """
    Update variable in file.

    Args:
        arguments: file_path, line_number, start_column, end_column.

    Notes:
        This function update your file.

    """
    lines = []

    file_path = arguments.file
    line_number = arguments.line_number
    start_column = arguments.start_column - 1
    end_column = arguments.end_column - 1

    with open(file_path, 'r', encoding='utf8') as f:
        for i, line in enumerate(f, start=1):
            if i != line_number:
                lines.append(line)
                continue

            variable_name = line[start_column:end_column]
            next_variable_name = next_case(variable_name)

            if next_variable_name is None:
                # Exit without file update.
                return

            new_line = (
                    line[:start_column]
                    + next_variable_name
                    + line[end_column:]
            )
            lines.append(new_line)

    with open(file_path, 'w', encoding='utf8') as f:
        f.writelines(lines)


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='Next case, please')
    subparsers = argument_parser.add_subparsers()

    # Clipboard
    parser_clipboard = subparsers.add_parser(
        'copy',
        help='Copy next case for variable to clipboard',
    )
    parser_clipboard.add_argument('variable_name', help='Name of variable')
    parser_clipboard.set_defaults(func=next_variable_name_to_clipboard)

    # File
    parser_update_file = subparsers.add_parser(
        'file',
        help='Update variable name in file',
    )
    parser_update_file.add_argument('file', help='File path')
    parser_update_file.add_argument(
        'line_number',
        type=int,
        help='Line number with variable',
    )
    parser_update_file.add_argument(
        'start_column',
        type=int,
        help='Start variable column',
    )
    parser_update_file.add_argument(
        'end_column',
        type=int,
        help='End variable column',
    )
    parser_update_file.set_defaults(func=update_file)

    args = argument_parser.parse_args()
    args.func(args)
