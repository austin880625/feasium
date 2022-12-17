import os
from typing import Type
import jinja2
from pathlib import Path
from feasium.content_type.content import Content
from feasium.collector.content_settings import Term, Taxonomy

class TaxonomyEmmiter:
    def __init__(self,
        templ: Type[jinja2.Template],
        content_type: str,
        taxonomy: Type[Taxonomy]
    ):
        self.content_type = content_type
        self.taxonomy = taxonomy
        self.template = templ
        self.urlset = []

    def emit_tax_tree(self, site, tree: Type[Term], is_root, slug: str, output_path: str):
        Path(output_path).mkdir(exist_ok=True, parents=True)
        path = os.path.join(output_path, "index.html")
        print("writing taxonomy ", slug)
        self.urlset.append({
            "url": {
                "loc": site["config"]["url"] + "/%s/%s%s" % (self.content_type, self.taxonomy.name, slug),
            }
        })
        with open(path, "w") as f:
            f.write(self.template.render({
                "config": site["config"],
                "content": site["content"],
                "is_root": is_root,
                "term": tree,
                "content_list": self.taxonomy.content_list.get(slug, []),
                "path": "%s/%s%s" % (self.content_type, self.taxonomy.name, slug)
            }))
        for child in tree.children:
            self.emit_tax_tree(site, child, False, slug + "/" + child.slug, output_path + "/" + child.slug)
    
    def emit(self, site, base_path: str):
        # like /post/category, /post/tag
        taxonomy_output_path = os.path.join(base_path, self.content_type, self.taxonomy.name)
        Path(taxonomy_output_path).mkdir(parents=True, exist_ok=True)
        self.emit_tax_tree(site, self.taxonomy.tree, True, "", taxonomy_output_path)
        return self.urlset