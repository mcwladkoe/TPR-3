from pyramid.response import Response
from pyramid.view import view_config

import json

import logging

from tpr_3 import utils


@view_config(route_name='index', renderer='index.mako')
def index(request):
    msg = ''
    indexes = []

    try:
        kriterii = int(request.params.get('kr', '5'))
    except:
        kriterii = 5
    if kriterii < 2:
        kriterii = 2
    
    try:
        alternativi = int(request.params.get('alt', '5'))
    except:
        alternativi = 5
    if alternativi < 2:
        alternativi = 2
    
    mas = utils.req_to_mas(request, kriterii, alternativi)
    ne = utils.req_ne_to_mas(request, kriterii)
    zn = utils.req_zn_to_mas(request, kriterii)

    if request.params.get('import'):
        try:
            input_file = request.POST['import_file'].file
            data = json.load(input_file)
            mas = data.get('mas')
            ne = data.get('ne')
            zn = data.get('zn')
            alternativi = len(mas[0])
            kriterii = len(mas)
        except:
            msg = 'Something went wrong'
    
    if request.params.get('smbt'):
        if request.params.get('meth') == 'maxmin':
            indexes = maxmin(mas)
        elif request.params.get('meth') == 'abs_resh':
            indexes = abs_resh(mas, ne)
        elif request.params.get('meth') == 'osn':
            indexes = osn_par(mas, utils.req_zn_to_mas(request, kriterii))
        elif request.params.get('meth') == 'kompr':
            indexes = kompr(mas, utils.req_zn_to_mas(request, kriterii))
        elif request.params.get('meth') == 'etalon':
            indexes = etalon(mas, ne, utils.req_zn_to_mas(request, kriterii))
        elif request.params.get('meth') == 'analiie':
            indexes = analiie(mas, utils.req_zn_to_mas(request, kriterii))
        else:
            indexes = []

    return {
        'msg': msg,
        'alternativi': alternativi,
        'kriterii': kriterii,
        'indexes': indexes,
        'mas': mas,
        'ne': ne,
        'zn': zn,
    }


def maxmin(mas):
    indexes = []
    tempInner = 0
    tempOuter = -99999999.0
    for i in range(len(mas)):
        tempInner = 999999999.0
        for j in range(len(mas[i])):
            tempInner = min(tempInner, mas[i][j])
        if tempInner > tempOuter:
            tempOuter = tempInner
            indexes.append(str(i + 1))
    return indexes


def abs_resh(mas, ne):
    indexes = []
    for i in range(len(mas[0])):
        is_ = True
        for j in range(len(mas)):
            if mas[j][i] < ne[j]:
                is_ = False
        if is_:
            indexes.append(str(i + 1))
    return indexes


def osn_par(mas, zn):
    indexes = range(len(mas[0]))
    tmp_zn = zn
    for i in range(len(tmp_zn)):
        if tmp_zn[i] == -9999999999:
            tmp_zn[i] = 0
    id_op = 0

    while len(indexes) > 1 and sum(tmp_zn) != 0:
        id_op+=1
        max_z = -1
        ind = -1
        ii = 0
        for i in tmp_zn:
            if i > max_z:
                max_z = i
                ind = ii
            ii += 1
        tmp_zn[ind] = 0
        ii = 0
        for i in mas[ind]:
            if i < max(mas[ind]) and ii in indexes:
                indexes.remove(ii)
            ii += 1
    return [str(i+1) for i in indexes]
    
def kompr(mas, zn):
    tmp_zn = zn
    for i in range(len(tmp_zn)):
        if tmp_zn[i] == -9999999999:
            tmp_zn[i] = 0
    id_op = 0

    znachimosti = []
        
    for i in tmp_zn:
        znachimosti.append(i/sum(tmp_zn))
    int_par = []
    for i in range(len(mas[0])):
        tmp = 0
        for j in range(len(znachimosti)):
            tmp += mas[j][i]*znachimosti[j]
        int_par.append(tmp)
    indexes = []
    for i in range(len(int_par)):
        if int_par[i] == max(int_par):
            indexes.append(i)
    return [str(i+1) for i in indexes]
    
