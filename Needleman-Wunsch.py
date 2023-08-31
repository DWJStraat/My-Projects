import numpy

def aligner(string1, string2, hit=1, miss=1, gap=1):
    """
    This piece of code runs a simplified version of the Needleman-Wunsch
    algorithm

    Credit to slowkow ( profile: https://gist.github.com/slowkow ) for his
    original code

    Parameters
    ----------
    string1 : Str
        The first string to be aligned.
    string2 : Str
        The second string to be aligned.
    hit : Int, optional
        Hit reward. The default is 1.
    miss : Int, optional
        Miss penalty. The default is 1.
    gap : Int, optional
        Gap penalty. The default is 1..

    Returns
    -------
    r1 : Str
        The first string, aligned with the second.
    r2 : Str
        The second string, aligned with the first.

    """
    n1 = len(string1)
    n2 = len(string2)
    # Score for each possible pair of characters
    score = numpy.zeros((n1 + 1, n2 + 1))
    score[:, 0] = numpy.linspace(0, -n1 * gap, n1 + 1)
    score[0, :] = numpy.linspace(0, -n2 * gap, n2 + 1)
    # Find optimal alignment
    aligner = numpy.zeros((n1 + 1, n2 + 1))
    aligner[:, 0] = 3
    aligner[0, :] = 4
    # Temporary scores
    temp = numpy.zeros(3)
    for i in range(n1):
        for j in range(n2):
            if string1[i] == string2[j]:
                temp[0] = score[i, j] + hit
            else:
                temp[0] = score[i, j] - miss
            temp[1] = score[i, j + 1] - gap
            temp[2] = score[i + 1, j] - gap
            tempmax = numpy.max(temp)
            score[i + 1, j + 1] = tempmax
            if temp[0] == tempmax:
                aligner[i + 1, j + 1] += 2
            if temp[1] == tempmax:
                aligner[i + 1, j + 1] += 3
            if temp[2] == tempmax:
                aligner[i + 1, j + 1] += 4

    # Find an optimal alignment
    i = n1
    j = n2
    r1 = []
    r2 = []
    while i > 0 or j > 0:
        if aligner[i, j] in [2, 5, 6, 9]:
            r1.append(string1[i - 1])
            r2.append(string2[j - 1])
            i -= 1
            j -= 1
        elif aligner[i, j] in [3, 5, 7, 9]:
            r1.append(string1[i - 1])
            r2.append('-')
            i -= 1
        elif aligner[i, j] in [4, 6, 7, 9]:
            r1.append('-')
            r2.append(string2[j - 1])
            j -= 1
    # Reverse the strings
    r1 = ''.join(r1)[::-1]
    r2 = ''.join(r2)[::-1]
    return r1, r2