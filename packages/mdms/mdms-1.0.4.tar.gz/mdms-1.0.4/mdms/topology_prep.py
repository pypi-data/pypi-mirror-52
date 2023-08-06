import os
import pandas as pd
import re
import subprocess
import readline
import fileinput
from pathlib import Path

# allowing tab completion of files' paths
readline.parse_and_bind("tab: complete")

# test if pdb4amber works
try:
    # global is declared - it will be checked upon when pdb4amber is supposed to start
    global pdb4amber_test
    # pdb4amber test - running it and checking output if it contains string is enough
    subprocess.run(['pdb4amber > out_1.txt 2>&1'], shell=True)
    if 'age: pdb4amber' not in open('out_1.txt').read():
        raise Exception
    pdb4amber_test = True
    # removing files that were required for tests
    os.remove(Path('out_1.txt'))
except:
    pdb4amber_test = False

def file_naming():
    # getting name for a control file, which will containg all info
    global filename
    while True:
        try:
            filename_inp: str = Path(input('Please, provide a path to the file that contains every piece of information for running MDMS (it should be already generated):\n'))
            filename = filename_inp
            if filename.exists():
                break
            else:
                print('There is no such file.')
        except BaseException:
            print('Please, provide valid input')


def save_to_file(content, filename):
    # saving to a control file
    with open(filename, 'a') as file:
        file.write(content)


def read_file(filename):
    # reading files
    with open(filename, 'r') as file:
        return file.read()


def file_check(file):
    # checking, if a file exists
    test = file.exists()
    return test


def stop_interface():
    # enforce stopping the entire interface
    global stop_generator
    stop_generator = True


def clearing_control():
    # this function clears control file from what will be inputted with topology_prep run
    # name of temporary file that will store what is important
    filetemp = 'temp.txt'
    # list of parameters that will be stripped out of control file
    parameters = [
        'charge_model',
        'atoms_type',
        'ligands_charges',
        'ligands_multiplicities',
        'prot_ff',
        'wat_ff',
        'top_name',
        'box_size'
        ]
    # writing content of control file without parameters in parameters list to
    # the temporary file
    with open(f"{filename}") as oldfile, open(filetemp, 'w') as newfile:
        for line in oldfile:
            if not any(parameters in line for parameters in parameters):
                newfile.write(line)
    # replacing control file with temporary file
    os.replace(filetemp, filename)


def clearing_control_mcpb():
    # this function clears control file after the original run of mcpb.py
    filetemp = 'temp.txt'
    # list of parameters that will be stripped out of control file
    parameters = [
        'prot_ff',
        'wat_ff',
        'top_name',
        'box_size'
        ]
    # writing content of control file without parameters in parameters list to
    # the temporary file
    with open(f"{filename}") as oldfile, open(filetemp, 'w') as newfile:
        for line in oldfile:
            if not any(parameters in line for parameters in parameters):
                newfile.write(line)
    # replacing control file with temporary file
    os.replace(filetemp, filename)


def hydrogen_check():
    # Checking if hydrogens are added to ligands file
    control = read_file(filename)
    ligands = r'ligands\s*=\s*\[(.*)\]'
    ligands_match = re.search(ligands, control)
    # if there are ligands, following clause will be executed
    if ligands_match:
        # taking only ligands entries
        ligands_match = ligands_match.group(1)
        # removing quotes from string
        ligands_string = ligands_match.replace("'", "")
        # removing whitespaces and turning string into a list
        ligands_list = re.sub(r'\s', '', ligands_string).split(',')
        # storing info about how many atoms are in ligands
        atoms_amount = []
        # storing info about how many hydrogen atoms are in ligands
        hydrogens_amount = []
        # following clause will be executed only if there are ligands in the
        # control file
        if ligands_list:
            for ligand in ligands_list:
                # reading 3rd column (pandas numbering - 2nd) from ligand.pdb -
                # if there are no hydrogens in residue names, there are no
                # hydrogens in the whole file
                df = pd.read_csv(f'{ligand}.pdb', header=None, delim_whitespace=True, usecols=[2], error_bad_lines=False)
                # getting info how many atoms are in a ligand
                df_len = len(df.iloc[:, 0])
                # storing info in list, which will contain info about all
                # ligands
                atoms_amount.append(df_len)
                # establishing if there are hydrogens in atom names
                hydrogen_match = (df[df.iloc[:, 0].str.match('H', na=False)])
                # counting how many hydrogens were in a ligand
                hydrogen_count = len(hydrogen_match.iloc[:, 0])
                # storing info about amount of hydrogens in a list
                hydrogens_amount.append(hydrogen_count)
            stop = False
            for x in range(0, len(ligands_list)):
                if hydrogens_amount[x] == 0:
                    USER_CHOICE_HYDROGENS = (f"\n!!WARNING!!\n"
                                             f"Even though there are {atoms_amount[x]} atoms in {ligands_list[x]} ligand, there are no "
                                             f"hydrogen atoms. Please keep in mind that all of the ligands MUST have all the "
                                             f"necessary hydrogen atoms in their structures. If you do not add chemically-"
                                             f"relevant hydrogen atoms to your ligands, your MD simulations will provide "
                                             f"unrealistic insight.\n"
                                             f"Are you sure that {ligands_list[x]} ligand should not have any hydrogen atoms?\n"
                                             f"- press 'y' to continue\n"
                                             f"- press 'n' to stop MDMS run\n")
                    while True:
                        try:
                            user_input_hydrogens = str(
                                input(USER_CHOICE_HYDROGENS).lower())
                            if user_input_hydrogens == 'y':
                                break
                            elif user_input_hydrogens == 'n':
                                stop = True
                                break
                        except BaseException:
                            print('Please, provide valid input')
                    if stop:
                        break
                    else:
                        pass
            if stop:
                stop_interface()


