import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from prince import util


def inertia(ratios, threshold, check):
    '''
    Plots the inertia of each principal component.
    '''
    fig, ax = plt.subplots()
    # Threshold
    ax.axhline(y=threshold, color='red', alpha=0.5, label='Threshold')
    # Inertia percentages
    ax.plot(ratios, color='blue', label='Normalized cumulative inertia')
    ax.plot(ratios, 'bo')
    # First value above threshold
    ax.axvline(x=np.where(check)[0][0], color='green', alpha=0.5,
               label='First component above threshold')
    ax.set_title('Axis contribution to inertia')
    ax.set_xlabel('Principals components')
    ax.set_ylabel('Cumulated contribution to inertia')
    ax.legend(loc='best')
    plt.show()


def rows(row_projections, var_exp, labels, axis, show_names):
    ''' Plot the row projections. Usually used for a PCA. '''
    fig, ax = plt.subplots()
    # X coordinates
    X = row_projections[[axis[0]]]
    # Y coordinates
    Y = row_projections[[axis[1]]]
    # If there are labels to color by
    if labels is not None:
        # Create a dataframe for conveniency
        data = pd.concat((X, Y, labels), axis=1)
        data.columns = ('X', 'Y', labels.name)
        groups = data.groupby(labels.name)
        for label, group in groups:
            ax.plot(group.X, group.Y, marker='o', linestyle='', ms=8, label=label)
        ax.legend(loc='best')
    else:
        ax.scatter(X, Y)
    # Row names
    if show_names is True:
        ax.scatter(X, Y, alpha=0)
        for row in row_projections.index:
            ax.text(x=X.loc[row], y=Y.loc[row], s=row)
    # Draw a default hline at y=1 that spans the xrange
    plt.axhline(y=0, color='grey', alpha=0.5)
    # Draw a default vline at x=1 that spans the yrange
    plt.axvline(x=0, color='grey', alpha=0.5)
    ax.set_title('Row projections')
    ax.set_xlabel('Component {0} ({1}%)'.format(axis[0], round(var_exp[0]), 2))
    ax.set_ylabel('Component {0} ({1}%)'.format(axis[1], round(var_exp[1]), 2))
    plt.axis('equal')
    plt.savefig('themes.png', dpi=300)
    plt.show()


def correlation_circle(variable_correlations, var_exp, axis, show_names):
    '''
    Plot the correlations between the principal components and the original
    variables. Usually used for a PCA.
    '''
    fig, ax = plt.subplots()
    X = variable_correlations[[axis[0]]]
    Y = variable_correlations[[axis[1]]]
    # Plot the arrows and add text
    for row in variable_correlations.index:
        x = X.loc[row]
        y = Y.loc[row]
        ax.arrow(0, 0, float(x), float(y), head_width=0.05,
                 head_length=0.1, ec='k')
        if show_names is True:
            ax.annotate(row, (x, y))
    # Draw a default hline at y=1 that spans the xrange
    plt.axhline(y=0, linestyle='--', color='grey', alpha=0.5)
    # Draw a default vline at x=1 that spans the yrange
    plt.axvline(x=0, linestyle='--', color='grey', alpha=0.5)
    # Draw circle
    circle = plt.Circle((0, 0), radius=1, color='g', fill=False, lw=3)
    ax.add_patch(circle)
    ax.set_title('Correlation circle')
    ax.set_xlabel('Component {0} ({1}%)'.format(
        axis[0] + 1, round(var_exp[0]), 2))
    ax.set_ylabel('Component {0} ({1}%)'.format(
        axis[1] + 1, round(var_exp[1]), 2))
    # Define axis
    plt.axis('equal')
    plt.axis([-1, 1, -1.2, 1.2])
    plt.show()


def rows_columns(row_projections, column_projections, var_exp, axis, show_names):
    ''' Plot the row and column projections. Usually used for a CA. '''
    fig, ax = plt.subplots()
    # Row projections
    X_row = row_projections[[axis[0]]]
    Y_row = row_projections[[axis[1]]]
    # Column projections
    X_column = column_projections[[axis[0]]]
    Y_column = column_projections[[axis[1]]]
    ax.plot(X_row, Y_row, marker='o', color='blue', linestyle='', ms=8, label='Row projections')
    ax.plot(X_column, Y_column, marker='o', color='red', linestyle='', ms=8, label='Column projections')
    if show_names is True:
        ax.plot(X_row, Y_row, alpha=0)
        ax.plot(X_column, Y_column, alpha=0)
        for row in row_projections.index:
            ax.annotate(row, (X_row.loc[row], Y_row.loc[row]), color='blue')
        for col in column_projections.index:
            ax.annotate(col, (X_column.loc[col], Y_column.loc[col]), color='red')
    # Draw a default hline at y=1 that spans the xrange
    plt.axhline(y=0, color='grey', alpha=0.5)
    # Draw a default vline at x=1 that spans the yrange
    plt.axvline(x=0, color='grey', alpha=0.5)
    ax.set_title('Row and column projections')
    ax.set_xlabel('Component {0} ({1}%)'.format(axis[0], round(var_exp[0]), 2))
    ax.set_ylabel('Component {0} ({1}%)'.format(axis[1], round(var_exp[1]), 2))
    plt.axis('equal')
    plt.legend(loc='best')
    plt.show()
