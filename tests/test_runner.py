"""Unit tests for runner module."""
import json
import os
from pprint import pprint

from pytest_web_ui import runner
from pytest_web_ui import result_tree


def test_init():
    """
    Test initialising the PyTestRunner. Ensures that the expected result tree skeleton
    is built.
    """
    directory = os.path.join(os.path.dirname(__file__), os.pardir, "pytest_examples")
    pyrunner = runner.PyTestRunner(directory)
    schema = result_tree.BranchNodeSchema()
    serialized = schema.dump(pyrunner.result_tree)
    pprint(serialized)

    json_filepath = os.path.join(
        os.path.dirname(__file__), os.pardir, "test_data", "result_tree_skeleton.json"
    )

    with open(json_filepath) as f:
        expected_serialization = json.load(f)

    assert serialized == expected_serialization


def test_run_tests():
    """
    Test running tests from a single module.
    """
    directory = os.path.join(os.path.dirname(__file__), os.pardir, "pytest_examples")
    runner_inst = runner.PyTestRunner(directory)
    runner_inst.run_tests("pytest_examples/test_a.py")

    for test_id in (
        "test_one",
        "test_two",
        "TestSuite::test_alpha",
        "TestSuite::test_beta",
    ):
        nodeid = f"pytest_examples/test_a.py::{test_id}"
        node = runner_inst._result_index[nodeid]
        assert node.report is not None
