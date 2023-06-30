'''
This is a simple script with class that allows you to read command line parameters
from XML file. Rather usefull for experiments.
'''
import argparse
import xml.etree.ElementTree as ET

class ExtendedArgumentParser(argparse.ArgumentParser):

    def __init__(self, config_argument='config_file' ,description=None):
        super().__init__(description)
        self.add_argument(f'--{config_argument}', type=str, default=None,
                          help='XML file with arguments')
        self.config_argument = config_argument

    def parse_args(self):
        args = super().parse_args()
        
        print(vars(args))

        try:
            defaults = self.parse_xml_file(getattr(args, self.config_argument))
            for arg in vars(args):
                if getattr(args, arg) is None and arg in defaults:
                    setattr(args, arg, defaults[arg])
        except KeyError:
            print('No config file given.')

        return args

    @staticmethod
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
    parser = ExtendedArgumentParser(description=__doc__)
    parser.add_argument('--param1', type=int, default=None, help='Parameter 1')
    parser.add_argument('--param2', type=float, default=None, help='Parameter 2')
    parser.add_argument('--param3', type=str, default=None, help='Parameter 3')

    args = parser.parse_args()

    # Print the parameter values
    print(f"param1: {args.param1}")
    print(f"param2: {args.param2}")
    print(f"param3: {args.param3}")

if __name__ == '__main__':
    main()
