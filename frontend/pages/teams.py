from taipy.gui import Markdown, State
import pandas as pd
import plotly.express as px

def create_page():
    # Sample team data
    teams_data = pd.DataFrame({
        'Team': ['Team A', 'Team B', 'Team C'],
        'Wins': [10, 8, 6],
        'Losses': [2, 4, 6],
        'Goals': [30, 25, 20]
    })

    # Create visualization using plotly
    fig = px.bar(teams_data, x='Team', y=['Wins', 'Losses', 'Goals'],
                 title='Team Performance Overview',
                 barmode='group',
                 template='plotly_dark')

    page = Markdown("""
    # Team Analysis

    <|{fig}|chart|>

    <|{teams_data}|table|>
    """)

    return page