import re
from PyPDF2 import PdfFileReader

# PATH = os.getcwd() + "/samples_pdfs_stj/"


class GetBookMarks:
    def __init__(self, file_buffer, file_name):
        self.__file_buffer = file_buffer
        self.__file_name = file_name
        self.__file_reader = self.__file_reader()

    def __is_volume(self):
        regex = re.match(r"(?P<proc>\w+_\d+)_\w+_(?P<cod>\d+)_\w+",
                         self.__file_name)
        if regex.group("cod") == "60":
            return True
        return False

    def __file_reader(self):
        return PdfFileReader(self.__file_buffer)

    def __return_bookmarks(self):
        list_bookmarks = []
        outlines = self.__file_reader.getOutlines()
        for bookmarks in outlines:
            if type(bookmarks) == list:
                for sub_bookmarks in bookmarks:
                    list_bookmarks.append((
                        sub_bookmarks["/Title"],
                        self.__file_reader.getDestinationPageNumber(
                            sub_bookmarks)+1))
            else:
                list_bookmarks.append((
                        bookmarks["/Title"],
                        self.__file_reader.getDestinationPageNumber(
                            bookmarks)+1))
        return list_bookmarks

    def get_bookmarks(self):
        if self.__is_volume():
            return self.__return_bookmarks()
        return list()

# if __name__ == "__main__":
#     for dir_path, dir_names, files_name in os.walk(PATH):
#         for f in files_name:
#             file_buffer = open(os.path.join(dir_path, f), "rb")
#             get_b = GetBookMarks(file_buffer, f)
#             result = get_b.get_bookmarks()
#             print("Document: {}\nBookmarks: {}".format(f, result))
