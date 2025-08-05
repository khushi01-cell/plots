# DXF File Processor

A comprehensive Python tool for processing DXF files with multiple functions for plotting, analysis, and area management.

## Features

- **Original Plots**: Generate plots showing all entities in the DXF file
- **Final Plots**: Create processed plots with color-coded areas (plot areas, pending areas, other entities)
- **Plot Assignment Checking**: Analyze and identify assigned, unassigned, and pending areas
- **Pending Area Analysis**: Detailed analysis of areas that need attention
- **Main Function**: Complete workflow that loads files and calls all functions

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install ezdxf matplotlib numpy
   ```

## Usage

### Command Line Mode

```bash
# Process a DXF file
python dxf_processor.py "path/to/your/file.dxf"

# Interactive mode (will prompt for file path)
python dxf_processor.py
```

### Programmatic Usage

```python
from dxf_processor import DXFProcessor

# Initialize processor
processor = DXFProcessor("path/to/your/file.dxf")

# Load DXF file
if processor.load_dxf_file():
    # Create original plots
    processor.create_original_plots("original_plot.png")
    
    # Create final plots
    processor.create_final_plots("final_plot.png")
    
    # Check plot assignments
    analysis = processor.check_plot_assignment()
    
    # Analyze pending areas
    pending_areas = processor.analyze_pending_areas()
```

## Functions Overview

### 1. `load_dxf_file()`
- **Purpose**: Load and read DXF file
- **Returns**: Boolean indicating success/failure
- **Features**: 
  - File existence validation
  - Entity extraction
  - Error handling

### 2. `create_original_plots(save_path=None)`
- **Purpose**: Generate plots showing all entities
- **Parameters**: 
  - `save_path`: Optional path to save plot image
- **Features**:
  - Plots all entities in blue
  - Equal aspect ratio
  - Grid overlay
  - High-resolution output

### 3. `create_final_plots(save_path=None)`
- **Purpose**: Create processed plots with color coding
- **Parameters**:
  - `save_path`: Optional path to save plot image
- **Features**:
  - Green: Plot areas
  - Red: Pending areas
  - Gray: Other entities
  - Legend included

### 4. `check_plot_assignment()`
- **Purpose**: Analyze plot assignments and identify issues
- **Returns**: Dictionary with analysis results
- **Features**:
  - Categorizes entities by type
  - Identifies unassigned areas
  - Provides summary statistics

### 5. `analyze_pending_areas()`
- **Purpose**: Detailed analysis of pending areas
- **Returns**: List of pending areas with details
- **Features**:
  - Area and perimeter calculations
  - Issue identification
  - Status tracking

### 6. `main()`
- **Purpose**: Complete workflow function
- **Features**:
  - Loads DXF file
  - Calls all processing functions
  - Generates summary report
  - Creates output plots

## Supported DXF Entities

- **Lines**: Straight line segments
- **Circles**: Circular entities
- **Arcs**: Arc segments
- **Polylines**: Connected line segments
- **Rectangles**: Rectangular shapes

## Area Classification

The processor automatically classifies areas based on layer names:

### Plot Areas
- Keywords: `plot`, `area`, `zone`, `lot`, `parcel`
- Color: Green in final plots

### Pending Areas
- Keywords: `pending`, `hold`, `reserved`, `temporary`
- Color: Red in final plots

### Unassigned Areas
- Keywords: `unassigned`, `unknown`, `undefined`
- Color: Gray in final plots

## Output Files

When running the main function, the following files are generated:

1. **`original_plot.png`**: Plot showing all entities
2. **`final_plot.png`**: Processed plot with color coding
3. **Console output**: Detailed analysis and summary

## Example Output

```
DXF File Processor
==================================================
Loading DXF file: example.dxf
Successfully loaded DXF file with 150 entities

1. Creating original plots...
Original plot saved to: original_plot.png

2. Creating final plots...
Final plot saved to: final_plot.png

3. Checking plot assignments...
Plot Assignment Analysis:
Total entities: 150
Plot areas: 25
Pending areas: 5
Unassigned areas: 3

4. Analyzing pending areas...
Found 5 pending areas

==================================================
PROCESSING SUMMARY
==================================================
DXF File: example.dxf
Total Entities: 150
Plot Areas: 25
Pending Areas: 5
Unassigned Areas: 3
Plots Generated: original_plot.png, final_plot.png

Processing completed successfully!
```

## Error Handling

The processor includes comprehensive error handling for:
- Missing DXF files
- Corrupted DXF files
- Unsupported entity types
- Plot generation issues
- File permission problems

## Customization

You can customize the processor by:
- Modifying layer name keywords in classification functions
- Adding new entity types to the plotting functions
- Extending area calculation algorithms
- Customizing plot styling and colors

## Troubleshooting

**Error: "No module named 'ezdxf'"**
- Install dependencies: `pip install -r requirements.txt`

**Error: "DXF file not found"**
- Check that the file path is correct and the file exists

**Error: "Could not plot entity"**
- Some entity types may not be supported
- Check the entity type and consider adding support

**Error: "Permission denied"**
- Make sure you have write permissions in the output directory 