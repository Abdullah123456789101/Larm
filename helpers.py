import sqlite3

import plotly.graph_objects as go
import pandas as pd

from datetime import datetime, timezone


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
def make_graf(query: [dict], x: str, y: str, groupKey: str) -> str:
    fig = go.Figure()
    df = pd.DataFrame(query)

    df["tid"] = df["tid"].map(lambda timestamp : datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z'))

    columns = list(df.columns)
    for items in [x, y, groupKey]:
        columns.remove(items)

    groupData = df.groupby(groupKey)
    valueNames = set(df.get(groupKey))

    for valueName in valueNames:
        values = groupData.get_group(valueName)

        item_texts = []
        for i in range(len(values)):
            items = []
            items.append(f"{groupKey}: {valueName}")
            for column in columns:
                items.append(f"{column}: {values.get(column)[i]}")
            text = " | ".join(items)
            item_texts.append(text)

        fig.add_trace(go.Scatter(
            x=values.get(x),
            y=values.get(y),
            name=valueName,
            visible=True,
            hoverinfo="x+y+text",
            text=item_texts,
        ))
    return fig.to_html()

#[f"Lokation: {lokation}, Sensor id: {sensor_id}" for (lokation, sensor_id) in zip(values.get("lokation"), values.get("sensor_id"))]
