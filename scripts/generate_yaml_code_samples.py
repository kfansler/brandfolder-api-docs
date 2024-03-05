import argparse
import os
from os import path
import ruamel.yaml
from os import listdir
from os.path import isfile, join
import pathlib


def main():
    parser = argparse.ArgumentParser(description='Generate markup files for SDK examples')
    parser.add_argument('--masteryaml', dest='master_yaml', action='store', default='./generated/spec/openapi.yaml')
    parser.add_argument('--nodocs', dest="no_docs", action='store_true', default=False,
                        help='Omit non-API definition components from the generated spec file.')
    parser.add_argument('--snippets', dest='snippets_directory', action='store', default='./snippets',
                        help='Folder containing code examples')
    parser.add_argument('--output', dest='output_file', action='store',
                        default='./generated/openapi_with_examples.yaml',
                        help='Destination file for the OpenAPI file containing code examples')

    args = parser.parse_args()

    yaml = ruamel.yaml.YAML()
    with open(args.master_yaml, encoding="utf-8") as fp:
        data = yaml.load(fp)

    endpoints = get_subdirectories(args.snippets_directory)
    for endpoint in endpoints:
        formatted_endpoint = "/" + endpoint.replace('@', '/')
        if formatted_endpoint not in data["paths"]:
            print('sample ' + formatted_endpoint + ' has no corresponding spec entry, skipping all methods...')
            continue
        request_methods = get_subdirectories(args.snippets_directory + "/" + endpoint)
        for request_method in request_methods:
            if request_method not in data["paths"][formatted_endpoint]:
                print('sample ' + formatted_endpoint + ' ' + request_method + ' has no corresponding spec entry, skipping...')
                continue

            source_dir = args.snippets_directory + "/" + endpoint + "/" + request_method + "/"
            curl = get_code_sample(source_dir + "example.curl", "cURL")
            cs = get_code_sample(source_dir + "example.cs", "C#")
            java = get_code_sample(source_dir + "example.java", "Java")
            node_js = get_code_sample(source_dir + "example.js", "JavaScript", "Node.js")
            python = get_code_sample(source_dir + "example.py", "Python")
            ruby = get_code_sample(source_dir + "example.rb", "Ruby")

            samples = [curl, cs, java, node_js, python, ruby]
            samples = list(filter(None, samples))
            data["paths"][formatted_endpoint][request_method]["x-codeSamples"] = samples

    with open(args.output_file, 'w', encoding="utf-8") as fp:
        yaml.dump(data, fp)

    return 0


def get_code_sample(example_file, language, language_readable=None):
    if not path.exists(example_file):
        return None
    with open(example_file) as f:
        lines = f.readlines()
    flattened = ""
    for line in lines:
        flattened = flattened + line
    sample = {'lang': language, 'source': flattened}
    if language_readable is not None:
        sample['label'] = language_readable
    return sample


def get_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


main()
