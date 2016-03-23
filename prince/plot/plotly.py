import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


def inertia(ratios, threshold, check):
    '''
    Plots the inertia of each principal component with plotly.
    '''
    # Redefine index
    ratios = [0] + ratios

    fig = {
        'data': [
            {
                'y': ratios,
                'mode': 'bar', 'name': 'Normalized cumulative inertia'
            },
            {
                'y': [threshold] * len(ratios),
                'mode': 'line', 'name': 'Threshold'
            },
            {
                'x': [np.where(check)[0][0]] * 2,
                'mode': 'line', 'name': 'First component above threshold'
            }
        ],
        'layout': {
            'xaxis': {'title': 'Principals components'},
            'yaxis': {'title': 'Cumulated contribution to inertia'},
            'title': 'Axis contribution to inertia',
        }
    }
    url = py.plot(fig, filename='plotly/inertia')


def rows(row_projections, var_exp, labels, axis):
    '''
    Plot row projections with pandas and plotly
    '''

    # X coordinates
    X = row_projections[[axis[0]]]
    # Y coordinates
    Y = row_projections[[axis[1]]]

    xlab = 'Component {0} ({1}%)'.format(
        axis[0] + 1, round(var_exp[0]), 2)
    ylab = 'Component {0} ({1}%)'.format(
        axis[1] + 1, round(var_exp[1]), 2)
    main = 'Row projections'
    # If there are labels to color by
    if labels is not None:
        # Create a dataframe for conveniency
        data = pd.concat((X, Y, labels), axis=1)
        data.columns = ('X', 'Y', labels.name)

        fig = {
            'data': [
                {
                    'x': data[data['Competition'] == lab]['X'],
                    'y': data[data['Competition'] == lab]['Y'],
                    'name': lab, 'mode': 'markers',
                } for lab in set(labels)
            ],
            'layout': {
                'xaxis': {'title': xlab},
                'yaxis': {'title': ylab},
                'title': main,
            }
        }

        url = py.plot(fig, filename='plotly/row_projections')
    else:
        data = pd.concat((X, Y), axis=1)
        data.columns = ('X', 'Y')

        fig = {
            'data': [
                {
                    'x': data['X'],
                    'y': data['Y'],
                    'mode': 'markers',
                }
            ],
            'layout': {
                'xaxis': {'title': xlab},
                'yaxis': {'title': ylab},
                'title': main,
            }
        }
        url = py.plot(fig, filename='plotly/row_projections')


def correlation_circle(variable_correlations, var_exp, axis):
    '''
    Plot the correlations between the principal components and the original
    variables using plotly. Usually used for a PCA.
    '''
    X = variable_correlations[[axis[0]]]
    Y = variable_correlations[[axis[1]]]

    xlab = 'Component {0} ({1}%)'.format(
        axis[0] + 1, round(var_exp[0]), 2)
    ylab = 'Component {0} ({1}%)'.format(
        axis[1] + 1, round(var_exp[1]), 2)

    fig = {
        'data': [
            {
                'x': float(X.loc[row]),
                'y': float(Y.loc[row]),
                'name': row, 'mode': 'markers',
            } for row in variable_correlations.index
        ],
        'layout': {
            'title': 'Correlation circle',
            'xaxis': {'title': xlab},
            'yaxis': {'title': ylab},
            'width': 600,
            'height': 600,
            'shapes': [
                {
                    'type': 'circle',
                    'x0': -1,
                    'y0': -1,
                    'x1': 1,
                    'y1': 1,
                }
            ] + [
                {
                    'type': 'line',
                    'x0': 0,
                    'y0': 0,
                    'x1': float(X.loc[row]),
                    'y1': float(Y.loc[row]),
                    'line': {
                        'color': 'rgb(192, 192, 192)',
                        'width': 3
                    }
                } for row in variable_correlations.index
            ]
        }
    }

    url = py.plot(fig, filename='plotly/correlation_circle')


def rows_columns(row_projections, col_projections, var_exp, axis):
    '''
    Plot row projections with pandas and plotly
    '''

    # Row projections
    X_row = row_projections[[axis[0]]]
    Y_row = row_projections[[axis[1]]]

    # Column projections
    X_column = col_projections[[axis[0]]]
    Y_column = col_projections[[axis[1]]]

    xlab = 'Component {0} ({1}%)'.format(
        axis[0] + 1, round(var_exp[0]), 2)
    ylab = 'Component {0} ({1}%)'.format(
        axis[1] + 1, round(var_exp[1]), 2)
    main = 'Row and column projections'

    fig = {
        'data': [
            {
                'x': X_row.loc[row],
                'y': Y_row.loc[row],
                'showlegend': False,
                'mode': 'markers+text',
                'marker':{'color': 'rgba(200, 50, 100, .7)', 'size': 10},
                'text': row,
                'textposition': 'top center'
            } for row in row_projections.index
        ] + [
            {
                'x': X_column.loc[col],
                'y': Y_column.loc[col],
                'showlegend': False,
                'mode': 'markers+text',
                'marker':{'color': 'rgba(10, 180, 180, .8)', 'size': 10},
                'text': col,
                'textposition': 'top center'
            } for col in col_projections.index
        ],
        'layout': {
            'xaxis': {'title': xlab},
            'yaxis': {'title': ylab},
            'title': main,
        }
    }
    url = py.plot(fig, filename='plotly/row_projections')
