from peloton import PelotonWorkout
import numpy as np
import pandas as pd

def get_all_workout_data():
    variables = ['timestamp', 'fitness_discipline', 'title', 'duration', 'instructor', 'calories', 'distance', 'avg_hr']
    workouts = PelotonWorkout.list()
    df = pd.DataFrame(columns=variables)
    for workout in workouts:
        try:
            wkout = workout.__dict__
            start_time = wkout['start_time']
            workout_type = wkout['fitness_discipline']
            workout_deets = wkout['ride'].__dict__
            title = workout_deets['title']
            duration = workout_deets['duration']
            instructor = workout_deets['instructor'].name
            cals = (workout.metrics.calories_summary.__dict__)['value']
            dist = (workout.metrics.distance_summary.__dict__)['value']
            avg_hr = workout.metrics.heart_rate.average
            if not (cals and dist):
                continue
            data = [start_time, workout_type, title, duration, instructor, cals, dist, avg_hr]
            df.loc[len(df.index)] = data
        except:
            # print("Uh oh. There was an error fetching data from workout", workout.id)
            continue
    return df

df = get_all_workout_data()
df.to_csv('workout_data.csv', index=False)