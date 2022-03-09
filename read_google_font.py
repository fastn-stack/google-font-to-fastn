import sys
import requests
import os


def get_url(comment, ff, fs, fw, src):
    if comment == None:
        return None
    file_name = "-".join([ff.strip(), fw.strip(), fs.strip(), comment.strip()]) + ".woff2"
    path = "./-/" + file_name
    if not os.path.exists('./-/'):
        os.makedirs('./-/')
    print (file_name, src)
    url = src.split(")")[0].replace("url(", "").strip()
    f = open(path, "w")
    req = requests.get(url)
    f.write(req.text)
    return "url(" + file_name + ")"



val = """
/* cyrillic-ext */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfCRc4AMP6lbBP.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C88, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfABc4AMP6lbBP.woff2) format('woff2');
  unicode-range: U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfCBc4AMP6lbBP.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfBxc4AMP6lbBP.woff2) format('woff2');
  unicode-range: U+0370-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfCxc4AMP6lbBP.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfChc4AMP6lbBP.woff2) format('woff2');
  unicode-range: U+0100-024F, U+0259, U+1E00-1EFF, U+2020, U+20A0-20AB, U+20AD-20CF, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Roboto';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(https://fonts.gstatic.com/s/roboto/v29/KFOlCnqEu92Fr1MmWUlfBBc4AMP6lQ.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
"""


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

-- fpm.package: foo

%s
    
""" % "\n\n\n".join(fonts)

f = open("FPM.ftd", "w")
f.write(content)




