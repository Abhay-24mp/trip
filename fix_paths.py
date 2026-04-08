import os
import re

templates_dir = "Trip_Flask/templates"

for filename in os.listdir(templates_dir):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # replace {{ request.getContextPath() }}/css with /static/css
    content = content.replace("{{ request.getContextPath() }}/css", "/static/css")
    content = content.replace("{{ request.getContextPath() }}/js", "/static/js")
    content = content.replace("{{ request.getContextPath() }}/fonts", "/static/fonts")
    content = content.replace("{{ request.getContextPath() }}/assets", "/static/assets")
    content = content.replace("{{ request.getContextPath() }}/", "/")
    content = content.replace("{{ request.getContextPath() }}", "")
    
    # replace css/style.css with /static/css/style.css if not already
    content = re.sub(r'href="css/([^"]+)"', r'href="/static/css/\1"', content)
    content = re.sub(r'src="css/([^"]+)"', r'src="/static/css/\1"', content)
    content = re.sub(r'src="js/([^"]+)"', r'src="/static/js/\1"', content)
    
    # replace any .jsp links with .html links
    content = re.sub(r'href="([^"]+?)\.jsp"', r'href="\1"', content) # wait, Flask uses routes like /buses, usually without .html. 
    # But since it's an existing app, I can map routes to either include .html or not. I'll just map /some.html to rendering some.html for static pages.

    with open(filepath, "w") as f:
        f.write(content)

