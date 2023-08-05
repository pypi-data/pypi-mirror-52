from abc import ABC, abstractmethod
import numpy as np
from tqdm.autonotebook import tqdm

from pytsmp import utils


class MatrixProfile(ABC):
    """
    The base class for matrix profile computation. This is an abstract class, you cannot instantiate from this class.
    """
    
    _epsilon = 1e-5  # a small positive value to be used in various places
    
    def __init__(self, ts1, ts2=None, window_size=None, exclusion_zone=1/2, verbose=True, s_size=1, seed=None):
        """
        Base constructor.

        :param ts1: Time series for calculating the matrix profile.
        :type ts1: numpy array
        :param ts2: A second time series to compute matrix profile with respect to ts1. If None, ts1 will be used.
        :type ts2: numpy array
        :param int window_size: Subsequence length, must be a positive integer less than the length of both ts1 and ts2
        :param float exclusion_zone: Exclusion zone, the length of exclusion zone is this number times window_size,
                                     centered at the point of interest.
                                     Must be non-negative. This parameter will be ignored if ts2 is not None.
        :param bool verbose: Whether to display progress or not.
        :param float s_size: Ratio of random calculations performed for anytime algorithms. Must be between 0 and 1,
                             1 means calculate all, and 0 means none. This parameter will be ignored if the algorithm
                             is not anytime.
        :param seed: Random seed used in numpy.random. None means to use a random seed.
        :type seed: int or None
        :raises: ValueError: If the input is invalid.
        """
        self.ts1 = np.copy(ts1).astype("float64")
        self.ts2 = np.copy(ts2).astype("float64") if ts2 is not None else np.copy(ts1)
        if type(window_size) == int and 0 < window_size <= min(len(self.ts1), len(self.ts2)):
            self.window_size = window_size
        else:
            raise ValueError("Incorrect window size specified.")
        if exclusion_zone >= 0:
            self.ez = exclusion_zone
            self.exclusion_zone = round(window_size * exclusion_zone + self._epsilon)
        else:
            raise ValueError("Exclusion zone must be non-negative.")
        self.verbose = bool(verbose)
        if 0 < s_size <= 1:
            self.s_size = s_size
        else:
            raise ValueError("s_size must be between 0 and 1.")
        self.seed = seed

        self._same_ts = ts2 is None
        self._matrix_profile = np.full((len(self.ts1) - self.window_size + 1,), np.inf)
        self._index_profile = np.full((len(self.ts1) - self.window_size + 1,), np.nan, dtype=int)

        self._preprocess()
        self._compute_matrix_profile()

    @property
    @abstractmethod
    def is_anytime(self):
        """
        A property stating whether the algorithm for computing the matrix profile
        in this class is an anytime algorithm.

        :return: whether the algorithm in this class is an anytime algorithm.
        :rtype: bool
        """
        return False

    @property
    @abstractmethod
    def _iterator(self):
        """
        The iterator to use in the computation of matrix profile. Defined separately to accomodate
        resume computation of anytime algorithms.

        :return: Iterator used in the computation of matrix profile.
        :rtype: iterator
        """
        return NotImplementedError

    def get_matrix_profile(self):
        """
        Get the matrix profile.

        :return: The matrix profile.
        :rtype: numpy array, of shape (len(ts1)-windows_size+1,)
        """
        return np.copy(self._matrix_profile)

    def get_index_profile(self):
        """
        Get the index profile.

        :return: The index profile.
        :rtype: numpy array, of shape (len(ts1)-windows_size+1,)
        """
        return np.copy(self._index_profile)

    def get_profiles(self):
        """
        Get the matrix profile and the index profile.

        :return: The matrix profile and the index profile.
        :rtype: 2 numpy arrays, both of shape (len(ts1)-window_size+1,)
        """
        return self.get_matrix_profile(), self.get_index_profile()

    def _preprocess(self):
        """
        Any preprocess (such as PreSCRIMP) to be done before the main computation. Default
        is to do nothing.

        :return: None.
        """
        pass

    @abstractmethod
    def _compute_matrix_profile(self):
        """
        Compute the matrix profile using the method indicated by the class.

        :return: None.
        """
        raise NotImplementedError

    def _elementwise_min(self, D, idx):
        """
        Subroutine for calculating elementwise min and min_index for matrix profile updates.

        :param D: Distance profile for update.
        :type D: numpy array
        :param int idx: Index (of ts2) corresponding to the distance profile.
        """
        if self._same_ts:
            lower_ez_bound = max(0, idx - self.exclusion_zone)
            upper_ez_bound = min(len(self.ts2), idx + self.exclusion_zone) + 1
            D[lower_ez_bound: upper_ez_bound] = np.inf
        self._index_profile[self._matrix_profile > D] = idx
        self._matrix_profile = np.minimum(self._matrix_profile, D)

    def update_ts1(self, pt):
        """
        Update the time-series ts1 with a new data point at the end of the series. If doing self-join (ts1 == ts2),
        both series will be updated.

        :param float pt: The value of the new data point, to be attached to the end of ts1.
        """
        self.ts1 = np.append(self.ts1, pt)
        if self._same_ts:
            self.ts2 = np.copy(self.ts1)
        s = self.ts1[-self.window_size:]
        idx = len(self.ts1) - self.window_size
        D = utils.mass(s, self.ts2)
        if self._same_ts:
            lower_ez_bound = max(0, idx - self.exclusion_zone)
            upper_ez_bound = min(len(self.ts2), idx + self.exclusion_zone) + 1
            D[lower_ez_bound:upper_ez_bound] = np.inf
            self._index_profile[self._matrix_profile > D[:-1]] = idx
            self._matrix_profile = np.minimum(self._matrix_profile, D[:-1])
        min_idx = np.argmin(D)
        self._index_profile = np.append(self._index_profile, min_idx)
        self._matrix_profile = np.append(self._matrix_profile, D[min_idx])

    def update_ts2(self, pt):
        """
        Update the time-series ts2 with a new data point at the end of the series. If doing self-join (ts1 == ts2),
        both series will be updated.

        :param float pt: The value of the new data point, to be attached to the end of ts2.
        """
        if self._same_ts:
            self.update_ts1(pt)
        else:
            self.ts2 = np.append(self.ts2, pt)
            s = self.ts2[-self.window_size:]
            idx = len(self.ts2) - self.window_size
            D = utils.mass(s, self.ts1)
            self._elementwise_min(D, idx)

    def find_discords(self, num_discords, exclusion_zone=None):
        """
        Find the top discords of the time series from the matrix profile.

        :param int num_discords: (Max) number of discord to be found. Must be positive.
        :param exclusion_zone: The exclusion zone from either side of a previously found discord. None means
                               to use the same exclusion_zone as defined in creating the matrix profile. The length
                               of exclusion zone is this number times window_size, centered at the point
                               of interest. Must be non-negative if not None.
        :type exclusion_zone: float or None
        :return: The indexes of the discords found, sorted by their corresponding values in the matrix profile.
        :rtype: numpy array
        :raises: ValueError: If the input is invalid.
        """
        profile = self._matrix_profile.copy()
        if num_discords > 0 and type(num_discords) == int:
            discords = np.empty(num_discords, dtype=int)
        else:
            raise ValueError("Incorrect num_discords entered.")
        if exclusion_zone is None:
            exclusion_zone = self.exclusion_zone
        if exclusion_zone >= 0:
            exclusion_number = round(self.window_size * exclusion_zone + self._epsilon)
        else:
            raise ValueError("Exclusion zone must be non-negative.")
        for i in range(num_discords):
            discords[i] = np.argmax(profile)
            if profile[discords[i]] == -np.inf:
                return discords[:i]
            lower_bound = max(0, discords[i] - exclusion_number)
            upper_bound = min(len(profile), discords[i] + exclusion_number) + 1
            profile[lower_bound:upper_bound] = -np.inf
        return discords

    def find_motifs(self, num_motifs, exclusion_zone=None):
        """
        Find the top motifs of the time series from the matrix profile.

        **Note**: The behaviour of this function does not match that of the implementation in R.

        :param int num_motifs: (Max) number of motifs to be found. Must be positive.
        :param exclusion_zone: The exclusion zone from either side of a previously found motif. None means
                               to use the same exclusion_zone as defined in creating the matrix profile. The length
                               of exclusion zone is this number times window_size, centered at the point
                               of interest. Must be non-negative if not None.
        :type exclusion_zone: float or None
        :return: The index pairs of the motifs found (of shape (n, 2) where n is the number of motifs found),
                 sorted by their corresponding values in the matrix profile.
        :rtype: numpy array
        :raises: ValueError: If the input is invalid.
        """
        profile = self._matrix_profile.copy()
        if num_motifs > 0 and type(num_motifs) == int:
            motifs = np.empty((num_motifs, 2), dtype=int)
        else:
            raise ValueError("Incorrect num_motifs entered.")
        if exclusion_zone is None:
            exclusion_number = self.exclusion_zone
        elif exclusion_zone >= 0:
            exclusion_number = round(self.window_size * exclusion_zone + self._epsilon)
        else:
            raise ValueError("Exclusion zone must be non-negative.")
        for i in range(num_motifs):
            motifs[i][0] = np.argmin(profile)
            motifs[i][1] = self._index_profile[motifs[i][0]]
            if profile[motifs[i][0]] == np.inf:
                return motifs[:i, :]
            lower_bound = max(0, motifs[i][0] - exclusion_number)
            upper_bound = min(len(profile), motifs[i][0] + exclusion_number) + 1
            profile[lower_bound:upper_bound] = np.inf
            if self._same_ts:
                lower_bound = max(0, motifs[i][1] - exclusion_number)
                upper_bound = min(len(profile), motifs[i][1] + exclusion_number) + 1
                profile[lower_bound:upper_bound] = np.inf
        return motifs


