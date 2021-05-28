import fundamentus

import flask
from flask import request, make_response

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=["GET"])
def papel():
    if 'papel' in request.args:
        ticker = request.args['papel']
    else:
        return make_response('Error: ticker not found', 400)

    return app.response_class(
        response=fundamentus.get_papel(ticker).to_json(),
        mimetype='application/json',
        status=200)

def filter_interval(df, filters, column, df_column=None):
    if not df_column:
        df_column = column

    if (column + '_min') in filters:
        df = df[df[df_column] >= float(filters[column + '_min'])]
    if (column + '_max') in filters:
        df = df[df[df_column] <= float(filters[column + '_max'])]

    return df

def filter(df, filters):
    df = filter_interval(df, filters, 'pl')
    df = filter_interval(df, filters, 'pvp')
    df = filter_interval(df, filters, 'psr')
    df = filter_interval(df, filters, 'divy', 'dy')
    df = filter_interval(df, filters, 'pativos', 'pa')
    df = filter_interval(df, filters, 'pcapgiro', 'pcg')
    df = filter_interval(df, filters, 'pebit')
    df = filter_interval(df, filters, 'fgrah', 'pacl')
    df = filter_interval(df, filters, 'firma_ebit', 'evebit')
    df = filter_interval(df, filters, 'firma_ebitda', 'evebitda')
    df = filter_interval(df, filters, 'margemebit', 'mrgebit')
    df = filter_interval(df, filters, 'margemliq', 'mrgliq')
    df = filter_interval(df, filters, 'liqcorr', 'liqc')
    df = filter_interval(df, filters, 'roic')
    df = filter_interval(df, filters, 'roe')
    df = filter_interval(df, filters, 'liq', 'liq2m')
    df = filter_interval(df, filters, 'patrim', 'patrliq')
    df = filter_interval(df, filters, 'divliq', 'divbpatr')
    df = filter_interval(df, filters, 'tx_cresc_rec', 'c5y')

    return df

@app.route('/', methods=["POST"])
def filtro():
    df = filter(fundamentus.get_resultado(), request.form)

    return app.response_class(
        response=df.to_json(),
        mimetype='application/json',
        status=200)

if __name__ == "__main__":
    app.run()