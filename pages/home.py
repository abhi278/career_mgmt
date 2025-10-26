"""
Home Page - Resume Analysis Interface
"""

import os
import json
import base64
from pathlib import Path

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

# Import the resume analyzer
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from resume_analyzer.resume_analyzer import ResumeAnalyzer

# Register page
dash.register_page(__name__, path='/', name='Home')

# Initialize the analyzer
try:
    analyzer = ResumeAnalyzer()
except ValueError:
    analyzer = None


def create_upload_section(id_prefix, label):
    """Create file upload or text input section."""
    return dbc.Card([
        dbc.CardHeader(html.H5(label, className="mb-0")),
        dbc.CardBody([
            dbc.Tabs([
                dbc.Tab(
                    label="Upload File",
                    tab_id=f"{id_prefix}-upload-tab",
                    children=[
                        html.Div([
                            dcc.Upload(
                                id=f'{id_prefix}-upload',
                                children=html.Div([
                                    html.I(className="fas fa-cloud-upload-alt fa-3x mb-3"),
                                    html.Br(),
                                    'Drag and Drop or ',
                                    html.A('Select File', style={'color': '#007bff', 'cursor': 'pointer'}),
                                    html.Br(),
                                    html.Small('Supported: .txt, .pdf, .docx', className="text-muted")
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '100px',
                                    'lineHeight': '100px',
                                    'borderWidth': '2px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '10px',
                                    'textAlign': 'center',
                                    'margin': '20px 0'
                                },
                                multiple=False
                            ),
                            html.Div(id=f'{id_prefix}-upload-status', className="mt-2")
                        ])
                    ]
                ),
                dbc.Tab(
                    label="Paste Text",
                    tab_id=f"{id_prefix}-text-tab",
                    children=[
                        html.Div([
                            dbc.Textarea(
                                id=f'{id_prefix}-text',
                                placeholder=f"Paste your {label.lower()} here...",
                                style={'height': '200px', 'marginTop': '20px'},
                                className="form-control"
                            )
                        ])
                    ]
                )
            ], id=f"{id_prefix}-tabs", active_tab=f"{id_prefix}-upload-tab")
        ])
    ], className="mb-4")


def get_match_color(match_level):
    """Get alert color based on match level."""
    colors = {
        'Excellent': 'success',
        'Good': 'info',
        'Fair': 'warning',
        'Poor': 'danger'
    }
    return colors.get(match_level, 'secondary')


def create_results_layout(results):
    """Create the results display layout."""
    if not results:
        return html.Div()

    # Similarity score gauge
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=results['similarity_score'],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Match Score", 'font': {'size': 24}},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffebee'},
                {'range': [50, 70], 'color': '#fff9c4'},
                {'range': [70, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    gauge_fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))

    # Skills comparison chart
    matching_count = len(results.get('matching_skills', []))
    missing_count = len(results.get('missing_skills', []))

    skills_fig = go.Figure(data=[
        go.Bar(
            x=['Matching Skills', 'Missing Skills'],
            y=[matching_count, missing_count],
            marker_color=['#4caf50', '#f44336'],
            text=[matching_count, missing_count],
            textposition='auto'
        )
    ])
    skills_fig.update_layout(
        title="Skills Overview",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis_title="Count"
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("📊 Analysis Results", className="mb-4")
            ])
        ]),

        # Score and Charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=gauge_fig, config={'displayModeBar': False})
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=skills_fig, config={'displayModeBar': False})
                    ])
                ])
            ], md=6)
        ], className="mb-4"),

        # Overall Match Badge
        dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H4([
                        html.I(className="fas fa-check-circle me-2"),
                        f"Overall Match: {results.get('overall_match', 'N/A')}"
                    ], className="mb-0")
                ], color=get_match_color(results.get('overall_match', '')))
            ])
        ], className="mb-4"),

        # Analysis Summary
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("📝 Summary", className="mb-0")),
                    dbc.CardBody([
                        html.P(results.get('analysis_summary', 'No summary available'))
                    ])
                ])
            ])
        ], className="mb-4"),

        # Key Strengths
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("✨ Key Strengths", className="mb-0")),
                    dbc.CardBody([
                        html.Ul([
                            html.Li(strength) for strength in results.get('key_strengths', [])
                        ]) if results.get('key_strengths') else html.P("No key strengths identified", className="text-muted")
                    ])
                ])
            ])
        ], className="mb-4"),

        # Skills Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("✅ Matching Skills", className="mb-0")),
                    dbc.CardBody([
                        html.Div([
                            dbc.Badge(skill, color="success", className="me-2 mb-2")
                            for skill in results.get('matching_skills', [])
                        ]) if results.get('matching_skills') else html.P("No matching skills found", className="text-muted")
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("❌ Missing Skills", className="mb-0")),
                    dbc.CardBody([
                        html.Div([
                            dbc.Badge(skill, color="danger", className="me-2 mb-2")
                            for skill in results.get('missing_skills', [])
                        ]) if results.get('missing_skills') else html.P("No missing skills identified", className="text-muted")
                    ])
                ])
            ], md=6)
        ], className="mb-4"),

        # Partial Matches
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("⚠️ Partial Matches", className="mb-0")),
                    dbc.CardBody([
                        html.Ul([
                            html.Li(match) for match in results.get('partial_matches', [])
                        ]) if results.get('partial_matches') else html.P("No partial matches found", className="text-muted")
                    ])
                ])
            ])
        ], className="mb-4"),

        # Recommendations
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("💡 Recommendations", className="mb-0")),
                    dbc.CardBody([
                        html.Ol([
                            html.Li(rec) for rec in results.get('recommendations', [])
                        ]) if results.get('recommendations') else html.P("No recommendations available", className="text-muted")
                    ])
                ])
            ])
        ], className="mb-4"),

        # Download Button
        dbc.Row([
            dbc.Col([
                dbc.Button(
                    [html.I(className="fas fa-download me-2"), "Download Results (JSON)"],
                    id="download-button",
                    color="success",
                    size="lg",
                    className="w-100"
                )
            ], md=6, className="mx-auto")
        ]),

        dcc.Download(id="download-json")

    ], fluid=True, className="mt-4")


