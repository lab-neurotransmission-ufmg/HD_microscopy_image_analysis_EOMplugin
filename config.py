# ======================= CONFIGURE HERE =======================
# Set your data directory path (absolute/relative)
DATA_DIR = "path/to/your/data_folder"  # <<< REQUIRED!

# Input file names (must exist in DATA_DIR)
FILES = {
    'study_object_1': 'study_object_1_data_table.xlsx',
    'study_object_2': 'study_object_2_data_table.xlsx',
    'study_object_3': 'study_object_3_data_table.xlsx',
    # Add all required .xlsx files 
}

# Experimental groups (rename according to your study)
GROUPS = {
    'control': 'WT',          # Control group name
    'experimental': 'GROUP_1'   # Experimental group name
}

# Visualization parameters  (insert the color RGB number after the group name)
COLORS = {
    'control': '#45a778', 
    'experimental': '#3c6682',
    'other': '#447fa6'
}

# Analysis parameters
YLIM = (0, 100)  # Y-axis limits for plots (must be adequated to your study maximum value)
# ==============================================================