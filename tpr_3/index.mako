<html lang="en">
<head>
    <title>ТПР3</title>
</head>
<body>
    <form action="${request.current_route_url()}" method="get">
        <label for="alt">Альтернатив<label><input id="alt" type="number" min="8" max="100" name="alt" onchange="this.form.submit()" value="${int(alternativi)}"></input>
        <label for="alt">Критериев<label><input id="kr" type="number" min="8" max="100" name="kr" onchange="this.form.submit()" value="${int(kriterii)}"></input>
    </form>
    <form action="${request.current_route_url()}" method="post">
        <table border='1'>
            <tr>
                <td></td>
                % for j in range(int(alternativi)):
                    <td>
                        Альтернатива ${j+1}
                    </td>
                % endfor
            </tr>
            % for i in range(int(kriterii)):
                <tr>
                    <td>
                        Критерий ${i+1}
                    </td>
                    % for j in range(int(alternativi)):
                        <td>
                            <input type="number" step="0.1" min="0.1" max="0.9" name="${u'{},{}'.format(i,j)}" value="${request.params.get(u'{},{}'.format(i,j))}"></input>
                        </td>
                % endfor
                </tr>
            % endfor
        </table>
        <button type="submit" name="smbt" value="1">Submit</button>
    </form>
    % if index:
        <script>alert('Index: '+${index})</script>
    % endif
</body>
</html>