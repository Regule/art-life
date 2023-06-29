
import argparse
import xml.etree.ElementTree as ET

class ExtendedArgumentParser(argparse.ArgumentParser):

    def __init__(self, config_argument='config_file' description=None):
        super().__init__(description)
        self.add_argument(f'--{config_argument}', type=str, default=None,
                          help='XML file with arguments')
        self.config_argument = config_file

    def parse_args(self):
        arguments = super().parse_args()

        try:
            defaults = parse_xml_file(args[config_argument])
            for arg in vars(args):
                if getattr(args, arg) is None and arg in defaults:
                    setattr(args, arg, defaults[arg])


def parse_xml_file(xml_file):
    defaults = {}
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for param in root.findall('param'):
            name = param.get('name')
            value = param.get('value')
            defaults[name] = value
    except ET.ParseError:
        print("Error parsing XML file.")
    return defaults

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('--param1', type=int, default=None, help='Parameter 1')
    parser.add_argument('--param2', type=float, default=None, help='Parameter 2')
    parser.add_argument('--param3', type=str, default=None, help='Parameter 3')
    parser.add_argument('--xml', type=str, default=None, help='XML file path')

    args = parser.parse_args()

    # Read default values from XML file if provided
    if args.xml:
        defaults = parse_xml_file(args.xml)
        for arg in vars(args):
            if getattr(args, arg) is None and arg in defaults:
                setattr(args, arg, defaults[arg])

    # Print the parameter values
    print(f"param1: {args.param1}")
    print(f"param2: {args.param2}")
    print(f"param3: {args.param3}")

if __name__ == '__main__':
    main()
