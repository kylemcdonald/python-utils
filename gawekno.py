# this util for generate directory with structure project
# just type : python gawekno.py [module name] [version]
# example : python gawekno.py account v1

import sys
import os

def main():

    if len(sys.argv) != 3:
        print("Wrong format : python gawekno.py [module name] [version]")
        os._exit(1)

    try:
        module_dir = 'src'
        tests_dir = 'tests'

        main_dir_module = '{}/{}'.format(str(module_dir), str(sys.argv[1]))
        main_dir_tests = '{}/{}'.format(str(tests_dir), str(sys.argv[1]))

        version_module = main_dir_module + '/{}'.format(str(sys.argv[2]))
        version_tests = main_dir_tests + '/{}'.format(str(sys.argv[2]))

        sub_dir = ['delivery', 'domain', 'repository', 'serializers', 'usecase', 'validator']

        for d in sub_dir:
            dir_location_module = '{}/{}'.format(version_module, d)
            dir_location_tests = '{}/{}'.format(version_tests, d)

            os.makedirs(dir_location_module)
            open("{}/__init__.py".format(dir_location_module), "w+")

            os.makedirs(dir_location_tests)
            open("{}/__init__.py".format(dir_location_tests), "w+")

        open("{}/__init__.py".format(main_dir_module), "w+")
        open("{}/__init__.py".format(main_dir_tests), "w+")

        open("{}/__init__.py".format(version_module), "w+")
        open("{}/__init__.py".format(version_tests), "w+")

        print("====Sukses Coy====")

    except Exception as e:

        print("====Gagal Coy====")
        print(str(e))

if __name__ == '__main__':
    main()