def ligands_parameters():
    # reading control file
    control = read_file(filename)
    # finding ligands residues in prep file
    ligands = r'ligands\s*=\s*\[(.*)\]'
    ligands_match = re.search(ligands, control)
    if ligands_match:
        # taking only ligands entries
        ligands_match = ligands_match.group(1)
        # removing quotes from string
        ligands_string = ligands_match.replace("'", "")
        # removing whitespaces and turning string into a list
        ligands_list = re.sub(r'\s', '', ligands_string).split(',')
        # getting necessary infor for antechamber input
        USER_CHOICE_CHARGE_MODEL = f"\nLigands' charges\n" \
            f"Please specify the charge model that you would like to apply to your ligands. If you want" \
            f"to employ RESP charges, you will need to manually modify antechamber input files.\n" \
            f"Please note that AM1-BCC charge model is a recommended choice.\n" \
            f"Following options are available:\n" \
            f"- 'bcc' - AM1-BCC charge model\n" \
            f"- 'mul' - Mulliken charge model\n" \
            f"Please, provide one of the options from available answers (single-quoted words specified above):\n"
        USER_CHOICE_ATOM_TYPES = f"\nLigands' force field\n" \
            f"Please, specify which atom types you would like to assign to your ligands.\n" \
            f"Please note that GAFF2 is a recommended choice.\n" \
            f"Following options are available:\n" \
            f"- 'gaff2' - General Amber Force Field, version 2\n" \
            f"- 'gaff' - General Amber Force Field, older version of GAFF2\n" \
        # the whole function will only do something, if ligands_list have
        # anything in it
        if ligands_list:
            # prompting user that he MUSTS have hydrogens already added to the
            # specifying charge model
            while True:
                try:
                    user_input_charge_model = str(
                        input(USER_CHOICE_CHARGE_MODEL).lower())
                    if user_input_charge_model == 'bcc':
                        charge_model = 'bcc'
                        break
                    elif user_input_charge_model == 'mul':
                        charge_model = 'mul'
                        break
                except BaseException:
                    print('The input that you have provided is not valid.')
            save_to_file(f"charge_model = {charge_model}\n", filename)
            # specifying atom types
            while True:
                try:
                    user_input_atom_types = str(
                        input(USER_CHOICE_ATOM_TYPES).lower())
                    if user_input_atom_types == 'gaff':
                        atoms_type = 'gaff'
                        break
                    elif user_input_atom_types == 'gaff2':
                        atoms_type = 'gaff2'
                        break
                except BaseException:
                    print('The input that you have provided is not valid')
            save_to_file(f"atoms_type = {atoms_type}\n", filename)
            # specifying charges and multiplicity for each ligand
            lig_charges = []
            lig_multiplicities = []
            for x in ligands_list:
                # those must be looped on, since each ligand might have different charge and multiplicity
                USER_CHOICE_CHARGE = f"Please, provide the net charge of {x} ligand (integer value):\n"
                while True:
                    # this loop gets info about ligands charges
                    try:
                        # this line already tests if input is integer
                        user_input_charge = int(input(USER_CHOICE_CHARGE))
                        lig_charges.append(user_input_charge)
                        break
                    except BaseException:
                        print("The input that you have provided is not valid")
            # once charges are known and good, they are put into control file
            save_to_file(f"ligands_charges = {lig_charges}\n", filename)
            for x in ligands_list:
                # this loop gets info about ligands multipicities
                USER_CHOICE_MULTIPLICITY = f"\nPlease, provide multiplicity of {x} ligand (positive integer value):\n"
                while True:
                    try:
                        # multiplicity must be integer but also must be
                        # positive
                        user_input_multiplicity = int(
                            input(USER_CHOICE_MULTIPLICITY))
                        if user_input_multiplicity < 1:
                            raise Exception
                        lig_multiplicities.append(user_input_multiplicity)
                        break
                    except BaseException:
                        print("The input that you have provided is not valid")
            # once multiplicity is good, its saved into control file
            save_to_file(f"ligands_multiplicities = {lig_multiplicities}\n", filename)


def antechamber_parmchk_input():
    # finding ligands residues in control file
    control = read_file(filename)
    ligands = r'ligands\s*=\s*\[(.*)\]'
    ligands_match = re.search(ligands, control)
    if ligands_match:
        # taking only ligands entries
        ligands_match = ligands_match.group(1)
        # removing quotes from string
        ligands_string = ligands_match.replace("'", "")
        # removing whitespaces and turning string into a list
        ligands_list = re.sub(r'\s', '', ligands_string).split(',')
        # getting charge_model info
        charge_model = r'charge_model\s*=\s*([a-z]*[A-Z]*[1-9]*)'
        charge_model_match = re.search(charge_model, control).group(1)
        # getting atom_types info
        atoms_type = r'atoms_type\s*=\s*([a-z]*[A-Z]*[1-9]*)'
        atoms_type_match = re.search(atoms_type, control).group(1)
        # finding ligands' charges in control file
        ligands_charges = r'ligands_charges\s*=\s*\[(.*)\]'
        ligands_charges_match = re.search(ligands_charges, control).group(1)
        # removing whitespaces and turning to a list
        ligands_charges_list = re.sub(
            r'\s', '', ligands_charges_match).split(',')
        # changing individual entries from string to integers
        for x in range(0, len(ligands_charges_list)):
            ligands_charges_list[x] = int(ligands_charges_list[x])
        # finding ligands multiplicities in control file
        ligands_multiplicities = r'ligands_multiplicities\s*=\s*\[(.*)\]'
        ligands_multiplicities_match = re.search(
            ligands_multiplicities, control).group(1)
        # removing whitespaces and turning to a list
        ligands_multiplicities_list = re.sub(
            r'\s', '', ligands_multiplicities_match).split(',')
        # changing individual entries from string to integers
        for x in range(0, len(ligands_multiplicities_list)):
            ligands_multiplicities_list[x] = int(
                ligands_multiplicities_list[x])
        # prior to to antechamber and parmchk execution, check ligands pdb with
        # pdb4amber
        # if pdb4amber works from MDMS, it is run automatically from MDMS
        if pdb4amber_test:
            for x in range(0, len(ligands_list)):
                # copying original ligand PDB file - output from pdb4amber will be
                # supplied to antechamber and parmchk
                ligand_copy = f"cp {ligands_list[x]}.pdb {ligands_list[x]}_prior_pdb4amber.pdb"
                subprocess.run([f"{ligand_copy}"], shell=True)
                # input for pdb4amber
                pdb4amber_input = f"pdb4amber -i {ligands_list[x]}_prior_pdb4amber.pdb -o {ligands_list[x]}.pdb "
                # running pdb4amber (both original and remade files are retained
                # but later on remade ligands will be operated on
                subprocess.run([f"{pdb4amber_input}"], shell=True)
                # if it doesn't input is saved to a file
        else:
            # try to find ligands_processing entry in the control file
            # try to find if there is a ligands_pdb4amber_inputs entry in the control file
            ligands_inputs = r'ligands_pdb4amber_inputs\s*=\s*\[(.*)\]'
            ligands_inputs_match = re.search(ligands_inputs, control)
            if ligands_inputs_match:
                # search for outputs from pdb4amber - they must have been processed manually; if they exist, everthing
                # is fine; if they don't print info on how to proceed again; every ligand in the list is checked
                for x in range(0, len(ligands_list)):
                    lig_path = Path(f'{ligands_list[x]}.pdb')
                    if lig_path.exists():
                        # processed pdb exists, so we might continue
                        continue
                    else:
                        print(f"\n!!WARNING!!\n"
                              f"\nYou have not processed ligands' files with pdb4amber yet\n"
                              f"There were some problems with running pdb4amber from within MDMS.\n"
                              f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                              f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                              f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                              f"your own installation of Python.\n"
                              f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                              f"interpreter (i. e. by loading the appropriate module).\n"
                              f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                              f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                              f"In such case, just copy the content of each line of ligand_pdb4amber.in file into terminal and press"
                              f"enter. As a result, you will obtain processed PDB ligands' file which will be ready for further"
                              f"steps.")
                        # just single printing of the prompt should be enough, therefore it is halted here
                        break
            else:
                print(f"\n!!WARNING!!\n"
                      f"There were some problems with running pdb4amber from within MDMS.\n"
                      f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                      f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                      f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                      f"your own installation of Python.\n"
                      f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                      f"interpreter (i. e. by loading the appropriate module).\n"
                      f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                      f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                      f"In such case, just copy the content of each line of ligand_pdb4amber.in file into terminal and press"
                      f"enter. As a result, you will obtain processed PDB ligands' file which will be ready for further"
                      f"steps.")
                pdb_process_input = ('ligand_pdb4amber.in')
                pdb_process_input_path = Path(pdb_process_input)
                if pdb_process_input_path.exists():
                    os.remove(pdb_process_input_path)
                for x in range(0, len(ligands_list)):
                    # copying original ligand PDB file - output from pdb4amber will be
                    # supplied to antechamber and parmchk
                    ligand_copy = f"cp {ligands_list[x]}_raw.pdb {ligands_list[x]}_prior_pdb4amber.pdb"
                    subprocess.run([f"{ligand_copy}"], shell=True)
                    # input for pdb4amber
                    pdb4amber_input = f"pdb4amber -i {ligands_list[x]}_prior_pdb4amber.pdb -o {ligands_list[x]}.pdb "
                    # input for pdb4amber appended to the file
                    with open(pdb_process_input, 'a') as file:
                        file.write(pdb4amber_input)
                print(f"\nYou will now be redirected to menu of MDMS. Please, quit MDMS and process ligands' PDB files"
                      f"from within the terminal."
                      f"Afer processing the file, proceed with topology preparation step within MDMS.\n")
                # saving info to the control file that pdb4amber was not run from within MDMS
                save_to_file(f"ligands_pdb4amber_inputs = True\n", filename)
                stop_interface()
        # creating antechamber and parmchk inputs
        for x in range(0, len(ligands_list)):
            antechamber_input = f"antechamber -fi pdb -fo mol2 -i {ligands_list[x]}.pdb -o {ligands_list[x]}.mol2 -at {atoms_type_match} -c {charge_model_match} -pf y -nc {ligands_charges_list[x]} -m {ligands_multiplicities_list[x]}"
            # running antechamber
            subprocess.run([f"{antechamber_input}"], shell=True)
            # checking if mol2 was successfully created
            mol2_path = Path(f'{ligands_list[x]}.mol2')
            if file_check(mol2_path) == False:
                # if mol2 was not created, loop stops and user is returned to
                # menu
                print(f"\nAntechamber has failed to determine atomic charges for {ligands_list[x]} ligand. Please, have a look"
                      f" at output files for more info.\n")
                break
            # input for parmchk
            parmchk_input = f"parmchk2 -i {ligands_list[x]}.mol2 -o {ligands_list[x]}.frcmod -f mol2 -s {atoms_type_match}"
            # running parmchk
            subprocess.run([f"{parmchk_input}"], shell=True)
            # checking if frcmod was successfully created
            frcmod_path = Path(f'{ligands_list[x]}.frcmod')
            if file_check(frcmod_path) == False:
                # if frcmod was not created, loop stops and user is returned to
                # menu
                print(f"\nParmchk has failed to run correctly for {ligands_list[x]} ligand. Please, check validity of"
                      f" {ligands_list[x]}.mol2 file.\n")
                break


