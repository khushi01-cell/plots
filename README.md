# DXF Plot Analyzer

A comprehensive Python tool for analyzing DXF files containing plot data, specifically designed for land survey and property mapping applications.

## 🎯 Overview

The `plot_analyzer.py` script analyzes DXF files to extract and calculate areas for original and final plots, identify unassigned plots, check for pending areas, and generate detailed reports in both square meters and square yards.

## ✨ Features

### Core Analysis Functions
- **Original Plots Analysis**: Extract and analyze green-colored entities (Color 3)
- **Final Plots Analysis**: Extract and analyze red-colored entities (Color 1)
- **Unassigned Plots Detection**: Find plots with survey numbers but no plot numbers
- **Area Pending Analysis**: Compare original vs final total areas
- **Text Entity Analysis**: Extract plot numbers from DXF text entities

### Area Calculations
- **Accurate Area Calculation**: Using shoelace formula for polygons
- **Perimeter Calculation**: For all plot boundaries
- **Unit Conversion**: Automatic conversion between drawing units, square meters, and square yards
- **Scale Factor Support**: Configurable scale factor (default: 1CM = 20M)

### Output Formats
- **Console Reports**: Detailed analysis with color-coded output
- **CSV Reports**: Structured data export in Table 1-4 format
- **Detailed Area Reports**: Individual plot breakdowns
- **Summary Statistics**: Totals, averages, and distributions

## 📋 Requirements

### Python Dependencies
```
ezdxf>=1.0.0
numpy>=1.21.0
```

### Installation
```bash
# Install required packages
pip install ezdxf numpy

# Or install from requirements.txt
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Usage
```bash
python plot_analyzer.py
```

### Expected DXF File Structure
- **File Name**: `CTP01(LALDARWAJA)FINAL.dxf`
- **Original Plots**: Green color (Color 3)
- **Final Plots**: Red color (Color 1)
- **Scale Factor**: 1CM = 20M (1:2000 scale)

### Configuration
The script uses these default settings:
```python
# Scale factor for unit conversion
scale_factor = 20.0  # 1CM = 20M

# Color definitions
ORIGINAL_COLOR = 3   # Green for original plots
FINAL_COLOR = 1      # Red for final plots
```

## 📊 Output

### Console Output
The script provides comprehensive console output including:

1. **Text Entity Analysis**: All text entities and potential plot numbers
2. **Original Plots Analysis**: 
   - Total entities found
   - Total area in square meters
   - Plot numbers identified
3. **Final Plots Analysis**: Same metrics for final plots
4. **Unassigned Plots**: Plots with survey numbers but no plot numbers
5. **Area Pending**: Comparison between original and final areas
6. **Detailed Area Report**: Individual plot breakdowns in square yards

### CSV Output
Generates `plot_analysis_report.csv` with columns:
- Case No.
- NAME OF OWNER
- Tenure
- R.S.NO.
- ORIGINAL PLOT
- Area in (Sq.Yds.)
- Area in (Sq.m)
- Perimeter (yd)
- FINAL PLOT
- Area in (Sq.Yds.)
- Area in (Sq.m)
- Perimeter (yd)
- Type
- Layer
- REMARKS

## 🔧 Key Functions

### Main Analysis Functions
- `original_plots()`: Analyze green-colored plot entities
- `final_plots()`: Analyze red-colored plot entities
- `check_unassigned_plots_with_survey()`: Find unassigned plots
- `check_area_pending()`: Compare original vs final areas
- `analyze_text_entities()`: Extract plot numbers from text

### Utility Functions
- `_calculate_entity_area_perimeter()`: Calculate area and perimeter
- `convert_to_square_meters()`: Convert raw DXF units to square meters
- `convert_to_square_yards()`: Convert to square yards
- `_is_plot_number()`: Validate plot number patterns
- `_clean_plot_number()`: Standardize plot number format

## 📏 Unit Conversions

The script handles multiple unit conversions:
- **Raw DXF Units** → **Square Meters**: `area_raw × (scale_factor)²`
- **Square Meters** → **Square Yards**: `sq_meters × 1.19599`
- **Raw DXF Units** → **Meters**: `distance_raw × scale_factor`
- **Meters** → **Yards**: `meters × 1.09361`

## 🎨 Color Coding

The script identifies plots by AutoCAD color codes:
- **Color 1 (Red)**: Final plots
- **Color 3 (Green)**: Original plots
- **Color 5 (Blue)**: Other plot types
- **Color 6 (Magenta)**: Additional plots

## 📁 File Structure

```
cal/
├── plot_analyzer.py          # Main analysis script
├── CTP01(LALDARWAJA)FINAL.dxf # DXF file to analyze
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── plot_analysis_report.csv # Generated report
├── Table 1.csv             # Reference data
├── Table 2.csv             # Reference data
├── Table 3.csv             # Reference data
└── Table 4.csv             # Reference data
```

## 🔍 Plot Number Detection

The script can detect plot numbers from:
- **TEXT entities**: Direct text labels
- **MTEXT entities**: Multi-line text
- **INSERT entities**: Block references
- **Layer names**: Layer-based plot numbers
- **Block definitions**: Block name patterns

### Supported Plot Number Formats
- Simple numbers: `1`, `2`, `30`
- Alphanumeric: `1A`, `2B`, `30A`
- Fractions: `2/A`, `30/A`, `1/2`
- Ranges: `1-5`, `A1-A5`
- Survey numbers: `R.S.1`, `SURVEY 30`

## ⚠️ Troubleshooting

### Common Issues
1. **File Not Found**: Ensure `CTP01(LALDARWAJA)FINAL.dxf` is in the same directory
2. **No Plots Found**: Check if plots use the expected colors (1=Red, 3=Green)
3. **Area Calculation Errors**: Verify DXF file integrity and entity types
4. **Scale Factor Issues**: Adjust `scale_factor` if measurements seem incorrect

### Debug Mode
The script includes extensive debug output to help identify issues:
- Entity type breakdowns
- Color and layer analysis
- Text entity content
- Plot number detection details

## 📈 Example Output

```
🔍 FINDING ORIGINAL PLOTS (Color 3 - Green)...
📊 ORIGINAL PLOTS FOUND: 12
📏 Total Area: 15,432.67 sq yards (12,900.00 sq meters)
📐 Total Perimeter: 1,234.56 yards (1,128.00 meters)
📊 Average Area: 1,286.06 sq yards per plot

🏷️  Plot numbers found: ['1', '2', '2/A', '3', '4', '5', '5/A', '6', '7', '24', '35']
```

## 🤝 Contributing

To modify or extend the script:
1. Update color definitions for different plot types
2. Modify scale factor for different drawing scales
3. Add new plot number detection patterns
4. Extend CSV output format
5. Add new analysis functions

## 📄 License

This tool is designed for land survey and property mapping applications. Use responsibly and verify all calculations for critical applications.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify DXF file structure
3. Review console output for error messages
4. Ensure all dependencies are installed

---

**Note**: This tool is specifically designed for DXF files with the structure and color coding described above. Adjustments may be needed for different DXF file formats or color schemes. 