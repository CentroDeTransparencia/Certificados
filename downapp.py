import os
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

UPLOAD_DIRECTORY = "app_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
# external_stylesheets = ['style.css']
app = dash.Dash(server=server)
# was app = dash.Dash(server=server, external_stylesheets=external_stylesheets)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div(
    [
        html.Link(
            rel='stylesheet',
            type='text/css',
            href='/style.css'
        ),
        html.Img(src='assets/head1.jpg'),
        html.H1('Certificado del Evento'),
        html.Div(children='''
                Descargue aquí su certificado del evento: \"Centro
                de Transparencia: La Información de la Exploración
                de Yacimientos No Convencionales en un Contexto Social
                Complejo\" llevado a cabo en julio 27 de 2022 puede
                obtenerse en esta página.
            '''),
        html.Br(),
        html.Div(children='''
                Ingrese su número de cédula y presione \"enviar\".        
            '''),
        html.Div(dcc.Input(id='upload-data', type='text')),
        html.Button('Enviar', id='submit-val', n_clicks=0, type="submit"),
        html.Div(id='container-button-basic'),

        html.Ul(id="file-list"),
    ],
    style={"maxWidth": "500px"},
)


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output('file-list', 'children'),
    Input('submit-val', 'n_clicks'),
    State('upload-data', 'value'),
)
def update_output(uploaded_filenames, value):
    """Generate the file list."""
    files = uploaded_files()
    if len(files) == 0:
        return [html.Li('No hay ningún certificado para descargar!!')]
    else:
        filename = str(value) + ".pdf"
        if filename in files:
            return html.Div([
                html.Div("Descargue el certificado en el siguiente enlace:"),
                html.Br(),
                file_download_link(filename),
                html.Br(),
                html.Br(),
                html.Div("Muchas gracias de parte del Centro de Transparencia")
            ])
        elif value is None:
            return html.Div()
        else:
            return html.Div("Desgraciadamente la cédula # " + str(value) +
                            " no se encuentra en la lista.", id="ced")

        # return [html.Li(file_download_link(filename)) for filename in files]


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
