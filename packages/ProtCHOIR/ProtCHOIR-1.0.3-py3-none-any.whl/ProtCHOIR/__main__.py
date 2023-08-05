#!/usr/bin/env python
#
# Imports
###############################################################################
from datetime import datetime
# Mark Initiation time
start_time = datetime.timestamp(datetime.now())-1
import os
import sys
import pickle
import shutil
import zipfile
import argparse
import textwrap as tw
import ProtCHOIR.Toolbox as pctools
from ProtCHOIR.Initialise import *
from ProtCHOIR.UpdateDatabases import update_databases
from ProtCHOIR.AnalyseProtomer import analyze_protomer
from ProtCHOIR.MakeOligomer import make_oligomer
from ProtCHOIR.AnalyseOligomer import analyse_oligomers

# License
###############################################################################
'''

ProtCHOIR: A tool for generation of homo oligomers from pdb structures

Authors: Torres, P.H.M.; Malhotra, S.; Blundell, T.L.

[The University of Cambridge]

Contact info:
Department Of Biochemistry
University of Cambridge
80 Tennis Court Road
Cambridge CB2 1GA
E-mail address: monteirotorres@gmail.com

This project is licensed under Creative Commons license (CC-BY-4.0)

'''

# Description
###############################################################################

# Dictionaries
###############################################################################

# Global Variables
###############################################################################

# Classes
###############################################################################

# Functions
###############################################################################

