import sys
import requests
import os

package_name = "fifthtry.github.io/roboto"
name = "roboto"

def get_url(comment, ff, fs, fw, src):
    if comment == None:
        return None
    file_name = "-".join([ff.strip(), fw.strip(), fs.strip(), comment.strip()]) + ".woff2"
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
        elif state == "ff":
            ff = line.split(":")[1].replace("'", "").replace(";", "").strip()
            state = "fs"
            continue
        elif state == "fs":
            fs = line.split(":")[1].replace("'", "").replace(";", "").strip()
            state = "fw"
            continue
        elif state == "fw":
            fw = line.split(":")[1].replace("'", "").replace(";", "").strip()
            state = "fd"
            continue
        elif state == "fd":
            fd = line.split(":")[1].replace("'", "").replace(";", "").strip()
            state = "src"
            continue
        elif state == "src":
            src = ":".join(line.split(":")[1:]).strip()
            state = "ur"
            continue
        elif state == "ur":
            ur = line.split(":")[1].replace("'", "").replace(";", "").strip()


    gurl = get_url(comment, ff, fs, fw, src)
    if gurl == None:
        continue

    font = """
-- fpm.font: %s
style: %s
weight: %s
woff2: %s
unicode-range: %s
    """ % (ff, fs, fw, gurl, ur)

    fonts.append(font)

content = """-- import: fpm

-- fpm.package: %s
zip: github.com/fifthtry/%s/archive/refs/heads/main.zip

%s
    
""" % (package_name, name, "\n\n\n".join(fonts))

f = open("FPM.ftd", "w")
f.write(content)




