from feasium.emitter.taxonomy_emitter import TaxonomyEmmiter
import jinja2
from typing import Type
import importlib

class ContentTaxonomyEmitter:
    def __init__(self, site, env: Type[jinja2.Environment], content_type: str):
        self.content_type = content_type
        self.env = env
        self.site = site
        self.content_class = \
            getattr(\
                importlib.import_module("feasium.content_type." + content_type),\
                content_type.capitalize()\
            )
    
    def emit(self, base_path):
        urlset = []
        for tax_name, tax in self.content_class.settings.taxonomies.items():
            templ = self.env.get_template("%s/taxonomy/%s.html" % (self.content_type, tax_name))
            taxonomy_emitter = TaxonomyEmmiter(templ, self.content_type, tax)
            urlset += taxonomy_emitter.emit(self.site, base_path)
        return urlset