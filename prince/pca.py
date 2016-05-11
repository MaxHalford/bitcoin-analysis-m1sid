import warnings
import pandas as pd
import numpy as np
import numpy.linalg as la
from prince import util
from prince.plot import mpl
from prince.plot import plotly


class PCA():

    ''' Principal Component Analysis '''

    def __init__(self, df, components=-1, ignored=[], reduced=True):
        # Check if the dataset is a pandas dataframe
        if not isinstance(df, pd.DataFrame):
            raise ValueError("'df' has not been assigned a pandas DataFrame object")
        self.df = df
        # Ignored variables
        self.ignored = ignored
        # Categorical variables are not allowed
        self.categorical = pd.DataFrame()
        # Remove ignored and non-numerical columns from the original dataframe
        self._tidy()
        # Dataframe dimensions
        (self.n, self.p) = df.shape
        # Number of components computed during SVD
        self.components = self.p if components == -1 else components
        # Reduced PCA or not
        self.reduced = reduced
        # Perform the calculations
        self._compute()

    def _tidy(self):
        ''' Remove the non-numerical and ignored columns. '''

        self.na_values = False
        # Check if value is NaN
        if self.df.isnull().any().any():
            self.na_values = True
            # Replace missing value with average of column
            self.df = self.df.fillna(self.df.mean(), inplace=True)
            warnings.warn('Missing values are imputed by the mean of the variable', UserWarning)

        for column in self.df.columns:
            # Variable is ignored
            if column in self.ignored:
                del self.df[column]
            # Variable is non-numerical
            elif self.df[column].dtype not in ('int64', 'float64'):
                self.categorical[column] = self.df[column]
                del self.df[column]

        if len(self.categorical.columns) != 0:
            warnings.warn("The following variables are not quantitative: {}. ".format(self.categorical.columns) + \
                          "You should use the 'ignored' parameter.", UserWarning)

    def _compute_row_projections(self):
        '''
        The right side of a SVD on X contains the eigenvectors of X's
        covariance matrix.
        '''
        projections = self.df @ self.V.T
        columns = ['Component {}'.format(i) for i in range(self.components)]
        self.row_projections = pd.DataFrame(projections, index=self.df.index,
                                            columns=columns)

    def _compute_variable_correlations(self):
        '''
        Compute the correlations between the variables and the eigenvectors.
        '''
        # Compute the correlations
        correlations = [[self.df[column].corr(self.row_projections[projection])
                         for projection in self.row_projections.columns]
                        for column in self.df.columns]
        # Store them in a dataframe
        self.variable_correlations = pd.DataFrame(
            correlations,
            columns=self.row_projections.columns,
            index=self.df.columns
        )
        # Check if correlation is NaN
        if self.variable_correlations.isnull().any().any():
            # Replace missing values with zero's
            self.variable_correlations = self.variable_correlations.fillna(0)

    def _compute_explained_variance(self):
        '''
        Compute the cumulative explained variance.
        '''
        tot = sum(self.eigenvalues)
        self.var_exp = [eig / tot * 100 for eig in self.eigenvalues]
        self.cum_var_exp = np.cumsum(self.var_exp).tolist()

    def _compute_row_inertia(self):
        ''' Compute the rowsum inertia '''
        self.row_inertia = np.sum(self.df ** 2, axis=1)

    def _compute_total_inertia(self):
        ''' Compute the total inertia '''
        self.total_inertia = sum(self.eigenvalues)

    def _compute(self):
        ''' Perform all the steps required for a PCA. '''
        # Center the dataframe
        self.df -= self.df.mean()
        # If specified, reduce the dataframe
        if self.reduced is True:
            self.df /= self.df.std()
        # Apply the SVD
        self.U, self.W, self.V = util.svd(self.df, k=self.components)
        # Compute eigenvectors
        self.eigenvectors = np.asmatrix(self.V)
        # Compute eigenvalues
        self.eigenvalues = self.W ** 2
        # Sort the eigenvalues from high to low
        self.eigenvalues = sorted(self.eigenvalues, reverse=True)
        # Compute the row projections
        self._compute_row_projections()
        # Compute the variable correlations towards the eigenvectors
        self._compute_variable_correlations()
        # Compute the cumulative explained variance
        self._compute_explained_variance()
        # Compute the rowsum inertia
        self._compute_row_inertia()
        # Compute the total inertia
        self._compute_total_inertia()

    def summary(self, ncp=None, nobs=None):
        if ncp is None:
            ncp = self.p
        if nobs is None:
            nobs = self.n
        print('n : {}'.format(nobs))
        print('p : {}'.format(ncp))
        if self.reduced is True:
            print('Reduced dataframe')
        if len(self.categorical.columns) != 0:
            print('The following variables are not quantitative: {}'.format(
                self.categorical.columns))
        if self.na_values:
            print('Missing values are imputed by the mean of the considered variable')

        print('Cumulative explained variance by eigenvalue')
        util.progress_bar([round(val, 2)
                           for val in self.cum_var_exp], bar_length=40, ncp=ncp)

        print('\nPCA analysis performed in Python')

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

    def plot_rows(self, by=None, axis=[0, 1], show_names=True, kind='mpl'):
        ''' Plot the row projections. '''
        # Check if the by parameter is a qualitative variable
        if by is None:
            labels = None
        elif by not in self.categorical:
            raise ValueError("'{}' assigned to 'by' is not a qualitative variable".format(by))
        else:
            labels = self.categorical[by]
        if kind == 'mpl':
            mpl.rows(self.row_projections, self.var_exp, labels, axis, show_names)
        elif kind == 'plotly':
            plotly.rows(self.row_projections, self.var_exp, labels, axis)
        else:
            raise ValueError("'{}' is not a valid value for parameter 'kind'".format(kind))

    def plot_correlation_circle(self, axis=[0, 1], show_names=True, kind='mpl'):
        '''
        Plot the correlations between the principal components and the original
        variables.
        '''
        if kind == 'mpl':
            mpl.correlation_circle(self.variable_correlations, self.var_exp, axis, show_names)
        elif kind == 'plotly':
            plotly.correlation_circle(self.variable_correlations, self.var_exp, axis)
        else:
            raise ValueError("'{}' is not a valid value for parameter 'kind'".format(kind))