def pdb_process():
    ## This function strips original PDB of anything apart from protein, checks its validity with pdb4amber and create
    ## PDB complex of protein and ligands, which will be passed onto tleap
    ## this will inform user what is being done
    print('\nRight now your PDB will be processed in order to ensure a proper working with Amber software. If there'
          ' are any missing atoms in amino acids, they will be automatically added with pdb4amber program.\n')
    ## reading pdb from control file
    control = read_file(filename)
    structure = r'pdb\s*=\s*(.*)'
    structure_match = re.search(structure, control).group(1)
    # stripping of extension from structure - this way it will be easier to
    # get proper names, i.e. 4zaf_old.pdb
    structure_match_split = structure_match.split('.')[0]
    # copying original PDB file so it will be retained after files operations
    struc_copy = f"cp {structure_match} {structure_match_split}_prior_pdb4amber.pdb"
    subprocess.run([f"{struc_copy}"], shell=True)
    # input for pdb4amber - ligands are removed
    # ADDING MISSING ATOMS WITH PDB4AMBER IS DISABLED NOW - WAS CAUSING PROBLEMS
    #pdb4amber_input = f"pdb4amber -i {structure_match_split}_prior_pdb4amber.pdb --add-missing-atoms -o {structure_match_split}_no_lig.pdb"
    pdb4amber_input = f"pdb4amber -i {structure_match_split}_prior_pdb4amber.pdb -p -o {structure_match_split}_no_lig.pdb"
    # running pdb4amber (both original and remade files are retained but later
    # on remade ligands will be operated on)
    # if pdb4amber works, it is run directly from MDMS
    if pdb4amber_test:
        # running pdb4amber (both original and remade files are retained
        # but later on remade ligands will be operated on
        subprocess.run([f"{pdb4amber_input}"], shell=True)
    else:
        protein_inputs = r'protein_pdb4amber_inputs\s*=\s*\[(.*)\]'
        protein_inputs_match = re.search(protein_inputs, control)
        if protein_inputs_match:
            # since protein_inputs_match is in the control file, MDMS has already got to this stage and user shoud've
            # already process the files
            prot_path = Path(f"{structure_match_split}_no_lig.pdb")
            if prot_path.exists():
                # protein was processed by the user, so everything is fine, program might proceed
                pass
            else:
                # even though pdb4amber inputs were created and user was asked to process them, he didn't do so -
                # therefore, he receives a prompt reminding what to do
                print(f"\n!!WARNING!!\n"
                      f"\nYou have not processed {structure_match_split}_prior_pdb4amber.pdb file with pdb4amber yet.\n"
                      f"Since there were some issues with running pdb4amber from within MDMS, you need to process "
                      f"{structure_match_split}_prior_pdb4amber.pdb with pdb4amber manually.\n"
                      f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                      f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                      f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                      f"your own installation of Python.\n"
                      f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                      f"interpreter (i. e. by loading the appropriate module).\n"
                      f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                      f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                      f"In such case, just copy the content of each line of protein_pdb4amber.in file into terminal and press"
                      f"enter. As a result, you will obtain processed PDB protein file which will be ready for further"
                      f"steps.")
                # user did not process PDB but he received another prompt on how to do so - it should be enough; program
                # is stopped so user can process PDB
                stop_interface()
                pass
        else:
            # there were problems with running pdb4amber and MDMS is run here for the first time
            print(f"\n!!WARNING!!\n"
                  f"There were some problems with running pdb4amber from within MDMS.\n"
                  f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                  f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                  f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                  f"your own installation of Python.\n"
                  f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                  f"interpreter (i. e. by loading the appropriate module).\n"
                  f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                  f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                  f"In such case, just copy the content of each line of protein_pdb4amber.in file into terminal and press"
                  f"enter. As a result, you will obtain processed PDB protein file which will be ready for further"
                  f"steps.")
            protein_process_input = ('protein_pdb4amber.in')
            protein_process_input_path = Path(protein_process_input)
            if protein_process_input_path.exists():
                os.remove(protein_process_input_path)
            # writing pdb4amber input
            with open(protein_process_input, 'w') as file:
                file.write(pdb4amber_input)
            print(f"\nYou will now be redirected to menu of MDMS. Please, quit MDMS and process the protein PDB file"
                  f"from within the terminal."
                  f"Afer processing the file, proceed with topology preparation step within MDMS.\n")
            save_to_file(f"protein_pdb4amber_inputs = True\n", filename)
            stop_interface()
    ## finding ligands residues in control file
    ligands = r'ligands\s*=\s*\[(.*)\]'
    ligands_match = re.search(ligands, control)
    # finding crystal waters residue in control file
    waters = r'waters\s*=\s*\[(.*)\]'
    waters_match = re.search(waters, control)
    # finding metal residues in control file
    metals = r'metals\s*=\s*\[(.*)\]'
    metals_match = re.search(metals, control)
    # creating list storing filenames that will create the whole complex
    full_files = []
    # protein without any ligands
    struc_no_lig = f"{structure_match_split}_no_lig.pdb"
    # protein filename appended
    full_files.append(struc_no_lig)
    if waters_match:
        # taking only residues names
        waters_match = waters_match.group(1)
        # removing quotes from string
        waters_string = waters_match.replace("'", "")
        # removing whitespaces and turning string into a list
        waters_list = re.sub(r'\s', '', waters_string).split(',')
        # formatting waters with pdb4amber
        if pdb4amber_test:
            # automatic run of pdb4amber
            for x in range(0, len(waters_list)):
                # copying original water PDB file
                water_copy = f"cp {waters_list[x]}_raw.pdb {waters_list[x]}_prior_pdb4amber.pdb"
                subprocess.run([f"{water_copy}"], shell=True)
                # input for pdb4amber
                pdb4amber_input = f"pdb4amber -i {waters_list[x]}_prior_pdb4amber.pdb -o {waters_list[x]}.pdb"
                # running pdb4amber - all files are retained though
                subprocess.run([f"{pdb4amber_input}"], shell=True)
                full_files.append(f'{waters_list[x]}.pdb')
            pass
        else:
            # manual run of pdb4amber
            # try to find if there is a water_pdb4amber_inputs entry in the control file
            water_inputs = r'ligands_pdb4amber_inputs\s*=\s*\[(.*)\]'
            water_inputs_match = re.search(water_inputs, control)
            if water_inputs_match:
                # search for outputs from pdb4amber - they must have been processed manually; if they exist, everthing
                # is fine; if they don't print info on how to proceed again
                for x in range(0, len(waters_list)):
                    wat_path = Path(f'{waters_list[x]}.pdb')
                    if wat_path.exists():
                        # processed pdb exists, we might continue to the next steps
                        continue
                    else:
                        print(f"\n!!WARNING!!\n"
                              f"\nYou have not processed water files with pdb4amber yet.\n"
                              f"There were some problems with running pdb4amber from within MDMS.\n"
                              f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                              f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                              f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                              f"your own installation of Python.\n"
                              f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                              f"interpreter (i. e. by loading the appropriate module).\n"
                              f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                              f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                              f"In such case, just copy the content of each line of water_pdb4amber.in file into terminal and press"
                              f"enter. As a result, you will obtain processed PDB water's file which will be ready for further"
                              f"steps.")
                        # just single printing of the prompt should be enough, therefore it is halted here
                        break
            else:
                # first run of this part - inputs for pdb4amber are created
                print(f"\n!!WARNING!!\n"
                      f"There were some problems with running pdb4amber from within MDMS.\n"
                      f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                      f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                      f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                      f"your own installation of Python.\n"
                      f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                      f"interpreter (i. e. by loading the appropriate module).\n"
                      f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                      f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                      f"In such case, just copy the content of each line of water_pdb4amber.in file into terminal and press"
                      f"enter. As a result, you will obtain processed PDB water's file which will be ready for further"
                      f"steps.")
                pdb_process_input = ('water_pdb4amber.in')
                pdb_process_input_path = Path(pdb_process_input)
                if pdb_process_input_path.exists():
                    os.remove(pdb_process_input_path)
                for x in range(0, len(waters_list)):
                    # copying original water PDB file
                    water_copy = f"cp {waters_list[x]}.pdb {waters_list[x]}_prior_pdb4amber.pdb"
                    subprocess.run([f"{water_copy}"], shell=True)
                    # input for pdb4amber
                    pdb4amber_input = f"pdb4amber -i {waters_list[x]}_prior_pdb4amber.pdb -o {waters_list[x]}.pdb"
                    # input for pdb4amber appended to the file
                    with open(pdb_process_input, 'a') as file:
                        file.write(pdb4amber_input)
                print(f"\nYou will now be redirected to menu of MDMS. Please, quit MDMS and process waters' PDB files"
                      f"from within the terminal."
                      f"Afer processing the file, proceed with topology preparation step within MDMS.\n")
                # saving info to the control file that pdb4amber was not run from within MDMS
                save_to_file(f"water_pdb4amber_inputs = True\n", filename)
                stop_interface()
    # finding crystal waters residue in control file
    if metals_match:
        # taking only ligands entries
        metals_match = metals_match.group(1)
        # removing quotes from string
        metals_string = metals_match.replace("'", "")
        # removing whitespaces and turning string into a list
        metals_list = re.sub(r'\s', '', metals_string).split(',')
        # creating a list that will store ligands filenames
        metals_files = []
        # appending ligands filenames to the list
        for metal in metals_list:
            metals_files.append(f"{metal}.pdb")
        # appending ligands filenames
        for metal in metals_files:
            full_files.append(metal)
    if ligands_match:
        # taking only ligands entries
        ligands_match = ligands_match.group(1)
        # removing quotes from string
        ligands_string = ligands_match.replace("'", "")
        # removing whitespaces and turning string into a list
        ligands_list = re.sub(r'\s', '', ligands_string).split(',')
        # creating a list that will store ligands filenames
        ligands_files = []
        # appending ligands filenames to the list
        for ligand in ligands_list:
            ligands_files.append(f"{ligand}.pdb")
        # appending ligands filenames
        for ligand in ligands_files:
            full_files.append(ligand)
    complex_raw = f"{structure_match_split}_raw.pdb"
    # using context manager to concatenate protein and ligands together
    with open(complex_raw, 'w') as outfile:
        # iterating over each file in full_files list
        for fname in full_files:
            # opening each file and writing it to outfile
            with open(fname) as infile:
                outfile.write(infile.read())
    # name of the pdb file that will be an input for tleap
    complex = f"{structure_match_split}_full.pdb"
    # processing protein-ligand complex pdb file with pdb4amber; hydrogen atoms are added to the protein
    # another round of pdb4amber - it must be changed
    pdb4amber_input_complex = f"pdb4amber --reduce --no-reduce-db -i {complex_raw} -o {complex}"
    if pdb4amber_test:
        # if test works, pdb4amber is run
        # running pdb4amber
        subprocess.run([f"{pdb4amber_input_complex}"], shell=True)
    else:
        # if test fails, user must process complex on his own
        # try to find if there is a complex_pdb4amber_inputs entry in the control file
        complex_inputs = r'complex_pdb4amber_inputs\s*=\s*\[(.*)\]'
        complex_inputs_match = re.search(complex_inputs, control)
        if complex_inputs_match:
            # MDMS was already run and user should've processed complex by this point
            complex_path = Path(complex)
            if complex_path.exists():
                # if this exist, user have processed the file and everything is fine - we might proceed
                pass
            else:
                # if it does not exist, a prompt reminding on how to proceed is printed
                print(f"\n!!WARNING!!\n"
                      f"\nYou have not processed complex file with pdb4amber yet\n"
                      f"There were some problems with running pdb4amber from within MDMS.\n"
                      f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                      f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                      f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                      f"your own installation of Python.\n"
                      f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                      f"interpreter (i. e. by loading the appropriate module).\n"
                      f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                      f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                      f"In such case, just copy the content of each line of complex_pdb4amber.in file into terminal and press"
                      f"enter. As a result, you will obtain processed PDB complex file which will be ready for further"
                      f"steps.")
            pass
        else:
            # MDMS is run for the first time; file must be written
            print(f"\n!!WARNING!!\n"
                  f"There were some problems with running pdb4amber from within MDMS.\n"
                  f"If you installed Ambertools previously and it suddenly stopped working, it might be due to "
                  f"the clash of Python versions - MDMS uses Python 3.6, whereas pdb4amber was written in Python 2.7.\n"
                  f"This issue usually occurs on HPC facilities which uses environmental modules feature alongside "
                  f"your own installation of Python.\n"
                  f"If that might be true in your case, for a moment please choose Python 2.7 as a default Python"
                  f"interpreter (i. e. by loading the appropriate module).\n"
                  f"Please also make sure that pdb4amber is installed correctly (just follow Amber Manual on how to "
                  f"install Ambertools).\nAt this point you should be able to use pdb4amber in the terminal.\n"
                  f"In such case, just copy the content of each line of complex_pdb4amber.in file into terminal and press"
                  f"enter. As a result, you will obtain processed PDB complex file which will be ready for further"
                  f"steps.")
            complex_process_input = ('complex_pdb4amber.in')
            complex_process_input_path = Path(complex_process_input)
            if complex_process_input_path.exists():
                os.remove(complex_process_input_path)
            # input for pdb4amber written to the file
            with open(complex_process_input, 'w') as file:
                file.write(pdb4amber_input_complex)
            print(f"\nYou will now be redirected to menu of MDMS. Please, quit MDMS and process complex PDB file"
                  f"from within the terminal.\n"
                  f"Afer processing the file, proceed with topology preparation step within MDMS.\n")
            # saving info to the control file that pdb4amber was not run from within MDMS
            save_to_file('complex_pdb4amber_inputs = True\n', filename)
            stop_interface()

