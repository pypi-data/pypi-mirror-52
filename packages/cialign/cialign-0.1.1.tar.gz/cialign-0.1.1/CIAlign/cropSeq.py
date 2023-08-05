#! /usr/bin/env python

def determineStartEnd(sequence, mingap=10):
    '''
    Determines the start and the end of a sequence by calling a subroutine

    Parameters
    ----------
    sequence: numpy array
        sequence

    mingap: int
        minimal gap number (default: 10)

    Returns
    -------
    start: int
        redefined start of the sequence

    end: int
        redefined end of the seuquence

    '''

    start = 0
    end = 0

    start = findValue(sequence, mingap)
    # put in reverse for end
    end = len(sequence) - findValue(sequence[::-1])


    if start > end:
        return (0, 0)
    return(start, end)

def findValue(sequence, mingap=10):
    '''
    Determines the start of the given sequence

    Parameters
    ----------
    sequence: numpy array
        sequence

    mingap: int
        minimal gap number (default: 10)

    Returns
    -------
    int
        value for start or end (when put in reverse) of sequence
    '''

    position = 0
    boundary1 = 50
    boundary2 = 80
    boundary3 = 20

    # todo: make boundarys parameters!

    gaps = countGaps(sequence)

    if len(gaps) < 11:
        return(gaps[0] + 1)

    if len(gaps) <= 80:
        boundary1 = 10
        boundary2 = 19
        boundary3 = 10


    # this pattern doesn't indicate an incomplete sequence, set start to 0
    if gaps[boundary1] < boundary3:
        return 0

    # for more fluctuation within the sequence, meaning we observe a few nt within many gaps -> indicates incomplete sequence
    for n in range(0, boundary2):
        if gaps[n+1] - gaps[n] > mingap:
            position = n + 1 + gaps[n+1]
    if position > 0:
        return position

    # if none of above, take the first nt/aa as start of the sequence
    return(gaps[0] + 1)

def countGaps(sequence):
    '''
    Counts the gaps in a sequence preceding each non-gap position

    Parameters
    ----------

    sequence: numpy array
        sequence

    Returns
    -------
    gapNumbers: list
        list of ints of the length of the sequence without gaps

    '''

    gapNumbers = []
    gapCounter = 0

    for element in sequence:
        if element == '-':
            gapCounter += 1
        else:
            gapNumbers.append(gapCounter)

    return gapNumbers
