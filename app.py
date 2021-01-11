import streamlit as st
from peloton import PelotonWorkout
import numpy as np
import pandas as pd
import altair as alt


def main():
    st.markdown("# Welcome to the Pelo Wolfpack!")
    df = get_workout_data()
    st.write(df)
    plot_distance_over_time(df)

@st.cache(allow_output_mutation=True)
def get_workout_data():
    workouts = PelotonWorkout.list()
    variables = ['start_time', 'end_time', 'fitness_discipline', 'title', 'duration', 'instructor', 'calories', 'distance', 'output']
    df = pd.DataFrame(columns=variables)
    for workout in workouts:
        try:
            wkout = workout.__dict__
            start_time = wkout['start_time']
            end_time = wkout['end_time']
            workout_type = wkout['fitness_discipline']
            workout_deets = wkout['ride'].__dict__
            title = workout_deets['title']
            duration = workout_deets['duration']
            instructor = workout_deets['instructor'].name
            cals = (workout.metrics.calories_summary.__dict__)['value']
            dist = (workout.metrics.distance_summary.__dict__)['value']
            output = (workout.metrics.output_summary.__dict__)['value']
            if not (cals and dist and output):
                continue
            data = [start_time, end_time, workout_type, title, duration, instructor, cals, dist, output]
            df.loc[len(df.index)] = data
        except:
            continue
    return df

def plot_distance_over_time(df):
    new_df = df.sort_values(by='start_time', ascending=True).reset_index()
    new_df['k'] = new_df.index.copy()
    graph = alt.Chart(new_df).mark_bar().encode(
        x=alt.X('k:Q'),
        y=alt.Y('distance:Q'),
        # y=alt.Y(str(y_axis)+":Q"),
        color=alt.Color('fitness_discipline'),
        tooltip=['instructor', 'title']
    ).interactive()
    st.altair_chart(graph, use_container_width=True)

if __name__ == "__main__":
    main()