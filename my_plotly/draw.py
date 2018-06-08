import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
# import plotly.figure_factory as fac
# import plotly.offline as off
# off.init_notebook_mode(connected=True)


party_color = {
    '더불어민주당': '#004EA2',
    '자유한국당': '#C8161E',
    '바른미래당': '#20B2AA',
    '민주평화당': '#40B02A',
    '정의당': '#FFCC00',
    '대한애국당': '#080B54',
    '민중당': '#F47920',
    '무소속': '#a6a6a6',
}


def get_header_and_cells_from_df(df):
    header = [f'<b>{e}</b>' for e in df.columns.tolist()]
    values_list = df.values.tolist()
    cells = list(map(list, zip(*values_list)))
    return header, cells


def get_horizontal_bar_layout(
    annotations, shapes,
    title='',
    x_axis_title='',
    width='370',
    height='530',
    left=45, r=20, t=30, b=30,
):
    return go.Layout(
        title=title,
        width=width,
        height=height,
        margin={
            'pad': .5,
            'l': left, 'r': r, 't': t, 'b': b,
        },
        xaxis=go.XAxis(
            title=x_axis_title,
            zeroline=False,
            showticklabels=False,
            fixedrange=True,
        ),
        yaxis=go.YAxis(
            fixedrange=True,
        ),
        annotations=annotations,
        shapes=shapes,
    )


def get_vertical_bar_layout(
    annotations, title='', width='370', height='400',
    x_axis_title='', y_axis_title='',
    left=30, r=20, t=30, b=60,
):
    return go.Layout(
        title=title,
        width=width,
        height=height,
        margin={
            'pad': 2,
            'l': left, 'r': r, 't': t, 'b': b,
        },
        xaxis=go.XAxis(
            title=x_axis_title,
            zeroline=False,
            showticklabels=True,
            fixedrange=True,
        ),
        yaxis=dict(
            title=y_axis_title,
            zeroline=False,
            showticklabels=False,
            fixedrange=True,
        ),
        annotations=annotations,
    #     shapes=shapes,
    )


def make_annotation(x, y):
    return go.Annotation(
        text=str(x),     # text is the y-coord
        showarrow=False, # annotation w/o arrows, default is True
        x=x,               # set x position
        xref='x',          # position text horizontally with x-coords
        xanchor='left',  # x position corresp. to center of text
        yref='y',            # set y position
        yanchor='auto',       # position text vertically with y-coords
        y=y,                 # y position corresp. to top of text
        font=go.Font(
            color='#262626',  # set font color
            size=13           #   and size
        )
    )


def get_hovertext_list(*args):
    '''
    *args: list of Series
    '''
    series_to_list = [x.tolist() for x in args]
    return list('<br>'.join(x) for x in zip(*series_to_list))


def get_party_color_dict(party_series):
    party_list = party_series.tolist()
    color_list = [party_color[x] for x in party_list]
    return dict(color=color_list)


def get_legend_text_party(party_series, y_start=0.94, y_height=0.05, x=0.9):
    party_counts = party_series.value_counts()
    res = []
    y_offset = 0
    for i, p in party_counts.iteritems():
        y = y_start - y_height * y_offset
        res.append(
            dict(
                text=f'{i}({p}명)',
                showarrow=False,
                xref='paper',
                yref='paper',
                x=x,
                y=y,
            )
        )
        y_offset += 1
    return res


def get_legend_rect_party(party_series, rect_height=0.04, rect_width=0.03,
                          rect_gap=0.01, y_start=0.94, x0=0.91):
    party_counts = party_series.value_counts()
    party_list = party_counts.index.tolist()
    res = []

    for i, p in enumerate(party_list):
        y0 = y_start - (rect_height + rect_gap)*i
        res.append(
            {
                'type': 'rect',
                'xref': 'paper',
                'yref': 'paper',
                'x0': x0,
                'x1': x0 + rect_width,
                'y0': y0,
                'y1': y0 - rect_height,
                'fillcolor': party_color[p],
                'line': {
                    'color': party_color[p],
                }
            }
        )
    return res
