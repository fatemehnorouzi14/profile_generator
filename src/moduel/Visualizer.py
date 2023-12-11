import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from typing import List

class DataVisualizer:
    def __init__(self):
        self.name = []  
        self.color = []  
        self.profile_value = [] 

    def plot_duration_curve(self, *profiles) -> go.Figure:
        profile_data = [np.array(profile.value) for profile in profiles]
        trace_names = [profile.name if profile.name else f"Profile {i+1}" for i, profile in enumerate(profiles)]
        line_colors = ['#47FB35', '#D53513', 'blue']

        for profile_index in range(len(profile_data)):
            profile_data[profile_index] = -np.sort(-profile_data[profile_index])

        return self.plot_annualTimeseriesOfMultipleProfiles(profile_data, trace_names, line_colors)

    def plot_annualTimeseriesOfMultipleProfiles(self, profile_data: List[np.ndarray], trace_names: List[str] = None, line_colors: List[str] = None) -> go.Figure:
        number_of_profiles = len(profile_data)
        number_of_time_steps = profile_data[0].shape[0] if number_of_profiles > 0 else 0

        if trace_names is None:
            trace_names = [f"Profile {i+1}" for i in range(number_of_profiles)]

        fig = go.Figure()
        time_vector = np.linspace(0, 8760, num=number_of_time_steps, endpoint=True)
        data = []

        for series_index in range(number_of_profiles):
            line_color = None
            if line_colors is not None and len(line_colors) > series_index:
                line_color = line_colors[series_index]

            data.append(dict(type='scatter', x=time_vector, y=profile_data[series_index], name=trace_names[series_index], line=dict(color=line_color)))

        layout = go.Layout(
            xaxis=dict(title="Hours in year [h]"),
            yaxis=dict(title="Power [MWh]"),
            showlegend=number_of_profiles > 1
        )
        fig = go.Figure(data=data, layout=layout)
        return st.plotly_chart(fig, use_container_width=True)


    def plot_load_profile(self, *profiles):
        fig = go.Figure()
        list_profiles = []
        for i, profile in enumerate(profiles):
            profile_value = pd.DataFrame(profile.value)
            name = profile.name if profile.name else f'Profile {i+1}'
            color_line = profile.color if profile.color else None
            list_profiles.append(profile)
            fig.add_trace(go.Scatter(x=profile_value.index, y=profile_value[profile_value.columns[0]], mode='lines', line=dict(color=color_line), name=name, showlegend=True))

        fig.update_layout(xaxis_title='Time', yaxis_title=None)
        fig.add_annotation(
            text=f'<br>Peak: {list_profiles[0].get_max()} KW<br>sum: {list_profiles[0].get_sum(name_sector=profile.name)} MWh<br>Mean: {list_profiles[0].get_average()} KW<br>Min: {list_profiles[0].get_min()} KW<br>',
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.12,
            y=0.4,
            bordercolor='white',
            borderwidth=1
        )
        
        for trace in fig.data:
            self.name.append(trace.name)  
            self.color.append(trace.line.color)
            self.profile_value.append(trace.y)

        st.plotly_chart(fig, use_container_width=True)
        return fig

    def plot_heatmap(self,profile,old_profile_name):
        profile_data = pd.DataFrame(profile.value)
        profile_data['Timestamp'] = profile_data.index
        profile_data['Timestamp'] = pd.to_datetime(profile_data['Timestamp'])
        profile_data.rename(columns={old_profile_name: profile.name}, inplace=True)
        profile_data = profile_data.set_index('Timestamp')
        profile_data['Hour'] = profile_data.index.hour
        profile_data = profile_data.pivot_table(index=profile_data['Hour'], columns=profile_data.index.date, values=profile.name)
        if profile.name == "Electrical demand":
            profile.color = 'Viridis'
        if profile.name == "Total thermal demand":
            profile.color = 'YlOrRd'
        if profile.name == "Cooling demand":
            profile.color = 'YlGnBu'

        fig = go.Figure(data=go.Heatmap(z=profile_data.values, x=profile_data.columns, y=profile_data.index, colorscale=profile.color))
        fig.update_layout(title=f'{profile.name} heat map', xaxis_nticks=24)
        fig.update_xaxes(title_text='Date')
        fig.update_yaxes(title_text='Hour of the day')
        return st.plotly_chart(fig)

    def bar_chart(self, *args, names: list, title="Standard load profiles for domestic hot water demand", xaxis_title="Hour of the day", yaxis_title="Weight %"):
        fig = go.Figure()
        hours = np.arange(1, 25)

        for i, data in enumerate(args):
            if data is not None:
                name = names[i] if names else f'Profile {i+1}'
                trace = go.Bar(x=hours, y=data[0], name=name)
                fig.add_trace(trace)

        fig.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            barmode='group'
        )
        return st.plotly_chart(fig, use_container_width=True)

