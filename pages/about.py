"""
About Page - Information about the Resume Analyzer
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

# Register page
dash.register_page(__name__, path='/about', name='About')

# Layout
def layout():
    """Create the about page layout."""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("About Resume Analyzer", className="mb-4"),
                
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🤖 AI-Powered Resume Analysis", className="mb-3"),
                        html.P([
                            "This application uses OpenAI's GPT-4o-mini model to provide intelligent ",
                            "resume analysis and job matching insights."
                        ]),
                        
                        html.H5("Features:", className="mt-4 mb-3"),
                        html.Ul([
                            html.Li("📊 Similarity Score: Get a 0-100 match score"),
                            html.Li("✅ Matching Skills: See which skills align with the job"),
                            html.Li("❌ Missing Skills: Identify gaps in your resume"),
                            html.Li("💡 Recommendations: Receive actionable improvement tips"),
                            html.Li("📥 Export Results: Download analysis as JSON"),
                        ]),
                        
                        html.H5("Supported File Formats:", className="mt-4 mb-3"),
                        html.Ul([
                            html.Li("📄 Text files (.txt)"),
                            html.Li("📕 PDF documents (.pdf)"),
                            html.Li("📘 Word documents (.docx)"),
                        ]),
                        html.P([
                            html.Strong("Note: "),
                            "Legacy .doc format is not supported. Please convert to .docx format."
                        ], className="text-muted"),
                        
                        html.H5("Technology Stack:", className="mt-4 mb-3"),
                        html.Ul([
                            html.Li("OpenAI GPT-4o-mini API"),
                            html.Li("Plotly Dash 3.2.0"),
                            html.Li("Dash Bootstrap Components 2.0.4"),
                            html.Li("Plotly 6.3.1"),
                            html.Li("Python 3.9+"),
                            html.Li("Docker & Docker Compose"),
                        ]),
                        
                        html.H5("How It Works:", className="mt-4 mb-3"),
                        html.Ol([
                            html.Li("Upload or paste your job description and resume"),
                            html.Li("AI analyzes both documents using natural language processing"),
                            html.Li("Get detailed insights on skill matches and gaps"),
                            html.Li("Receive personalized recommendations to improve your resume"),
                            html.Li("Download results for future reference"),
                        ]),
                        
                        html.H5("Privacy & Security:", className="mt-4 mb-3"),
                        html.P([
                            "Your documents are processed securely and are not stored permanently. ",
                            "Files are temporarily saved during analysis and deleted immediately after. ",
                            "We use OpenAI's API which follows strict data privacy guidelines."
                        ]),
                        
                        html.Hr(),
                        
                        html.Div([
                            html.P([
                                html.Strong("Version: "),
                                "1.0.0"
                            ], className="mb-2"),
                            html.P([
                                html.Strong("License: "),
                                "MIT"
                            ], className="mb-2"),
                            html.P([
                                html.I(className="fab fa-github me-2"),
                                html.A(
                                    "View on GitHub",
                                    href="https://github.com/yourusername/resume-analyzer",
                                    target="_blank",
                                    className="text-decoration-none"
                                )
                            ], className="mb-0")
                        ], className="mt-4")
                    ])
                ], className="shadow-sm")
            ], md=10, lg=8, className="mx-auto")
        ])
    ], fluid=True, className="py-4")
