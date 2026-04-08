import re
import os

templates_dir = "Trip_Flask/templates"

# Convert hotels.html
filepath = os.path.join(templates_dir, "hotels.html")
with open(filepath, "r") as f:
    content = f.read()

# remove DB logic entirely and expect `hotels` to be passed from Flask
content = re.sub(r'<%[\s\S]*?hotels\.add\(h\);\s*\}\s*con\.close\(\);\s*\}catch\(Exception e\)\{ out\.println\(e\.getMessage\(\)\);\ \}\s*%>', '', content)
content = re.sub(r'<%\s*for\(Map<String,String> h:hotels\){\s*%>', '{% for h in hotels %}', content)
content = re.sub(r'<%\s*}\s*%>', '{% endfor %}', content)
content = re.sub(r'\{\{\s*h\.get\("([^"]+)"\)\s*\}\}', r'{{ h.\1 }}', content)
content = re.sub(r'hotels\.jsp', 'hotels', content)

# Drop the selected hotel logic since we can pass it from flask or use javascript url parsing
content = re.sub(r'<%\s*String selectedHotel = request\.getParameter\("hotel"\);\s*for\(Map<String,String> h:hotels\){\s*%>', '{% for h in hotels %}', content)
content = re.sub(r'\{\{\s*h\.name\.equals\(selectedHotel\)\ \?\ "selected"\ :\ ""\s*\}\}', '{% if h.name == selected_hotel %}selected{% endif %}', content)


with open(filepath, "w") as f:
    f.write(content)

# Convert bookingHistory.html
filepath = os.path.join(templates_dir, "bookingHistory.html")
with open(filepath, "r") as f:
    content = f.read()

content = re.sub(r'<%\s*ArrayList<String\[\]> history = \(ArrayList<String\[\]>\) request\.getAttribute\("history"\);\s*if\(history != null && !history\.isEmpty\(\)\){\s*for\(String\[\] h : history\){\s*%>', '{% if history %}\n{% for h in history %}', content)
content = re.sub(r'<%\s*}\s*} else {\s*%>', '{% endfor %}\n{% else %}', content)
content = re.sub(r'<%\s*}\s*%>', '{% endif %}', content)
content = re.sub(r'<%=\s*(.*?)\s*%>', r'{{ \1 }}', content)

with open(filepath, "w") as f:
    f.write(content)

