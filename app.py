import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Care Transition Analytics",
    page_icon="📊",
    layout="wide"
)


# =====================================================
# DATA FUNCTIONS
# =====================================================


@st.cache_data
def load_data(file):

    return pd.read_csv(file)



def preprocess(df):

    column_map = {

        "Children apprehended and placed in CBP custody":
            "CBP_Intake",

        "Children in CBP custody":
            "CBP_Custody",

        "Children transferred out of CBP custody":
            "Transferred_to_HHS",

        "Children in HHS Care":
            "HHS_Care",

        "Children discharged from HHS Care":
            "Discharged"
    }


    df.rename(
        columns=column_map,
        inplace=True
    )


    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )


    numeric_columns = [

        "CBP_Intake",
        "CBP_Custody",
        "Transferred_to_HHS",
        "HHS_Care",
        "Discharged"

    ]


    for col in numeric_columns:

        df[col] = (

            df[col]
            .astype(str)
            .str.replace(",","")

        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    df.dropna(
        subset=["Date"],
        inplace=True
    )


    return df



def create_metrics(df):


    # Efficiency Metrics

    df["Transfer_Efficiency_%"] = (

        df["Transferred_to_HHS"]
        /
        df["CBP_Custody"]
        *100

    )


    df["Discharge_Efficiency_%"] = (

        df["Discharged"]
        /
        df["HHS_Care"]
        *100

    )


    df["Pipeline_Throughput_%"] = (

        df["Discharged"]
        /
        df["CBP_Intake"]
        *100

    )


    df["Placement_Ratio_%"] = (

        df["Discharged"]
        /
        df["Transferred_to_HHS"]
        *100

    )


    # Backlog Metrics

    df["Daily_Backlog"] = (

        df["CBP_Intake"]
        -
        df["Discharged"]

    )


    df["Cumulative_Backlog"] = (

        df["Daily_Backlog"]
        .cumsum()

    )


    df["Unresolved_Cases"] = (

        df["CBP_Custody"]
        +
        df["HHS_Care"]

    )


    # Temporal Metrics

    df["Month"] = (

        df["Date"]
        .dt
        .to_period("M")
        .astype(str)

    )


    df["Placement_Change_%"] = (

        df["Placement_Ratio_%"]
        .pct_change()
        *100

    )


    return df



# =====================================================
# VISUALIZATION FUNCTIONS
# =====================================================


def pipeline_sankey(df):


    fig = go.Figure(
        go.Sankey(

            node=dict(

                label=[
                    "CBP Custody",
                    "HHS Care",
                    "Sponsor Placement"
                ]

            ),

            link=dict(

                source=[
                    0,
                    1
                ],

                target=[
                    1,
                    2
                ],

                value=[

                    df["Transferred_to_HHS"].mean(),

                    df["Discharged"].mean()

                ]

            )

        )
    )


    fig.update_layout(
        title="Care Pipeline Flow"
    )


    return fig




def efficiency_chart(df):

    return px.line(

        df,

        x="Date",

        y=[
            "Transfer_Efficiency_%",
            "Discharge_Efficiency_%"
        ],

        title="Transfer & Discharge Efficiency"

    )




def backlog_chart(df):

    return px.area(

        df,

        x="Date",

        y="Cumulative_Backlog",

        title="Backlog Accumulation"

    )




def outcome_chart(df):


    monthly = (

        df.groupby("Month")
        ["Placement_Ratio_%"]
        .mean()
        .reset_index()

    )


    return px.bar(

        monthly,

        x="Month",

        y="Placement_Ratio_%",

        title="Monthly Placement Outcome"

    )



# =====================================================
# APPLICATION
# =====================================================


st.title(
    "Care Transition Efficiency & Placement Outcome Analytics"
)


st.write(
"""
CBP Custody → HHS Care → Sponsor Placement Pipeline Dashboard
"""
)



uploaded_file = st.file_uploader(

    "Upload Cleaned CSV Dataset",

    type=["csv"]

)



if uploaded_file:


    df = load_data(uploaded_file)


    df = preprocess(df)


    df = create_metrics(df)



    # =================================================
    # SIDEBAR
    # =================================================


    st.sidebar.header(
        "Dashboard Controls"
    )


    start_date = st.sidebar.date_input(

        "Start Date",

        df.Date.min()

    )


    end_date = st.sidebar.date_input(

        "End Date",

        df.Date.max()

    )


    threshold = st.sidebar.slider(

        "Backlog Alert Threshold",

        0,

        10000,

        500

    )



    metric_mode = st.sidebar.radio(

        "Metric View",

        [
            "Absolute Values",
            "Efficiency Ratios"
        ]

    )



    filtered = df[

        (df.Date >= pd.to_datetime(start_date))

        &

        (df.Date <= pd.to_datetime(end_date))

    ]



    # =================================================
    # KPI SECTION
    # =================================================


    st.subheader(
        "Key Performance Indicators"
    )


    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "Transfer Efficiency",

        f"{filtered['Transfer_Efficiency_%'].mean():.2f}%"

    )


    c2.metric(

        "Discharge Efficiency",

        f"{filtered['Discharge_Efficiency_%'].mean():.2f}%"

    )


    c3.metric(

        "Pipeline Throughput",

        f"{filtered['Pipeline_Throughput_%'].mean():.2f}%"

    )


    c4.metric(

        "Placement Ratio",

        f"{filtered['Placement_Ratio_%'].mean():.2f}%"

    )



    # =================================================
    # ALERT SYSTEM
    # =================================================


    backlog = filtered.Unresolved_Cases.iloc[-1]


    if backlog > threshold:

        st.error(

            f"⚠ High backlog detected: {backlog:.0f} cases"

        )

    else:

        st.success(
            "Pipeline backlog is stable"
        )



    # =================================================
    # PIPELINE FLOW
    # =================================================


    st.plotly_chart(

        pipeline_sankey(filtered),

        use_container_width=True

    )



    # =================================================
    # EFFICIENCY PANELS
    # =================================================


    st.plotly_chart(

        efficiency_chart(filtered),

        use_container_width=True

    )



    # =================================================
    # BOTTLENECK DETECTION
    # =================================================


    st.subheader(
        "Bottleneck Detection"
    )


    filtered["Bottleneck"] = np.where(

        (

            filtered["Daily_Backlog"] > 0

        )

        &

        (

            filtered["Discharge_Efficiency_%"]

            <
            
            filtered["Discharge_Efficiency_%"].mean()

        ),

        "High Risk",

        "Normal"

    )


    bottlenecks = filtered[

        filtered.Bottleneck=="High Risk"

    ]


    st.dataframe(

        bottlenecks[

            [

            "Date",
            "Daily_Backlog",
            "Discharge_Efficiency_%",
            "Bottleneck"

            ]

        ]

    )



    st.plotly_chart(

        backlog_chart(filtered),

        use_container_width=True

    )



    # =================================================
    # OUTCOME ANALYSIS
    # =================================================


    st.subheader(
        "Outcome Trend Analysis"
    )


    st.plotly_chart(

        outcome_chart(filtered),

        use_container_width=True

    )



    # Sudden drops


    drops = filtered[

        filtered["Placement_Change_%"] < -20

    ]


    st.subheader(
        "Sudden Placement Drops"
    )


    st.dataframe(

        drops[

            [

            "Date",
            "Placement_Ratio_%",
            "Placement_Change_%"

            ]

        ]

    )



    # =================================================
    # METRIC TOGGLE
    # =================================================


    st.subheader(
        "Metric Comparison"
    )


    if metric_mode=="Efficiency Ratios":


        st.line_chart(

            filtered[

                [

                "Transfer_Efficiency_%",

                "Discharge_Efficiency_%",

                "Pipeline_Throughput_%",

                "Placement_Ratio_%"

                ]

            ]

        )


    else:


        st.line_chart(

            filtered[

                [

                "CBP_Intake",

                "Transferred_to_HHS",

                "Discharged"

                ]

            ]

        )



    # =================================================
    # DOWNLOAD
    # =================================================


    st.download_button(

        "Download Processed Dataset",

        filtered.to_csv(index=False),

        "care_transition_analysis.csv",

        "text/csv"

    )


else:

    st.info(
        "Upload your CSV dataset to start analysis."
    )