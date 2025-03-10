# ======================================================
# WORKFLOW PIPELINE
# 1. INSTALL DEPENDENCIES: pip install pandas matplotlib seaborn scipy scikit-image openpyxl
# 2. REPLACE ALL FILE/FOLDER PATHS (Marked with 'REPLACE HERE')
# 3. RUN CODE SECTION-BY-SECTION (Follow the order below)
# ======================================================

# ====================== IMPORTS ======================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from scipy.stats import ttest_ind, mannwhitneyu, spearmanr
from skimage import io, measure, morphology, color

# ====================== DATA ANALYSIS (TABULAR DATA) ======================
# ------------ GENERAL SETTINGS (REPLACE HERE) ------------
# Define paths and group names
DATA_PATHS = {
    'fragmentation': 'path/to/fragmentation_data.xlsx',  # REPLACE: Fragmentation percentage data
    'colocalization': 'path/to/colocalization_data.xlsx',  # REPLACE: Colocalization index data
    'global_area': 'path/to/global_area_data.xlsx',  # REPLACE: Global muscle area data
    'fiber_types': 'path/to/fiber_type_data.xlsx'  # REPLACE: Muscle fiber type percentages
}

GROUP_NAMES = ['Group1', 'Group2']  # REPLACE: e.g., ['WT', 'BACHD']
CUSTOM_PALETTE = {"Group1": "#45a778", "Group2": "#3c6682"}  # REPLACE: Hex color codes

# ------------ DATA ANALYSIS FUNCTIONS ------------
def load_and_process_data(file_path, value_name):
    """Load Excel data and convert to long format for analysis."""
    data = pd.read_excel(file_path)
    data_long = data.melt(var_name='Group', value_name=value_name)
    return data_long

