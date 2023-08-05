# Imports
###############################################################################
import os
import re
import math
import pickle
import subprocess
import matplotlib
import collections
import numpy as np
import pandas as pd
matplotlib.use('Agg')
import textwrap as tw
import networkx as nx
import matplotlib.pyplot as plt
from multiprocessing import Pool
from ProtCHOIR.Initialise import *
import xml.etree.ElementTree as et
from matplotlib.lines import Line2D
import ProtCHOIR.Toolbox as pctools
from progressbar import progressbar as pg
# LICENSE
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
def parse_vivace_model(sequence, modelfile):
    print(clrs['g']+"Vivace model! New homologue search not necessary!\n"+clrs['n'])
    # # Read Chain correspondences
    # chain_correspondences_file = os.path.join(pdb_homo_archive, 'stats', 'chain_correspondences.pickle')
    # try:
    #     with open(chain_correspondences_file, 'rb') as p:
    #         chain_correspondences = pickle.load(p)
    # except FileNotFoundError:
    #     print(clrs['r']+'Chain correspondence file could not be found! Please regenerate the database.'+clrs['n'])

    pattern = 'REMARK   6 TEMPLATE:'
    templates_ids = {}
    with open(modelfile, 'r') as f:
        for line in f:
            if re.search(pattern, line):
                template = line.split()[3]
                vivace_pid = line.split()[-1].replace('%', '')
                if len(template) == 5:
                    template_pdbcode = template[:4].lower()
                    # print('Template PDB: '+template_pdbcode)
                    # print('Original pdb chain:'+template[4])
                    # corresponding_chains = chain_correspondences['template_pdbcode']
                    # corresponding_chains_inverted = {v: k for k, v in corresponding_chains.items()}
                    vivace_chain = template[4]
                    # print('New CHOIR chain:'+template_chain)
                elif len(template) == 7:
                    if template.startswith('d'):
                        template_pdbcode = template[1:5].lower()
                        # print('Template PDB: '+template_pdbcode)
                        # print('Original pdb chain:'+template[5])
                        # corresponding_chains = chain_correspondences[template_pdbcode]
                        # corresponding_chains_inverted = {v: k for k, v in corresponding_chains.items()}
                        vivace_chain = template[5]
                        # print('New CHOIR chain: '+template_chain)
                    else:
                        template_pdbcode = template[:4].lower()
                        # print('Template PDB: '+template_pdbcode)
                        # print('Original pdb chain:'+template[4])
                        # corresponding_chains = chain_correspondences[template_pdbcode]
                        # corresponding_chains_inverted = {v: k for k, v in corresponding_chains.items()}
                        vivace_chain = template[4]
                        # print('New CHOIR chain: '+template_chain)
                template_chain, pid = pctools.find_most_similar_chain(sequence, template_pdbcode)
                if template_chain is None:
                    print(clrs['r']+'Hit '+str(template_pdbcode)+' not found in oligomeric database. Disregarding it.'+clrs['n']+'\n')
                    continue
                else:
                    templates_ids[template_pdbcode+":"+template_chain] = float(pid)
                    print('Vivace-determined hit: '+clrs['p']+template_pdbcode+clrs['n']+' Chain: '+clrs['y']+vivace_chain+clrs['n']+' id: '+clrs['c']+str(vivace_pid)+clrs['n'])
                    print('Most identical chain found in CHOIRdb oligomer: '+clrs['y']+template_chain+clrs['n']+' id: '+clrs['c']+str(pid)+clrs['n'])
    return templates_ids

def write_fasta(sequence):
    # Write protomer sequence to file
    fasta_file = os.path.join(workdir, pdb_name+'_CHOIR_MonomerSequence.fasta')
    with open(fasta_file, 'w') as f:
        f.write('>'+pdb_name+'\n')
        wrapped_seq = "\n".join(tw.wrap(sequence))
        f.write(wrapped_seq+'\n')
    return fasta_file

