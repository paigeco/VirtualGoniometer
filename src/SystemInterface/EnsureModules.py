"""[ ensure that the necessary packages are installed ]"""

from os import access, path, W_OK, X_OK
import ctypes
from sys import exec_prefix, platform, executable
from subprocess import call, Popen, PIPE

def check_install() -> 'bool':
    #Sklearn and Scipy don't come preinstalled, so install them if they haven't been
    ############################################
    print(access(path.join(exec_prefix, "lib", "site-packages"), W_OK | X_OK))
    print(path.join(exec_prefix, "lib"))
    
    # QUESTIONABLE PACKAGES
    try:
        # Attempt an import
        import scipy # pylint: disable=unused-import, import-outside-toplevel
        import sklearn # pylint: disable=unused-import, import-outside-toplevel
        print("Both installed")
        return True
        
    except ModuleNotFoundError:
        print("INSTALLING")
        install_necessary_packages()
        return False

def install_necessary_packages(elevation_needed=False):
    
    if platform.startswith("win"):
        print(exec_prefix)
        windows_install = """echo 'Some packages will now be installed! It may take a few minutes...' && timeout 5 && "{}" -m pip install --prefix "{}" --force-reinstall --isolated --no-input --no-cache-dir -- scipy scikit-learn && exit""".format(executable, exec_prefix)
        
        if elevation_needed:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", "cmd", "/k " + windows_install, None, 1)
            quit()
            return

        else:
            try:
                print(windows_install)
                args = [
                    executable,
                    '-m',
                    'pip',
                    'install',
                    '--prefix',
                    exec_prefix,
                    '--force-reinstall',
                    '--no-input',
                    '--no-cache-dir',
                    '--upgrade',
                    'scipy',
                    'scikit-learn'
                ]
                process = call(args)
                print(process)
                #if stderr:
                    
                #    print('The process raised an error:', stderr.decode())
                    
                #else:
                #    print('Command works!')
                #    return
            except PermissionError:
                pass
        
        install_necessary_packages(elevation_needed=True)
            
        
    elif platform.startswith("linux"):
        
        linux_install = """cd {} && cd bin && ./pip3 install --upgrade pip scipy scikit-learn""".format(exec_prefix)
        
        commands = []
        
        # Check if install 
        if elevation_needed:
            commands.append("pkexec " + linux_install)
            commands.append("gksudo " + linux_install)
            commands.append("kdesudo " + linux_install)
            commands.append("sudo " + linux_install)
        else:
            # Run install without elevation
            commands.append(linux_install)
        
        for command in commands:
            process = Popen([command], stdout=PIPE, stderr=PIPE, shell=True)
            _, stderr = process.communicate()
            
            if stderr:
                print('The process raised an error: ', stderr.decode())
            else:
                print('Command works!')
                return
        
        install_necessary_packages(elevation_needed=True)
                
        
    
    elif platform.startswith("darwin"):
        # TODOS: Okay, so I don't have access to a MAC computer so uhh,
        #    I have no idea if this works
        
        apple_install = """cd {} && cd bin && ./pip3 install --upgrade pip scipy scikit-learn""".format(exec_prefix)
        
        commands = []
        
        if elevation_needed:
            pass
        else:
            process = Popen([apple_install], stdout=PIPE, stderr=PIPE, shell=True)
            _, stderr = process.communicate()
            
            if stderr:
                print('The process raised an error: ', stderr.decode())
            else:
                print('Command works!')
                return
        
        install_necessary_packages(elevation_needed=True)