# Layout
def layout():
    """Create the home page layout."""
    if analyzer is None:
        return dbc.Container([
            dbc.Alert([
                html.H4("⚠️ Configuration Required", className="alert-heading"),
                html.P("OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable."),
                html.Hr(),
                html.P([
                    "Create a ",
                    html.Code(".env"),
                    " file with: ",
                    html.Code("OPENAI_API_KEY=your-key-here")
                ], className="mb-0")
            ], color="warning")
        ], fluid=True)

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("🎯 Analyze Your Resume", className="mb-4"),
                html.P("Upload or paste your job description and resume to get detailed analysis with AI-powered insights.",
                       className="lead text-muted")
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                create_upload_section("job", "Job Description")
            ], md=6),
            dbc.Col([
                create_upload_section("resume", "Resume")
            ], md=6)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Button(
                    [html.I(className="fas fa-chart-bar me-2"), "Analyze Resume"],
                    id="analyze-button",
                    color="primary",
                    size="lg",
                    className="w-100",
                    disabled=False
                )
            ], md=6, className="mx-auto mb-4")
        ]),

        # Loading spinner
        dcc.Loading(
            id="loading",
            type="default",
            children=html.Div(id="loading-output")
        ),

        # Results section
        html.Div(id="results-section", className="mt-4"),

        # Store components for data
        dcc.Store(id='job-content-store'),
        dcc.Store(id='resume-content-store'),
        dcc.Store(id='analysis-results-store')

    ], fluid=True)