def blast_protomer(fasta_file, database, nhits, nint, nthreads, verbosity):
    print('\nRunning '+clrs['b']+'PSI-BLAST'+clrs['n']+' ( '+clrs['c']+os.path.basename(fasta_file)+clrs['n']+' x '+clrs['c']+os.path.basename(database)+clrs['n']+' )')
    blast_cmd = [psiblast_exe,
                 '-query', fasta_file,
                 '-db', database,
                 '-gapopen', '25',
                 '-gapextend', '2',
                 '-matrix', 'BLOSUM80',
                 '-word_size', '3',
                 '-num_threads', str(nthreads),
                 '-inclusion_ethresh', '0.005',
                 '-num_iterations', str(nint),
                 '-outfmt', '5',
                 '-num_alignments', '500',
                 '-comp_based_stats', '1',
                 '-max_hsps', '1']
    if database == uniref50:
        blast_cmd += ['-qcov_hsp_perc', '75']
    pctools.printv(clrs['b']+'BLAST'+clrs['n']+' command line: '+' '.join(blast_cmd), verbosity)
    blast_res = subprocess.Popen(blast_cmd, stdout=subprocess.PIPE)
    blast_xml = blast_res.stdout.read().decode()
    with open(os.path.join(workdir, 'tree.xml'), 'w') as f:
        f.write(blast_xml)
    blast_tree = et.fromstring(blast_xml)
    blast_list = {}
    for iteration in blast_tree:
        if iteration.tag == 'BlastOutput_query-len':
            query_length = iteration.text
        if iteration.tag == 'BlastOutput_iterations':
            for hits in iteration[-1]:
                if hits.tag == 'Iteration_iter-num':
                    last_iter = hits.text
                if hits.tag == 'Iteration_hits':
                    for hit in hits:
                        for hsps in hit:
                            if database == homoblast:
                                if hsps.tag == 'Hit_def':
                                    code = ':'.join(hsps.text.split('|')[-2:])
                            elif database == uniref50:
                                if hsps.tag == 'Hit_id':
                                    code = hsps.text.split(' ')[0]
                            if hsps.tag == 'Hit_hsps':
                                for hsp in hsps:
                                    for data in hsp:
                                        if data.tag == 'Hsp_score':
                                            score = data.text
                                        if data.tag == 'Hsp_identity':
                                            nid = data.text
                                        if data.tag == 'Hsp_align-len':
                                            ali_length = data.text
                                        if data.tag == 'Hsp_query-from':
                                            from_res = data.text
                                        if data.tag == 'Hsp_query-to':
                                            to_res = data.text
                        cov_length = int(to_res)-int(from_res)
                        cov = round((int(cov_length)/int(query_length))*100, 2)
                        pid = round((int(nid)/int(ali_length))*100, 2)
                        blast_list[code] = [int(score), float(pid), float(cov)]
    print('Last '+clrs['b']+'PSI-BLAST'+clrs['n']+' iteration was: '+clrs['c']+last_iter+clrs['n'])
    topn = collections.OrderedDict()
    if blast_list:
        for i in range(1,nhits+1):
            if blast_list:
                top = max(blast_list.keys(), key=(lambda x: blast_list[x][0]))
                topn[top]=blast_list[top]
                del blast_list[top]
        return topn
    else:
        return False

def generate_msa_input(topn, fasta_file, verbosity):
    multi_fasta = os.path.join(workdir, pdb_name+'_CHOIR_UniRef50Hits.fasta')
    if os.path.isfile(multi_fasta):
        os.remove(multi_fasta)
    for hit in topn:
        pctools.printv(clrs['p']+hit+clrs['y']+' score:'+clrs['c']+str(topn[hit][0])+clrs['y']+' id:'+clrs['c']+str(topn[hit][1])+clrs['y']+' cov:'+clrs['c']+str(topn[hit][2])+clrs['n'], verbosity)
        blastdbcmd = [blastdbcmd_exe, '-entry', hit, '-db', uniref50]
        pctools.printv(clrs['b']+'Blastdbcmd'+clrs['n']+' command line: '+' '.join(blastdbcmd), verbosity)
        blastdb_out = subprocess.Popen(blastdbcmd, stdout=subprocess.PIPE)
        blastdb_res = blastdb_out.stdout.read().decode()
        with open(multi_fasta, 'a') as f:
            f.write(blastdb_res+'\n')
    with open(fasta_file, 'r') as fin:
        with open(multi_fasta, 'a') as fout:
            for line in fin:
                fout.write(line)
    return multi_fasta