class STAMP(MatrixProfile):
    """
    Class for the calculation of matrix profile using STAMP algorithm. See [MP1]_ for more details.

    .. [MP1] C.C.M. Yeh, Y. Zhu, L. Ulanova, N. Begum, Y. Ding, H.A. Dau, D. Silva, A. Mueen and E. Keogh.
       "Matrix profile I: All pairs similarity joins for time series: A unifying view that includes
       motifs, discords and shapelets". IEEE ICDM 2016.

    :param ts1: Time series for calculating the matrix profile.
    :type ts1: numpy array
    :param ts2: A second time series to compute matrix profile with respect to ts1. If None, ts1 will be used.
    :type ts2: numpy array
    :param int window_size: Subsequence length, must be a positive integer less than the length of both ts1 and ts2.
    :param float exclusion_zone: Exclusion zone, the length of exclusion zone is this number times window_size,
                                 centered at the point of interest.
                                 Must be non-negative. This parameter will be ignored if ts2 is not None.
    :param bool verbose: Whether to display progress or not.
    :param float s_size: Ratio of random calculations performed for anytime algorithms. Must be between 0 and 1,
                         1 means calculate all, and 0 means none.
    :param seed: Random seed used in numpy.random. None means to use a random seed.
    :type seed: int or None
    :raises: ValueError: If the input is invalid.
    """
    def __init__(self, ts1, ts2=None, window_size=None, exclusion_zone=1/2, verbose=True, s_size=1, seed=None):
        super().__init__(ts1, ts2, window_size, exclusion_zone, verbose, s_size, seed)

    @property
    def is_anytime(self):
        """
        A property stating whether the algorithm for computing the matrix profile
        in this class is an anytime algorithm.

        :return: whether the algorithm in this class is an anytime algorithm.
        :rtype: bool
        """
        return True

    @property
    def _iterator(self):
        idxes = np.random.RandomState(self.seed).permutation(range(len(self.ts2) - self.window_size + 1))
        idxes = idxes[:round(self.s_size * len(idxes) + self._epsilon)]
        if self.verbose:
            _iterator = tqdm(idxes)
        else:
            _iterator = idxes
        return _iterator

    def _compute_matrix_profile(self):
        """
        Compute the matrix profile using STAMP.
        """
        try:
            for n_iter, idx in enumerate(self._iterator):
                D = utils.mass(self.ts2[idx: idx+self.window_size], self.ts1)
                self._elementwise_min(D, idx)
        except KeyboardInterrupt:
            if self.verbose:
                tqdm.write("Calculation interrupted at iteration {}. Approximate result returned.".format(n_iter))


