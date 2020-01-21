#
# Test the base experiment class
#
import pybamm
import unittest


class TestExperiment(unittest.TestCase):
    def test_read_strings(self):
        experiment = pybamm.Experiment(
            [
                "Discharge at 1 C for 0.5 hours",
                "Charge at 0.5 C for 45 minutes",
                "Discharge at 1 A for 0.5 hours",
                "Charge at 200 mA for 45 minutes",
                "Discharge at 1 W for 0.5 hours",
                "Charge at 200 mW for 45 minutes",
                "Rest for 10 minutes",
                "Hold at 1 V for 20 seconds",
                "Charge at 1 C until 4.1 V",
                "Hold at 4.1 V until 50 mA",
            ],
            {"test": "test"},
            frequency="1 minute",
        )
        self.assertEqual(
            experiment.operating_conditions,
            [
                (1, "C", 1800.0),
                (-0.5, "C", 2700.0),
                (1, "A", 1800.0),
                (-0.2, "A", 2700.0),
                (1, "W", 1800.0),
                (-0.2, "W", 2700.0),
                (0, "A", 600.0),
                (1, "V", 20.0),
                (-1, "C", None),
                (4.1, "V", None),
            ],
        )
        self.assertEqual(
            experiment.events,
            [None, None, None, None, None, None, None, None, (4.1, "V"), (0.05, "A")],
        )
        self.assertEqual(experiment.parameters, {"test": "test"})
        self.assertEqual(experiment.frequency, 60)

    def test_read_strings_repeat(self):
        experiment = pybamm.Experiment(
            ["Discharge at 10 mA for 0.5 hours"]
            + ["Charge at 0.5 C for 45 minutes", "Hold at 1 V for 20 seconds"] * 2,
            {},
        )
        self.assertEqual(
            experiment.operating_conditions,
            [
                (0.01, "A", 1800.0),
                (-0.5, "C", 2700.0),
                (1, "V", 20.0),
                (-0.5, "C", 2700.0),
                (1, "V", 20.0),
            ],
        )
        self.assertEqual(experiment.frequency, 1)

    def test_str_repr(self):
        conds = ["Discharge at 1 C for 20 seconds", "Charge at 0.5 W for 10 minutes"]
        experiment = pybamm.Experiment(conds, {})
        self.assertEqual(str(experiment), str(conds))
        self.assertEqual(
            repr(experiment),
            "pybamm.Experiment(['Discharge at 1 C for 20 seconds'"
            + ", 'Charge at 0.5 W for 10 minutes'])",
        )

    def test_bad_strings(self):
        with self.assertRaisesRegex(
            TypeError, "Operating conditions should be strings"
        ):
            pybamm.Experiment([1, 2, 3], {})
        with self.assertRaisesRegex(ValueError, "Operating conditions must contain"):
            pybamm.Experiment(["Discharge at 1 A at 2 hours"], {})
        with self.assertRaisesRegex(ValueError, "instruction must be"):
            pybamm.Experiment(["Run at 1 A for 2 hours"], {})
        with self.assertRaisesRegex(ValueError, "instructions not recognized"):
            pybamm.Experiment(["Run 1 A for 2 hours"], {})
        with self.assertRaisesRegex(ValueError, "units must be"):
            pybamm.Experiment(["Discharge at 1 B for 2 hours"], {})
        with self.assertRaisesRegex(ValueError, "time units must be"):
            pybamm.Experiment(["Discharge at 1 A for 2 years"], {})
        with self.assertRaisesRegex(
            TypeError, "experimental parameters should be a dictionary"
        ):
            pybamm.Experiment([], "not a dictionary")


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    pybamm.settings.debug_mode = True
    unittest.main()

# {
#     "Reference temperature [K]": 298.15,
#     "Heat transfer coefficient [W.m-2.K-1]": 10,
#     "Number of electrodes connected in parallel to make a cell": 1,
#     "Number of cells connected in series to make a battery": 1,
#     "Lower voltage cut-off [V]": 3.105,
#     "Upper voltage cut-off [V]": 4.7,
#     "C-rate": 1,
#     "Initial concentration in negative electrode [mol.m-3]": 19986,
#     "Initial concentration in positive electrode [mol.m-3]": 30730,
#     "Initial concentration in electrolyte [mol.m-3]": 1000,
#     "Initial temperature [K]": 298.15,
# }
