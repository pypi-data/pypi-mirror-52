#!/usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def FastaToArray(infile):
    '''
    Convert an alignment into a numpy array.

    Parameters
    ----------
    fasta_dict: dict
        dictionary based on a fasta file with sequence names as keys and
        sequences as values

    Returns
    -------
    arr: np.array
        2D numpy array in the same order as fasta_dict where each row
        represents a single column in the alignment and each column a
        single sequence.
    nams: list
        List of sequence names in the same order as in the input file
    '''

    nams = []
    seqs = []
    nam = ""
    seq = ""
    with open(infile) as input:
        for line in input:
            line = line.strip()
            if line[0] == ">":
                    seqs.append(seq)
                    nams.append(nam)
                    seq = []
                    nam = line.replace(">", "")
            else:
                seq += list(line)
    seqs.append(seq)
    nams.append(nam)
    arr = np.array(seqs[1:])
    return (arr, nams[1:])


def getAAColours():
    '''
    Generates a dictionary which assigns a colour to each amino acid.
    Based on the "RasmMol" amino colour scheme and the table here:
        http://acces.ens-lyon.fr/biotic/rastop/help/colour.htm
    (plus grey for "X" and white for "-")

    Parameters
    ----------
    None

    Returns
    -------
    dict
        Dictionary where keys are single letter amino acid codes and
        values are hexadecimal codes for colours
    '''
    return {'D': '#E60A0A',
            'E': '#E60A0A',
            'C': '#E6E600',
            'M': '#E6E600',
            'K': '#145AFF',
            'R': '#145AFF',
            'S': '#FA9600',
            'T': '#FA9600',
            'F': '#3232AA',
            'Y': '#3232AA',
            'N': '#00DCDC',
            'Q': '#00DCDC',
            'G': '#EBEBEB',
            'L': '#0F820F',
            'V': '#0F820F',
            'I': '#0F820F',
            'A': '#C8C8C8',
            'W': '#B45AB4',
            'H': '#8282D2',
            'P': '#DC9682',
            'X': '#b2b2b2',
            '-': '#FFFFFF00'}


def getNtColours():
    '''
    Generates a dictionary which assigns a colour to each nucleotide (plus grey
    for "N" and white for "-")
    Parameters
    ----------
    None

    Returns
    -------
    dict
        Dictionary where keys are single letter nucleotide codes and
        values are hexadecimal codes for colours
    '''
    return {'A': '#1ed30f',
            'G': '#f4d931',
            'T': '#f43131',
            'C': '#315af4',
            'N': '#b2b2b2',
            "-": '#FFFFFF',
            "U": '#f43131'}


def writeOutfile(outfile, arr, nams, removed, rmfile=None):
    '''
    Writes an alignment stored in a numpy array into a FASTA file.

    Parameters
    ----------
    outfile: str
        Path to FASTA file where the output should be stored
    arr: np.array
        Numpy array containing the parsed alignment
    nams: list
        List of nams of sequences in the input alignment
    removed: set
        Set of names of sequences which have been removed
    rmfile: str
        Path to file used to log sequences and columns which have been removed

    Returns
    -------
    None

    '''
    out = open(outfile, "w")
    if rmfile is not None:
        rm = open(rmfile, "a")
        rm.write("Removed sequences:\n")
    else:
        rm = None
    i = 0
    for nam in nams:
        if nam not in removed:
            out.write(">%s\n%s\n" % (nam, "".join(list(arr[i]))))
            i += 1
        else:
            if rm is not None:
                rm.write("%s\n" % nam)
    out.close()
    if rm is not None:
        rm.close()


def seqType(arr):
    '''
    Detects if an alignment is of nucleotides or amino acids using pre-built
    dictionarys of amino acid and nucleotide codes.

    Parameters
    ----------
    arr: np.array
        Numpy array containing the alignment

    Returns
    -------
    str
    'aa' for amino acid and 'nt for nucleotide
    '''
    seq1 = arr[0]
    nucs = set(list(getNtColours().keys()))
    aas = set(list(getAAColours().keys()))
    n = 0
    a = 0
    x = 0
    for s in seq1:
        s = s.upper()
        if s in nucs:
            n += 1
        if s in aas:
            a += 1
        if s not in aas and s not in nucs:
            x += 1
    counts = n, a, x
    if n == max(counts):
        return "nt"
    elif a == max(counts):
        return "aa"
    else:
        raise RuntimeError("Majority of positions are not known \
                            nucleotides or amino acids")


def updateNams(nams, removed_seqs):
    '''
    Takes nams, a list of sequence names in the input file, and removed_seqs,
    a set of sequences which have been removed from the file and subtracts
    the removed sequences from nams while maintaining the order.

    Parameters
    ----------
    nams: list
        A list of sequence names in the input file
    removed_seqs: set
        Set of sequence names to remove

    Returns
    -------
    nams2: list
        A list of sequence names which have not been removed
    '''
    nams2 = []
    for nam in nams:
        if nam not in removed_seqs:
            nams2.append(nam)
    return (nams2)


def checkArrLength(arr, log):
    '''
    Checks the shape of the array containing the alignment to ensure that it
    all the sequences haven't been removed by parsing and that all the
    sequences have the same number of columns

    Parameters
    -----------
    arr: np.array
        Numpy array containing the multiple sequence alignment
    log: logging.Logger
        An open log file object
    Returns
    -------
    None
    '''
    emptyAlignmentMessage = """Error: Parsing your alignment with these \
    settings has removed all of the sequences."""
    differentLengthsMessage = """Error: The sequences in your alignment \
    are not all the same length."""
    if 0 in np.shape(arr):
        log.error(emptyAlignmentMessage)
        raise RuntimeError(emptyAlignmentMessage)
    if len(np.shape(arr)) == 1:
        log.error(differentLengthsMessage)
        raise RuntimeError(differentLengthsMessage)


def listFonts(outfile):
    '''
    Generates an image file containing a sample of all the fonts matplotlib
    has access to on your system, which can be used to choose a font for a
    text-based sequence logo.
    Not parameterised - the same image will be generated every time.

    Parameters
    ----------
    outfile: str
        Path to the file in which to save the image

    Returns
    -------
    None
    '''
    flist = matplotlib.font_manager.get_fontconfig_fonts()
    flist2 = []
    for fname in flist:
        try:
            g = matplotlib.font_manager.FontProperties(fname=fname).get_name()
            flist2.append(g)
        except:
            # Some of the fonts seem not to have a name? Ignore these.
            pass
    f = plt.figure(figsize=(3, len(flist2) / 4), dpi=200)
    a = f.add_subplot(111)
    a.set_ylim(0, len(flist2))
    a.set_xlim(0, 1)
    for i, fname in enumerate(flist2):
        a.text(0, i, fname, fontdict={'name': fname})
    a.set_axis_off()
    f.savefig(outfile, dpi=200, bbox_inches='tight')
