from .content_collector import ContentCollector

import os
import shutil
import importlib
from pathlib import Path
from feasium.content_type.content import Content

class SiteCollector:
    def __init__(self, base_path):
        self.base_path = base_path
    def collect(self):
        cwd = self.base_path
        site = {
            "config": {
                "title": "",
                "subtitle": "",
                "theme": "default",
                "url": "http://127.0.0.1:8000",
                "staticurl": "/static/theme",
                "logo_url": ""
            },
            "content_type": [],
            "content": {}
        }
        content_path = os.path.join(cwd, "content")
        public_path = os.path.join(cwd, "public")
        for type_name in os.listdir(content_path):
            ent = os.path.join(content_path, type_name)
            if type_name == "static":
                dst = os.path.join(public_path, "static", "content")
                Path(os.path.join(public_path, "static")).mkdir(parents=True, exist_ok=True)
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(ent, dst)
            elif type_name == "site.md":
                content = Content(ent)
                site["config"].update(content.meta)
            elif type_name == "favicon.ico":
                shutil.copy(ent, os.path.join(public_path, "favicon.ico"))
            elif type_name == "draft":
                continue
            elif os.path.isdir(ent):
                site["content_type"].append(type_name)
                site["content"][type_name] = []
                ContentCollector(ent, type_name).collect(site["content"])
                
        return site