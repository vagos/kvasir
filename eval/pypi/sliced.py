def sliced(lst, n):
    '''Yield n number of slices from lst.'''
    # Original algorithm from Jurgen Strydom posted 2019-02-21 Stack Overflow
    for i in range(n):
        yield lst[i::n]
