import re


class XmlParser:

    def __init__(self, xml_str):
        self.xml_doc = xml_str
        self.__del_info_data()
        self.__find_sub(self.xml_doc)

    def __find_sub(self, line: str, tab_count=0, needs_minus=False):
        tag, info, rest = self.__match_tag(line)
        info_has_tags, rest_has_tags = self.__has_tags(info), self.__has_tags(rest)
        if not needs_minus:
            print('  ' * tab_count, end='')
        else:
            print('  ' * (tab_count - 2) + '  - ', end='')
        if not info_has_tags and not rest_has_tags:
            print(tag + ':', self.__beauty_var(info))
        if not info_has_tags and rest_has_tags:
            if self.__get_tag(rest) == tag:
                print(tag + ': ')
                for i in self.__get_list(line):
                    print('  ' * tab_count + '  - ' + i)
                return
            print(tag + ':', info)
            self.__find_sub(rest, tab_count)
        if info_has_tags and not rest_has_tags:
            print(tag + ':')
            self.__find_sub(info, tab_count + 1)
        if info_has_tags and rest_has_tags:
            if self.__get_tag(rest) == tag:
                print(tag + ': ')
                for element in self.__split_list(line):
                    self.__find_sub(element, tab_count + 2, needs_minus=True)
                return
            print(tag + ':')
            self.__find_sub(info, tab_count + 1)
            self.__find_sub(rest, tab_count)

    @staticmethod
    def __beauty_var(i: str):
        return f"'{i}'" if i.isdecimal() else i

    @staticmethod
    def __split_list(line):
        info = re.findall(r'<(?P<tag>\b\w+\b)[\w ]*>\s?(.*?)[ \s]*</\1>', line, flags=re.S)
        return [i[1] for i in info]

    @staticmethod
    def __get_list(lines):
        infos = re.findall(r'<(\b\w+\b[\w ]*)>(.*?)</\1>', lines, flags=re.S)
        return [i[1] for i in infos]

    @staticmethod
    def __has_tags(lines):
        matched = re.search(r'<(?P<tag>\b\w+\b)[\w ]*>\s?(?P<info>.*?)</\1>', lines, flags=re.S)
        return bool(matched)

    @staticmethod
    def __get_tag(lines):
        match = re.search(r'<(?P<tag>\b\w+\b)[\w ]*>', lines, flags=re.S)
        return match.group("tag")

    @staticmethod
    def __match_tag(lines):
        matched = re.search(r'<(?P<tag>\b\w+\b)[\w ]*>\s?(?P<info>.*?)</\1>\s?(?P<rest>.*)', lines, flags=re.S)
        del_start_spaces = re.sub('^ {0,4}\t?', '', matched.group("info"), flags=re.M)
        return matched.group("tag"), del_start_spaces, matched.group("rest")

    def __del_info_data(self):
        self.xml_doc = re.sub('<\?.*\?>\\n', '', self.xml_doc)


if __name__ == '__main__':
    with open("Myxml.xml", "r", encoding="utf16") as input_file:
        parser = XmlParser(input_file.read())
