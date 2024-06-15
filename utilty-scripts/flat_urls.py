import os
import json

with open(os.path.join("..", "data", "maven-urls", "maven-url.json"), "r") as file:
    urls = json.loads(file.read())

for dependency in urls:
    if isinstance(urls[dependency], list):
        flat_list = []
        for u in urls[dependency]:
            flat_list.append(u[1])
        urls[dependency] = flat_list

with open(os.path.join("..", "data", "maven-urls", "maven-url_flat.json"), "w") as file:
    file.write(json.dumps(urls))
