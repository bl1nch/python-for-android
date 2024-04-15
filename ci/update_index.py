import json
import sys


def load_index(json_file):
    try:
        with open(json_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_index(json_file, index):
    with open(json_file, "w") as f:
        json.dump(index, f, indent=4)


def main():
    if len(sys.argv) < 3:
        print("Specify json filename, package name and version")
        sys.exit(1)

    json_file = sys.argv[1]
    package_name = sys.argv[2]
    package_version = sys.argv[3]

    # Load index
    index = load_index(json_file)

    # updare index
    index[package_name] = package_version

    # Save index
    save_index(json_file, index)


if __name__ == "__main__":
    main()