def run_mafft(multi_fasta, verbosity):
    print('\nRunning '+clrs['b']+'MAFFT'+clrs['n']+'...')
    msa_file = os.path.join(workdir, pdb_name+'_CHOIR_UniRef50Hits.msa')
    mafftcmd = [mafft_exe, '--localpair', '--maxiterate', '1000', '--quiet', '--thread', '8', multi_fasta]
    pctools.printv(clrs['b']+'MAFFT'+clrs['n']+' command line: '+' '.join(mafftcmd), verbosity)
    with open(msa_file, 'w') as f:
        subprocess.run(mafftcmd, stdout=f, check=True)
    print('Done running '+clrs['b']+'MAFFT'+clrs['n']+'. MSA file written to '+clrs['g']+os.path.basename(msa_file)+clrs['n'])
    return msa_file


def parse_msa(msa_file):
    msa_dict = {}
    entry = None
    with open(msa_file, 'r') as fin:
        for line in fin:
            if line.startswith('>'):
                if entry:
                    msa_dict[entry]=seq
                entry = line.split('>')[1].replace('\n','')
                seq = ''
            else:
                seqline = line.replace('\n','')
                seq += seqline
        msa_dict[entry]=seq
    return msa_dict

def trim_msa(msa_file):
    trimmed_msa = os.path.join(workdir, pdb_name+'_CHOIR_UniRef50HitsTrim.msa')
    if os.path.isfile(trimmed_msa):
        os.remove(trimmed_msa)
    # Create initial dictionary
    msa_dict = parse_msa(msa_file)
    # Get start and end positions of pdb
    for entry, seq in msa_dict.items():
        if entry == pdb_name:
            start = 0
            end = len(seq)
            for i in seq:
                if i != '-':
                    break
                start += 1
            for i in seq[::-1]:
                if i != '-':
                    break
                end -= 1
    # Create trimmed dictionary
    msa_dict_trimmed = {}
    for entry, seq in msa_dict.items():
        msa_dict_trimmed[entry] = seq[start:end]

    # Write trimmed MSA file
    with open(trimmed_msa, 'a') as fout:
        for entry, seq in msa_dict_trimmed.items():
            wrapped_seq = "\n".join(tw.wrap(seq,break_on_hyphens=False))
            fasta_entry = '>'+entry+'\n'+wrapped_seq+'\n\n'
            fout.write(fasta_entry)
    print('Trimmed MSA file written to '+clrs['g']+os.path.basename(trimmed_msa)+clrs['n'])
    return trimmed_msa

def shannon_entropy(msa_dict_trim,  surface_residues):
    # Turn sequences into arrays
    for entry, seq in msa_dict_trim.items():
        msa_dict_trim[entry] = np.array(list(seq))
    # Make dataframe
    df = pd.DataFrame.from_dict(msa_dict_trim, orient='index')
    # Remove gaps from reference sequence (the protomer sequence)
    df = df.loc[: , df.loc[pdb_name].ne('-')]
    # Fix column numbering
    x = []
    if surface_residues:
        for res in surface_residues.keys():
            x.append(int(res[3:]))

    else:
        for res in range(1,len(df.columns)+1):
            x.append(res)
    df.columns = x
    # Calculate entropies
    entropies = collections.OrderedDict()
    for column_number in df.columns:
        column = np.array(df[column_number])
        entropy = 0
        frequencies = {}
        for aa in set(column):
            count = 0
            for residue in column:
                if aa == residue:
                    count+=1
            entropy += -(count / len(column))*math.log2(count / len(column))
        entropies[column_number+1] = entropy
    return entropies

def relative_entropy(msa_dict_trim, surface_residues):
    # Turn sequences into arrays
    for entry, seq in msa_dict_trim.items():
        msa_dict_trim[entry] = np.array(list(seq))
    # Make dataframe
    df = pd.DataFrame.from_dict(msa_dict_trim, orient='index')
    # Remove gaps from reference sequence (the protomer sequence)
    df = df.loc[: , df.loc[pdb_name].ne('-')]
    # Fix column numbering
    x = []
    if surface_residues:
        for res in surface_residues.keys():
            x.append(int(res[3:]))

    else:
        for res in range(1,len(df.columns)+1):
            x.append(res)
    df.columns = x

    # Calculate entropies
    entropies = collections.OrderedDict()
    for column_number in df.columns:
        column = np.array(df[column_number])
        entropy = 0
        frequencies = {}
        for aa in set(column):
            if aa != '-' and aa != 'X':
                count = 0
                for residue in column:
                    if aa == residue:
                        count+=1
                entropy += (count / len(column))*math.log2((count / len(column))/aa_bgf[aa])
        entropies[column_number] = entropy
    return entropies