class STOMP(MatrixProfile):
    """
    Class for the calculation of matrix profile using STOMP algorithm. This is faster than STAMP (actually the
    fastest known algorithm), but is not an anytime algorithm. See [MP2]_ for more details.

    .. [MP2] Y. Zhu, Z. Zimmerman, N.S. Senobari, C.C.M. Yeh, G. Funning, A. Mueen, P. Berisk and E. Keogh.
       "Matrix Profile II: Exploiting a Novel Algorithm and GPUs to Break the One Hundred Million
       Barrier for Time Series Motifs and Joins". IEEE ICDM 2016.

    :param ts1: Time series for calculating the matrix profile.
    :type ts1: numpy array
    :param ts2: A second time series to compute matrix profile with respect to ts1. If None, ts1 will be used.
    :type ts2: numpy array
    :param int window_size: Subsequence length, must be a positive integer less than the length of both ts1 and ts2.
    :param float exclusion_zone: Exclusion zone, the length of exclusion zone is this number times window_size,
                                 centered at the point of interest.
                                 Must be non-negative. This parameter will be ignored if ts2 is not None.
    :param bool verbose: Whether to display progress or not.
    :param float s_size: This parameter will be ignored by STOMP since it is not an anytime algorithm.
    :param seed: This parameter will be ignored by STOMP since no randomness is needed in this algorithm.
    :type seed: int or None
    :raises: ValueError: If the input is invalid.
    """
    def __init__(self, ts1, ts2=None, window_size=None, exclusion_zone=1/2, verbose=True, s_size=1, seed=None):
        super().__init__(ts1, ts2, window_size, exclusion_zone, verbose, s_size, seed)

    @property
    def is_anytime(self):
        """
        A property stating whether the algorithm for computing the matrix profile
        in this class is an anytime algorithm.

        :return: whether the algorithm in this class is an anytime algorithm.
        :rtype: bool
        """
        return False

    @property
    def _iterator(self):
        idxes = range(1, len(self.ts2) - self.window_size + 1)
        if self.verbose:
            _iterator = tqdm(idxes)
        else:
            _iterator = idxes
        return _iterator

    def _compute_matrix_profile(self):
        """
        Compute the matrix profile using STOMP.
        """
        mu_T, sigma_T = utils.rolling_avg_sd(self.ts1, self.window_size)
        QT = utils.sliding_dot_product(self.ts2[:self.window_size], self.ts1)
        if self._same_ts:
            mu_Q, sigma_Q = mu_T, sigma_T
            TQ = np.copy(QT)
        else:
            mu_Q, sigma_Q = utils.rolling_avg_sd(self.ts2, self.window_size)
            TQ = utils.sliding_dot_product(self.ts1[:self.window_size], self.ts2)
        D = utils.calculate_distance_profile(QT, self.window_size, mu_Q[0], sigma_Q[0], mu_T, sigma_T)
        if self._same_ts:
            lower_ez_bound = 0
            upper_ez_bound = min(len(self.ts2), self.exclusion_zone) + 1
            D[lower_ez_bound:upper_ez_bound] = np.inf
        self._matrix_profile = np.copy(D)
        self._index_profile = np.zeros((len(self.ts1) - self.window_size + 1,))
        for idx in self._iterator:
            QT[1:] = QT[:len(self.ts1)-self.window_size] - self.ts1[:len(self.ts1)-self.window_size] * self.ts2[idx-1] \
                     + self.ts1[self.window_size:] * self.ts2[idx + self.window_size - 1]
            QT[0] = TQ[idx]
            D = utils.calculate_distance_profile(QT, self.window_size, mu_Q[idx], sigma_Q[idx], mu_T, sigma_T)
            self._elementwise_min(D, idx)


