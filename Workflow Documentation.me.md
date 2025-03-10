# Table.xlsx Data Analysis Pipeline

# Directory Structure
project/ 
├── data_analysis.py
├── image_processing.py
├── statistics.py
├── main.py
├── data/
│   ├── experimental_data.xlsx
│   └── control_data.xlsx
└── results/
    ├── plots/
    └── processed_images/


## Workflow Overview
1. **Data Preparation**
   - Place raw data files in `/data` folder
   - File naming must match `config.FILES`
   
2. **Configuration**
   - Edit `config.py`:
     - Set `DATA_DIR` path
     - Define experimental groups
     - Customize visualization parameters

3. **Run Analyses**
   ```bash
   # Install dependencies
   pip install pandas seaborn matplotlib scipy openpyxl
   
   # Execute analysis scripts
   python fragmentation_analysis.py
   python vesicle_analysis.py
   ```

4. **Outputs**
   - Visualizations saved to `/results/figures`
   - Statistical reports in `/results/stats`
   - Processed data in `/processed_data`

## Customization Guide
- **Change Groups**: Modify `GROUPS` in `config.py`
- **Adjust Colors**: Update `COLORS` dictionary
- **Set Axis Limits**: Modify `YLIM` values
- **Add New Analyses**: Create new scripts following existing patterns
