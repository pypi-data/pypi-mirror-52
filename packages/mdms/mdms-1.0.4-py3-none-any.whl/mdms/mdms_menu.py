#!/usr/bin/env python3
import subprocess
import os
import sys
import platform
import mdms.initial_struc
import mdms.topology_prep
import mdms.run_simulations
import mdms.amber_parameters
from pathlib import Path

# testing Python version
if sys.version_info < (3, 6):
    raise RuntimeError("MDMS works best Python 3.6 or later. The current"
                       " Python version is %s installed in %s. Consider "
                       " upgrading Python prior to MDMS usage."
                       % (platform.python_version(), sys.executable))

# testing if AmberTools is installed silently
try:
    # pdb4amber test - running it and checking output if it contains string is enough
    subprocess.run(['pdb4amber > out_1.txt 2>&1'], shell=True)
    if 'age: pdb4amber' not in open('out_1.txt').read():
        raise Exception
    # sander test - run without any input, but if it is available specific error will appear
    subprocess.run(['sander -O > out_2.txt 2>&1'], shell=True)
    if 'File "mdin"' not in open('out_2.txt').read():
        raise Exception
    # check if output from running tleap has 'Welcome to LEaP!' string
    with open('tleap_test.in', 'w') as file:
        file.write('quit')
    subprocess.run(['tleap -f tleap_test.in > out_3.txt 2>&1'], shell=True)
    if 'Welcome to LEaP!' not in open('out_3.txt').read():
        raise Exception
    # removing files that were required for tests
    os.remove(Path('tleap_test.in'))
    os.remove(Path('out_1.txt'))
    os.remove(Path('out_2.txt'))
    os.remove(Path('out_3.txt'))
except:
    print('It seems as AmberTools with its components (pdb4amber and tleap in particular) are not installed properly.\n'
          'Please, prior to using MDMS make sure that AmberTools is running properly.')

print(
    "\nHello and welcome to Molecular Dynamics Made Simple (MDMS) created by Szymon Zaczek!\n"
    "This piece of software makes running Molecular Dynamics easy and straightforward, allowing non-experts "
    "in the field of computational chemistry to use Amber\n- one of the most renowned Molecular Dynamics packages available.\n"
    "If you use MDMS in your work, please, consider acknowledging my work by citing the original paper: xxx.\n"
    "If you have any suggestions, queries, bug reports or simply questions about how to proceed with your work using "
    "MDMS, please, contact me at: "
    "szymon.zaczek@edu.p.lodz.pl\n"
    "MDMS aids in preparing and running classical Molecular Dynamics. Nonetheless, such simulations might sometimes"
    " not sample the phase space enough to provide statistically relevant results within nanoseconds time scale. For such cases, "
    "the use of enhanced sampling methods is strongly encouraged. In future releases, it will be possible to run "
    "such simulations directly from within MDMS, but for now, if you decide to use them, you will need to manually modify"
    " files controlling simulations after they will be generated.\n\n")

USER_CHOICE_MENU = """\nPlease specify, what you would like to do:
- press 'p' for establishing the protein (or protein-ligand complex) initial structure
- press 't' for preparing topology and coordinate files for Amber, which are necessary for running MD simulations
- press 'i' for preparing Amber input files - they contain parameters for your simulations
- press 'r' for running simulations
- press 'q' in order to quit
Please, provide your choice: """


def menu():
    while True:
        try:
            user_input_menu = str(input(USER_CHOICE_MENU)).lower()
            if user_input_menu == 'p':
                print(
                    '\nYou will be getting an initial structure for your system. Buckle up!\n')
                mdms.initial_struc.queue_methods()
                print(
                    '\nYou have completed the first step required for running MD simulations. Congratulations!')
            elif user_input_menu == 't':
                print(
                    '\nYou will obtain topology and coordinate files for Amber. Buckle up!\n')
                mdms.topology_prep.queue_methods()
                print(
                    '\nYou have completed the next step required for running MD simulations. Congratulations\n')
            elif user_input_menu == 'i':
                print(
                    '\nYou will be obtaining input files for Amber, which will control your simulations. Buckle up!\n')
                mdms.amber_parameters.queue_methods()
                print(
                    '\nYou have managed to obtain input Amber input parameters. Get ready for starting your calculations!\n')
            elif user_input_menu == 'r':
                print('\nYou will be guided on how to run your simulations. Buckle up!\n')
                mdms.run_simulations.queue_methods()
            elif user_input_menu == 'q' or user_input_menu == 'quit':
                print('\nGood luck with your endeavors and have a great day!\n')
                break
            else:
                print('Please, provide one of the available options.')
        except BaseException:
            print('Please, provide a valid input.')


#menu()