def metal_modelling():
    # MCPB.py is run in order to get parameters for metal ions
    # read metal ions
    control = read_file(filename)
    # finding metal residues in control file
    metals = r'metals\s*=\s*\[(.*)\]'
    metals_match = re.search(metals, control)
    # getting info about pdb filename
    structure = r'pdb\s*=\s*(.*)'
    structure_match = re.search(structure, control).group(1)
    # stripping of extension from structure - this way it will be easier to
    # get proper names, i.e. 4zaf_old.pdb
    structure_match_split = structure_match.split('.')[0]
    if metals_match:
        # checking if metal_modelling function was run - if it was, extract necessary info from obtained tleap input file
        mcpb = r'mcpb_input\s*=\s*(.*)'
        mcpb_match = re.search(mcpb, control)
        if mcpb_match:
            # look for groupname in the control file
            #save_to_file(f"mcpb_groupname = {user_input_groupname}\n", filename)
            groupname = r'mcpb_groupname\s*=\s*(.*)'
            groupname_match = re.search(groupname, control).group(1)
            # establishing tleap input name
            mcpb_tleap = f'{groupname_match}_tleap.in'
            # getting necessary info about additional atoms from tleap input
            # NEW VERSION OF MCPB.PY TLEAP OUTPUT
            tleap_modifications_file = Path(f'tleap_{groupname_match}.in')
            # checking if mcpb otuput in a tleap format is already present
            # removing old version of tleap output
            if tleap_modifications_file.exists():
                os.remove(tleap_modifications_file)
            # creating a string, to which tleap modifications will be appended
            tleap_modifications_string = ''
            # opening tleap output and extracting important information
            with open(f'{mcpb_tleap}', 'r') as file:
                a = file.read()
                for line in a.splitlines():
                    # getting rid of tleap lines which should be taken from mdms
                    if line.startswith('source'):
                        pass
                    elif line.startswith('savepdb'):
                        pass
                    elif line.startswith('saveamberparm'):
                        pass
                    elif line.startswith('solvatebox'):
                        pass
                    elif line.startswith('addions'):
                        pass
                    elif line.startswith('quit'):
                        pass
                    # if line does not start with the above, given info is required for a succesfull tleap input
                    else:
                        tleap_modifications_string = tleap_modifications_string + line + '\n'
            # remove last line from string (it is an empty line)
            temp_string = tleap_modifications_string.splitlines()
            temp_string = temp_string[:-1]
            tleap_modifications_string = '\n'.join(temp_string)
            # saving tleap modifications to a file
            with open(tleap_modifications_file, 'w') as file:
                file.write(tleap_modifications_string)
        else:
            # mcpb_input = True was not written to the control file, this will be run
            # taking only ligands entries
            metals_match = metals_match.group(1)
            # removing quotes from string
            metals_string = metals_match.replace("'", "")
            # removing whitespaces and turning string into a list
            metals_list = re.sub(r'\s', '', metals_string).split(',')
            # generating mol2 file for the metal
            for metal in metals_list:
                USER_CHOICE_METAL_CHARGE = f"\nCharge of {metal} ion\n" \
                    f"What charge of {metal} ion would you like to use in your simulations?\n" \
                    f"Please, provide integer value.\n"
                while True:
                    try:
                        # user provides metal ion charge
                        user_input_metal_charge = int(input(USER_CHOICE_METAL_CHARGE))
                        # if charge value is between -5 and 8, it is fine
                        if -5 <= user_input_metal_charge <= 8:
                            charge = user_input_metal_charge
                            break
                    except:
                        print('Please, provide valid input.')
                # look for residue number for metal in the pdb file
                resname = ''
                resid = ''
                atom_nr = ''
                with open(f'{structure_match_split}_full.pdb', 'r') as file:
                    a = file.read()
                    for line in a.splitlines():
                        if line.startswith('HETATM'):
                            resname = line[17:20]
                            resname = resname.replace(' ', '')
                            # if resname is equal to metal, just take the line and overwrite as a metal.pdb
                            if resname == metal:
                                if Path(f'{metal}.pdb').exists():
                                    os.remove(Path(f'{metal}.pdb'))
                                with open(f'{metal}.pdb', 'w') as file:
                                    file.write(line)
                                resid = line[24:27]
                                resid = str(resid).replace(' ', '')
                                atom_nr = line[8:12]
                                atom_nr = str(atom_nr).replace(' ', '')
                antechamber_input = f"antechamber -fi pdb -fo mol2 -i {metal}.pdb -o {metal}.mol2 -at amber -pf y"
                # running antechamber
                subprocess.run([f"{antechamber_input}"], shell=True)
                # replacing DU entry in pre.mol2 and change with their actual values
                mol2_metal = ''
                with open(f'{metal}.mol2', 'r') as file:
                    a = file.read()
                    for line in a.splitlines():
                        if "DU" in line:
                            if len(metal) == 1:
                                line = line.replace("DU", f"{metal} ")
                                #line = line.replace("0.000000", f'{charge}.000000')
                            elif len(metal) == 2:
                                line = line.replace("DU", f"{metal}")
                                #line = line.replace("0.000000", f'{charge}.000000')
                        if "0.000000" in line:
                            line = line.replace("0.000000", f'{charge}.000000')
                        mol2_metal = mol2_metal + line + '\n'
                # replacing {metal}.mol2
                os.remove(Path(f'{metal}.mol2'))
                with open(f'{metal}.mol2', 'w') as file:
                    file.write(mol2_metal)
                # get the residue number for metal - it must be replaced with newer value from {structure_match_split}_full.pdb
                # previous resid was given from pdb without hydrogens
                metal_pdb = f'{metal}.pdb'
                metal_atom_number = ''
                with open(f'{metal}.pdb', 'r') as file:
                    a = file.read()
                    for line in a.splitlines():
                        metal_atom_number = int(line[6:11])
                # radius over which take the atoms for  MCPB
                USER_CHOICE_CUTOFF = f"Please, provide the cutoff value indicating maximum bond length between metal ion" \
                    f" and surrounding atoms (default value is 2.8):\n"
                while True:
                    try:
                        user_input_cutoff = float(input(USER_CHOICE_CUTOFF))
                        break
                    except:
                        print('Please, provide valid input')
                # determine which residues create bonds with the metal ion
                metal_center_file = 'metal_center.pdb'
                metal_cpptraj_input= f"parm {structure_match_split}_full.pdb noconect\n" \
                    f"trajin {structure_match_split}_full.pdb\n" \
                    f"reference {structure_match_split}_full.pdb\n" \
                    f"strip !(@{metal_atom_number}<:{user_input_cutoff})\n" \
                    f"trajout {metal_center_file}\n" \
                    f"run\n" \
                    f"quit"
                if Path('met_cpptraj.in').exists():
                    os.remove(Path('met_cpptraj.in'))
                with open('met_cpptraj.in', 'w') as file:
                    file.write(metal_cpptraj_input)
                try:
                    subprocess.run([f'cpptraj -i met_cpptraj.in'], shell=True)
                except:
                    print('Cpptraj failed to run.\n'
                          'For modelling of metal ions, cpptraj must be run.')
                # metal_center pdb is written; find out what residues are within
                unique_res_list = []
                with open(f'{metal_center_file}', 'r') as file:
                    a = file.read()
                    for line in a.splitlines():
                        if line[17:20] not in unique_res_list:
                            unique_res_list.append(line[17:20])
                # find if there is a mol2 file for entry in unique res list - if there is, ligand files will be put into
                # input file for MCPB.py; otherwise there is no ligand around metal ion
                ligands_metal_center = []
                for residue in unique_res_list:
                    residue_file_mol2 = Path(f'{residue}.mol2')
                    if residue_file_mol2.exists():
                        ligands_metal_center.append(residue)
                # provide group name - it will be changed to uppercase
                USER_CHOICE_GROUPNAME = f"Group name is used for naming files throughout MCPB.py modelling.\n" \
                    f"What group name would you like to use? \n"
                while True:
                    try:
                        user_input_groupname = str(input(USER_CHOICE_GROUPNAME).upper())
                        if len(user_input_groupname) == 0:
                            raise Exception
                        break
                    except:
                        print('Please, prvide a group name.')
                # save input group name to the control file - it will enable extracting info from tleap input obtained
                # once MCPB.py is finished
                save_to_file(f"mcpb_groupname = {user_input_groupname}\n", filename)
                opt_options = ['0', '1', '2']
                opt_choice = ''
                USER_CHOICE_OPT = f"Would you like to optimize the geometry of the large model? Such optimization should" \
                    f" slightly enhance the quality of the obtained force constants but the computational cost associated " \
                    f"with calculations will drastically increase.\n" \
                    f"There are 3 options available:\n" \
                    f"- press '0' if you do not want to optimize geometry of the large model at all\n" \
                    f"- press '1' if you want to optimize geometry only of the hydrogen atoms\n" \
                    f"- press '2' if you want to run full geometry optimization\n" \
                    f"Please, provide your choice:\n"
                while True:
                    try:
                        user_input_opt = str(input(USER_CHOICE_OPT))
                        if user_input_opt in opt_options:
                            opt_choice = user_input_opt
                            break
                        else:
                            raise Exception
                    except:
                        print('Please, provide valid input')
                # check if mcpb_input exists
                if Path(f"{user_input_groupname}.in").exists():
                    os.remove(Path(f'{user_input_groupname}.in'))
                # everything should be ready - create input file
                mcpb_input = (f"original_pdb {structure_match_split}_full.pdb\n" \
                    f"group_name {user_input_groupname}\n" \
                    f"cut_off {user_input_cutoff}\n" \
                    f"ion_ids {metal_atom_number}\n" \
                    f"ion_mol2files {metal}.mol2\n")
                # mol2 and frcmod files must be added in a slightly different way, separated by a coma
                ligands_mol2 = []
                ligands_frcmod = []
                if ligands_metal_center:
                    mol2_extension = 'mol2'
                    frcmod_extension = 'frcmod'
                    for x in ligands_metal_center:
                        ligands_mol2.append(x + '.' + mol2_extension + '\n')
                        ligands_frcmod.append(x + '.' + frcmod_extension + '\n')
                    ligands_mol2 = ', '.join(ligands_mol2)
                    ligands_frcmod = ', '.join(ligands_frcmod)
                if ligands_mol2:
                    mcpb_input = mcpb_input + f'naa_mol2files {ligands_mol2}'
                if ligands_frcmod:
                    mcpb_input = mcpb_input + f'frcmod_files {ligands_frcmod}'
                mcpb_input = mcpb_input + f'large_opt {opt_choice}'
                # save mcpb input file; its naming is according to group_name
                if Path(f'{user_input_groupname}.in').exists():
                    os.remove(Path(f'{user_input_groupname}.in'))
                with open(f'{user_input_groupname}.in', 'w') as file:
                    file.write(mcpb_input)
                # print to user that he should run MCPB.py
                print(f'Input file for obtaining force field parameters for MCPB.py was created. It is named '
                      f'{user_input_groupname}.in.\n'
                      f'Right now, you need to run MCPB.py with following command:\n'
                      f'MCPB.py -i {user_input_groupname}.in -s 1\n'
                      f'Once executed, first step of MCPB.py will be run - its purpose is to create Gaussian input files.\n'
                      f'After that, you will need to perform QM calculations with either Gaussian or GAMESS-US software.\n'
                      f'Further on, you will need to follow MCPB.py tutorial available at http://ambermd.org/tutorials/advanced/tutorial20/mcpbpy.htm.\n'
                      f'Once you will finish obtaining paramers with MCPB.py, please, run topology_prep step of MDMS once more - '
                      f'MDMS will notice that parameters are ready and you will not be prompted to fill any more info regarding MCPB.py\n.')
            # saving info to the prep file that MCPB.py input was prepared
            save_to_file(f"mcpb_input = True\n", filename)
            # since user must proceed with MCPB.py by himself, interface is stopped
            stop_interface()

