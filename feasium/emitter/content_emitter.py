from feasium.emitter.taxonomy_emitter import TaxonomyEmmiter
import jinja2
from typing import Type
from pathlib import Path
import importlib

class ContentEmitter:
    def __init__(self, site, templ: Type[jinja2.Template], listing_templ: Type[jinja2.Template], content_type: str):
        self.content_type = content_type
        self.site = site
        self.page_list = site["content"][content_type]
        self.template = templ
        self.listing_template = listing_templ
    
    def emit(self, base_path):
        urlset = []
        for i, page in enumerate(self.page_list):
            if self.listing_template != None:
                Path("%s/%s" % (base_path, self.content_type)).mkdir(exist_ok=True)
                with open(Path("%s/%s/p%d.html" % (base_path, self.content_type, i)), "w") as f:
                    f.write(self.listing_template.render({
                        "config": self.site["config"],
                        "content_type": self.site["content_type"],
                        "content": self.site["content"],
                        "page_current": i,
                        "page_num": len(self.page_list),
                        "content_list": page
                }))
            for post in page:
                print('writing', self.content_type, "with name", post.filename, "into", post.permalink)
                Path(base_path + post.path).mkdir(parents=True, exist_ok=True)
                urlset.append({
                    "url": {
                        "loc": self.site["config"]["url"] + post.permalink,
                        "lastmod": post.datetime.strftime("%Y-%m-%d")
                    }
                })
                with open(Path(base_path + post.permalink), "w") as f:
                    f.write(self.template.render({
                        "config": self.site["config"],
                        "content_type": self.site["content_type"],
                        "content": self.site["content"],
                        self.content_type: post
                    }))
        return urlset