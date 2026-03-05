#!/usr/bin/env python3
import argparse
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.core.converter import MD2WordConverter

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown to Word using a template.")
    parser.add_argument('input_file', help="Path to input Markdown file")
    parser.add_argument('--template', required=True, help="Path to template Word file")
    parser.add_argument('--output', required=True, help="Path to output Word file")
    parser.add_argument('--data', help="Path to JSON data file for placeholders")

    args = parser.parse_args()

    data = {}
    if args.data:
        with open(args.data, 'r') as f:
            data = json.load(f)

    with open(args.input_file, 'r') as f:
        md_text = f.read()

    converter = MD2WordConverter(args.template)
    converter.generate(md_text, args.output, data)

if __name__ == "__main__":
    main()
