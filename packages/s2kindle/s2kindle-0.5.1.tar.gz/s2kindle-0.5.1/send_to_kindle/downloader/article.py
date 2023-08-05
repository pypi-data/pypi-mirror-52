class Article:
    def __init__(self, url, title, template):
        self.url = url
        self.title = title
        self.template = template
        self._content = None
        self._img_map = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def image_map(self):
        return self._img_map

    @image_map.setter
    def image_map(self, value):
        self._img_map = value

    def to_html(self):
        self.template.find("title").string = self.title
        self.template.body.insert(0, self.content)
        return self.template