def calc_z_scores(entropies):
    #Entropy Z Scores
    average = sum(entropies.values()) / len(entropies)
    sum_dev2 = 0
    for col, entropy in entropies.items():
        dev2 = (entropy - average)**2
        sum_dev2 += dev2
    stdev = math.sqrt(sum_dev2/len(entropies))
    z_entropies = collections.OrderedDict()
    for column_number, entropy in entropies.items():
        z = (entropy - average)/stdev
        z_entropies[column_number] = z
    return z_entropies


def map_conservation(structure, z_entropies):
    for atom in structure.get_atoms():
        for res, entropy in z_entropies.items():
            if int(atom.get_parent().id[1]) == int(res):
                atom.bfactor = entropy
    io.set_structure(structure)
    outfile = os.path.join(workdir, pdb_name+'_CHOIR_Conservation.pdb')
    io.save(outfile)
    return outfile


def confirm_homo_state(hit_code, candidate_chains, interfaces_list):
    output = []
    # Create cluster dictionary and flag chains with cluster number
    clustered_nodes = {}
    for node in candidate_chains:
        clustered_nodes[node] = 0

    # Define list of edges from interfaces calculated by PISA
    edges = []
    for interface in interfaces_list:
        edge = tuple(interface['chains'])
        edges.append(edge)

    # Use edges to determine clusters
    n = 1
    while any(cluster == 0 for chain, cluster in clustered_nodes.items()):
        for chain, cluster in clustered_nodes.items():
            if cluster == 0:
                clustered_nodes[chain] = n
                break
        marked = True
        while marked is True:
            marked = False
            for edge in edges:
                for chain in edge:
                    if clustered_nodes[chain] == n:
                        for chain in edge:
                            if clustered_nodes[chain] != n:
                                clustered_nodes[chain] = n
                                marked = True

        n += 1

    # Conclusion
    clusters = set([cluster for chain, cluster in clustered_nodes.items()])
    nclusters = len(clusters)
    cluster_dict = collections.OrderedDict()
    # List clusters and choose largest
    current_largest = 0
    for cluster_n in clusters:
        cluster_chains = []
        for chain, cluster in clustered_nodes.items():
            if cluster == cluster_n:
                cluster_chains.append(chain)
        if len(cluster_chains) > current_largest:
            current_largest = len(cluster_chains)
            largest_cluster = cluster_n
        cluster_dict[cluster_n] = cluster_chains

    if nclusters == 1:
        chain_string = (', ').join(cluster_dict[cluster_n])
        output.append('All candidate chains ('+clrs['y']+chain_string+clrs['n']+') are in close contact.')
        output.append('If used as template, would yield a '+clrs['y']+' HOMO-'+oligo_dict[len(candidate_chains)]+clrs['n']+' structure.')
    elif nclusters > 1:
        output.append('Not all candidate chains in structure '+clrs['c']+hit_code+clrs['n']+' are in close contact...')
        output.append('Instead, they are divided in '+clrs['r']+str(nclusters)+' clusters:'+clrs['n'])

        for cluster_n, chains in cluster_dict.items():
            if len(chains) > 1:
                chain_string = (', ').join(chains)
                output.append('Cluster '+clrs['y']+str(cluster_n)+clrs['n']+' contains chains: '+clrs['y']+chain_string+clrs['n']+'.')
                monomeric_cluster = False
            elif len(chains) == 1:
                chain_string = (', ').join(chains)
                output.append('Cluster '+clrs['y']+str(cluster_n)+clrs['n']+' contains a single chain: '+clrs['y']+chain_string+clrs['n']+'.')
                monomeric_cluster = True
        if monomeric_cluster is False:
            output.append('Largest cluster (Cluster No. '+clrs['y']+str(largest_cluster)+clrs['n']+'), would yield a '+clrs['y']+'HOMO-'+oligo_dict[len(cluster_dict[largest_cluster])]+clrs['n']+' structure.')
        elif monomeric_cluster is True:
            output.append('Largest cluster (Cluster No. '+clrs['y']+str(largest_cluster)+clrs['n']+'), would yield a '+clrs['y']+oligo_dict[len(cluster_dict[largest_cluster])]+clrs['n']+' structure.')

    return cluster_dict, largest_cluster, '\n'.join(output)


