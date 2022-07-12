# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 15:45:05 2022

@author: bryce
"""

import os
import sys
import glob
from openbabel import pybel

def get_pwd():
    return os.getcwd()

def convert_SMILES_to_XYZ(): #needs docstring
    '''
    

    Returns
    -------
    None.

    '''
    i = 0
    # sep = '\t'
    for mol in pybel.readfile('smi', './SMILES_example.smi'):
        i += 1
        # smi_str = mol.write('smi')
        # stripped_smi_str = smi_str.split(sep, 1)[0]
        mol.make2D()
        mol.make3D()
        mol.localopt()
        mol = pybel.readstring('sdf', mol.write('sdf'))
        mol.write('gau', 'Molecule%s.inp' % i, True)
        print('Finished with Molecule #%s' % i)
        print(mol.write('smi'))
    print('Fin')
    
def make_gaussian(file, method, basis_set, solvent):
    '''
    Overwrites first 5 lines of file to make it gaussian input compliant.

    Parameters
    ----------
    file : Gaussian output file from openbale.
    method : method for DFT optimization
    basis_set : basis set for DFT optimization

    Returns
    -------
    Gaussian compliant input file.

    '''
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        lines[0] = "%NProcShared=20\n"
        lines[1] = "%mem=50GB\n"
        lines[2] = "%chk={}.chk\n\n".format(file)
        lines[3] = "#p opt freq {}/{} integral=superfinegrid SCRF=({})\n\n".format(method, basis_set, solvent)
        lines[4] = "title\n"
        for line in lines:
            f.write(line)
    f.close()
    
def make_four(file):
    os.system("cp {} solv_{}".format(file, file))
    os.system("cp {} pos_{}".format(file, file))    # creates file for postive charged 
    os.system("cp {} solv_pos_{}".format(file, file))
    

def run_bash(i, mol_name=''): #needs lots of work
    """
    :type i: int
    :type mol_name: str
    """
    # os.chdir('mol_name')
    cwd = os.getcwd()
    input_file: str = cwd + '/q-tala-gauss'
    job_name: str = os.path.splitext(os.path.split(glob.glob(cwd + "/*.in")[0])[1])[0]
    with open(input_file, "w") as fh:
        fh.writelines("#!/bin/bash\n")
        fh.writelines("#SBATCH --partition=hendon      ### Partition (short, long, fat, longfat)\n")
        fh.writelines("#SBATCH --job-name=%s   ### Job Name\n" % job_name)
        fh.writelines("#SBATCH --time=24:00:00         ### WallTime\n")
        fh.writelines("#SBATCH --nodes=1               ### Number of Nodes (14 cores per CPU, 2 CPU per node)\n")
        fh.writelines("#SBATCH --ntasks-per-node=20    ### Number of tasks (MPI processes)\n")
        fh.writelines("#SBATCH --account=hmsoregon     ### account\n")
        fh.writelines("\n")
        fh.writelines("module load intel-mpi\n")
        fh.writelines("module load mkl\n")
        fh.writelines("module load gaussian\n")
        fh.writelines("\n")
        fh.writelines("g09 < %s.in > %s.out\n" % (job_name, job_name))
        fh.writelines("\n")
        fh.writelines("/bin/rm -vf /tmp/$USER/Gau*")
    # arg at [1] is python path for pass to bash
   #  os.system(" bash nics_bash.sh " + main_dir + "/nics.py")    # TODO: find a way to pass q-tala-gauss into slurm
    # os.system("sbatch %s" % input_file)