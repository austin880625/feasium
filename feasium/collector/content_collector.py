import os
import importlib
import yaml
from .content_settings import ContentSettings

class ContentCollector:
    def __init__(self, base_path, type_name):
        self.base_path = base_path
        self.type_name = type_name
        self.content_class = \
            getattr(\
                importlib.import_module("feasium.content_type." + type_name),\
                type_name.capitalize()\
            )
        settings_path = os.path.join(base_path, "content.yaml")
        with open(settings_path, "r") as f:
            settings_data = yaml.load(f, yaml.Loader)
            self.content_class.settings.set_data(settings_data)

    def collect(self, content):
        dir = self.base_path
        type_name = self.type_name
        content_list = []
        content[type_name] = []
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name == 'content.yaml':
                    continue
                post = self.content_class(os.path.join(root, name))
                content_list.append(post)
        
        content_list.sort(reverse=True)
        length = len(content_list)
        page_size = self.content_class.get_pagination_size()
        if page_size == 0:
            page_size = length
        for i in range(0, length, page_size):
            end = min(i+page_size, length)
            content[type_name].append(content_list[i:end])
                