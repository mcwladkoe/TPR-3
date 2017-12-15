<!DOCTYPE html>
<html lang="en">
<head>
    <title>ТПР3</title>
    <!-- BOOTSTRAP -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <script type="text/javascript" src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.2.1.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/4.3.9/css/fileinput.min.css">
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/javascript-canvas-to-blob/3.7.0/js/canvas-to-blob.min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/js/sortable.min.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/0.8.5/purify.min.js" type="text/javascript"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/4.3.9/js/fileinput.min.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/4.3.9/themes/fa/theme.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/4.3.9/js/locales/ru.js"></script>
    
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.12.2/css/bootstrap-select.min.css">
</head>
<body>
    <p style="margin: 10px">${msg}</p>
    <form action="${request.current_route_url()}" method="post" enctype="multipart/form-data">
        <div class="row">
            <div class="form-inline">
                <div class="col-md-3 col-xs-6 col-sm-3 col-lg-3 form-group">
                    <label for="alt" style="margin: 10px">Альтернатив</label><input id="alt" class="form-control input-sm" type="number" min="2" max="100" name="alt" onchange="this.form.submit()" value="${alternativi}"></input>
                </div>
                <div class="col-md-3 col-xs-6 col-sm-3 col-lg-3 form-group">
                    <label for="alt" style="margin: 10px">Критериев</label><input id="kr" class="form-control input-sm" type="number" min="2" max="100" name="kr" onchange="this.form.submit()" value="${kriterii}"></input>
                </div>
            </div>
        </div>
        <div class="row" style="margin: 10px">
            <table class="table table-striped" border="1">
            <colgroup>
                <col>
                % for j in range(int(alternativi)):
                    <col class="col-xs-1 col-lg-1">
                % endfor
                <col class="col-xs-1 col-lg-1">
                <col class="col-xs-1 col-lg-1">
            </colgroup>
                <tr>
                    <td></td>
                    % for j in range(int(alternativi)):
                        <td ${"bgcolor=green" if str(j+1) in indexes else ""} style="margin: 10px">
                            Альтернатива ${j+1}
                        </td>
                    % endfor
                    <td>Не меньше(эталлонное значение)</td>
                    <td>Значимость</td>
                </tr>
                % for i in range(kriterii):
                    <tr>
                        <td style="margin: 10px">
                            Критерий ${i+1}
                        </td>
                        % for j in range(alternativi):
                            <td ${"bgcolor=green" if str(j+1) in indexes else ""}>
                                <input class="form-control input-sm" type="number" step="0.01" min="0.1" max="0.9" name="${u'{},{}'.format(i,j)}" value="${'' if mas[i][j] == -9999999999 else mas[i][j]}" onchange="this.form.submit()"></input>
                            </td>
                        % endfor
                        <td>
                            <input class="form-control input-sm" type="number" step="0.01" min="0.1" max="0.9" name="${u'ne{}'.format(i)}" value="${'' if ne[i] == -9999999999 else ne[i]}" onchange="this.form.submit()"></input>
                        </td>
                        <td>
                            <input class="form-control input-sm" type="number" step="0.01" min="0.1" max="0.9" name="${u'zn{}'.format(i)}" value="${'' if zn[i] == -9999999999 else zn[i]}" onchange="this.form.submit()"></input>
                        </td>
                    </tr>
                % endfor
            </table>
        </div>
        <div class="form-inline">
            <div class="col-md-5 col-xs-12 col-sm-5 col-lg-5 form-group">
                <label style="margin: 10px" for="meth_id">Method</label>
                <select id="meth_id" name="meth" class="bootstrap-select">
                    <option value="maxmin">Максминный</option>
                    <option value="abs_resh">Абсолютного решения</option>
                    <option value="osn">Основного параметра</option>
                    <option value="kompr">Компромисного решения</option>
                    <option value="etalon">Эталонного сравнения</option>
                    <option value="analiie">МАИ</option>
                </select>
                <button class="btn btn-primary" type="submit" name="smbt" value="1">Submit</button>
            </div>
            <div class="col-md-5 col-xs-12 col-sm-5 col-lg-5 form-group">
                <label style="margin: 10px" for="file_id">Input file</label><input type="file" name="import_file" id="file_id" class="file-loading"></input>
                <script>
                    $(document).on('ready', function() {
                        $("#file_id").fileinput({showCaption: false});
                    });
                </script>
                <button class="btn btn-primary" type="submit" name="import" value="1">Import</button>
            </div>
            <div class="col-md-2 col-xs-12 col-sm-2 col-lg-2 form-group">
                <button class="btn btn-primary" type="submit" formaction="${request.route_url('export')}?alt=${alternativi}&&kr=${kriterii}" target="_blank">Export</button>
            </div>
        <div>
    </form>
    
    % if indexes:
        <script>alert('Indexes: '+${' '.join(indexes)})</script>
    % endif
</body>
</html>