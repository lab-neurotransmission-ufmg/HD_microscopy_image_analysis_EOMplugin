from scipy.stats import ttest_ind, mannwhitneyu

def calculate_stats(data, group1, group2):
    """Calculate statistical significance between groups."""
    group1_data = data[data['Group'] == group1]
    group2_data = data[data['Group'] == group2]
    
    t_stat, t_p = ttest_ind(group1_data, group2_data)
    u_stat, u_p = mannwhitneyu(group1_data, group2_data)
    
    print(f"T-test: p = {t_p:.4f}")
    print(f"Mann-Whitney U: p = {u_p:.4f}")