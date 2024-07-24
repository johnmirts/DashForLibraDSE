# Import the libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, callback
import dash_ag_grid as dag
import plotly.graph_objects as go

# Import data
df_fs = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_fs.csv")
df_np = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_np.csv")
df_fA = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_fA.csv")
df = pd.read_csv("D:\\OneDrive\\Research\\Libra\\Application studies\\20240722_2D_ArchBridge_symmetric_v1.3.0 (Dash)\\data\\data_all_params.csv")

# Get the number of designs AND total steps/iterations
designs = df.shape[0]
steps = len([col for col in df.columns if 'in:' in col])

# List all the metric column labels
df1 = df.columns.values[steps:len(df.columns.values)-1]
df2 = df.iloc[:,:steps]
histogram_values = ["Force Selection param", "Node Placement param", "Force Indeterminacies (A) param"]

# Instatiate the app
app = Dash()
server = app.server

# App layout
app.layout = [html.Div(
    children = "Using the Dash application for DSE and interpreting Libra generated designs"),
              html.Hr(),
              html.H3("You have imported " + str(designs) + " designs. Their parameters are showcased below."),
              #----------------------------------------------------------------
              dag.AgGrid(
                  id="all-parameters-table",
                  columnDefs=[{"field": x} for x in df.columns],
                  rowData=df.to_dict("records"),
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
                  columnDefs=[{"field": x} for x in df.columns],
                  rowData=df.to_dict("records"),
                  dashGridOptions={"pagination":True}
              ),
              #----------------------------------------------------------------
              html.H3("Below, the parameter histograms per iteration (step) are showcased."),
              #----------------------------------------------------------------
              html.H4("Select the parameter you wish to investigate:"),
              dcc.Dropdown(
                  id="dropdown-histogram-value",
                  options=histogram_values,
                  value = histogram_values[0]),
              html.H4("Select the iteration (step) you wish to investigate:"),
              dcc.Slider(0, 
                         steps-1,
                         1,
                         value=0,
                        id="slider-histogram-iteration"
               ),
               #html.Div(id='slider-output-container'),
              #----------------------------------------------------------------
              dcc.Graph(
                  id="histogram",
                  figure= {},
                  ),
              #----------------------------------------------------------------
              html.H3("Below, the parallel coordinates per iteration (step) are showcased."),
              #----------------------------------------------------------------
              html.H4("Select the parameter you wish to investigate:"),
              dcc.Dropdown(
                  id="dropdown-parallelcoords-value",
                  options=histogram_values,
                  value = histogram_values[0]),
              html.H4("Select how the parallel coordinates lines will be sorted:"),
              dcc.Dropdown(
                  id="dropdown-parallelcoords-sorting-metrics",
                  options=df1,
                  value="out:StaticAction"),
              html.H4("Sorting order:"),
              dcc.RadioItems(
                  id="radiobutton-parallelcoords-sorting-order",
                  options=["Ascending", "Descending"],
                  value="Ascending"),
              html.H4("Select the color style:"),
              dcc.Dropdown(
                  id="dropdown-parallelcoords-colorstyle",
                  options=["Plotly3 (sequetial)", "Magma (sequential)", "Grayscale (sequential)", "Tealrose (diverging)"],
                  value = "Grayscale (sequential)"),
              html.H4("Select the background color:"),
              dcc.RadioItems(
                  id="radiobutton-parallelcoords-background",
                  options=["Black", "White"],
                  value="Black"),
              #----------------------------------------------------------------
              dcc.Graph(
                  id="parallelcoords",
                  figure= {}
                  ),
                #   dcc.Graph(
                #       id="parallelcoords2",
                #       figure= {}
                #       )
              ]              


#----------------------------------------------------------------
@callback(
    Output(component_id="sorted-parameters-table", component_property="rowData"),
    Input(component_id="dropdown-sorting-metrics", component_property="value"),
    Input(component_id="radiobutton-sorting-order", component_property="value")
)
def update_output(sort_metrics, sort_order):
    asc_order=False
    if sort_order=="Ascending": asc_order = True
    df_sorted = df.sort_values(by=sort_metrics, ascending=asc_order)
    rowData=df_sorted.to_dict("records")
    return rowData
#----------------------------------------------------------------
@callback(
    Output(component_id="histogram", component_property="figure"),
    Input(component_id="dropdown-histogram-value", component_property="value"),
    Input(component_id="slider-histogram-iteration", component_property="value")
)
def update_histograms(parameter, iteration_value):
    if parameter == "Force Selection param":
        fig = px.histogram(data_frame = df_fs, x="in:fs_" + str(iteration_value), nbins=100)
    elif parameter == "Node Placement param":
        fig = px.histogram(data_frame = df_np, x="in:np_" + str(iteration_value), nbins=100)
    elif parameter == "Force Indeterminacies (A) param":
        fig = px.histogram(data_frame = df_fA, x="in:fA_" + str(iteration_value), nbins=50)
    fig.update_layout(bargap=0.1)
    return fig
#----------------------------------------------------------------
@callback(
    Output(component_id="parallelcoords", component_property="figure"),
    Input(component_id="dropdown-parallelcoords-value", component_property="value"),
    Input(component_id="dropdown-parallelcoords-sorting-metrics", component_property="value"),
    Input(component_id="radiobutton-parallelcoords-sorting-order", component_property="value"),
    Input(component_id="dropdown-parallelcoords-colorstyle", component_property="value"),
    Input(component_id="radiobutton-parallelcoords-background", component_property="value"),
)
def update_parallelcoords(parameter, sort_by, ascending_order, color_style, background_color):
    
    asc_order=False
    if ascending_order=="Ascending": asc_order = True
    
    if parameter == "Force Selection param":
        df_pc = df_fs.sort_values(by=sort_by, ascending=asc_order)
        title_fig="Parallel coordinates for Force Selection param"
    elif parameter == "Node Placement param":
        df_pc = df_np.sort_values(by=sort_by, ascending=asc_order)
        title_fig="Parallel coordinates for Node Placement param"
    elif parameter == "Force Indeterminacies (A) param":
        df_pc = df_fA.sort_values(by=sort_by, ascending=asc_order)
        title_fig="Parallel coordinates for Force Indeterminacies A param"
    
    if color_style == "Plotly3 (sequetial)":
        color_style_px = px.colors.sequential.Plotly3
    elif color_style == "Magma (sequential)":
        color_style_px = px.colors.sequential.Magma
    elif color_style == "Grayscale (sequential)":
        color_style_px = px.colors.sequential.gray
    elif color_style == "Tealrose (diverging)":
        color_style_px = px.colors.diverging.Tealrose
    
    fig = px.parallel_coordinates(
            data_frame=df_pc,
            color=sort_by,
            title=title_fig,
            color_continuous_scale=color_style_px,
            range_color = [min(df_pc[sort_by]), max(df_pc[sort_by])],
        )
        
    if background_color =="Black":
        fig.update_layout(
            paper_bgcolor = "black"
        )
       
    return fig

# @callback(
#     Output(component_id="parallelcoords2", component_property="figure"),
#     Input(component_id="radiobutton-parallelcoords-background", component_property="value"),
#     Input(component_id="histogram", component_property="hoverData"),
# )
# def update_hover(background_color, hover_data):
#     print(hover_data)
#     filtering_value = hover_data["out:StaticAction"]
#     d_temp = df[df["out:StaticAction"] == filtering_value]
#     fig = px.scatter(d_temp, x="in:fs_0", y="in:np_0")
    
#     if background_color =="Black":
#         fig.update_layout(
#             paper_bgcolor = "black"
#         )
       
#     return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)