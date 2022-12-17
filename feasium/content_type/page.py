import os
from feasium.collector.content_settings import ContentSettings
import markdown
from .content import Content

class Page(Content):
    settings = ContentSettings()
    def __init__(self, name):
        Content.__init__(self, name)
        self.path = Page.settings.render_single_path(self)
        self.permalink = self.path + "/" + self.filename + ".html"
        self.title = self.meta.get("title")
        self.excerpt = self.meta.get("excerpt", "")
        self.content = ""
        configs = {
            'extra': {
                'fenced_code': {
                    'lang_prefix': 'language-'
                }
            }
        }
        if self.file_type == ".md":
            self.content = markdown.markdown(
                self.raw_content,
                extensions=['extra', 'markdown_del_ins'],
                extension_configs=configs
            )
    def get_content(self):
        return self.content