class SCRIMP(MatrixProfile):
    """
    Class for the calculation of matrix profile using SCRIMP algorithm. This is faster than STAMP (slightly slower
    than STOMP), and is also an anytime algorithm. See [MP3]_ for more details.

    .. [MP3] Y. Zhu, C.C.M. Yeh, Z. Zimmerman, K. Kamgar and E. Keogh.
       "Matrix Proﬁle XI: SCRIMP++: Time Series Motif Discovery at Interactive Speed". IEEE ICDM 2018.

    :param ts1: Time series for calculating the matrix profile.
    :type ts1: numpy array
    :param ts2: A second time series to compute matrix profile with respect to ts1. If None, ts1 will be used.
    :type ts2: numpy array
    :param int window_size: Subsequence length, must be a positive integer less than the length of both ts1 and ts2.
    :param float exclusion_zone: Exclusion zone, the length of exclusion zone is this number times window_size,
                                 centered at the point of interest.
                                 Must be non-negative. This parameter will be ignored if ts2 is not None.
    :param bool verbose: Whether to display progress or not.
    :param float s_size: Ratio of random calculations performed for anytime algorithms. Must be between 0 and 1,
                         1 means calculate all, and 0 means none.
    :param float pre_scrimp: Whether to perform an approximate PreSCRIMP algorithm before running SCRIMP. 0 means
                             not performing PreSCRIMP, and any number greater than 0 means performing PreSCRIMP with
                             its sample_rate parameter set to that number.
    :param seed: Random seed used in numpy.random. None means to use a random seed.
    :type seed: int or None
    :raises: ValueError: If the input is invalid.
    """
    def __init__(self, ts1, ts2=None, window_size=None, exclusion_zone=1/2, verbose=True, s_size=1, seed=None, pre_scrimp=1/4):
        if pre_scrimp >= 0:
            self.pre_scrimp = pre_scrimp
        else:
            raise ValueError("pre_scrimp parameter must be non-negative.")
        super().__init__(ts1, ts2, window_size, exclusion_zone, verbose, s_size, seed)

    @property
    def is_anytime(self):
        """
        A property stating whether the algorithm for computing the matrix profile
        in this class is an anytime algorithm.

        :return: whether the algorithm in this class is an anytime algorithm.
        :rtype: bool
        """
        return True

    @property
    def _iterator(self):
        if self._same_ts:
            idxes = np.random.RandomState(self.seed).permutation(range(self.exclusion_zone + 1,
                                                len(self.ts2) - self.window_size + 1))
        else:
            idxes = np.random.RandomState(self.seed).permutation(range(-len(self.ts1) + self.window_size,
                                                len(self.ts2) - self.window_size + 1))
        idxes = idxes[:round(self.s_size * len(idxes) + self._epsilon)]
        if self.verbose:
            _iterator = tqdm(idxes)
        else:
            _iterator = idxes
        return _iterator

    def _preprocess(self):
        """
        Here we do the PreSCRIMP before the SCRIMP algorithm if pre_scrimp = True.
        """
        if self.pre_scrimp > 0:
            if self.verbose:
                tqdm.write("PreSCRIMP:")
            self._pre_scrimp_class = PreSCRIMP(self.ts1, None if self._same_ts else self.ts2,
                                               window_size=self.window_size,
                                               exclusion_zone=self.ez, verbose=self.verbose,
                                               s_size=self.s_size, sample_rate=self.pre_scrimp)
            self._matrix_profile, self._index_profile = self._pre_scrimp_class.get_profiles()

    def _compute_matrix_profile(self):
        """
        Compute the matrix profile using SCRIMP.
        """
        if self.verbose and self.pre_scrimp > 0:
            tqdm.write("SCRIMP:")
        try:
            n1 = len(self.ts1)
            n2 = len(self.ts2)
            mu_T, sigma_T = utils.rolling_avg_sd(self.ts1, self.window_size)
            if self._same_ts:
                mu_Q, sigma_Q = mu_T, sigma_T
            else:
                mu_Q, sigma_Q = utils.rolling_avg_sd(self.ts2, self.window_size)
            for n_iter, k in enumerate(self._iterator):
                if k >= 0:
                    # compute diagonals starting from a slot in first column
                    q = self.ts2[k:k+n1] * self.ts1[:n2-k]
                    q = utils.rolling_sum(q, self.window_size)
                    D = utils.calculate_distance_profile(q, self.window_size, mu_Q[k:k+len(q)], sigma_Q[k:k+len(q)],
                                                         mu_T[:len(q)], sigma_T[:len(q)])
                    self._index_profile[:len(q)] = np.where(D < self._matrix_profile[:len(q)],
                                                    np.arange(k, k + len(q)), self._index_profile[:len(q)])
                    self._matrix_profile[:len(q)] = np.minimum(D, self._matrix_profile[:len(q)])
                    if self._same_ts:
                        self._index_profile[k:k+len(q)] = np.where(D < self._matrix_profile[k:k+len(q)],
                                                    np.arange(len(q)), self._index_profile[k:k+len(q)])
                        self._matrix_profile[k:k+len(q)] = np.minimum(D, self._matrix_profile[k:k+len(q)])
                else:
                    # compute diagonals starting from a slot in first row
                    k = -k
                    q = self.ts2[:n1-k] * self.ts1[k:k+n2]
                    q = utils.rolling_sum(q, self.window_size)
                    D = utils.calculate_distance_profile(q, self.window_size, mu_Q[:len(q)], sigma_Q[:len(q)],
                                                         mu_T[k:k+len(q)], sigma_T[k:k+len(q)])
                    self._index_profile[k:k+len(q)] = np.where(D < self._matrix_profile[k:k+len(q)],
                                                            np.arange(len(q)), self._index_profile[k:k+len(q)])
                    self._matrix_profile[k:k+len(q)] = np.minimum(D, self._matrix_profile[k:k+len(q)])
        except KeyboardInterrupt:
            if self.verbose:
                tqdm.write("Calculation interrupted at iteration {}. Approximate result returned.".format(n_iter))


