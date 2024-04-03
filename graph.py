import matplotlib.pyplot as plt
import seaborn as sns
from database import Profile, Overall_Stats, All_Time_Ranked_Stats


# Grabs data from Overall_Stats collection and creates a Bar chart for Overall Kills per Profile
def overall_kills_bar():
    sns.set_style('dark')
    palette = sns.color_palette('pastel')
    all_profiles = Overall_Stats.get_overall_stats()
    profile_names = [profile.get('profile_name', 'unknown') for profile in all_profiles]
    overall_kills_data = [int(profile.get('overall_kills', '0').replace(',', '')) for profile in all_profiles]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(profile_names, overall_kills_data, color=palette)
    plt.title('Overall Kills for Each Profile')
    plt.xlabel('Profiles')
    plt.ylabel('Overall Kills')
    plt.xticks(rotation=90)
    plt.ylim(bottom=0, top=max(overall_kills_data) + 2000)

    # Add text labels on top of each bar
    for bar, overall_kills in zip(bars, overall_kills_data):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), overall_kills,
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


# Grabs data from Overall_Stats collection and creates a bar chart of Overall Wins per Profile
def overall_wins_bar():
    palette = sns.color_palette('tab10')
    all_profiles = Overall_Stats.get_overall_stats()
    profile_names = [profile.get('profile_name', 'unknown') for profile in all_profiles]
    overall_wins_data = [int(profile.get('overall_wins', '0').replace(',', '')) for profile in all_profiles]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(profile_names, overall_wins_data, color=palette)
    plt.title('Overall Wins for Each Profile')
    plt.xlabel('Profiles')
    plt.ylabel('Overall Wins')
    plt.xticks(rotation=90)
    plt.ylim(bottom=0, top=max(overall_wins_data) + 200)

    # Add text labels on top of each bar
    for bar, overall_wins in zip(bars, overall_wins_data):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), overall_wins,
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


# Grabs data from Overall_Stats collection and creates a bar chart of Overall K/D per Profile
def overall_k_d_bar():
    palette = sns.color_palette('deep')
    all_profiles = Overall_Stats.get_overall_stats()
    profile_names = [profile.get('profile_name', 'unknown') for profile in all_profiles]
    overall_k_d_data = [float(profile.get('overall_k_d', '0')) for profile in all_profiles]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(profile_names, overall_k_d_data, color=palette)
    plt.title('Overall K/D for Each Profile')
    plt.xlabel('Profiles')
    plt.ylabel('Overall K/D')
    plt.xticks(rotation=90)
    plt.ylim(bottom=0, top=max(overall_k_d_data) + 1)

    # Add text labels on top of each bar
    for bar, overall_k_d in zip(bars, overall_k_d_data):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), overall_k_d,
                 ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


# Grabs data from Overall_Stats collection and creates four bar charts for each category comparing Profiles
def overall_stats_bar():
    sns.set_style('darkgrid')
    palette1 = sns.color_palette('cubehelix')
    palette2 = sns.color_palette('rocket')
    palette3 = sns.color_palette('flare_r')
    palette4 = sns.color_palette('viridis')
    all_profiles = Overall_Stats.get_overall_stats()

    # Initialize lists to store values for each profile
    profile_names = []
    overall_wins = []
    overall_win_pct = []
    overall_kills = []
    overall_k_d = []

    # Extract values for each profile
    for profile in all_profiles:
        profile_names.append(profile.get('profile_name', 'Unknown'))
        overall_wins.append(int(profile.get('overall_wins', '0').replace(',', '')))
        overall_win_pct.append(float(profile.get('overall_win_pct', '0')))
        overall_kills.append(int(profile.get('overall_kills', '0').replace(',', '')))
        overall_k_d.append(float(profile.get('overall_k_d', '0')))

    # Create subplots for each value
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Plot overall wins
    axs[0, 0].bar(profile_names, overall_wins, color=palette1)
    axs[0, 0].set_title('Overall Wins')
    axs[0, 0].tick_params(axis='x', rotation=90)

    # Plot overall win percentage
    axs[0, 1].bar(profile_names, overall_win_pct, color=palette2)
    axs[0, 1].set_title('Overall Win Percentage')
    axs[0, 1].tick_params(axis='x', rotation=90)

    # Plot overall kills
    axs[1, 0].bar(profile_names, overall_kills, color=palette3)
    axs[1, 0].set_title('Overall Kills')
    axs[1, 0].tick_params(axis='x', rotation=90)

    # Plot overall kill/death ratio
    axs[1, 1].bar(profile_names, overall_k_d, color=palette4)
    axs[1, 1].set_title('Overall Kill/Death Ratio')
    axs[1, 1].tick_params(axis='x', rotation=90)

    # Adjust layout
    plt.tight_layout()

    # Show plot
    plt.show()
