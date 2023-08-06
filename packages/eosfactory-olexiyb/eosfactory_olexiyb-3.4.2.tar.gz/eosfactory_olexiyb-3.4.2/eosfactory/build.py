import argparse
import eosfactory.core.teos as teos

def build(
        contract_dir_hint,
        c_cpp_properties_path="", 
        compile_only=False, is_test_options=False, is_execute=False, silent=False):

    verbosity=[] if silent else None
    teos.build(
                        contract_dir_hint, c_cpp_properties_path, compile_only, 
                        is_test_options, is_execute, verbosity)

def main():
    '''Build a contract.

    usage: python3 -m eosfactory.build [-h] [--compile] [--silent] dir

    The contract is determined with its project directory. The directory may be
    absolute or relative to the *contract workspace* directory as defined with
    :func:`.core.config.contract_workspace_dir()`. If the *dir* argument is not set,
    it is substituted with the current working directory.

    The dependencies of the contract are determined with the json file given with the argument *c_cpp_prop* -- if it is set -- or with the file
    *.vscode/c_opp_properties.json* in the project's directory, otherwise.

    Args:
        dir: Contract name or directory.
        --c_cpp_prop: c_cpp_properties.json file path.        
        --compile: Do not build, compile only.
        --test_options: Use test options, not code ones.
        --execute: Execute the target.
        --silent: Do not print info.
        -h: Show help message and exit
    '''
    parser = argparse.ArgumentParser(description='''
    Build a contract.

    The contract is determined with its project directory. The directory may be
    absolute or relative to the *contract workspace* directory as defined with
    :func:`.core.config.contract_workspace_dir(). If the *dir* argument is not set,
    it is substituted with the current working directory.

    The dependencies of the contract are determined with the json file given with the argument *c_cpp_prop* -- if it is set -- or with the file
    *.vscode/c_opp_properties.json* in the project's directory, otherwise.
    ''')

    parser.add_argument("dir", help="Contract name or directory.")
    parser.add_argument(
        "--c_cpp_prop", help="c_cpp_properties.json file path.", default="")
    parser.add_argument(
        "--compile", help="Do not build, compile only.", action="store_true")
    parser.add_argument(
                        "--test_options", help="Use test options, not code ones", 
                        action="store_true")
    parser.add_argument(
                        "--execute", help="Execute the target", 
                        action="store_true")
    parser.add_argument(
        "--silent", help="Do not print info.", action="store_true")


    args = parser.parse_args()
    build(args.dir, args.c_cpp_prop, args.compile, args.test_options, args.execute,
    args.silent)    

if __name__ == '__main__':
    main()
