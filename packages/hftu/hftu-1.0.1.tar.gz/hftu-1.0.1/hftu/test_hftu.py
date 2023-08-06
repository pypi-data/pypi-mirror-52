from .hftu import HFTU
import unittest
from test import support
from sklearn.datasets import make_blobs
from random import randint
import numpy as np


def print_results(H):
    print('\n---- Results ----')
    print("Φ = {:.5f}".format(H.folding_statistics_))
    print('Unimodal: ', H.is_unimodal(0.05))
    print('-----------------')


class TestFit(unittest.TestCase):
    def setUp(self):
        self.random_state = randint(0, pow(2, 32) - 1)
        self.data, _ = make_blobs(n_samples=1000,
                                  n_features=2,
                                  centers=1,
                                  random_state=self.random_state)

    def test_legacy_variance_fit(self):
        H = HFTU()
        H.fit(self.data, method='legacy', init='variance')
        print_results(H)

    def test_legacy_random_fit(self):
        H = HFTU()
        H.fit(self.data, method='legacy', init='random')
        print_results(H)

    def test_heuristic_random_fit(self):
        H = HFTU()
        H.fit(self.data, method='heuristic', init='random')
        print_results(H)

    # def test_heuristic_ortho_fit(self):
    #     H = HFTU()
    #     H.fit(self.data, method='heuristic', init='ortho')
    #     print_results(H)

    def test_heuristic_variance_fit(self):
        H = HFTU()
        H.fit(self.data, method='heuristic', init='variance')
        print_results(H)


class TestBimodal(unittest.TestCase):
    def setUp(self):
        self.random_state = randint(0, pow(2, 32) - 1)
        self.data, _ = make_blobs(n_samples=1000,
                                  n_features=2,
                                  centers=2,  #  two blobs
                                  random_state=self.random_state)

    def test_legacy_variance_fit(self):
        H = HFTU()
        H.fit(self.data, method='legacy', init='variance')
        print_results(H)

    def test_legacy_random_fit(self):
        H = HFTU()
        H.fit(self.data, method='legacy', init='random')
        print_results(H)

    def test_heuristic_random_fit(self):
        H = HFTU()
        H.fit(self.data, method='heuristic', init='random')
        print_results(H)

    def test_heuristic_variance_fit(self):
        H = HFTU()
        H.fit(self.data, method='heuristic', init='variance')
        print_results(H)


class TestTrimodal(unittest.TestCase):
    def setUp(self):
        self.random_state = randint(0, pow(2, 32) - 1)
        self.data, _ = make_blobs(n_samples=1500,
                                  n_features=2,
                                  centers=3,  #  two blobs
                                  random_state=self.random_state)

    def test_legacy_variance_fit(self):
        H = HFTU()
        H.fit(self.data, method='legacy', init='variance')
        print_results(H)

    def test_legacy_random_fit(self):
        H = HFTU()
        H.fit(self.data, method='legacy', init='random')
        print_results(H)

    def test_heuristic_random_fit(self):
        H = HFTU()
        H.fit(self.data, method='heuristic', init='random')
        print_results(H)

    def test_heuristic_variance_fit(self):
        H = HFTU()
        H.fit(self.data, method='heuristic', init='variance')
        print_results(H)


class TestTransform(unittest.TestCase):
    def test_fit_transform(self):
        H = HFTU()
        n = 5000
        dim = 3
        mean = np.zeros(dim)
        shift = 20 * np.ones(dim)
        cov = np.eye(dim)
        X0 = np.random.multivariate_normal(mean, cov, n)
        X = np.vstack((X0, X0 + shift))
        Z = H.fit_transform(X)
        X0_cov = np.cov(X0.T)
        folded_cov = np.cov(Z.T)
        print('\n', folded_cov)
        print(np.abs(folded_cov - X0_cov).sum())


if __name__ == '__main__':
    unittest.main()
