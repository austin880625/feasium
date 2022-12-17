import jinja2
class ContentSettings:
    environ = jinja2.Environment(loader=jinja2.BaseLoader)
    def __init__(self, singlePath = "/", uncategorized_slug="uncategorized"):
        self.single_path = singlePath
        self.taxonomies = {}
        self.uncategorized_slug = uncategorized_slug
    
    def set_data(self, data):
        single_path = data.get("single_path", "/")
        self.single_path = single_path
        taxonomies = data.get("taxonomy", {})
        for tax_name, tax_item_list in taxonomies.items():
            if self.taxonomies.get(tax_name) == None:
                print("taxonomy %s is not available" % (tax_name))
                continue
            tax = self.taxonomies[tax_name]
            print(tax_name, tax.source)
            if tax.source == "tree":
                self.add_terms(tax_name, tax.tree, tax_item_list)

    def render_single_path(self, content):
        templ = ContentSettings.environ.from_string(self.single_path)
        return templ.render(content=content)
    
    def add_taxonomy(self, tax):
        self.taxonomies[tax.name] = tax
    
    def add_term(self, taxonomy, name, slug, desc="", thumbnail=""):
        term = Term(name, "", slug, desc, thumbnail)
        self.taxonomies[taxonomy].tree.children.append(term)
        self.taxonomies[taxonomy].terms[term.slug_path] = term

    def add_terms(self, tax_name, tree, term_list):
        for term_data in term_list:
            name = term_data.get("name", "")
            slug = term_data.get("slug", name)
            desc = term_data.get("desc", "")
            thumbnail = term_data.get("thumbnail", "")
            children = term_data.get("children", [])
            term = Term(name, tree.slug_path, slug, desc, thumbnail)
            tree.children.append(term)
            self.taxonomies[tax_name].terms[term.slug_path] = term
            if len(children) != 0:
                self.add_terms(tax_name, term, children)
            tree.children.sort()

class Taxonomy:
    def __init__(self, name, is_multi, source):
        self.name = name
        self.is_multi = is_multi
        self.source = source
        self.content_list = {}
        self.terms = {}
        self.tree = Term()
    
    def add_content(self, slug, content):
        if slug[0] != "/":
            slug = "/" + slug
        if self.content_list.get(slug) == None:
            self.content_list[slug] = []
        self.content_list[slug].append(content)

class Term:
    def __init__(self, name="", parent="", slug="", desc="", thumbnail=""):
        self.name = name
        self.slug_path = parent + "/" + slug
        if slug == "" and parent == "":
            self.slug_path = ""
        self.permalink = ""
        self.slug = slug
        self.desc = desc
        self.thumbnail = thumbnail
        self.children = []
    def get_permalink(self, content_type, tax_name):
        return "%s/%s%s" % (content_type, tax_name, self.slug_path)
    def __lt__(self, other):
        return self.name < other.name
    def __repr__(self) -> str:
        return "name: "+self.name + "slug: "+self.slug + ", ch: " + str(self.children)