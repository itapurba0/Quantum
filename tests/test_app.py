def test_app_layout_contains_heading():
    """Simple unit test: verify the Dash app layout contains the expected H1 heading.
    This avoids requiring a browser/webdriver during local tests.
    """
    import app

    # app.layout is an html.Div with children; first child is html.H1
    layout = app.app.layout
    # Access children safely (could be tuple or list)
    children = getattr(layout, "children", [])
    assert len(children) >= 1
    h1 = children[0]
    # The H1 component has the text as .children
    assert "Quantium starter" in h1.children
