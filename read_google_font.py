import sys
import requests
import os

package_name = "fifthtry.github.io/opensans"
repo = "opensans"

def get_url(comment, ff, fs, fw, src):
    if comment == None:
        return None
    file_name = "-".join([ff, fw, fs, comment]).replace(" ", "-") + ".woff2"
    path = "./static/" + file_name
    if not os.path.exists('./static/'):
        os.makedirs('./static/')
    print ("Processing...", file_name)
    url = src.split(")")[0].replace("url(", "").strip()
    f = open(path, "wb")
    req = requests.get(url)
    f.write(req.content)
    return "-/" + package_name + "/static/" + file_name


font_txt = open("font.txt")
val = font_txt.read()
fonts = []
for doc in val.split("}"):
    comment = None
    ff = None
    fs = None
    fw = None
    fstretch = None
    fd = None
    src = None
    ur = None
    state = "C"

    for line in doc.splitlines():
        if line == "@font-face {" or len(line.strip()) == 0:
            continue
        if state == "C":
            comment = line.strip("/*").strip()
            state = "ff"
            continue
        name = line.split(":")[0].strip()
        if name == "font-family":
            ff = line.split(":")[1].replace("'", "").replace(";", "").strip().replace(" ", "-")
        elif name == "font-style":
            fs = line.split(":")[1].replace("'", "").replace(";", "").strip()
        elif name == "font-weight":
            fw = line.split(":")[1].replace("'", "").replace(";", "").strip()
        elif name == "font-stretch":
            fstretch = line.split(":")[1].replace("'", "").replace(";", "").strip()
        elif name == "font-display":
            fd = line.split(":")[1].replace("'", "").replace(";", "").strip()
        elif name == "src":
            src = ":".join(line.split(":")[1:]).strip()
        elif name == "unicode-range":
            ur = line.split(":")[1].replace("'", "").replace(";", "").strip()


    gurl = get_url(comment, ff, fs, fw, src)
    if gurl == None:
        continue

    font = """
-- fastn.font: %s
style: %s
weight: %s
woff2: %s
unicode-range: %s
""" % (ff, fs, fw, gurl, ur)

    if fstretch != None:
        font += "stretch: " + fstretch

    fonts.append(font)

content = """-- import: fastn

-- fastn.package: %s
zip: github.com/fifthtry/%s/archive/refs/heads/main.zip

%s
    
""" % (package_name, repo, "\n\n\n".join(fonts))

f = open("FASTN.ftd", "w")
f.write(content)




