def pa(item):
    for ei in item:
        if isinstance(ei,list):
            pa(ei)
        else:
            print(ei)