import os
import re
import sys

template_file_path = sys.argv[1]
templates_base_dir_path = sys.argv[2]
out_file_path = sys.argv[3]

def read_file(file_path):
    with open(file_path) as the_file:
        return the_file.read()

template = read_file(template_file_path)

tokens = re.findall(r"{.+}", template)

for token in tokens:
    text_file_path = templates_base_dir_path + "/" + token.replace("{", "").replace("}", "")

    if os.path.exists(text_file_path):
        text = read_file(text_file_path).rstrip("\n")
        template = template.replace(token, text)
    else:
        print("Template {} has a token of {}. No file exists at {}.".format(template_file_path, token, text_file_path))

with open(out_file_path, 'w') as out_file:
    out_file.write(template)
