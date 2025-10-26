"""
Resume Analyzer - Main Dash Application
Uses Dash Pages for multi-page structure
"""

import dash
import dash_bootstrap_components as dbc
from dash import html

# Initialize Dash app with Pages plugin
app = dash.Dash(
    __name__,
    use_pages=True,  # Enable Dash Pages
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    title="Resume Analyzer"
)

# Server for deployment
server = app.server


def create_navbar():
    """Create navigation bar."""
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("About", href="/about")),
        ],
        brand="📄 Resume Analyzer",
        brand_href="/",
        color="primary",
        dark=True,
        className="mb-4"
    )


# App layout with navbar and page container
app.layout = html.Div([
    create_navbar(),
    dash.page_container  # This will render the page content
])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
