# Include standard modules
import argparse

# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("--width", "-w", help="set output width")

# Read arguments from the command line
args = parser.parse_args()

# Check for --width
if args.width:
    print("Set output width to %s" % args.width)