def tleap_input():
    tleap_file = Path('tleap.in')
    # if input file already exists, remove it
    if tleap_file.exists():
        os.remove(tleap_file)
    # reading pdb from control file
    control = read_file(filename)
    structure = r'pdb\s*=\s*(.*)'
    structure_match = re.search(structure, control).group(1)
    # stripping of extension from structure - this way it will be easier to
    # get proper names, i.e. 4zaf_old.pdb
    structure_match_split = structure_match.split('.')[0]
    # name of the pdb file that will be an input for tleap
    complex = f"{structure_match_split}_full.pdb"
    # options for tleap
    # protein force field
    USER_CHOICE_PROTEIN_FF = (
        f"\nProtein force field\n"
        f"Please, choose force field which will be used for the protein during your simulations.\n"
        f"Please, note that the recommended choice is ff14SB.\n"
        f"The following options are available:\n"
        f"- 'ff14sb'\n"
        f"- 'ff15ipq'\n"
        f"- 'fb15'\n"
        f"- 'ff03'\n"
        f"- 'ff03ua'\n"
        f"Please, provide your choice:\n"
    )
    while True:
        try:
            # user chooses which protein force field to use
            user_input_protein_ff = str(input(USER_CHOICE_PROTEIN_FF).lower())
            if user_input_protein_ff == 'ff14sb':
                # changing co capitals SB so it will be accepted by tleap
                user_input_protein_ff = 'ff14SB'
                break
            elif user_input_protein_ff == 'ff15ipq':
                break
            elif user_input_protein_ff == 'fb15':
                break
            elif user_input_protein_ff == 'ff03':
                user_input_protein_ff = 'ff03.r1'
                break
            elif user_input_protein_ff == 'ff03ua':
                break
        except:
            print('Please, provide valid input')
    # saving choice to control file and tleap input
    save_to_file(f"prot_ff = {user_input_protein_ff}\n", filename)
    with open(tleap_file, "a") as f:
        f.write(f"source leaprc.protein.{user_input_protein_ff}\n")
    # saving ligand force field to control file
    ligands = r'ligands\s*=\s*\[(.*)\]'
    ligands_match = re.search(ligands, control)
    if ligands_match:
        # if there are ligands, find which force field was used
        lig_ff = r'atoms_type\s*=\s*(.*)'
        lig_ff_match = re.search(lig_ff, control).group(1)
        # saving match to tleap input
        # this is done earlier
        with open(tleap_file, "a") as f:
            print('here7')
            f.write(f"source leaprc.{lig_ff_match}\n")
            print('here8')
    # water force field
    water_ff_list = ['tip3p', 'tip4pew', 'spce']
    # getting box info based on the chosen water ff
    water_box_dict = {
        'tip3p': 'TIP3PBOX',
        'tip4pew': 'TIP4PEWBOX',
        'spce': 'SPCBOX',
    }
    # getting ions parameters based on the chosen water ff
    ions_dict = {
        'tip3p': 'frcmod.ionsjc_tip3p',
        'tip4pew': 'frcmod.ionsjc_tip4pew',
        'spce': 'frcmod.ionsjc_spce'
    }
    USER_CHOICE_WATER_FF = (
        f"\nWater force field\n"
        f"Please, choose force field which will be used for water during your simulations.\n"
        f"Please, note that the most common choice is tip3p.\n"
        f"The following options are available:\n"
        f"- 'tip3p'\n"
        f"- 'tip4pew'\n"
        f"- 'spce'\n"
        f"Please, provide your choice:\n"
    )
    while True:
        try:
            # getting user input
            user_input_water_ff = str(input(USER_CHOICE_WATER_FF).lower())
            if user_input_water_ff in water_ff_list:
                break
        except:
            print('Provided input is not valid')
    # saving water force field choice to control file and tleap input
    save_to_file(f"wat_ff = {user_input_water_ff}\n", filename)
    # getting ions parameters
    ions = ions_dict.get(user_input_water_ff)
    # water and ion parameters put into tleap input
    with open(tleap_file, "a") as f:
        f.write(f"loadoff solvents.lib\n")
        f.write(f"loadoff atomic_ions.lib\n")
        f.write(f"loadamberparams frcmod.{user_input_water_ff}\n")
        f.write(f"loadamberparams {ions}\n")
    # finding if there are results from mcpb.py
    mcpb = r'mcpb_input\s*=\s*(.*)'
    mcpb_match = re.search(mcpb, control)
    tleap_mcpb_modifications = ''
    if mcpb_match:
        # look for groupname in the control file
        groupname = r'mcpb_groupname\s*=\s*(.*)'
        groupname_match = re.search(groupname, control).group(1)
        tleap_modifications_file = Path(f'tleap_{groupname_match}.in')
        # assign the whole tleap modification to the string
        with open(tleap_modifications_file, 'r') as file:
            tleap_mcpb_modifications = file.read()
        # saving mcpb modifications to tleap input file
        with open(tleap_file, "a") as f:
            f.write(f"{tleap_mcpb_modifications}\n")
    # finding if there are ligands in control file
    ligands = r'ligands\s*=\s*\[(.*)\]'
    ligands_match = re.search(ligands, control)
    # saving ligands parameters is done only if mcpb was not run - MUST BE CHANGED TO INCORPORATE LIGANDS
    # WHICH WERE NOT INCLUDED IN METAL CENTER
    # taking ligands info
    if ligands_match:
        # taking only ligands' entries values
        ligands_match = ligands_match.group(1)
        # replacing quotes in string
        ligands_string = ligands_match.replace("'", "")
        # converting string to list
        ligands_list = re.sub(r'\s', '', ligands_string).split(',')
        # list which will have ligands that were found in metal center
        metal_center_ligands_list = []
        # checking if mcpb was run
        if mcpb_match:
            # list which will cot
            # reading metal center file
            metal_center_file = 'metal_center.pdb'
            with open(metal_center_file, 'r') as file:
                a = file.readlines()
                # iterating over each line in metal_center
                for line in a:
                    # iterating over each ligand
                    for x in ligands_list:
                        # if x ligand is in line, check if it is in metal_center_ligands_list
                        if x in line[17:20]:
                            # if there is no x ligand in metal_center_ligands_list, add it to the list
                            if x not in metal_center_ligands_list:
                                metal_center_ligands_list.append(x)
            # if those 2 lists are the same, all of the ligands are included in metal center; nothing to be done
            if metal_center_ligands_list == ligands_list:
                pass
            else:
                # not all of the ligands were found in metal center; they must be added to tleap input
                # remove from ligands_list entries that were found in metal_center
                ligands_list = [elem for elem in ligands_list if elem not in metal_center_ligands_list]
                # mol2 and frcmod must be added for each element in ligands_list
                # putting mol2 and frcmod for each ligand into tleap input
                for ligand in ligands_list:
                    with open(tleap_file, 'a') as f:
                        f.write(f"{ligand} = loadmol2 {ligand}.mol2\n")
                        f.write(f"loadamberparams {ligand}.frcmod\n")
            pass
        # mcpb.py was not run - execute normally
        else:
            # if there are ligands, find which force field was used
            lig_ff = r'atoms_type\s*=\s*(.*)'
            lig_ff_match = re.search(lig_ff, control).group(1)
            # saving match to tleap input
            # this is done earlier
            # with open(tleap_file, "a") as f:
            #   f.write(f"source leaprc.{lig_ff_match}\n")
            # taking only ligands entries
            #ligands_match = ligands_match.group(1)
            # removing quotes from string
            #ligands_string = ligands_match.replace("'", "")
            # removing whitespaces and turning string into a list
            #ligands_list = re.sub(r'\s', '', ligands_string).split(',')
            # putting mol2 and frcmod for each ligand into tleap input
            for ligand in ligands_list:
                with open(tleap_file, 'a') as f:
                    f.write(f"{ligand} = loadmol2 {ligand}.mol2\n")
                    f.write(f"loadamberparams {ligand}.frcmod\n")
    # finding if crystal waters were retained for MD
    waters = r'waters\s*=\s*\[(.*)\]'
    waters_match = re.search(waters, control)
    if waters_match:
        # taking only residues names
        waters_match = waters_match.group(1)
        # removing quotes from string
        waters_string = waters_match.replace("'", "")
        # removing whitespaces and turning string into a list
        waters_list = re.sub(r'\s', '', waters_string).split(',')
        # 3 letter codes for water models
        water_models_dict = {
            'tip3p': 'TP3',
            'tip4pew': 'TP4',
            'spce': 'SPC'
        }
        # assigning crystal waters to chosen water model
        for x in range(0, len(waters_list)):
            water_model = water_models_dict.get(user_input_water_ff)
            with open(tleap_file, 'a') as f:
                f.write(f"{waters_list[x]} = {water_model}\n")
    # reading complex file - if mcpb py was run, skip this due to the fact that mcpb py changes mol file
    if mcpb_match:
        pass
    else:
        with open(tleap_file, 'a') as f:
            f.write(f"mol = loadpdb {complex}\n")
            # checking complex pdb for validity
            f.write(f"check mol\n")
    # provide filaneme for topology and coordinates
    USER_CHOICE_NAME = "\nPrefix\n" \
                       "Please, provide name for the prefix for the topology and coordinates files.\n" \
                       "Ideally, it should be just a few letters-long.\n" \
                       "For instance, if you type 'my_complex' your topology will be named my_complex.prmtop" \
                       " and coordinates will be named my_complex.inpcrd.\n" \
                       "Please, provide your choice:\n"
    while True:
        try:
            user_input_name = str(input(USER_CHOICE_NAME).lower())
            break
        except:
            print("Please, provide valid input")
    # saving chosen name to control file
    save_to_file(f"top_name = {user_input_name}\n", filename)
    # saving unsolvated file
    with open(tleap_file, 'a') as f:
        f.write(f"savepdb mol {user_input_name}_no_water.pdb\n")
    # determining solvation box size
    USER_CHOICE_WATERBOX_SIZE = (
        f"\nSolvation shell size\n"
        f"Please, provide the size of a periodic solvent box around the complex (in Angstroms).\n"
        f"Most commonly used values are between 8 - 14.\n"
        f"Please, provide your choice:\n"
    )
    while True:
        try:
            user_input_waterbox_size = float(input(USER_CHOICE_WATERBOX_SIZE))
            # solvatebox must be positive
            if user_input_waterbox_size > 0:
                # solvatebox should be between 8 and 14 - if it is not, user is informed that it may be troublesome
                if user_input_waterbox_size < 8:
                    print(f"\nYou've chosen that solvent will create box of {user_input_waterbox_size} Angstroms around"
                          f"complex. This is smaller than the recommended size. Such a box might not be enough"
                          f"to properly solvate your complex.\n Please, proceed with caution")
                    break
                elif user_input_waterbox_size > 14:
                    print(f"\nYou've chosen that solvent will create box of {user_input_waterbox_size} Angstroms around"
                          f"complex. This is larger than the recommended size. A vast amount of water molecules might"
                          f"introduce very high computational cost.\n Please, proceed with caution."
                          f"might Please, proceed with caution")
                    break
                else:
                    break
        except:
            print('Please, provide valid input')
    # save waterbox size to control file
    save_to_file(f"box_size = {user_input_waterbox_size}\n", filename)
    # get box info
    waterbox = water_box_dict.get(user_input_water_ff)
    # save everything about solvation to tleap input
    with open(tleap_file, 'a') as f:
        f.write(f"solvatebox mol {waterbox} {user_input_waterbox_size}\n")
        f.write(f"addions mol Na+ 0\n")
        f.write(f"addions mol Cl- 0\n")
        f.write(f"savepdb mol {user_input_name}_solvated.pdb\n")
        f.write(f"saveamberparm mol {user_input_name}.prmtop {user_input_name}.inpcrd\n")
        f.write(f"quit\n")
    # tleap input from a command line
    tleap_run = f"tleap -f {tleap_file}"
    # execute tleap input
    subprocess.run([f"{tleap_run}"], shell=True)

