from flask import Flask, render_template, jsonify, request
from services.mysql_db import all_weather_records, save_record
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

COMMON_LAYOUT = dict(
    template="plotly_white",
    hovermode="x unified",
    margin=dict(l=40, r=40, t=60, b=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    xaxis=dict(
        showgrid=False,
        title="Czas"
    )
)

@app.route("/")
def home_page():

    try:
        weather = all_weather_records()
    except Exception as e:
        weather = []
        print(e)

    df = pd.DataFrame(weather)

    temp_fig = px.line(
        df,
        x="data_pomiaru",
        y="temperatura",
        title="Temperatura"
    )

    humidity_fig = px.scatter(
        df,
        x="data_pomiaru",
        y="wilgotnosc",
        labels=["A","B"]
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["data_pomiaru"],
        y=df["temperatura"],
        name="Temperatura rzeczywista"
    ))
    fig.add_trace(go.Bar(
        x=df["data_pomiaru"],
        y=df["odczuwalna_temperatura"],
        name="Temperatura odczuwalna"
    ))
    fig.update_layout(
        **COMMON_LAYOUT,
        title="Porównanie temp. odczuwalnej i rzeczywistej",
        xaxis_title="Czas",
        yaxis_title="Temperatura"
    )


    return render_template(
        "index.html",
        weather=weather,
        temp_plot=temp_fig.to_html(full_html=False),
        humidity_plot=humidity_fig.to_html(full_html=False),
        temp_compare_plot= fig.to_html(full_html=False)
    )

@app.get("/health")
def get_health():
    return jsonify(
        {
            "message":"API Pogoda",
            "version":"4.44"
        }
    )

@app.get("/weather/all")
def get_all_weather():
    try:
        data = all_weather_records()
    except Exception as e:
        data = []
        print(e)

    return jsonify({
        "message": "Pobrano dane",
        "status":200,
        "data": data
    })

@app.post("/weather/create")
def create_weather_record():
    weather = request.json()

    save_record(weather)

    return jsonify({
        "message": "Pobrano dane",
        "status":200,
        "data": weather
    })

