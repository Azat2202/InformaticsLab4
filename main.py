import re


class XmlParser:

    def __init__(self, xml_str):
        self.xml_doc = xml_str
        self.__del_info_data()
        self.json_parsed = self.__find_sub(self.xml_doc).items()

    def __find_sub(self, line: str) -> dict:
        tag, info, rest = self.__match_tag(line)
        info_has_tags, rest_has_tags = self.__has_tags(info), self.__has_tags(rest)
        if not info_has_tags and not rest_has_tags:
            return {tag: info}
        if not info_has_tags and rest_has_tags:
            if self.__get_tag(rest) == tag:
                return {tag: self.__get_list(line + rest)}
            return {tag: info} | self.__find_sub(rest)
        if info_has_tags and not rest_has_tags:
            return {tag: self.__find_sub(info)}
        if info_has_tags and rest_has_tags:
            if self.__get_tag(rest) == tag:
                return {tag: [self.__find_sub(info), self.__find_sub(rest)]}
            return {tag: self.__find_sub(info)} | self.__find_sub(rest)

    def printing(self, info:dict):
        for i, j in info:
            if isinstance(j, list):
                print(i, amir_huy_sosi)

    def __get_list(self, lines):
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