# these are run normally
top_prep_functions = [
#    file_naming,
    clearing_control,
    hydrogen_check,
    ligands_parameters,
    antechamber_parmchk_input,
    pdb_process,
    metal_modelling,
    tleap_input]


# if mcpb.py was run, these are run
top_prep_functions_after_mcpb = [
    clearing_control_mcpb,
    metal_modelling,
    tleap_input
]

#methods_generator = (y for y in top_prep_functions)
#next(methods_generator, None)


def queue_methods():
    #next(methods_generator, None)
    global stop_generator
    stop_generator = False
    # file naming must be run prior to generators
    file_naming()
    # check if mcpb.py was run
    control = read_file(filename)
    # finding if there are metal ions considered in the system
    metals = r'metals\s*=\s*\[(.*)\]'
    metals_match = re.search(metals, control)
    if metals_match:
        # checking if mcpb.py input was generated
        mcpb = r'mcpb_input\s*=\s*(.*)'
        mcpb_match = re.search(mcpb, control)
        # if mcpb.py was run, run generator with functions from top_prep_functions_after_mcpb
        if mcpb_match:
            methods_generator = (y for y in top_prep_functions_after_mcpb)
            next(methods_generator, None)
            for x in top_prep_functions_after_mcpb:
                x()
                # if a condition is met, generator is stopped
                if stop_generator:
                    # I do not know if this prompt is necessary
                    print(
                        '\nProgram has not finished normally - it appears that something was wrong with your structure. \n'
                        'Apply changes and try again!\n')
                    break
        else:
            methods_generator = (y for y in top_prep_functions)
            next(methods_generator, None)
            # mcpb.py input was not generated yet; run top_prep_functions generator
            for x in top_prep_functions:
                x()
                # if a condition is met, generator is stopped
                if stop_generator:
                    # I do not know if this prompt is necessary
                    print(
                        '\nProgram has not finished normally - it appears that something was wrong with your structure. \n'
                        'Apply changes and try again!\n')
                    break
    else:
        # there are no metal ions; run top_prep_functions generator
        methods_generator = (y for y in top_prep_functions)
        next(methods_generator, None)
        for x in top_prep_functions:
            x()
            # if a condition is met, generator is stopped
            if stop_generator:
                # I do not know if this prompt is necessary
                print(
                    '\nProgram has not finished normally - it appears that something was wrong with your structure. \n'
                    'Apply changes and try again!\n')
                break
