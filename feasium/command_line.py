import sys, os, shutil
import http.server
import socketserver
import operator
from pathlib import Path
from typing import Type
from feasium.collector.site_collector import SiteCollector
from feasium.emitter.content_taxonomy_emitter import ContentTaxonomyEmitter
from feasium.emitter.content_emitter import ContentEmitter
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def generate_site(site, cwd=os.getcwd()):
    theme_path = os.path.join(cwd, "theme", site["config"]["theme"])
    public_path = os.path.join(cwd, "public")
    if os.path.exists(os.path.join(theme_path, "static")):
            dst = os.path.join(public_path, "static", "theme")
            Path(os.path.join(public_path, "static")).mkdir(parents=True, exist_ok=True)
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(os.path.join(theme_path, "static"), dst)
    env = Environment(
        loader=FileSystemLoader(theme_path)
    )

    urlset = []
    for content_type in site["content_type"]:
        taxonomy_emitter = ContentTaxonomyEmitter(site, env, content_type)
        content_template = env.get_template("%s/single.html" % content_type)
        try:
            listing_template = env.get_template("%s/listing.html" % content_type)
        except TemplateNotFound:
            listing_template = None
        content_emitter = ContentEmitter(site, content_template, listing_template, content_type)

        public_path = os.path.join(cwd, "public")
        tax_urlset = taxonomy_emitter.emit(public_path)
        content_urlset = content_emitter.emit(public_path)
        urlset += content_urlset
    
    print("writing index.html")
    index_templ = env.get_template("index.html")
    with open(os.path.join(public_path, "index.html"), "w") as f:
        f.write(index_templ.render(site))
    
    print("generating sitemap")
    with open(Path("public/sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urlset:
            f.write(make_tag(url))
        f.write('</urlset>')
    with open(Path("public/robots.txt"), "w") as f:
        f.write("User-agent: *\n")
        f.write("Allow: /\n")
        f.write("Sitemap: %s" % (site["config"]["url"] + "/sitemap.xml"))

def make_tag(d):
    s = ""
    for k, v in d.items():
        if isinstance(v, str):
            s += "<%s>%s</%s>\n" % (k, v, k)
        else:
            s += "<%s>\n%s</%s>\n" % (k, make_tag(v), k)
    return s

def main():
    public_path = os.path.join(os.getcwd(), "public")
    site_collector = SiteCollector(os.getcwd())
    if len(sys.argv) > 1:
        if sys.argv[1] == "serve":
            site = site_collector.collect()
            site["debug"] = True
            site["config"]["url"] = "http://127.0.0.1:8000"
            generate_site(site)
            PORT = 8000
            web_dir = os.path.join(public_path)
            os.chdir(web_dir)

            Handler = http.server.SimpleHTTPRequestHandler
            socketserver.TCPServer.allow_reuse_address = True
            httpd = socketserver.TCPServer(("", PORT), Handler)
            print("serving at port", PORT)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                httpd.shutdown()
                httpd.server_close()
    else:
        site = site_collector.collect()
        site["debug"] = False
        generate_site(site)

if __name__ == "__main__":
    main()