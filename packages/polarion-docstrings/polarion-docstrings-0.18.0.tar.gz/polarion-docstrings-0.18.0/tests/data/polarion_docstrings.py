# pylint: disable=missing-docstring,no-self-use

import pytest


class TestClassFoo:
    def test_in_class_no_docstring(self):
        pass

    def test_in_class_no_polarion(self):
        """FOO"""

    @pytest.mark.skip
    def test_in_class_polarion(self):
        """FOO

        Polarion:
            assignee: mkourim
            casecomponent: nonexistent
            caseimportance: low

            testSteps:
                1. Step with really long description
                   that doesn't fit into one line
                2. Do that

            expectedResults:
                1. Success outcome with really long description
                   that doesn't fit into one line
                2. second

            title: Some test with really long description
                   that doesn't fit into one line

            setup: Do this:
                   - first thing
                   - second thing

            teardown: Tear it down
            caselevel: level1
            caseautomation: automated
            linkedWorkItems: FOO, BAR
            foo: this is an unknown field
            description: ignored

        This is not included.
        """


@pytest.mark.skip
def test_annotated_no_docstring():
    pass


def test_standalone_no_docstring():
    pass


@pytest.mark.skip
def test_annotated_no_polarion():
    """FOO"""


@pytest.mark.skip
def test_annotated_polarion():

    """FOO

    Polarion:
        assignee: mkourim
        initialEstimate: 1/4
        testSteps: wrong


        expectedResults:
    """


def test_blacklisted():
    """FOO

    Polarion:
        initialEstimate: 1/4
    """


def test_blacklisted_and_whitelisted():
    """FOO

    Polarion:
        initialEstimate: 1/4
            assignee: someone
    """


def test_wrong_steps_indent():
    """Polarion:
        initialEstimate: 1/4
        testSteps:
            1. Step with really long description
               that doesn't fit into one line
               assignee: someone"""