# Callbacks
@callback(
    [Output('job-upload-status', 'children'),
     Output('job-content-store', 'data')],
    [Input('job-upload', 'contents'),
     Input('job-text', 'value')],
    [State('job-upload', 'filename')]
)
def handle_job_input(upload_contents, text_value, filename):
    """Handle job description input (file or text) without tabs (dash pages)."""
    if upload_contents:
        content = parse_contents(upload_contents, filename or "uploaded_file")
        if content:
            return dbc.Alert(f"✓ Loaded: {filename or 'uploaded file'}", color="success", className="mt-2"), content
        else:
            return dbc.Alert("✗ Failed to load file", color="danger", className="mt-2"), None
    elif text_value:
        return dbc.Alert("✓ Text loaded", color="success", className="mt-2"), text_value

    return no_update, None


@callback(
    [Output('resume-upload-status', 'children'),
     Output('resume-content-store', 'data')],
    [Input('resume-upload', 'contents'),
     Input('resume-text', 'value')],
    [State('resume-upload', 'filename'),
     State('resume-tabs', 'active_tab')]
)
def handle_resume_input(upload_contents, text_value, filename, active_tab):
    """Handle resume input (file or text)."""
    if active_tab == 'resume-upload-tab' and upload_contents:
        content = parse_contents(upload_contents, filename)
        if content:
            return dbc.Alert(f"✓ Loaded: {filename}", color="success", className="mt-2"), content
        else:
            return dbc.Alert("✗ Failed to load file", color="danger", className="mt-2"), None
    elif active_tab == 'resume-text-tab' and text_value:
        return dbc.Alert("✓ Text loaded", color="success", className="mt-2"), text_value

    return no_update, None


@callback(
    [Output('results-section', 'children'),
     Output('analysis-results-store', 'data'),
     Output('loading-output', 'children')],
    Input('analyze-button', 'n_clicks'),
    [State('job-content-store', 'data'),
     State('resume-content-store', 'data')],
    prevent_initial_call=True
)
def analyze_resume(n_clicks, job_content, resume_content):
    """Perform resume analysis."""
    if not n_clicks:
        raise PreventUpdate

    if not job_content or not resume_content:
        return dbc.Alert(
            "⚠️ Please provide both job description and resume",
            color="warning"
        ), None, None

    if analyzer is None:
        return dbc.Alert(
            "⚠️ OpenAI API key not configured",
            color="danger"
        ), None, None

    try:
        # Perform analysis
        results = analyzer.analyze(job_content, resume_content)

        # Create results layout
        results_layout = create_results_layout(results)

        return results_layout, results, None

    except Exception as e:
        return dbc.Alert(
            f"❌ Error during analysis: {str(e)}",
            color="danger"
        ), None, None


@callback(
    Output('download-json', 'data'),
    Input('download-button', 'n_clicks'),
    State('analysis-results-store', 'data'),
    prevent_initial_call=True
)
def download_results(n_clicks, results):
    """Download analysis results as JSON."""
    if not n_clicks or not results:
        raise PreventUpdate

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resume_analysis_{timestamp}.json"

    return dict(
        content=json.dumps(results, indent=2),
        filename=filename
    )


def parse_contents(contents, filename):
    """Parse uploaded file contents."""
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        if filename.endswith('.txt'):
            return decoded.decode('utf-8')

        elif filename.endswith('.pdf'):
            # Save temporarily and extract
            temp_path = f"./tmp/{filename}"
            with open(temp_path, 'wb') as f:
                f.write(decoded)
            text = analyzer._extract_from_pdf(temp_path)
            os.remove(temp_path)
            return text

        elif filename.endswith('.docx'):
            # Save temporarily and extract
            temp_path = f"./tmp/{filename}"
            with open(temp_path, 'wb') as f:
                f.write(decoded)
            text = analyzer._extract_from_docx(temp_path)
            os.remove(temp_path)
            return text

        else:
            return None

    except Exception as e:
        print(f"Error parsing file: {str(e)}")
        return None
