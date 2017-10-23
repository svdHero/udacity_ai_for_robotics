from unittest import TestCase

import numpy as np
from lesson_1_assignment.localization import localize


class LocalizationTests(TestCase):
    def test_localize(self):
        colors = [['G', 'G', 'G'],
                  ['G', 'R', 'R'],
                  ['G', 'G', 'G']]
        measurements = ['R', 'R']
        motions = [[0, 0], [0, 1]]
        sensor_right = 0.8
        p_move = 1.0
        expected_prob_dist = (
            [[0.03333333333, 0.03333333333, 0.03333333333],
             [0.13333333333, 0.13333333333, 0.53333333333],
             [0.03333333333, 0.03333333333, 0.03333333333]])
        actual_prob_dist = localize(colors, measurements, motions, sensor_right, p_move)
        np.testing.assert_allclose(expected_prob_dist, actual_prob_dist)
