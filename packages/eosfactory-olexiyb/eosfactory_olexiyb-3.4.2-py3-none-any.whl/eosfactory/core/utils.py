import time
import os
import shutil
import threading
import subprocess

import eosfactory.core.errors as errors

def wslMapLinuxWindows(path, back_slash=True):
    if not path or path.find("/mnt/") != 0:
        return path
    path = path[5].upper() + ":" + path[6:]
    if back_slash:
        path = path.replace("/", r"\\")
    return path


def wslMapWindowsLinux(path):
    if path.find(":") == -1:
        return path
    path = path.replace("\\", "/")
    drive = path[0]
    return path.replace(drive + ":/", "/mnt/" + drive.lower() + "/")


def heredoc(message):
    from textwrap import dedent
    message = dedent(message).strip()
    message.replace("<br>", "\n")
    return message


def spawn(command_line, error_message='', shell=False, raise_exception=True):
    stdout = None
    stderr = None
    try:
        p = subprocess.run(
            command_line,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        stdout = p.stdout.decode("ISO-8859-1").strip()
        stderr = p.stderr.decode("ISO-8859-1").strip()          
    except Exception as e:
        stderr = str(e)

    if raise_exception:
        if stderr:
            raise errors.Error('''
    {}

    command line:
    =============
    {}

    error message:
    ==============
    {}
            '''.format(error_message, " ".join(command_line), stderr),
            translate=False)

        return stdout
    else:
        return (stdout, stderr)

UBUNTU = "Ubuntu"
DARWIN = "Darwin"
OTHER_OS = None

def os_version():
    version = spawn(["uname", "-v"])
    if "Microsoft" in version or "ubuntu" in version:
        return UBUNTU
    if "Darwin" in version:
        return DARWIN
    return OTHER_OS


def is_windows_ubuntu():
    return "Microsoft" in spawn(["uname", "-v"])


def which(file_path):
    return spawn("which {}".format(file_path), shell=True)


def long_process(command_line, build_dir=None, is_verbose=True, prompt=None, 
                                shell=False):
    stop = False
    PERIOD = 2

    def thread_function():
        if prompt:
            print("{}: ".format(prompt), end="", flush=True)
        while True:
            print(".", end="", flush=True)
            time.sleep(PERIOD)
            if stop:
                break

    cwd = None
    if build_dir:
        cwd = os.path.join(build_dir, "cwd")
        if os.path.exists(cwd):
            try:
                shutil.rmtree(cwd)
            except Exception as e:
                raise errors.Error('''
Cannot remove the directory {}.
error message:
==============
{}
                '''.format(cwd, str(e)))
        os.mkdir(cwd)

    threading.Thread(target=thread_function).start()
    try:
        p = subprocess.run(
            command_line,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    except Exception as e:
        stop = True
        time.sleep(PERIOD)
        print(str(e))
        exit()

    stop = True
    time.sleep(PERIOD)
    print()
    stdout = p.stdout.decode("ISO-8859-1")
    stderr = p.stderr.decode("ISO-8859-1")
    returncode = p.returncode
    if is_verbose:
        print(stdout)
    if cwd:
        shutil.rmtree(cwd)

    if returncode:
        raise errors.Error('''
command line:
=============
{}

error message:
==============
{}
        '''.format(" ".join(command_line), stderr))

    return p


def locate(start_dir, partial_path):
    cl = ["find", start_dir, "-wholename", '"*{}"'.format(partial_path)]
    p = long_process(" ".join(cl), None, False, 
                    "locating '{}'".format(partial_path), True)
    stdout = p.stdout.decode("ISO-8859-1")
    if stdout:
        return stdout.strip()
    
    return ""


def project_zip():
    # from zipfile_infolist import print_info
    import zipfile

    zip_file = '/mnt/c/Workspaces/EOS/contracts/examples/project_zip.zip'
    with zipfile.ZipFile(zip_file, mode='w') as zf:
        print('adding README.txt')
        zf.write('/mnt/c/Workspaces/EOS/contracts/examples/fund/build/fund.abi')




    # print('creating archive')
    # zf = zipfile.ZipFile(zip_file, mode='w')
    # try:
    #     for f in "/mnt/c/Workspaces/EOS/contracts/examples/fund/build":
    #         print("adding {}".format(f))
    #         zf.write(f)
    # finally:
    #     print('closing') 
    #     zf.close()

    # print(print_info(zip_file))






    # zip_file = "/mnt/c/Workspaces/EOS/contracts/examples/project_zip.zip"
    # zip_object = zipfile.ZipFile(zip_file, 'w')
    # for f in "/mnt/c/Workspaces/EOS/contracts/examples/fund":
    #     zip_object.write(f)
