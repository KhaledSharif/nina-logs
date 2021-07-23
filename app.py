NINA_LOG_FOLDER = "C:\\Users\\*\\AppData\\Local\\NINA\\Logs"

from flask import Flask,send_from_directory,Response
from pandas import read_csv
from io import StringIO
from glob import glob

app = Flask(__name__, static_url_path='')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route("/api/logs.json")
def get_logs():
    df = None
    
    g = sorted(list(glob(NINA_LOG_FOLDER+"\\*")))[::-1]
    if len(g) > 3:
        g = g[:3]
    
    for f in g:
        with open(f, 'r') as log_file:
            lines = [x for x in log_file.readlines() if x.startswith("20")]

        lines = "DATE|LEVEL|SOURCE|MEMBER|LINE|MESSAGE \n" + "\n".join(lines)

        new_df = read_csv(StringIO(lines), sep="|")

        if df is None:
            df = new_df
        else:
            df = df.append(new_df, ignore_index=True)

    return Response(df.to_json(orient="records"), mimetype="application/json")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)