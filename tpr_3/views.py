from pyramid.response import Response
from pyramid.view import view_config

import json

from tpr_3 import utils


@view_config(route_name='index', renderer='index.mako')
def index(request):
    msg = ''
    indexes = []

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

    if request.params.get('import'):
        try:
            input_file = request.POST['import_file'].file
            data = json.load(input_file)
            mas = data['mas']
            alternativi = len(mas[0])
            kriterii = len(mas)
        except:
            msg = 'Something went wrong'
    
    if request.params.get('smbt'):
        if request.params.get('meth') == 'maxmin':
            indexes = maxmin(mas)
        elif request.params.get('meth') != 'maxmin':
            pass
    
    return {
        'msg': msg,
        'alternativi': alternativi,
        'kriterii': kriterii,
        'indexes': indexes,
        'mas': mas,
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
    request.response.body = json.dumps({'mas': mas})
    
    headers = request.response.headers
    headers['Content-Description'] = 'File Transfer'
    headers['Content-Type'] = 'application/force-download'
    headers['Accept-Ranges'] = 'bytes'
    headers['Content-Disposition'] = 'attachment'
    return request.response
    