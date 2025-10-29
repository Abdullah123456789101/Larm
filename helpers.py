import sqlite3

import plotly.graph_objects as go
from plotly.io import to_html
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

    if len(df)==0:
        return "Vi har ikke data indenfor denne periode"

    # ændre så at tid går fra timestamps til en rigtig dato
    df["tid"] = df["tid"].map(lambda timestamp: datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z'))

    columns = list(df.columns)
    # fjerner kolonner som ikke skal være i ekstra info når man holder musen over et datapunkt
    for i in [x, y, groupKey]:
        columns.remove(i)

    groupData = df.groupby(groupKey) #gruppere data efter givet key
    valueNames = set(df.get(groupKey)) # henter alle unikke værdier så der kan lave traces til hver

    for valueName in valueNames:
        values = groupData.get_group(valueName)

        # Laver teksten som står der når man putter mus over et datapunkt
        item_texts = []
        for i in range(len(values)):
            items = []
            items.append(f"{groupKey}: {valueName}")
            for column in columns:
                items.append(f"{column}: {values.get(column)[i]}")
            text = " | ".join(items)
            item_texts.append(text)

        # Laver en række punkter som er knyttet sammen med en linje
        fig.add_trace(go.Scatter(
            x=values.get(x),
            y=values.get(y),
            name=valueName,
            visible=True,
            hoverinfo="x+y+text",
            text=item_texts,
        ))

    fig.update_layout(
        autosize=True,
        margin = dict(l=20, r=20, t=40, b=20)
    )

    return to_html(
        fig,
        full_html=False,
        include_plotlyjs='cdn',
        default_height='100%',  # key: make div height 100%
        default_width='100%',  # key: make div width 100%)
        config = {'responsive': True}
    )
