import urllib.request
import re

urls = [
    "https://gist.github.com/KaushikShresth07/037cad9ce160a79c96aca13c626baad5",
    "https://gist.github.com/KaushikShresth07/069e6bef5092e86913c1ca3282533cd8",
    "https://gist.github.com/KaushikShresth07/09b2a40d6fe51bd95ef22025bd44a89b",
    "https://gist.github.com/KaushikShresth07/20a420ecfd0a262678b71054cb54b8a8",
    "https://gist.github.com/KaushikShresth07/352a919999797b9c8b1620d6ed840625",
    "https://gist.github.com/KaushikShresth07/37ecffe2dc153e984c47950509502d51",
    "https://gist.github.com/KaushikShresth07/396193cd1567bc3fbfdc1c3ba0a84369",
    "https://gist.github.com/KaushikShresth07/41380960cd4215dae438077b2f10f12c",
    "https://gist.github.com/KaushikShresth07/678f480a8c52a3b6b8fc5ea230fd756d",
    "https://gist.github.com/KaushikShresth07/800cdadb4b24722ca15d09eec55ab4d6",
    "https://gist.github.com/KaushikShresth07/97475d5178d29b12f84c45945f9858e7",
    "https://gist.github.com/KaushikShresth07/99e8c898c449d7b884dce9ed88d3becb",
    "https://gist.github.com/KaushikShresth07/9a6a68869f50d50e2d3cc4b622f6967c",
    "https://gist.github.com/KaushikShresth07/9ed9361c7852f1ef5ef73f540cb46208",
    "https://gist.github.com/KaushikShresth07/a9837995c3e43a1ad4de50f30ee173cf",
    "https://gist.github.com/KaushikShresth07/ad1b3659136d7ecf3e4777c0210c68d3",
    "https://gist.github.com/KaushikShresth07/b0d9e1c7e0a8dc1263299ef57a4b80d5",
    "https://gist.github.com/KaushikShresth07/e15fccfc1d0da828587d4bfc79ad2100",
    "https://gist.github.com/KaushikShresth07/e4e6c6697450402e9e028017f30de318",
    "https://gist.github.com/KaushikShresth07/e6a5727f48a6192501c685fe5cff4fb5",
    "https://gist.github.com/KaushikShresth07/f17a01594763df25a5f3115a929f8b06",
    "https://gist.github.com/KaushikShresth07/f80156920ff2aa122cf7e54677986adb",
    "https://gist.github.com/KaushikShresth07/fe0c7af6b700c183c257f65a62aa84de"
]

imports = set()
def_funcs = set()
keywords = set()

for url in urls:
    try:
        req = urllib.request.Request(url + "/raw", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            code = response.read().decode('utf-8')
            for line in code.split('\n'):
                line = line.strip()
                if line.startswith('import ') or line.startswith('from '):
                    imports.add(line.split()[1].split('.')[0])
                elif line.startswith('def '):
                    def_funcs.add(line.split('(')[0].replace('def ', ''))
                elif "in query" in line or "in command" in line or "in self.query" in line:
                    match = re.search(r"'(.*?)'", line)
                    if match:
                        keywords.add(match.group(1))
    except Exception as e:
        pass

print("LIBRARIES:", ", ".join(list(imports)[:20]))
print("FUNCTIONS:", ", ".join(list(def_funcs)[:20]))
print("FEATURES/KEYWORDS:", ", ".join(list(keywords)[:30]))
