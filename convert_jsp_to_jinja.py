import re
import os

templates_dir = "Trip_Flask/templates"

for filename in os.listdir(templates_dir):
    if not filename.endswith(".html"):
        continue
    filepath = os.path.join(templates_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()

    # If it has JSP imports, it's a dynamic file
    if "<%@" in content or "<%" in content:
        print(f"Converting {filename}...")
        
        # Remove Page directives
        content = re.sub(r'<%@\s*page.*?%>', '', content, flags=re.IGNORECASE)
        
        # Convert <%= var %> to {{ var }}
        content = re.sub(r'<%=\s*(.*?)\s*%>', r'{{ \1 }}', content)
        
        # For busList.html
        if filename == "busList.html":
            content = re.sub(r'<%\s*ArrayList<String\[\]> buses.*?\s*if \(buses != null.*?\)\s*\{\s*for \(String\[\] b : buses\)\s*\{\s*int price = Integer\.parseInt\(b\[9\]\).*?%>', 
                             '{% if buses %}\n{% for b in buses %}\n{% set price = b[9]|int %}', content, flags=re.DOTALL)
            content = re.sub(r'<%\s*\}\s*\}\s*else\s*\{\s*%>', '{% endfor %}\n{% else %}', content, flags=re.DOTALL)
            content = re.sub(r'<%\s*\}\s*%>', '{% endif %}', content, flags=re.DOTALL)
            
        # For carList.html
        elif filename == "carList.html":
            content = re.sub(r'<%\s*ArrayList<String\[\]> cars.*?\s*if\(cars != null.*?\)\{\s*for\(String\[\] c : cars\)\{\s*int price = Integer\.parseInt\(c\[3\]\).*?%>',
                             '{% if cars %}\n{% for c in cars %}\n{% set price = c[3]|int %}', content, flags=re.DOTALL)
            content = re.sub(r'<%\s*\}\s*\}else\{\s*%>', '{% endfor %}\n{% else %}', content, flags=re.DOTALL)
            content = re.sub(r'<%\s*\}\s*%>', '{% endif %}', content, flags=re.DOTALL)
            
        with open(filepath, "w") as f:
            f.write(content)

