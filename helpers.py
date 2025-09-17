import sqlite3

import plotly.graph_objects as go
import pandas as pd

def query_db(query, args=()):
    conn = sqlite3.connect('larm.db')
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    cursor = conn.cursor()

    cursor.execute(query, args)
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


# returner html for plot
# warning: kan se underlig ud hvis der er optaget i samme rum, men med forskellige lokationer på en gang
def make_plot(query: [dict], key: str) -> str:
    fig = go.Figure()
    df = pd.DataFrame(query)
    #print(df)

    groupLokale = df.groupby(key)
    lokaler = set(df.get(key))

    for lokale in lokaler:
        lokaleData = groupLokale.get_group(lokale)
        print(lokaleData)
        fig.add_trace(go.Scatter(
            x=lokaleData.get("tid"),
            y=lokaleData.get("db"),
            name=lokale,
            visible=True,
            hoverinfo="x+y+name+text",
            text=[f"Lokation: {lokation}, Sensor id: {sensor_id}" for (lokation, sensor_id) in zip(lokaleData.get("lokation"), lokaleData.get("sensor_id"))],
        ))
    fig.show()
    print(fig.to_html())
    return fig.to_html()