def plot_topology(complex_name, interfaces_list, cluster_dict):
    '''

    '''
    complex_name, chain_name = complex_name.split(':')
    G = nx.Graph()
    labels = {}
    for cluster, chains in cluster_dict.items():
        for chain in sorted(chains):
            G.add_nodes_from(chain)
            labels[chain] = chain

    # Fetch maximum and minimum areas of interaction from interfaces list
    if interfaces_list:
        maxw = max([abs(interface['interface area']) for interface in interfaces_list])
        minw = min([abs(interface['interface area']) for interface in interfaces_list])
    else:
        minw = 0
        maxw = 0

    # Initalize plots
    p, ax = plt.subplots(figsize=(8, 8))
    if interfaces_list:
        ax.title.set_text('Edge Weight: '+str(round(minw, 2))+' Å² - '+str(round(maxw, 2))+' Å²')
        ax.title.set_fontweight('bold')
        ax.title.set_fontsize(20)
    plt.axis('off')
    plt.suptitle('Topology of '+complex_name, fontsize=30, fontweight='bold')
    pos = nx.drawing.circular_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=3000, alpha=0.9, linewidths=4, node_color='skyblue' )
    nodes.set_edgecolor('k')
    nx.draw_networkx_labels(G,pos,labels,font_size=25, font_weight="bold",)

    # # Create edges and set weights
    if interfaces_list:
        for interface in interfaces_list:
            edge = tuple(interface['chains'])
            w = abs(interface['interface area'])**(1/2)/abs(maxw)**(1/2)*15
            G.add_edges_from([edge])
            nx.draw_networkx_edges(G,pos,edgelist=[edge],alpha=0.9,width=w)

    # Save figure
    outpath = os.path.join(workdir, complex_name+'_'+chain_name+"_CHOIR_Topology.png")
    plt.savefig(outpath, dpi=600)
    # Close figure
    plt.close()

    # Be verbose about it
    print('Topology plot for '+complex_name+' generated : '+clrs['g']+os.path.basename(outpath)+clrs['n']+'\n')


def analyse_hits(hit):
    output = []
    hit_code, hit_chain = hit.split(':')
    if vivacemodel is False:
        output.append('\nHit '+clrs['p']+hit_code.upper()+clrs['n']+', Chain: '+clrs['y']+hit_chain+clrs['n']+', Score: '+clrs['c']+str(hits[hit][0])+clrs['n']+', %id: '+clrs['c']+str(hits[hit][1])+clrs['n']+', Coverage: '+clrs['c']+str(hits[hit][2])+clrs['n'])
    else:
        output.append('\nVivace Hit '+clrs['p']+hit_code.upper()+clrs['n']+', Chain: '+clrs['y']+hit_chain+clrs['n']+', %id: '+clrs['c']+str(hits[hit])+clrs['n'])
    middle_letters = hit_code[1:3]
    hit_pdb = os.path.join(pdb_homo_archive, middle_letters, hit_code+'.pdb.gz')
    if not os.path.isfile(hit_pdb):
        output.append(clrs['r']+'Hit '+str(hit_code)+' not found in oligomeric database. Disregarding it.'+clrs['n']+'\n')
        return hit_code, None, None, None, '\n'.join(output)
    hit_pdb_name, hit_structure, hit_nchains = pctools.parse_pdb_structure(hit_pdb)
    hit_nchains, hit_seqs, hit_chain_ids = pctools.extract_seqs(hit_structure, 0)
    hit_pids, protein_bool = pctools.get_pairwise_ids(hit_seqs, hit_nchains)
    n = 1
    candidate_chains = set()
    for id in hit_pids:
        if (id[1] == hit_chain or id[2] == hit_chain) and id[0] >= 90:
            if verbosity > 0:
                output.append('Identity between chains '+clrs['y']+str(id[2])+clrs['n']+' and '+clrs['y']+str(id[1])+clrs['n']+' is '+clrs['g']+str(round(id[0], 2))+"%"+clrs['n']+".")
            n += 1
            candidate_chains.add(id[1])
            candidate_chains.add(id[2])
    if all(id[0] > 90 for id in hit_pids) and protein_bool is True:
        hetero_complex = False
    else:
        hetero_complex = True

    initial_homo_chains = n
    if n == 1:
        output.append('No similar chains. Would yield '+clrs['y']+oligo_dict[n]+clrs['n']+' model.\n')
        return hit, None, None, None, hit_nchains, initial_homo_chains, hetero_complex, '\n'.join(output)
    else:
        chain_string = ','.join(candidate_chains)
        output.append('Similar chains '+clrs['y']+chain_string+clrs['n']+' would yield '+clrs['y']+'HOMO-'+oligo_dict[n]+clrs['n']+' model.')
        output.append('\nRunning '+clrs['b']+'PISA'+clrs['n']+' for '+clrs['p']+hit_code+clrs['n']+'...')
        pisa_output, pisa_error = pctools.run_pisa(hit_pdb, hit_chain, verbosity, gen_monomer_data=False, gen_oligomer_data=True)
        output.append(pisa_output)
        if pisa_error is True:
            output.append(clrs['r']+'Disregarding hit '+str(hit_code)+clrs['n']+'\n')
            return hit, None, None, None, hit_nchains, initial_homo_chains, hetero_complex, '\n'.join(output)
        xml_out = os.path.join(workdir, hit_code+hit_chain+'_CHOIR_PisaInterfaces.xml')
        try:
            interfaces_list, interfaces_output = pctools.parse_interfaces(xml_out, candidate_chains, verbosity)
        except et.ParseError:
            output.append(clrs['r']+'Failed to parse xml file for PISA interfaces. Disregarding hit.'+clrs['n'])
            return hit, None, None, None, hit_nchains, initial_homo_chains, hetero_complex, '\n'.join(output)
        if verbosity > 0:
            output.append(interfaces_output)
        cluster_dict, largest_cluster, confirm_homo_output = confirm_homo_state(hit_code, candidate_chains, interfaces_list)
        output.append(confirm_homo_output)
        if candidate_chains == set(cluster_dict[largest_cluster]):
            output.append('Homo-oligomeric state '+clrs['g']+'CONFIRMED'+clrs['n']+' by '+clrs['b']+' PISA'+clrs['n']+'.')
        else:
            output.append('Homo-oligomeric state '+clrs['r']+'NOT CONFIRMED'+clrs['n']+' by '+clrs['b']+' PISA'+clrs['n']+'.')
            if len(cluster_dict[largest_cluster]) == 1:
                output.append('A '+clrs['r']+oligo_dict[len(cluster_dict[largest_cluster])]+clrs['n']+' cluster means no homo-oligomeric interface was detected. Disregarding hit.')
                return hit, None, None, None, hit_nchains, initial_homo_chains, hetero_complex, '\n'.join(output)
        return hit, cluster_dict[largest_cluster], interfaces_list, cluster_dict, hit_nchains, initial_homo_chains, hetero_complex, '\n'.join(output)


