# Import the libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_ag_grid as dag

# Import data
df_fs = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_fs.csv")
df_np = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_np.csv")
df_fA = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_fA.csv")

# Get the number of designs AND total steps/iterations
designs = df_fs.shape[0]
steps = len([col for col in df_fs.columns if 'in:' in col])

# List all the metric column labels
df1 = df_fs.columns.values[steps:len(df_fs.columns.values)-1]
df2 = df_fs.iloc[:,:steps]
histogram_values = ["Force Selection param", "Node Placement param", "Force Indeterminacies (A) param"]

# Instatiate the app
app = Dash()
server = app.server

# App layout
app.layout = [html.Div(
    children = "Using the Dash application for DSE and interpreting Libra generated designs"),
              html.Hr(),
              html.H3("You have imported " + str(df_fs.shape[0]) + " designs."),
              #----------------------------------------------------------------
              html.H4("Below, their parameters are showcased."),
              dag.AgGrid(
                  id="all-parameters-table",
                  columnDefs=[{"field": x} for x in df_fs.columns],
                  rowData=df_fs.to_dict("records"),
                  dashGridOptions={"pagination":True}
              ),
              #----------------------------------------------------------------
              html.H4("Sort by:"),
              dcc.Dropdown(
                  id="dropdown-sorting-metrics",
                  options=df1,
                  value="out:StaticAction"),
              html.H4("Sorting order:"),
              dcc.RadioItems(
                  id="radiobutton-sorting-order",
                  options=["Ascending", "Descending"],
                  value="Ascending"),
              dag.AgGrid(
                  id="sorted-parameters-table",
                  columnDefs=[{"field": x} for x in df_fs.columns],
                  rowData=df_fs.to_dict("records"),
                  dashGridOptions={"pagination":True}
              ),
              #----------------------------------------------------------------
              html.H3("Below, the parameter histograms per iteration (step) are showcased."),
              html.H4("Select the parameter you wish to investigate:"),
              dcc.Dropdown(
                  id="dropdown-histogram-value",
                  options=histogram_values,
                  value = histogram_values[0]),
              html.H4("Select the parameter (step) you wish to investigate:"),
              dcc.Slider(0, 
                         steps-1,
                         1,
                         value=0,
                        id="slider-iteration"
               ),
               #html.Div(id='slider-output-container'),
              #----------------------------------------------------------------
              dcc.Graph(
                  id="histogram",
                  figure= {},
                  ),
              html.Hr()
              ]

@callback(
    Output(component_id="sorted-parameters-table", component_property="rowData"),
    Input(component_id="dropdown-sorting-metrics", component_property="value"),
    Input(component_id="radiobutton-sorting-order", component_property="value")
)
def update_output(sort_metrics, sort_order):
    asc_order=False
    if sort_order=="Ascending": asc_order = True
    df_sorted = df_fs.sort_values(by=sort_metrics, ascending=asc_order)
    rowData=df_sorted.to_dict("records")
    return rowData

@callback(
    Output(component_id="histogram", component_property="figure"),
    Input(component_id="dropdown-histogram-value", component_property="value"),
    Input(component_id="slider-iteration", component_property="value")
)
def update_histograms(parameter, iteration_value):
    if parameter == "Force Selection param":
        fig = px.histogram(df_fs, x="in:fs_" + str(iteration_value), nbins=200)
    elif parameter == "Node Placement param":
        fig = px.histogram(df_np, x="in:np_" + str(iteration_value), nbins=200)
    elif parameter == "Force Indeterminacies (A) param":
        fig = px.histogram(df_fA, x="in:fA_" + str(iteration_value), nbins=200)
    fig.update_layout(bargap=0.05)
    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)