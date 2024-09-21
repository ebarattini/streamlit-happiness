import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# title of the app
st.title("World Happiness Report Visualisation")

# sidebar for navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Map of World Happiness", "Maps of Other Factors", "More Plots", "About the Dataset"])

# load the dataset
try:
    df = pd.read_csv('data/world_happiness_combined.csv')
except FileNotFoundError:
    st.error("csv file not found. please make sure 'world_happiness_combined.csv' is in the correct directory.")
    st.stop()

# manually categorize countries by continent for use in the more plots section
continent_mapping = {
    "Europe": [
        'Ukraine','Switzerland', 'Iceland', 'Denmark', 'Norway', 'Finland', 'Netherlands', 'Sweden', 'Austria', 'Ireland', 
        'Belgium', 'United Kingdom', 'Luxembourg', 'Germany', 'France', 'Czech Republic', 'Spain', 'Malta', 
        'Slovakia', 'Italy', 'Slovenia', 'Lithuania', 'Poland', 'Croatia', 'Estonia', 'Portugal', 'Latvia', 
        'Romania', 'Serbia', 'Hungary', 'Greece', 'Bosnia and Herzegovina', 'Montenegro', 'North Macedonia', 
        'Albania', 'Bulgaria', 'Kosovo', 'Cyprus', 'Moldova'
    ],
    "Asia": [
        'Russia', 'Israel', 'United Arab Emirates', 'Oman', 'Singapore', 'Qatar', 'Japan', 'South Korea', 'Taiwan', 'Kuwait', 
        'Uzbekistan', 'Bahrain', 'Kazakhstan', 'Turkmenistan', 'Hong Kong', 'Indonesia', 'Vietnam', 'Turkey', 
        'Kyrgyzstan', 'Bhutan', 'Azerbaijan', 'Pakistan', 'Jordan', 'China', 'Mongolia', 'Laos', 'Lebanon', 
        'Tajikistan', 'Palestinian Territories', 'Bangladesh', 'Iran', 'Iraq', 'Myanmar', 'Sri Lanka', 'Armenia', 
        'Georgia', 'Yemen', 'Afghanistan', 'Cambodia', 'Syria', 'Taiwan Province of China', 'Hong Kong S.A.R.', 'Saudi Arabia'
    ],
    "Africa": [
        'Central African Republic', 'Sudan', 'Angola','Libya', 'Algeria', 'Morocco', 'Zambia', 'Nigeria', 'Zimbabwe', 'Sudan', 'Ghana', 'Ethiopia', 'Liberia', 
        'Sierra Leone', 'Mauritania', 'Kenya', 'Djibouti', 'Botswana', 'Cameroon', 'Egypt', 'Angola', 'Mali', 
        'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Comoros', 'Uganda', 'Senegal', 'Gabon', 'Niger', 'Tanzania', 
        'Madagascar', 'Central African Republic', 'Chad', 'Guinea', 'Ivory Coast', 'Burkina Faso', 'Rwanda', 
        'Benin', 'Burundi', 'Togo', 'Somalia', 'Namibia', 'South Africa', 'Gambia', 'South Sudan', 'Malawi', 
        'Swaziland', 'Lesotho', 'Mozambique'
    ],
    "North America": [
        'Canada', 'Mexico', 'United States', 'Costa Rica', 'Trinidad and Tobago', 'Belize', 'Jamaica', 
        'Guatemala', 'El Salvador', 'Honduras', 'Nicaragua', 'Dominican Republic', 'Haiti', 'Panama', 'Puerto Rico'
    ],
    "South America": [
        'Brazil', 'Argentina', 'Chile', 'Venezuela', 'Uruguay', 'Colombia', 'Suriname', 'Paraguay', 
        'Bolivia', 'Ecuador', 'Peru'
    ],
    "Oceania": ['Australia', 'New Zealand']
}

# add continent column to the dataframe based on the mapping
df['Continent'] = df['Country'].apply(lambda x: next((k for k, v in continent_mapping.items() if x in v), 'Unknown'))
df = df[df['Continent'] != 'Unknown']

# define color palette for maps
color_scale = ["#1984c5", "#22a7f0", "#63bff0", "#a7d5ed", "#e2e2e2", "#e1a692", "#de6e56", "#e14b31", "#c23728"]

# 1. world happiness map page
if menu == "Map of World Happiness":
    st.subheader("World Happiness Report Visualisation")
    
    st.markdown("""
    This app visualizes data from the [World Happiness Report](https://worldhappiness.report/), 
    which collects happiness scores and six factors that might explain differences in life satisfaction.
    """)

    # year slider for world happiness map
    year = st.slider("Select Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=int(df['Year'].max()), step=1)

    # filter dataframe for the selected year
    filtered_df = df[df['Year'] == year]

    st.subheader(f"World Happiness Map for {year}")

    # create a map for happiness score
    fig_happiness = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color="Happiness Score",
        hover_name="Country",
        hover_data=["Happiness Rank", "Happiness Score", "GDP per capita", "Life expectancy", "Freedom", "Trust", "Generosity"],
        title=f"World Happiness Score in {year}",
        color_continuous_scale=color_scale,
        range_color=(filtered_df["Happiness Score"].min(), filtered_df["Happiness Score"].max())
    )

    # layout settings
    fig_happiness.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
        ),
        height=700, 
        margin={"r":0,"t":0,"l":0,"b":0},
    )

    # display the map
    st.plotly_chart(fig_happiness, use_container_width=True)

