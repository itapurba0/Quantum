import os
import sys



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import app as app_module


def start_app(dash_duo):
    dash_duo.start_server(app_module.app)
    return dash_duo


def test_header_renders(dash_duo):
    runner = start_app(dash_duo)
    header = runner.find_element(".header-card h1")
    assert "Pink Morsel" in header.text


def test_visualisation_renders(dash_duo):
    runner = start_app(dash_duo)
    graph = runner.find_element("#sales-line")
    assert graph is not None


def test_region_picker_available(dash_duo):
    runner = start_app(dash_duo)
    radio = runner.wait_for_element("#region-filter")
    assert radio is not None
    panel_text = radio.text.lower()
    for option in ["north", "south", "east", "west", "all regions"]:
        assert option in panel_text
