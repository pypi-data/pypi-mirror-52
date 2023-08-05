from os import path

import pytest

import test.mock
import autofit as af

directory = path.dirname(path.realpath(__file__))


class MockClass(object):
    pass


@pytest.fixture(name="label_config")
def make_label_config():
    return af.conf.LabelConfig("{}/test_files/config/label.ini".format(directory))


class TestLabel(object):
    def test_basic(self, label_config):
        assert label_config.label("centre_0") == "x"
        assert label_config.label("redshift") == "z"

    def test_escaped(self, label_config):
        assert label_config.label("gamma") == r"\gamma"
        assert label_config.label("contribution_factor") == r"\omega0"

    def test_subscript(self, label_config):
        assert label_config.subscript(test.mock.EllipticalLP) == "l"

    def test_inheritance(self, label_config):
        assert label_config.subscript(test.mock.EllipticalGaussian) == "l"

    def test_exception(self, label_config):
        with pytest.raises(af.exc.PriorException):
            label_config.subscript(MockClass)


class TestTextUtil(object):
    def test_string(self):
        assert af.text_util.format_string_for_label("radius") == "radius_value"
        assert af.text_util.format_string_for_label("mass") == "mass_value"

    def test_substring(self):
        assert af.text_util.format_string_for_label("einstein_radius") == "radius_value"
        assert af.text_util.format_string_for_label("mass_something") == "mass_value"
