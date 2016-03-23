import pandas as pd
import numpy as np
import numpy.linalg as la
from prince import util
from prince.plot import mpl
from prince.plot import plotly


class CA():

    ''' Correspondence Analysis '''

    def __init__(self, df, components=-1):
        # Check if the dataset is a pandas dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError("'df' has not been assigned a pandas DataFrame object")
        self.df = df
        # Dataframe dimensions
        (self.n, self.p) = df.shape
        # Number of components computed during SVD
        self.components = self.p if components == -1 else components
        # Perform the calculations
        self._compute()

    def _compute(self):
        ''' Perform all the steps required for a CA. '''
        data = np.matrix(self.df, float)
        N = np.sum(data)
        # Stochastic matrix
        self.stochastic_matrix = data / N
        # Row sums
        self.row_sums = np.sum(self.stochastic_matrix, 1)
        # Row weights
        self.row_weights = (1 / self.row_sums).reshape(1, -1).tolist()[0]
        # Column sums
        self.col_sums = np.sum(self.stochastic_matrix, 0)
        # Column weights
        self.col_weights = (1 / self.col_sums).tolist()[0]
        # Expected values
        self.expected_values = np.prod((
            np.diag(np.sqrt(self.row_weights)),
            self.stochastic_matrix - self.row_sums * self.col_sums,
            np.diag(np.sqrt(self.col_weights))
        ))
        # Singular Value Decomposition
        self.U, self.W, self.V = util.svd(self.df, k=self.components)
        # Singular values
        d = np.diag(self.W.tolist())
        columns = ['Component {}'.format(i) for i in range(self.p)]
        # Row projections
        N = np.diag(np.sqrt(self.row_sums.reshape(1, -1).tolist()[0])) * self.U
        projections = np.diag(self.row_weights) * N * d
        self.row_projections = pd.DataFrame(
            projections,
            index=self.df.index,
            columns=columns
        )
        # Column projections
        M = np.diag(np.sqrt(self.col_sums.tolist()[0])) * np.transpose(self.V)
        projections = np.diag(self.col_weights) * M * d.T
        self.column_projections = pd.DataFrame(
            projections,
            index=self.df.columns,
            columns=columns
        )
        # Compute eigenvalues
        self.eigenvalues = self.W ** 2
        # Compute total inertia
        self.total_inertia = sum(self.eigenvalues)
        # Sort the eigenvalues from high to low
        self.eigenvalues = sorted(self.eigenvalues, reverse=True)
        self._compute_explained_variance()

    def summary(self, ncp=None, nobs=None):
        if ncp is None:
            ncp = self.p
        if nobs is None:
            nobs = self.n
        print('n : {}'.format(nobs))
        print('p : {}'.format(ncp))

        print('Cumulative explained variance by eigenvalue')
        util.progress_bar([round(val, 2)
                           for val in self.cum_var_exp], bar_length=40, ncp=ncp)

        print('\nCA analysis performed with Prince')

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
            raise ValueError(
                "'{}' is not a valid value for parameter 'kind'".format(kind))

    def plot_rows_columns(self, axis=[0, 1], show_names=True, kind='mpl'):
        ''' Plot the row projections. '''
        if kind == 'mpl':
            mpl.rows_columns(self.row_projections, self.column_projections,
                             self.var_exp, axis, show_names)
        elif kind == 'plotly':
            plotly.rows_columns(self.row_projections, self.column_projections,
                                self.var_exp, axis)
        else:
            raise ValueError(
                "'{}' is not a valid value for parameter 'kind'".format(kind))
