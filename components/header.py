import dash_html_components as html
import dash_core_components as dcc

def Header():
    return html.Div([
        # get_logo(),
        get_header(),
        html.Br([]),
        get_menu()
    ])

def get_logo():
    logo = html.Div([

        html.Div([
            html.Img(src='http://logonoid.com/images/vanguard-logo.png', height='40', width='160')
        ], className="ten columns padded"),

        html.Div([
            dcc.Link('Full View   ', href='/dash-vanguard-report/full-view')
        ], className="two columns page-view no-print")

    ], className="row gs-header")
    return logo


def get_header():
    header = html.Div([

        html.Div([
            html.H5(
                'Expected Goals (xG) for Argentina Super League')
        ], className="twelve columns padded")

    ], className="row gs-header gs-text-header")
    return header


def get_menu():
    menu = html.Div([

        dcc.Link('Overview   ', href='/argentina_superliga/overview', className="tab first"),

        dcc.Link('Top Goal Scorers   ', href='/argentina_superliga/top_scorers', className="tab"),

        dcc.Link('Total xG + xA Leaders   ', href='/argentina_superliga/total_contributions', className="tab"),

        dcc.Link('Best xG + xA/90 Minutes   ', href='/argentina_superliga/per_90', className="tab"),

        dcc.Link('Potential Transfer Gems   ', href='/argentina_superliga/gems', className="tab"),

        dcc.Link('About   ', href='/argentina_superliga/about', className="tab")

    ], className="row ")
    return menu
