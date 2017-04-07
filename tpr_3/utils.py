
def req_to_mas(request, kriterii, alternativi):
    mas = []
    for i in range(kriterii):
        mas.append([])
        for j in range(alternativi):
            try:
                tmp = float(request.params.get('{},{}'.format(i, j)))
                if tmp < 0.1 or tmp > 0.9:
                    raise ValueError(123)
            except:
                tmp = -9999999999
            mas[i].append(tmp)
    return mas