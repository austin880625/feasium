import os, datetime

class Content:
    def __init__(self, name, widget_type="content"):
        self.meta = {
        }
        filename = os.path.basename(name)
        self.widget_type = widget_type
        self.raw_content = ""
        name_ext = os.path.splitext(filename)
        self.filename = name_ext[0]
        self.file_type = name_ext[-1]
        if self.file_type != ".md":
            return
        with open(name) as f:
            lines = f.readlines()
            for (i, line) in enumerate(lines):
                if line.strip() == "---":
                    self.raw_content = "".join(lines[i+1:])
                    break
                elif line.strip() == "":
                    continue
                elif line.startswith("# "):
                    self.meta["title"] = line[2:].strip()
                else:
                    kv = line.split(": ")
                    key = kv[0]
                    self.meta[key] = ""
                    if len(kv) < 2:
                        continue
                    value = kv[1].strip()
                    self.meta[key] = value
        self.datetime = datetime.datetime.strptime(
            self.meta.get("date", datetime.datetime.now().strftime("%Y/%m/%d")),
            "%Y/%m/%d"
        )
        self.date = self.datetime.strftime("%Y-%m-%d")
        self.order = self.meta.get("order", 0)
    def get_content(self):
        return self.raw_content
    def get_pagination_size():
        return 0
    
    def __lt__(self, other):
        return self.datetime < other.datetime if self.order == other.order else self.order < other.order 