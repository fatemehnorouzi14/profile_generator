import unittest

import numpy as np

from src.moduel.Visualizer import (bar_chart,
                                   plot_annualTimeseriesOfMultipleProfiles,
                                   plot_durationCurvesOfMultipleProfiles,
                                   plot_heatmap, plot_load_profile)


class TestPlottingFunctions(unittest.TestCase):

    def test_plot_durationCurvesOfMultipleProfiles(self):
        # Create some sample profile data
        profileData = np.random.rand(3, 8760) * 1000
        traceNames = ["Profile 1", "Profile 2", "Profile 3"]
        line_colors = ["blue", "green", "red"]

        fig = plot_durationCurvesOfMultipleProfiles(profileData, traceNames, line_colors)
        self.assertIsNotNone(fig)

    def test_plot_annualTimeseriesOfMultipleProfiles(self):
        # Create some sample profile data
        profileData = np.random.rand(3, 8760) * 1000
        traceNames = ["Profile 1", "Profile 2", "Profile 3"]
        line_colors = ["blue", "green", "red"]

        fig = plot_annualTimeseriesOfMultipleProfiles(profileData, traceNames, line_colors)
        self.assertIsNotNone(fig)





if __name__ == '__main__':
    unittest.main()
