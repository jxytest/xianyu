import os


class FilterXY:
    def __init__(self, file_name):
        self.file_path = os.path.join(os.path.dirname(__file__), file_name)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.filter_keywords = []
        self.read_filter()

    def read_filter(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.filter_keywords = f.read().splitlines()
        else:
            self.write_filter()

    def write_filter(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            self.filter_keywords = list(set(self.filter_keywords))
            f.write('\n'.join(self.filter_keywords))

    def filter(self, data):
        for keyword in self.filter_keywords:
            if keyword in data:
                return True
        return False

    def filter_list(self):
        return self.filter_keywords

    def del_filter(self, keyword):
        self.filter_keywords.remove(keyword)
        self.write_filter()

    def add_filter(self, keyword):
        self.filter_keywords.append(keyword)
        self.write_filter()

    def clear_filter(self):
        self.filter_keywords.clear()
        self.write_filter()

    def update_filter(self, keywords):
        self.filter_keywords = keywords
        self.write_filter()

    def filter_count(self):
        return len(self.filter_keywords)