# Main Function
###############################################################################
def main():

    args = initial_args

    if args.update is True:
        print(tw.dedent("""
                                         !WARNING!

                      You have chosen to updtate the local databases.

              ** The root directory for the database files is: """+clrs['y']+choirdb+clrs['n']+"""

              ** The path to local pdb mirror is: """+clrs['y']+pdb_archive+clrs['n']+"""

              ** The path to local pdb biounit mirror is: """+clrs['y']+pdb1_archive+clrs['n']+"""

              ** The path to local gesamt archive is: """+clrs['y']+ges_homo_archive+clrs['n']+"""

              ** The path to local UniRef50 blast database is: """+clrs['y']+uniref50+clrs['n']+"""


              This could take a long time.

              <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

              """))
        option = input('Do you confirm the information above? (y/n)')
        if option == 'y' or option == 'Y' or option == 'YES' or option == 'yes' or option == 'Yes':
            update_databases(args.verbosity)
            print('\n\nDone updating all databases. Exiting.\n')
        else:
            print('\n\nNo positive confirmation, will not update databases.\n')
            exit()
    # Actually run oligomerization protocol
    else:
        outdir = os.getcwd()
        input_file = args.input_file
        assert os.path.isdir(pdb_archive), clrs['r']+'\n\n Not able to find PDB directory.\n\n Does "'+pdb_archive+'" exist?'+clrs['n']
        assert os.path.isdir(pdb1_archive), clrs['r']+'\n\n Not able to find PDB1 assemblies directory.\n\n Does "'+pdb1_archive+'" exist?'+clrs['n']
        assert os.path.isdir(pdb_homo_archive), clrs['r']+'\n\n Not able to find ProtCHOIR database directory.\n\n Does "'+pdb_homo_archive+'" exist?'+clrs['n']
        assert os.path.isdir(ges_homo_archive), clrs['r']+'\n\n Not able to find GESAMT archive directory.\n\n Does "'+ges_homo_archive+'" exist?'+clrs['n']
        assert args.refine_level in [0, 1, 2, 3, 4], clrs['r']+'\n\n Refinement level must be an integer number from 0 to 4.\n Run ./ProtCHOIR -h for more information\n\n'+clrs['n']
        assert input_file is not None, clrs['r']+'\n\n Please inform the input file name.\n Run ./ProtCHOIR -h for more information.\n\n'+clrs['n']
        assert os.path.isfile(input_file), clrs['r']+'\n\n Not able to find input file.\n\n Does "'+input_file+'" exist?\n'+clrs['n']

        # Force generation of topologies and all assessments if final report is requested
        if args.generate_report is True:
            args.assessment = 'MIG'
            args.plot_topologies = True

        # Deal with dots in the input file and remove dots
        if input_file.lower().endswith('.pdb'):
            input_basename = os.path.basename(input_file).split('.pdb')[0]
            input_basename = input_basename.replace(".", "_")
            new_input_file = input_basename+'.pdb'
            if os.path.basename(input_file) == os.path.basename(new_input_file):
                pass
            else:
                shutil.copy(input_file, new_input_file)

        # Also process filename to fasta header if input file is fasta
        elif input_file.lower().endswith('.fasta'):
            input_basename = os.path.basename(input_file).split('.fasta')[0]
            input_basename = input_basename.replace(".", "_")
            new_input_file = os.path.join(outdir, input_basename+'_CHOIR_MonomerSequence.fasta')
            with open(input_file, 'r') as infile, open(new_input_file, 'w') as outfile:
                outfile.write('>'+input_basename+'\n')
                n = 0
                for line in infile.readlines():
                    if not line.startswith('>'):
                        outfile.write(line)
                    else:
                        n += 1
                    if n == 2:
                        break
            args.sequence_mode = True
        else:
            raise pctools.FileFormatError(clrs['r']+'\n\n Input format must be either pdb or fasta\n Run ./ProtCHOIR -h for more information\n\n'+clrs['n'])

        # Pickle Runtime arguments
        pickle.dump(args, open('CHOIR_Args.pickle', 'wb'))

        # Show arguments used and create CHOIR.conf
        pctools.print_section(0, "Runtime Arguments")
        runtime_arguments = {}
        choir_args = os.path.join(outdir, "CHOIR.args")
        with open(choir_args, 'w') as f:
            for name, value in vars(args).items():
                runtime_arguments[name] = value
                print(name+"="+str(value))
                f.write(name+"="+str(value)+"\n")
        print('\nRuntime parameters written to: '+clrs['g']+os.path.basename(choir_args)+clrs['n']+'\n')

        # Initialize report
        report = {}
        report['runtime_arguments'] = runtime_arguments


        # Start analysis of protomer
        analyse_protomer_results = analyze_protomer(new_input_file, report, args)

        # If no suitable homo-oligomeric template wasfound, exit nicely.
        if analyse_protomer_results is None:
            pctools.print_sorry()
            sys.exit(0)

        # Else, proceed conditionally on runtime arguments
        elif analyse_protomer_results is not None and args.sequence_mode is True:
            residue_index_mapping = None
            minx = None
            maxx = None
            if args.skip_conservation:
                pdb_name, largest_oligo_complexes, interfaces_dict, report = analyse_protomer_results
            elif not args.skip_conservation:
                pdb_name, largest_oligo_complexes, interfaces_dict, entropies, z_entropies, report = analyse_protomer_results

        elif analyse_protomer_results is not None and args.sequence_mode is False:
            if args.skip_conservation:
                minx = None
                maxx = None
                entropies = None
                z_entropies = None
                pdb_name, largest_oligo_complexes, interfaces_dict, residue_index_mapping, report = analyse_protomer_results
            elif not args.skip_conservation:
                pdb_name, largest_oligo_complexes, interfaces_dict, entropies, z_entropies, residue_index_mapping, minx, maxx, report = analyse_protomer_results

        # Use information of complexes to build oligomers
        best_oligo_template, built_oligomers, report = make_oligomer(new_input_file, largest_oligo_complexes, report, args, residue_index_mapping=residue_index_mapping)

        # Analyse built models
        reports = analyse_oligomers(new_input_file, best_oligo_template, built_oligomers, interfaces_dict, report, args, entropies=entropies, z_entropies=z_entropies, minx=minx, maxx=maxx)

        # Generate HTML report
        nozip = [report['model_filename'] for report in reports]
        for report in reports:
            if args.generate_report is True:
                report['html_report'] = pctools.html_report(report, args)
                for key, value in report.items():
                    if key in ['html_report', 'molprobity_radar', 'comparison_plots', 'protomer_figure', 'protomer_plot', 'template_figure', 'topology_figure', 'assemblied_protomer_plot', 'input_filename']:
                        nozip.append(os.path.basename(value))
                    if key == 'model_figures':
                        for figure in value:
                            nozip.append(os.path.basename(figure))

        # Finalise
        end_time = datetime.timestamp(datetime.now())
        if args.zip_output is True:
            try:
                import zlib
                compression = zipfile.ZIP_DEFLATED
            except (ImportError, AttributeError):
                compression = zipfile.ZIP_STORED

            with zipfile.ZipFile(pdb_name+'ProtCHOIR_OUT.zip', 'w', compression=compression) as zipf:
                for f in os.listdir(os.getcwd()):
                    if f != 'ProtCHOIR_OUT.zip' and os.path.getctime(f) > start_time and os.path.getctime(f) < end_time:
                        print('Compressing... '+f)
                        zipf.write(f)
                        if f not in nozip:
                            if os.path.isdir(f):
                                shutil.rmtree(f)
                            elif os.path.isfile(f):
                                os.remove(f)

        print('FINISHED AT: '+datetime.now().strftime("%d-%m-%Y %H:%M"))


# Execute
###############################################################################
if __name__ == "__main__":
    main()
