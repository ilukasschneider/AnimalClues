import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_game_stats, delete_stats
import plotly.graph_objects as go

from streamlit_js_eval import streamlit_js_eval




# load the data of the user
games = load_game_stats()['games']
total_games = len(games)

games_won = 0
for game in games:
    if game[1]:
        games_won += 1

games_lost = total_games - games_won

data = {
    "Game ID": list(range(1, total_games+1)),
    "Win": list(game[1] for game in games),
    "Clues": list(game[0] for game in games),
    "Good Guesses": list(game[2].count(4) + game[2].count(3) for game in games),
    "Average Guesses": list(game[2].count(2) + game[2].count(1) for game in games),
    "Bad Guesses": list(game[2].count(0) for game in games),
    "Quality": list(sum(game[2])/len(game[2]) for game in games)
}
df = pd.DataFrame(data)

# Streamlit app layout
st.title("Guessing Game Statistics")

# only display stats if you already played some games
if total_games > 0:

    # Total games played
    st.subheader(f"Total Games Played: {total_games}")

    # Display overall game statistics
    st.write("## Overall Statistics")

    # Average number of guesses per game
    avg_guesses = df["Clues"].mean()
    st.write(f"**Average Number of Guesses per Game:** {avg_guesses:.2f}")
    #
    # # Average number of good guesses per game
    avg_good_guesses = df["Good Guesses"].mean()
    st.write(f"**Average Good Guesses per Game:** {avg_good_guesses:.2f}")



    # Win rate
    win_rate = df["Win"].mean() * 100
    st.write(f"**Win Rate:** {win_rate:.2f}%")

    # Summary table for each game
    st.write("## Game-by-Game Summary")
    st.dataframe(df)

    st.session_state.detailed_view = False

    st.write("## Number of Guesses per Game")
    # Use columns to place buttons side by side
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Show Good and Bad Guesses"):
            st.session_state.detailed_view = True
    with col2:
        if st.button("Show Total Guesses"):
            st.session_state.detailed_view = False

    # Display the appropriate bar chart based on the toggle state
    if st.session_state.detailed_view:
        # Color-coded chart showing Good, Average and Bad Guesses
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df.index, y=df["Good Guesses"], name="Good Guesses", marker=dict(color='green')))
        fig.add_trace(go.Bar(x=df.index, y=df["Bad Guesses"], name="Bad Guesses"))
        fig.add_trace(go.Bar(x=df.index, y=df["Average Guesses"], name="Average Guesses", marker=dict(color='blue')))

    else:
        # Default view showing only the Total Guesses
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df.index, y=df["Clues"], name="Total Guesses"))

    # Add an average line for the Clues
    fig.add_trace(go.Scatter(x=df.index, y=[df["Clues"].mean()] * len(df),
                             mode='lines', name='Average Guesses',
                             line=dict(color='red', dash='dash')))

    # Update layout for better visibility
    fig.update_layout(barmode='stack', title="Guesses per Game",
                      xaxis_title="Game Index", yaxis_title="Number of Guesses")

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig)



    # Display pie chart for win/loss distribution
    st.write("## Win/Loss Distribution")
    win_loss_count = df["Win"].value_counts()
    st.write("Win-Loss Chart")
    st.write("Wins: ", games_won, " Losses: ", games_lost)
    # Create a new Figure and Axes
    fig, ax = plt.subplots()
    win_loss_count.plot.pie(autopct="%1.1f%%", labels=["Loss", "Win"], ax=ax)

    ax.set_ylabel('')  # Remove the y-axis label for a cleaner look

    # Display the pie chart in Streamlit
    st.pyplot(fig)

else:
    st.write("You have not played any games yet")

# reset the stats by deleting the file
if st.button("Reset"):
    delete_stats()
    streamlit_js_eval(js_expressions="parent.window.location.reload()")