# Main Function
###############################################################################
def analyze_protomer(input_file, report, args):
    global workdir
    global pdb_name
    global vivacemodel
    global hits
    global verbosity
    verbosity = args.verbosity
    workdir = os.getcwd()
    ignorevivace = args.ignorevivace
    max_candidates = args.max_candidates
    largest_oligo_complexes = collections.OrderedDict()

    if args.sequence_mode is False:
        pctools.print_section(1, 'PROTOMER ANALYSIS')
        pctools.print_subsection('1[a]', 'Protomer structure check')
        filename = os.path.basename(input_file)
        report['input_filename'] = os.path.basename(filename)
        print('Will now begin analysis of '+clrs['p']+filename+clrs['n']+'\n')
        print('Loading structure...')
        pattern = 'REMARK   6 TEMPLATE:'
        templates_ids = {}

        # Check if we are dealing with a vivace model!
        vivacemodel = False
        if ignorevivace is False:
            for line in open(input_file, 'r'):
                if re.search(pattern, line):
                    print(clrs['y']+'Dealing with a Vivace model! Kudos!'+clrs['n'])
                    vivacemodel = True
                    break

        # Check number of chains in input
        pdb_name, structure, nchains = pctools.parse_any_structure(input_file)
        if nchains == 1:
            print('Structure '+clrs['p']+pdb_name+clrs['n']+' is '+clrs['y']+'MONOMERIC'+clrs['n']+' as expected')
        else:
            print('Structure '+clrs['p']+pdb_name+clrs['n']+' contains '+clrs['y']+str(nchains)+clrs['n']+' chains.')
            print('Will consider only first chain')
            input_file = pctools.split_chains(pdb_name, structure, workdir)
            pdb_name, structure, nchains = pctools.parse_any_structure(input_file)

        # Run PISA for monomer and get surface residues
        print('\nRunning '+clrs['b']+'PISA'+clrs['n']+' for '+clrs['p']+pdb_name+clrs['n']+'...')
        output, pisa_error, monomer_data = pctools.run_pisa(input_file, '', args.verbosity, gen_monomer_data=True, gen_oligomer_data=False)
        if output:
            print(output)
        protomer_surface_residues = pctools.get_areas(monomer_data)
        residue_index_mapping = pctools.map_residue_index(protomer_surface_residues)


        # Extract sequence of (first) chain in structure
        nchains, seqs, chain_ids = pctools.extract_seqs(structure, 0)
        sequence = seqs[0][1]
        report['protomer_residues'] = str(len(sequence))
        fasta_file = write_fasta(sequence)

        # If not a Vivace model, Use PSI-BLAST to search homodb and return hits
        pctools.print_subsection('1[b]', 'Oligomeric homologues search')
        if vivacemodel is False:
            hits = blast_protomer(fasta_file, homoblast, max_candidates, 8, 8, args.verbosity)
            if not hits:
                print('PSI-BLAST found NO hits in Homo-Oligomeric database')
                return None
            else:
                for hit in hits:
                    hit_code, hit_chain = hit.split(':')
                    print('\nHit '+clrs['p']+hit_code.upper()+clrs['n']+', Chain: '+clrs['y']+hit_chain+clrs['n']+', Score: '+clrs['c']+str(hits[hit][0])+clrs['n']+', %id: '+clrs['c']+str(hits[hit][1])+clrs['n']+', Coverage: '+clrs['c']+str(hits[hit][2])+clrs['n'])
        else:
            hits = parse_vivace_model(sequence, input_file)
            if not hits:
                print('No Vivace-determined hits were found in the homo-oligomeric database. Try using --ignore-vivace.\n')
                return None

        # Run Molprobity for monomer
        protomer_molprobity = pctools.run_molprobity(input_file, args)
        report['protomer_molprobity'] = protomer_molprobity['molprobity_score']
        report['protomer_clashscore'] = protomer_molprobity['clashscore']

        if not args.skip_conservation:
            pctools.print_subsection('1[c]', 'Sequence conservation analysis')
            # Use PSI-BLAST to search UniRef50 and return hits
            uni50hits = blast_protomer(fasta_file, uniref50, 50, 1, 8, args.verbosity)
            if not uni50hits:
                print('PSI-BLAST found NO hits in Uniref50 database')
            if uni50hits:
                multi_fasta = generate_msa_input(uni50hits, fasta_file, args.verbosity)
                msa_file = run_mafft(multi_fasta, args.verbosity)
                trimmed_msa = trim_msa(msa_file)
                msa_dict_trim = parse_msa(trimmed_msa)
                entropies = relative_entropy(msa_dict_trim, protomer_surface_residues)
                z_entropies = calc_z_scores(entropies)
                report['protomer_plot'], report['protomer_exposed_area'], report['protomer_hydrophobic_area'], report['protomer_conserved_area'], minx, maxx = pctools.plot_analysis(pdb_name, protomer_surface_residues, entropies, z_entropies, args)
                monomer_conservation = map_conservation(structure, z_entropies)
                report['protomer_figure'] = pctools.pymol_screenshot_mono(monomer_conservation, z_entropies, args)
        else:
            print(clrs['y']+"Skipping section 1[c] - Sequence conservation analysis"+clrs['n']+"\n")

    elif args.sequence_mode is True:
        pctools.print_section(1, 'PROTOMER ANALYSIS - SEQUENCE MODE')
        print(clrs['y']+"Skipping section 1[a] - Protomer structure check"+clrs['n']+"\n")
        if input_file.lower().endswith('.fasta'):
            fasta_file = input_file
            pdb_name = os.path.basename(fasta_file).split("_CHOIR_MonomerSequence.fasta")[0].replace('.', '_')
            report['input_filename'] = os.path.basename(fasta_file)

        elif args.input_file.endswith('.pdb'):
            report['input_filename'] = os.path.basename(input_file)
            pdb_name, structure, nchains = pctools.parse_any_structure(input_file)
            nchains, seqs, chain_ids = pctools.extract_seqs(structure, 0)
            sequence = seqs[0][1]
            residue_index_mapping = {}
            for i in sequence:
                residue_index_mapping[i] = i
            fasta_file = write_fasta(sequence)
            if nchains == 1:
                print('Structure '+clrs['p']+pdb_name+clrs['n']+' is '+clrs['y']+'MONOMERIC'+clrs['n']+' as expected')
            else:
                print('Structure '+clrs['p']+pdb_name+clrs['n']+' contains '+clrs['y']+str(nchains)+clrs['n']+' chains.')
                print('Will consider only first chain')
        vivacemodel = False

        pctools.print_subsection('1[b]', 'Oligomeric homologues search')
        hits = blast_protomer(fasta_file, homoblast, max_candidates, 8, 8, args.verbosity)
        if not hits:
            print('PSI-BLAST found NO hits in Homo-Oligomeric database')
            return None

        if not args.skip_conservation:
            pctools.print_subsection('1[c]', 'Sequence conservation analysis')
            # Use PSI-BLAST to search UniRef50 and return hits
            uni50hits = blast_protomer(fasta_file, uniref50, 50, 1, 8, args.verbosity)
            if not uni50hits:
                print('PSI-BLAST found NO hits in Uniref50 database')
            if uni50hits:
                multi_fasta = generate_msa_input(uni50hits, fasta_file, args.verbosity)
                msa_file = run_mafft(multi_fasta, args.verbosity)
                trimmed_msa = trim_msa(msa_file)
                msa_dict_trim = parse_msa(trimmed_msa)
                entropies = relative_entropy(msa_dict_trim, None)
                z_entropies = calc_z_scores(entropies)
                report['protomer_plot'] = pctools.plot_entropy_only(pdb_name, entropies, z_entropies, args)
        else:
            print(clrs['y']+"Skipping section 1[c] - Sequence conservation analysis"+clrs['n']+"\n")



    # Analyse hits
    report['hits'] = {}
    if hits:
        pctools.print_subsection('1[d]', 'Oligomeric homologues analysis')
        p = Pool()
        interfaces_dict = {}
        for hitchain, largest_cluster, interfaces_list, cluster_dict, total_chains, initial_homo_chains, hetero_complex, output in p.map_async(analyse_hits, hits).get():
        #for hit in hits:
        #    hitchain, largest_cluster, interfaces_list, cluster_dict, total_chains, initial_homo_chains, hetero_complex, output = analyse_hits(hit)
            report['hits'][hitchain] = {}
            report['hits'][hitchain]['hetero_complex'] = hetero_complex
            report['hits'][hitchain]['total_chains'] = total_chains
            report['hits'][hitchain]['initial_homo_chains'] = initial_homo_chains
            print(output)

            if largest_cluster is None:
                report['hits'][hitchain]['qscore'] = 'N/A'
                report['hits'][hitchain]['final_homo_chains'] = '0'
                print('-------------------------------------------------------------------')
                continue
            largest_oligo_complexes[hitchain] = largest_cluster
            report['hits'][hitchain]['final_homo_chains'] = str(len(largest_cluster))
            if args.plot_topologies is True:
                plot_topology(hitchain, interfaces_list, cluster_dict)
            interfaces_dict[hitchain] = interfaces_list
            print('-------------------------------------------------------------------')
        p.close()
        p.join()

    if not largest_oligo_complexes:
        print('**ProtCHOIR'+clrs['r']+' failed '+clrs['n']+'to select good oligomeric templates.\n')
        return None

    for hitchain in hits:
        hit_code, chain = hitchain.split(':')
        report['hits'][hitchain]['hit_code'] = hit_code
        report['hits'][hitchain]['chain'] = chain
        if vivacemodel is False:
            report['hits'][hitchain]['score'] = str(hits[hitchain][0])
            report['hits'][hitchain]['id'] = str(hits[hitchain][1])
            report['hits'][hitchain]['coverage'] = str(hits[hitchain][2])
        else:
            report['hits'][hitchain]['score'] = 'N/A'
            report['hits'][hitchain]['id'] = str(round(hits[hitchain], 1))
            report['hits'][hitchain]['coverage'] = 'N/A'

    pickle.dump(largest_oligo_complexes, open('CHOIR_OligoComplexes.pickle', 'wb'))

    if args.sequence_mode:
        if args.skip_conservation:
            return pdb_name, largest_oligo_complexes, interfaces_dict, report
        elif not args.skip_conservation:
            return pdb_name, largest_oligo_complexes, interfaces_dict, entropies, z_entropies, report

    elif not args.sequence_mode:
        if args.skip_conservation:
            return pdb_name, largest_oligo_complexes, interfaces_dict, residue_index_mapping, report
        elif not args.skip_conservation:
            return pdb_name, largest_oligo_complexes, interfaces_dict, entropies, z_entropies, residue_index_mapping, minx, maxx, report
