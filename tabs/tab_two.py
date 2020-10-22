import dash
import dash_core_components as dcc
import dash_html_components as html
import graphs

def tab_two():
    """ Contents in the second tab 'Climate Summary'.
    """
    return html.Div(
        children = [
            html.Div(
                className = "container-col",
                children = [
                    html.H3('Climate Profiles'),
                    html.Div(
                        className = "container-row",
                        children = [
                            dcc.Graph(
                                id = 'temp-profile-graph',
                                figure = graphs.create_violin_temperature()
                            ), 
                            dcc.Graph(
                                id = 'humidity-profile-graph',
                                figure = graphs.create_violin_humidity()
                            ), 
                            dcc.Graph(
                                id = 'solar-radiation-graph',
                                figure = graphs.create_violin_solar()
                            ), 
                            dcc.Graph(
                                id = 'wind-speed-graph',
                                figure = graphs.create_violin_wind()
                            )
                        ]
                    )
                ]
            )
        ]
    )