import os
from feasium.collector.content_settings import ContentSettings, Taxonomy
import markdown
from .content import Content

class Post(Content):
    settings = ContentSettings()
    #settings.add_taxonomy(Taxonomy("tag", True, "content"))
    settings.add_taxonomy(Taxonomy("category", True, "tree"))
    settings.add_term("category", "Uncategorized", "uncategorized")
    #settings.add_taxonomy(Taxonomy("series", False, "tree"))
    def __init__(self, name):
        Content.__init__(self, name)
        self.path = Post.settings.render_single_path(self)
        self.permalink = self.path + "/" + self.filename + ".html"
        self.title = self.meta.get("title")
        self.category_slug = self.meta.get("category", "uncategorized")
        if self.category_slug[0] != "/":
            self.category_slug = "/" + self.category_slug
        self.thumbnail = self.meta.get("thumbnail", "")
        self.excerpt = self.meta.get("excerpt", "")

        Post.settings.taxonomies["category"].add_content(self.category_slug, self)
        self.category = Post.settings.taxonomies["category"].terms[self.category_slug]
        self.category.permalink = self.category.get_permalink("post", "category")
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
                extensions=['extra', 'markdown_del_ins', 'markdown_katex', 'feasium.md.figure_caption'],
                extension_configs=configs
            )
    def get_pagination_size():
        return 10
    def get_content(self):
        return self.content