import os


def main():
    html_list = "<head><title>OpenAPI Documentation List</title></head><body><table><tr><th>Branch</th><th>Internal</th><th>External</th>"
    for x in os.walk("./public/"):
        trimmed = x[0].replace("./public/", "")
        if trimmed == "":
            continue

        line = "<tr><td>" + trimmed + "</td><td><a href=\"" + trimmed + "\">Internal</a></td><td><a href=\"" + trimmed + "/externalVersion.html\">External</a></td></tr>"
        html_list = html_list + line
    html_list = html_list + "</table></body>"

    text_file = open("index.html", "w")
    text_file.write(html_list)
    text_file.close()


main()
