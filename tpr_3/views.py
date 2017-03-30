from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='index', renderer='index.mako')
def index(request):
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

    index = 0
    if request.params.get('smbt'):
        tempInner = 0
        tempOuter = -99999999.0
        for i in range(alternativi):
            tempInner = 999999999.0
            for j in range(kriterii):
                try:
                    tmp_zn = float(request.params.get('{},{}'.format(j, i)))
                except:
                    tmp_zn = -999999999.0
                tempInner = min(tempInner, tmp_zn)
            if tempInner > tempOuter:
                tempOuter = tempInner
                index = i+1
    return {
        'alternativi': alternativi,
        'kriterii': kriterii,
        'index': index,
    }
