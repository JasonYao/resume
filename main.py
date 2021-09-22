# Library dependencies
from pyresume import load_data
from pyresume import template_data

# Project dependencies
from data import all_data


def run() -> None:
    loaded_data = load_data(all_data)
    templated_data = template_data(loaded_data)

    for templated_datum in templated_data:
        templated_datum.write()


if __name__ == '__main__':
    run()
