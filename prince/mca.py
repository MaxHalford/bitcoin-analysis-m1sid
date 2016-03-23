import pandas as pd
import numpy as np
import prince
from prince import util
from prince.plot import mpl
from prince.plot import plotly


class MCA():

    ''' Multiple Correspondence Analysis '''

    def __init__(self, df, components=-1, ignored=[], reduced=True):
        # Check if the dataset is a pandas dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError("'df' has not been assigned a pandas DataFrame object")
        self.df = df
        # Number of qualitative variables
        self.Q = len(self.df.columns)
        # Ignored variables
        self.ignored = ignored
        # Numerical variables are not allowed
        self.numerical = pd.DataFrame()
        # Remove ignored and non-numerical columns from the original dataframe
        self._tidy()
        # Dataframe dimensions
        (self.n, self.p) = df.shape
        # Number of components computed during SVD
        self.components = self.p if components == -1 else components
        # Perform the calculations
        self._compute()

    def _tidy(self):
        ''' Remove the numerical and ignored columns. '''
        for column in self.df.columns:
            # Variable is ignored
            if column in self.ignored:
                del self.df[column]
            # Variable is numerical
            elif self.df[column].dtype in ('int64', 'float64'):
                self.numerical[column] = self.df[column]
                del self.df[column]

    def _compute(self):
        # Build the indicator matrix
        self.indicator_matrix = pd.get_dummies(self.df)
        # Compute the correspondance analysis of the indicator matrix
        ca = prince.CA(self.indicator_matrix, components=self.components)
        # Extract the needed values
        self.column_projections = ca.column_projections
        self.row_projections = ca.row_projections
        self.U = ca.U
        self.W = ca.W
        self.V = ca.V
        # Compute Benzécri scores instead of classical eigenvalues
        self.eigenvalues = [
            ((self.Q / (self.Q - 1)) ** 2 * (w - 1 / self.Q) ** 2) ** 2
            if w < 1 / self.Q
            else w ** 2
            for w in self.W
        ]
        self._compute_explained_variance()

    def _compute_explained_variance(self):
        '''
        Compute the cumulative explained variance.
        '''
        tot = sum(self.eigenvalues)
        self.var_exp = [eig / tot * 100 for eig in self.eigenvalues]
        self.cum_var_exp = np.cumsum(self.var_exp).tolist()

    def plot_inertia(self, threshold=0.8, kind='mpl'):
        '''
        Plots the inertia of each principal component.
        '''
        ratios, check = util.check_inertia(self.eigenvalues)
        if kind == 'mpl':
            mpl.inertia(ratios, threshold, check)
        elif kind == 'plotly':
            plotly.inertia(ratios, threshold, check)
        else:
            raise ValueError("'{}' is not a valid value for parameter 'kind'".format(kind))

    def plot_rows_columns(self, axis=[0, 1], show_names=True, kind='mpl'):
        ''' Plot the row projections. '''
        if kind == 'mpl':
            mpl.rows_columns(self.row_projections, self.column_projections,
                             self.var_exp, axis, show_names)
        elif kind == 'plotly':
            plotly.rows_columns(self.row_projections, self.column_projections,
                                self.var_exp, axis)
        else:
            raise ValueError("'{}' is not a valid value for parameter 'kind'".format(kind))