class PreSCRIMP(MatrixProfile):
    """
    Class for the calculation of matrix profile using PreSCRIMP algorithm. This is a very fast *approximate*
    anytime algorithm. See [MP3]_ for more details.

    :param ts1: Time series for calculating the matrix profile.
    :type ts1: numpy array
    :param ts2: A second time series to compute matrix profile with respect to ts1. If None, ts1 will be used.
    :type ts2: numpy array
    :param int window_size: Subsequence length, must be a positive integer less than the length of both ts1 and ts2.
    :param float exclusion_zone: Exclusion zone, the length of exclusion zone is this number times window_size,
                                 centered at the point of interest.
                                 Must be non-negative. This parameter will be ignored if ts2 is not None.
    :param bool verbose: Whether to display progress or not.
    :param float s_size: Ratio of random calculations performed for anytime algorithms. Must be between 0 and 1,
                         1 means calculate all, and 0 means none.
    :param sample_rate: Sample rate in the PreSCRIMP algorithm. The sample interval is this number times window_size.
                        Must be positive. Defaults to 1/4.
    :param seed: Random seed used in numpy.random. None means to use a random seed.
    :type seed: int or None
    :raises: ValueError: If the input is invalid.
    """
    def __init__(self, ts1, ts2=None, window_size=None, exclusion_zone=1/2, verbose=True, s_size=1, seed=None, sample_rate=1/4):
        if sample_rate > 0:
            self.sr = sample_rate
        else:
            raise ValueError("sample_rate must be positive.")
        self.sample_interval = round(window_size * sample_rate + self._epsilon)
        super().__init__(ts1, ts2, window_size, exclusion_zone, verbose, s_size, seed)

    @property
    def is_anytime(self):
        """
        A property stating whether the algorithm for computing the matrix profile
        in this class is an anytime algorithm.

        :return: whether the algorithm in this class is an anytime algorithm.
        :rtype: bool
        """
        return True

    @property
    def _iterator(self):
        idxes = np.random.RandomState(self.seed).permutation(range(0, len(self.ts2) - self.window_size + 1, self.sample_interval))
        idxes = idxes[:round(self.s_size * len(idxes) + self._epsilon)]
        if self.verbose:
            _iterator = tqdm(idxes)
        else:
            _iterator = idxes
        return _iterator

    def _compute_matrix_profile(self):
        """
        Compute the matrix profile using PreSCRIMP.
        """
        try:
            mu_T, sigma_T = utils.rolling_avg_sd(self.ts1, self.window_size)
            if self._same_ts:
                mu_Q, sigma_Q = mu_T, sigma_T
            else:
                mu_Q, sigma_Q = utils.rolling_avg_sd(self.ts2, self.window_size)
            for n_iter, idx in enumerate(self._iterator):
                D = utils.mass(self.ts2[idx: idx+self.window_size], self.ts1)
                self._elementwise_min(D, idx)
                jdx = np.argmin(D)  # the index of closest profile to the current idx

                # compute diagonals until the next sampled point
                q1 = self.ts2[idx:idx + self.sample_interval + self.window_size - 1]
                q2 = self.ts1[jdx:jdx + self.sample_interval + self.window_size - 1]
                lq = min(len(q1), len(q2))
                q = q1[:lq] * q2[:lq]
                q = utils.rolling_sum(q, self.window_size)
                D = utils.calculate_distance_profile(q, self.window_size, mu_Q[idx:idx + len(q)], sigma_Q[idx:idx + len(q)],
                                                     mu_T[jdx:jdx + len(q)], sigma_T[jdx:jdx + len(q)])
                self._index_profile[jdx: jdx + len(q)] = np.where(D < self._matrix_profile[jdx:jdx + len(q)],
                                                        np.arange(idx, idx + len(q)), self._index_profile[jdx:jdx + len(q)])
                self._matrix_profile[jdx:jdx + len(q)] = np.minimum(D, self._matrix_profile[jdx:jdx + len(q)])
                if self._same_ts:
                    self._index_profile[idx:idx + len(q)] = np.where(D < self._matrix_profile[idx:idx + len(q)],
                                                                 np.arange(jdx, jdx + len(q)), self._index_profile[idx:idx + len(q)])
                    self._matrix_profile[idx:idx + len(q)] = np.minimum(D, self._matrix_profile[idx:idx + len(q)])

                # compute diagonals until the previous sampled point
                if idx != 0 and jdx != 0:
                    q1 = self.ts2[max(0, idx - self.sample_interval):(idx + self.window_size - 1)]
                    q2 = self.ts1[max(0, jdx - self.sample_interval):(jdx + self.window_size - 1)]
                    lq = min(len(q1), len(q2))
                    q = q1[-lq:] * q2[-lq:]
                    q = utils.rolling_sum(q, self.window_size)
                    D = utils.calculate_distance_profile(q, self.window_size, mu_Q[idx - len(q):idx],
                                                         sigma_Q[idx - len(q):idx],
                                                         mu_T[jdx - len(q):jdx], sigma_T[jdx - len(q):jdx])
                    self._index_profile[jdx - len(q): jdx] = np.where(D < self._matrix_profile[jdx - len(q):jdx],
                                                                      np.arange(idx - len(q), idx),
                                                                      self._index_profile[jdx - len(q):jdx])
                    self._matrix_profile[jdx - len(q):jdx] = np.minimum(D, self._matrix_profile[jdx - len(q):jdx])
                    if self._same_ts:
                        self._index_profile[idx - len(q):idx] = np.where(D < self._matrix_profile[idx - len(q):idx],
                                                                         np.arange(jdx - len(q), jdx),
                                                                         self._index_profile[idx - len(q):idx])
                        self._matrix_profile[idx - len(q):idx] = np.minimum(D, self._matrix_profile[idx - len(q):idx])
        except KeyboardInterrupt:
            if self.verbose:
                tqdm.write("Calculation interrupted at iteration {}. Approximate result returned.".format(n_iter))