def etalon(mas, ne, zn):
    tmp_zn = zn
    for i in range(len(tmp_zn)):
        if tmp_zn[i] == -9999999999:
            tmp_zn[i] = 0
    id_op = 0

    znachimosti = []
        
    for i in tmp_zn:
        znachimosti.append(i/sum(tmp_zn))
    tmp_indexes = []
    for i in range(len(mas[0])):
        is_et = True
        for j in range(len(mas)):
            if mas[j][i] < ne[j]:
                is_et = False
        if is_et:
            tmp_indexes.append(i)
    int_par = []
    for i in tmp_indexes:
        tmp = 0
        for j in range(len(znachimosti)):
            tmp += (mas[j][i]-ne[j])*znachimosti[j]
        int_par.append(tmp)
    indexes = []
    for i in range(len(tmp_indexes)):
        if int_par[i] == max(int_par):
            indexes.append(tmp_indexes[i])
    return [str(i+1) for i in indexes]


def analiie(mas, zn):
    zn_new_matrix = []
    for i in range(len(zn)):
        tmp = []
        for j in range(len(zn)):
            t = zn[i] - zn[j]
            koef = round(10 * abs(t)) + 1
            if not koef % 2:
                koef -= 1
            if t < 0:
                tmp.append(1.0/koef)
            else:
                tmp.append(koef)
        zn_new_matrix.append(tmp)
    sobstv_vektor_krit = []
    for i in range(len(zn_new_matrix)):
        tmp = 1
        for j in range(len(zn_new_matrix)):
            tmp *= zn_new_matrix[i][j]
        sobstv_vektor_krit.append((tmp)**(1.0/len(zn_new_matrix)))
    ves_krit = []
    for i in range(len(sobstv_vektor_krit)):
        ves_krit.append(sobstv_vektor_krit[i]/sum(sobstv_vektor_krit))
    #for all krit
    new_mas = []
    for i in range(len(mas)):
        tmp_mas = mas[i]
        tmp_mas_new = []
        for l in range(len(tmp_mas)):
            tmp = []
            for j in range(len(tmp_mas)):
                t = tmp_mas[l] - tmp_mas[j]
                koef = round(10 * abs(t)) + 1
                if not koef % 2:
                    koef -= 1
                if t < 0:
                    tmp.append(1.0/koef)
                else:
                    tmp.append(koef)
            tmp_mas_new.append(tmp)
        sobstv_vektor_tmp = []
        for l in range(len(tmp_mas_new)):
            tmp = 1
            for j in range(len(tmp_mas_new)):
                tmp *= tmp_mas_new[l][j]
            sobstv_vektor_tmp.append((tmp)**(1.0/len(tmp_mas_new)))
        ves_zn = []
        for l in range(len(sobstv_vektor_tmp)):
            ves_zn.append(round(sobstv_vektor_tmp[l]/sum(sobstv_vektor_tmp), 4))
        new_mas.append(ves_zn)
    #calc total
    funct = []
    for i in range(len(mas[0])):
        tmp = 0
        for j in range(len(mas)):
            tmp += new_mas[j][i]*ves_krit[j]
        funct.append(tmp)
    indexes = []
    for i in range(len(funct)):
        if funct[i] == max(funct):
            indexes.append(i)
    return [str(i+1) for i in indexes]


@view_config(route_name='export', renderer='json')
def export(request):
    try:
        kriterii = int(request.params.get('kr', '8'))
    except:
        kriterii = 8
    if kriterii < 8:
        kriterii = 8
    
    try:
        alternativi = int(request.params.get('alt', '8'))
    except:
        alternativi = 8
    if alternativi < 8:
        alternativi = 8

    mas = utils.req_to_mas(request, kriterii, alternativi)
    ne = utils.req_ne_to_mas(request, kriterii)
    zn = utils.req_zn_to_mas(request, kriterii)
    request.response.body = json.dumps({
        'mas': mas,
        'ne': ne,
        'zn': zn,
    })
    
    headers = request.response.headers
    headers['Content-Description'] = 'File Transfer'
    headers['Content-Type'] = 'application/force-download'
    headers['Accept-Ranges'] = 'bytes'
    headers['Content-Disposition'] = 'attachment'
    return request.response
    