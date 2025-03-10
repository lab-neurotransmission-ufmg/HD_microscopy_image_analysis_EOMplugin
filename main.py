from data_analysis import analyze_fragmentation, analyze_colocalization
from image_processing import process_images
from statistics import calculate_stats

# Config (REPLACE THESE VALUES)
DATA_PATHS = {
    'fragmentation': 'path/to/fragmentation_data.xlsx',
    'colocalization': 'path/to/colocalization_data.xlsx'
}
IMAGE_DIR = 'path/to/raw_images'
OUTPUT_DIR = 'path/to/processed_images'
GROUPS = ['WT', 'BACHD']
PALETTE = {"WT": "#45a778", "BACHD": "#3c6682"}

# Execute workflow
if __name__ == "__main__":
    # 1. Data Analysis
    analyze_fragmentation(DATA_PATHS['fragmentation'], GROUPS, PALETTE)
    analyze_colocalization(DATA_PATHS['colocalization'], GROUPS, PALETTE)
    
    # 2. Image Processing
    process_images(IMAGE_DIR, OUTPUT_DIR)
    
    # 3. Statistical Analysis
    df = pd.read_excel(DATA_PATHS['fragmentation'])
    calculate_stats(df, 'WT', 'BACHD')