def plot_violin_box(data, y_label, titles):
    """Generate violin, box, and bar plots for comparative analysis."""
    # Violin plot (distribution)
    plt.figure(figsize=(8,6))
    sns.violinplot(x='Group', y=y_label, data=data, palette=CUSTOM_PALETTE)
    plt.title(titles[0], fontsize=14)
    plt.xlabel('Group', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.show()

    # Boxplot + individual data points
    plt.figure(figsize=(8,6))
    sns.boxplot(x='Group', y=y_label, data=data, palette=CUSTOM_PALETTE, width=0.5, fliersize=0)
    sns.stripplot(x='Group', y=y_label, data=data, color="black", alpha=0.5, jitter=True)
    plt.title(titles[1], fontsize=14)
    plt.xlabel('Group', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.show()

    # Bar plot (mean + standard deviation)
    mean_std = data.groupby('Group').agg(['mean', 'std']).reset_index()
    plt.figure(figsize=(8,6))
    sns.barplot(x='Group', y='mean', data=mean_std, palette=CUSTOM_PALETTE, ci='sd', capsize=0.1)
    plt.title(titles[2], fontsize=14)
    plt.xlabel('Group', fontsize=12)
    plt.ylabel(f'Mean {y_label}', fontsize=12)
    plt.show()

# ------------ FRAGMENTATION ANALYSIS ------------
frag_data = load_and_process_data(DATA_PATHS['fragmentation'], 'Fragmentation (%)')
plot_violin_box(frag_data, 'Fragmentation (%)', 
               ["Fragmentation Distribution", "Group Comparison", "Mean Fragmentation"])

# ------------ COLOCALIZATION ANALYSIS ------------
coloc_data = load_and_process_data(DATA_PATHS['colocalization'], 'Colocalization Index')
plot_violin_box(coloc_data, 'Colocalization Index', 
               ["Colocalization Distribution", "Group Comparison", "Mean Colocalization"])

# ------------ FIBER TYPE ANALYSIS ------------
# Custom analysis for fiber type percentages
df_fibers = pd.read_excel(DATA_PATHS['fiber_types'])
# REPLACE COLUMN NAMES based on your Excel sheet structure:
df_fibers.columns = ['FiberA_Group1', 'FiberA_Group2', 'FiberB_Group1', 'FiberB_Group2']

# Compare fiber types between groups
for fiber_type in ['FiberA', 'FiberB']:
    plt.figure(figsize=(8,6))
    sns.boxplot(data=df_fibers[[f'{fiber_type}_Group1', f'{fiber_type}_Group2']], palette=CUSTOM_PALETTE)
    plt.title(f"{fiber_type} Percentage Comparison", fontsize=14)
    plt.ylabel("Percentage (%)", fontsize=12)
    plt.show()

# ====================== IMAGE PROCESSING ======================
# ------------ IMAGE SETTINGS (REPLACE HERE) ------------
IMAGE_DIR = "path/to/image_folder"  # REPLACE: Folder containing PNG/JPG images
OUTPUT_DIR = "path/to/output_folder"  # REPLACE: Folder to save results

# ------------ IMAGE PROCESSING FUNCTIONS ------------
def interpolate_contour(contour, num_points=100):
    """Resample contour to fixed number of points for consistency."""
    t = np.linspace(0, 1, len(contour))
    t_new = np.linspace(0, 1, num_points)
    return np.column_stack([np.interp(t_new, t, contour[:, i]) for i in [0, 1]])

def detect_contours(image_path):
    """Detect magenta-colored contours in images using HSV color space."""
    image = io.imread(image_path)
    if image.shape[-1] == 4:  # Remove alpha channel if present
        image = image[..., :3]
    
    # Convert to HSV and create mask
    hsv = color.rgb2hsv(image)
    lower_mask = np.array([0.8, 0.3, 0.3])  # Adjust HSV range for magenta
    upper_mask = np.array([1.0, 1.0, 1.0])
    mask = np.all((hsv >= lower_mask) & (hsv <= upper_mask), axis=-1)
    
    # Clean up small objects
    mask = morphology.remove_small_objects(mask, min_size=50)
    contours = measure.find_contours(mask, level=0.8)
    return [interpolate_contour(cnt) for cnt in contours]

# ------------ PROCESS IMAGES ------------
for img_file in os.listdir(IMAGE_DIR):
    if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
        contours = detect_contours(os.path.join(IMAGE_DIR, img_file))
        
        # Plot and save results
        plt.figure(figsize=(6,6))
        for cnt in contours:
            plt.plot(cnt[:, 1], cnt[:, 0], 'r-', linewidth=1)
        plt.axis('off')
        plt.savefig(os.path.join(OUTPUT_DIR, f'processed_{img_file}'), bbox_inches='tight')
        plt.close()

# ====================== STATISTICAL ANALYSIS ======================
# Example: Compare fragmentation between groups
group1 = frag_data[frag_data['Group'] == 'Group1']['Fragmentation (%)'].dropna()
group2 = frag_data[frag_data['Group'] == 'Group2']['Fragmentation (%)'].dropna()

# T-test
t_stat, t_p = ttest_ind(group1, group2)
print(f"T-test: t = {t_stat:.2f}, p = {t_p:.4f}")

# Mann-Whitney U test
u_stat, u_p = mannwhitneyu(group1, group2)
print(f"Mann-Whitney U: U = {u_stat:.0f}, p = {u_p:.4f}")

# ====================== USAGE NOTES ======================
"""
1. DATA ANALYSIS:
   - Requires Excel files with columns named after groups (e.g., 'Group1', 'Group2')
   - Handles percentage data, colocalization indices, and fiber type percentages

2. IMAGE PROCESSING:
   - Detects magenta-colored regions in images
   - Saves processed images with contours to OUTPUT_DIR
   - Adjust HSV ranges in detect_contours() for different colors

3. STATISTICS:
   - Automatically compares first two groups
   - Includes parametric and non-parametric tests

4. CUSTOMIZATION:
   - All paths marked with 'REPLACE HERE' must be updated
   - Modify GROUP_NAMES and CUSTOM_PALETTE to match experimental groups
"""