# 2. other factors map page
elif menu == "Maps of Other Factors":
    st.subheader("Other Factors Compared to Happiness Scores")

    st.markdown("""
    Select one of the other factors collected in the study to view how it compares to happiness rates:
    """)

    # define factors available for visualization
    factors = ["GDP per capita", "Life expectancy", "Freedom", "Trust", "Generosity"]

    # dropdown to select the factor
    selected_factor = st.selectbox("Select a factor", factors)

    # year slider for the selected factor
    year = st.slider("Select Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=int(df['Year'].max()), step=1)

    # filter dataframe for the selected year
    filtered_df = df[df['Year'] == year]

    # create a map for the selected factor
    st.subheader(f"Map of {selected_factor} in {year}")

    fig_factor = px.choropleth(
        filtered_df,
        locations="Country",
        locationmode="country names",
        color=selected_factor,
        hover_name="Country",
        hover_data=["Happiness Rank", selected_factor],
        title=f"{selected_factor} in {year}",
        color_continuous_scale=color_scale,
        range_color=(filtered_df[selected_factor].min(), filtered_df[selected_factor].max())
    )

    # layout settings
    fig_factor.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
        ),
        height=700,
        margin={"r":0,"t":0,"l":0,"b":0},
    )

    # display the map
    st.plotly_chart(fig_factor, use_container_width=True)

# 3. more plots page with arrow navigation
elif menu == "More Plots":
    st.subheader("More Plots")

    # initialize session state for plot index if it doesn't exist
    if 'plot_index' not in st.session_state:
        st.session_state['plot_index'] = 0

    # create the list of available plots
    available_plots = ["Correlation Plot", "Average Happiness per Continent", "Top 10 Most Improved Countries"]

    # navigation buttons for cycling through the plots
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col1:
        # left arrow to go to the previous plot
        if st.button("⬅️"):
            st.session_state.plot_index = (st.session_state.plot_index - 1) % len(available_plots)
    
    with col3:
        # right arrow to go to the next plot
        if st.button("➡️"):
            st.session_state.plot_index = (st.session_state.plot_index + 1) % len(available_plots)
    
    # display current plot name as a subtitle
    current_plot = available_plots[st.session_state.plot_index]
    st.subheader(current_plot)

    # logic for displaying the current plot
    if current_plot == "Correlation Plot":
        st.write("Correlation of Happiness Score with Other Factors")
        # calculate correlation matrix between happiness score and other factors
        correlation_data = df[['Happiness Score', 'GDP per capita', 'Life expectancy', 'Freedom', 'Trust', 'Generosity']].corr()

        # plot the correlation matrix using seaborn heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_data, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    elif current_plot == "Average Happiness per Continent":
        st.write("Average Happiness Score per Continent Over Time")

        # calculate average happiness score per continent for each year
        avg_happiness_continent = df.groupby(['Year', 'Continent'])['Happiness Score'].mean().reset_index()

        # custom colors for continents
        continent_colors = {
            'Europe': "#fd7f6f",
            'Asia': "#7eb0d5",
            'Africa': "#b2e061",
            'North America': "#bd7ebe",
            'South America': "#ffb55a",
            'Oceania': "#ffee65"
        }

        # create a line plot using plotly for average happiness score per continent
        fig_line = px.line(
            avg_happiness_continent, 
            x='Year', 
            y='Happiness Score', 
            color='Continent',
            title="Average Happiness Score per Continent Over Time",
            color_discrete_map=continent_colors
        )

        # layout settings
        fig_line.update_layout(
            xaxis_title='Year',
            yaxis_title='Average Happiness Score',
            height=600,
            width=1000
        )

        # display the line plot
        st.plotly_chart(fig_line, use_container_width=True)

    elif current_plot == "Top 10 Most Improved Countries":
        st.write("Top 10 Most Improved Countries in Happiness Score (2015–2019)")

        # filter the dataset for the first (2015) and last (2019) years
        df_2015 = df[df['Year'] == 2015][['Country', 'Happiness Score']].rename(columns={'Happiness Score': 'Happiness Score 2015'})
        df_2019 = df[df['Year'] == 2019][['Country', 'Happiness Score']].rename(columns={'Happiness Score': 'Happiness Score 2019'})

        # merge the two years to calculate the difference
        df_improvement = pd.merge(df_2015, df_2019, on='Country')
        df_improvement['Score Change'] = df_improvement['Happiness Score 2019'] - df_improvement['Happiness Score 2015']

        # sort by the most improved countries and select the top 10
        top_10_improved = df_improvement.sort_values(by='Score Change', ascending=False).head(10)

        # plot the top 10 most improved countries using a bar chart
        fig_top_10 = px.bar(
            top_10_improved, 
            x='Country', 
            y='Score Change', 
            title="Top 10 Most Improved Countries in Happiness Score (2015–2019)", 
            labels={'Score Change': 'Change in Happiness Score'},
            color='Score Change',
            color_continuous_scale='Blues'
        )

        # layout settings
        fig_top_10.update_layout(
            xaxis_title='Country',
            yaxis_title='Change in Happiness Score',
            height=500,
            width=900
        )

        # display the bar chart
        st.plotly_chart(fig_top_10, use_container_width=True)

# 4. about the dataset page
elif menu == "About the Dataset":
    st.subheader("About the World Happiness Dataset")
    st.markdown("""
    The World Happiness Report is a landmark survey of the state of global happiness and is based on happiness scores taken from individual self-reports, with other factors collected including 
    GDP per capita, social support (Family), healthy life expectancy, freedom to make life choices, 
    generosity, and perceptions of corruption (Trust). 

    Data from 2015–2019 has been used for this visualization.
    """)

    # display a preview of the dataset
    st.write("Here is a preview of the dataset:")
    st.dataframe(df.head(10))

