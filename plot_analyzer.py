import ezdxf
import numpy as np
import re
from typing import Dict, List, Tuple, Optional

class PlotAnalyzer:
    def __init__(self, dxf_file_path: str):
        """Initialize the plot analyzer with DXF file path."""
        self.dxf_file_path = dxf_file_path
        self.doc = None
        self.msp = None
        self.scale_factor = 20.0  # 1CM = 20M conversion factor
        
        # Color definitions
        self.ORIGINAL_COLOR = 3  # Green for original plots
        self.FINAL_COLOR = 1     # Red for final plots
        
        # Load the DXF file
        self.load_dxf_file()
    
    def load_dxf_file(self):
        """Load and validate the DXF file."""
        try:
            print(f"📁 Loading DXF file: {self.dxf_file_path}")
            self.doc = ezdxf.readfile(self.dxf_file_path)
            self.msp = self.doc.modelspace()
            print(f"✅ Successfully loaded DXF file with {len(self.msp)} entities")
        except FileNotFoundError:
            print(f"❌ Error: File '{self.dxf_file_path}' not found!")
            raise
        except Exception as e:
            print(f"❌ Error loading DXF file: {e}")
            raise
    
    def original_plots(self) -> Dict:
        """
        Extract and analyze original plots (green colored entities).
        Returns plot numbers, areas, and details.
        """
        print("\n🔍 Analyzing Original Plots...")
        
        original_entities = []
        plot_numbers = []
        total_area = 0.0
        total_perimeter = 0.0
        
        # Find all green-colored entities (original plots)
        for entity in self.msp:
            color = getattr(entity.dxf, 'color', 7)
            if color == self.ORIGINAL_COLOR:
                entity_type = entity.dxftype()
                if entity_type in ['LWPOLYLINE', 'POLYLINE', 'CIRCLE', 'RECTANGLE']:
                    area, perimeter = self._calculate_entity_area_perimeter(entity)
                    total_area += area
                    total_perimeter += perimeter
                    
                    original_entities.append({
                        'type': entity_type,
                        'layer': entity.dxf.layer,
                        'area': area,
                        'perimeter': perimeter,
                        'center': self._get_entity_center(entity),
                        'entity': entity
                    })
        
        # Find plot numbers associated with original plots
        plot_numbers = self._find_plot_numbers_near_entities(original_entities)
        
        # Assign plot numbers to individual entities
        for i, entity_data in enumerate(original_entities):
            if i < len(plot_numbers):
                entity_data['plot_number'] = plot_numbers[i]
            else:
                entity_data['plot_number'] = f"Plot_{i+1}"
        
        # Convert to square meters
        area_sq_meters = total_area * (self.scale_factor ** 2)
        perimeter_meters = total_perimeter * self.scale_factor
        
        result = {
            'total_entities': len(original_entities),
            'total_area_sq_meters': area_sq_meters,
            'total_perimeter_meters': perimeter_meters,
            'plot_numbers': plot_numbers,
            'entities': original_entities
        }
        
        print(f"   📊 Found {len(original_entities)} original plot entities")
        print(f"   📏 Total area: {area_sq_meters:.2f} sq meters")
        print(f"   📐 Total perimeter: {perimeter_meters:.2f} meters")
        print(f"   🏷️  Plot numbers found: {plot_numbers}")
        
        return result
    
    def final_plots(self) -> Dict:
        """
        Extract and analyze final plots (red colored entities).
        Returns plot numbers, areas, and details.
        """
        print("\n🔍 Analyzing Final Plots...")
        
        final_entities = []
        plot_numbers = []
        total_area = 0.0
        total_perimeter = 0.0
        
        # Find all red-colored entities (final plots)
        for entity in self.msp:
            color = getattr(entity.dxf, 'color', 7)
            if color == self.FINAL_COLOR:
                entity_type = entity.dxftype()
                if entity_type in ['LWPOLYLINE', 'POLYLINE', 'CIRCLE', 'RECTANGLE']:
                    area, perimeter = self._calculate_entity_area_perimeter(entity)
                    total_area += area
                    total_perimeter += perimeter
                    
                    final_entities.append({
                        'type': entity_type,
                        'layer': entity.dxf.layer,
                        'area': area,
                        'perimeter': perimeter,
                        'center': self._get_entity_center(entity),
                        'entity': entity
                    })
        
        # Find plot numbers associated with final plots
        plot_numbers = self._find_plot_numbers_near_entities(final_entities)
        
        # Assign plot numbers to individual entities
        for i, entity_data in enumerate(final_entities):
            if i < len(plot_numbers):
                entity_data['plot_number'] = plot_numbers[i]
            else:
                entity_data['plot_number'] = f"Plot_{i+1}"
        
        # Convert to square meters
        area_sq_meters = total_area * (self.scale_factor ** 2)
        perimeter_meters = total_perimeter * self.scale_factor
        
        result = {
            'total_entities': len(final_entities),
            'total_area_sq_meters': area_sq_meters,
            'total_perimeter_meters': perimeter_meters,
            'plot_numbers': plot_numbers,
            'entities': final_entities
        }
        
        print(f"   📊 Found {len(final_entities)} final plot entities")
        print(f"   📏 Total area: {area_sq_meters:.2f} sq meters")
        print(f"   📐 Total perimeter: {perimeter_meters:.2f} meters")
        print(f"   🏷️  Plot numbers found: {plot_numbers}")
        
        return result
    
    def check_unassigned_plots_with_survey(self) -> Dict:
        """
        Check for plots that are not assigned but have survey numbers.
        Returns unassigned plots with their survey numbers.
        """
        print("\n🔍 Checking Unassigned Plots with Survey Numbers...")
        
        # Get all plot entities (both original and final)
        all_plot_entities = []
        for entity in self.msp:
            color = getattr(entity.dxf, 'color', 7)
            if color in [self.ORIGINAL_COLOR, self.FINAL_COLOR]:
                entity_type = entity.dxftype()
                if entity_type in ['LWPOLYLINE', 'POLYLINE', 'CIRCLE', 'RECTANGLE']:
                    all_plot_entities.append({
                        'type': entity_type,
                        'layer': entity.dxf.layer,
                        'color': color,
                        'center': self._get_entity_center(entity),
                        'entity': entity
                    })
        
        # Get all text entities
        text_entities = []
        for entity in self.msp:
            if entity.dxftype() in ['TEXT', 'MTEXT']:
                text_content = ""
                if entity.dxftype() == 'TEXT':
                    text_content = getattr(entity.dxf, 'text', '').strip()
                elif entity.dxftype() == 'MTEXT':
                    text_content = getattr(entity.dxf, 'text', '').strip()
                
                if text_content:
                    text_entities.append({
                        'content': text_content,
                        'layer': entity.dxf.layer,
                        'position': (entity.dxf.insert.x, entity.dxf.insert.y),
                        'entity': entity
                    })
        
        # Find survey numbers
        survey_numbers = []
        for text in text_entities:
            if self._is_survey_number(text['content']):
                survey_numbers.append(text)
        
        # Check for unassigned plots (no plot number nearby)
        unassigned_plots = []
        tolerance = 50.0  # Distance tolerance
        
        for plot_entity in all_plot_entities:
            plot_center = plot_entity['center']
            has_plot_number = False
            has_survey_number = False
            nearby_survey = None
            
            # Check for nearby plot numbers
            for text in text_entities:
                if self._is_plot_number(text['content']):
                    distance = self._calculate_distance(plot_center, text['position'])
                    if distance <= tolerance:
                        has_plot_number = True
                        break
            
            # Check for nearby survey numbers
            for survey in survey_numbers:
                distance = self._calculate_distance(plot_center, survey['position'])
                if distance <= tolerance:
                    has_survey_number = True
                    nearby_survey = survey
                    break
            
            # If no plot number but has survey number
            if not has_plot_number and has_survey_number:
                area, perimeter = self._calculate_entity_area_perimeter(plot_entity['entity'])
                unassigned_plots.append({
                    'type': plot_entity['type'],
                    'layer': plot_entity['layer'],
                    'color': plot_entity['color'],
                    'area_sq_meters': area * (self.scale_factor ** 2),
                    'perimeter_meters': perimeter * self.scale_factor,
                    'center': plot_center,
                    'survey_number': nearby_survey['content'],
                    'survey_layer': nearby_survey['layer']
                })
        
        result = {
            'total_unassigned_with_survey': len(unassigned_plots),
            'total_survey_numbers_found': len(survey_numbers),
            'unassigned_plots': unassigned_plots,
            'survey_numbers': [s['content'] for s in survey_numbers]
        }
        
        print(f"   📊 Found {len(unassigned_plots)} unassigned plots with survey numbers")
        print(f"   🏷️  Total survey numbers found: {len(survey_numbers)}")
        print(f"   📋 Survey numbers: {[s['content'] for s in survey_numbers[:10]]}")
        
        return result
    
    def check_area_pending(self, original_result: Dict, final_result: Dict) -> Dict:
        """
        Compare original and final plot areas to find pending/missing areas.
        """
        print("\n🔍 Checking Area Pending...")
        
        original_area = original_result['total_area_sq_meters']
        final_area = final_result['total_area_sq_meters']
        
        area_difference = abs(original_area - final_area)
        if original_area > 0:
            percentage_difference = (area_difference / original_area) * 100
        else:
            percentage_difference = 0
        
        result = {
            'original_area_sq_meters': original_area,
            'final_area_sq_meters': final_area,
            'area_difference_sq_meters': area_difference,
            'percentage_difference': percentage_difference,
            'has_pending_area': area_difference > 0.01  # 0.01 sq meters tolerance
        }
        
        print(f"   📏 Original area: {original_area:.2f} sq meters")
        print(f"   📏 Final area: {final_area:.2f} sq meters")
        print(f"   📊 Area difference: {area_difference:.2f} sq meters")
        print(f"   📈 Percentage difference: {percentage_difference:.2f}%")
        
        if result['has_pending_area']:
            print(f"   ⚠️  Pending area detected!")
        else:
            print(f"   ✅ No pending area detected")
        
        return result
    
    def _find_plot_numbers_near_entities(self, entities: List[Dict]) -> List[str]:
        """Find plot numbers near the given entities."""
        plot_numbers = []
        tolerance = 100.0  # Increased tolerance
        
        for entity in entities:
            center = entity['center']
            
            # Check all text entities for plot numbers
            for text_entity in self.msp:
                if text_entity.dxftype() in ['TEXT', 'MTEXT']:
                    text_content = ""
                    if text_entity.dxftype() == 'TEXT':
                        text_content = getattr(text_entity.dxf, 'text', '').strip()
                    elif text_entity.dxftype() == 'MTEXT':
                        text_content = getattr(text_entity.dxf, 'text', '').strip()
                    
                    if text_content:
                        # Check if it's a plot number
                        if self._is_plot_number(text_content) or self._is_simple_number(text_content):
                            text_pos = (text_entity.dxf.insert.x, text_entity.dxf.insert.y)
                            distance = self._calculate_distance(center, text_pos)
                            
                            if distance <= tolerance:
                                # Clean and format the plot number
                                plot_number = self._clean_plot_number(text_content)
                                plot_numbers.append(plot_number)
        
        return sorted(set(plot_numbers), key=self._extract_numeric_plot_number)
    
    def _is_plot_number(self, text: str) -> bool:
        """Check if text represents a plot number."""
        text = text.strip().upper()
        
        patterns = [
            r'^PLOT\s*#?\s*(\d+[A-Z]?/?\d*)$',  # PLOT 1, PLOT 2A, PLOT 30/A
            r'^(\d+[A-Z]?/?\d*)$',              # 1, 2A, 30/A, 2/A
            r'^P\s*(\d+[A-Z]?/?\d*)$',          # P1, P2A, P30/A
            r'^NO\s*\.?\s*(\d+[A-Z]?/?\d*)$',   # NO 1, NO. 1, NO 30/A
            r'^(\d+/\d+)$',                      # 2/A, 30/A, 1/2
            r'^(\d+[A-Z]/\d+)$',                 # 2A/1, 30A/2
        ]
        
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        
        return False
    
    def _is_simple_number(self, text: str) -> bool:
        """Check if text is a simple number that could be a plot number."""
        text = text.strip()
        
        # Check for simple numeric patterns
        patterns = [
            r'^\d+$',                    # 1, 2, 30, 100
            r'^\d+[A-Z]$',              # 1A, 2B, 30A
            r'^\d+/\d+$',               # 1/2, 2/A, 30/A
            r'^\d+[A-Z]/\d+$',          # 1A/2, 2B/A
            r'^[A-Z]\d+$',              # A1, B2, C30
        ]
        
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        
        return False
    
    def _clean_plot_number(self, text: str) -> str:
        """Clean and format plot number to standard format."""
        text = text.strip().upper()
        
        # Remove common prefixes
        prefixes_to_remove = ['PLOT', 'P', 'NO', 'NO.']
        for prefix in prefixes_to_remove:
            if text.startswith(prefix):
                text = text[len(prefix):].strip()
        
        # Remove extra spaces and special characters
        text = re.sub(r'\s+', '', text)  # Remove spaces
        text = re.sub(r'[#\.]', '', text)  # Remove # and .
        
        return text
    
    def _extract_numeric_plot_number(self, plot_number: str) -> int:
        """Extract numeric part from plot number for sorting."""
        if not plot_number:
            return 999999
        
        # Extract first number from plot number
        match = re.search(r'(\d+)', plot_number)
        if match:
            return int(match.group(1))
        return 999999
    
    def _is_survey_number(self, text: str) -> bool:
        """Check if text represents a survey number."""
        text = text.strip().upper()
        
        # Patterns for survey numbers
        patterns = [
            r'^SURVEY\s*NO\s*\.?\s*(\d+[A-Z]?/?\d*)$',  # SURVEY NO 1, SURVEY NO. 1
            r'^S\s*\.?\s*NO\s*\.?\s*(\d+[A-Z]?/?\d*)$', # S NO 1, S. NO. 1
            r'^SURVEY\s*(\d+[A-Z]?/?\d*)$',             # SURVEY 1, SURVEY 30/A
            r'^(\d+[A-Z]?/?\d*)\s*SURVEY$',             # 1 SURVEY, 30/A SURVEY
        ]
        
        for pattern in patterns:
            if re.match(pattern, text):
                return True
        
        return False
    
    def _calculate_entity_area_perimeter(self, entity) -> Tuple[float, float]:
        """Calculate area and perimeter of an entity."""
        try:
            entity_type = entity.dxftype()
            
            if entity_type in ['LWPOLYLINE', 'POLYLINE']:
                return self._calculate_polygon_area_perimeter(entity)
            elif entity_type == 'CIRCLE':
                radius = entity.dxf.radius
                area = np.pi * radius * radius
                perimeter = 2 * np.pi * radius
                return area, perimeter
            elif entity_type == 'RECTANGLE':
                # For rectangle, we need to get the width and height
                # This is a simplified calculation
                center = self._get_entity_center(entity)
                area = 100.0  # Default area
                perimeter = 40.0  # Default perimeter
                return area, perimeter
            else:
                return 0.0, 0.0
                
        except Exception as e:
            print(f"Warning: Could not calculate area/perimeter for {entity_type}: {e}")
            return 0.0, 0.0
    
    def analyze_text_entities(self) -> Dict:
        """
        Analyze all text entities to find potential plot numbers.
        """
        print("\n🔍 Analyzing all text entities for plot numbers...")
        
        all_text_entities = []
        potential_plot_numbers = []
        
        for entity in self.msp:
            if entity.dxftype() in ['TEXT', 'MTEXT']:
                text_content = ""
                if entity.dxftype() == 'TEXT':
                    text_content = getattr(entity.dxf, 'text', '').strip()
                elif entity.dxftype() == 'MTEXT':
                    text_content = getattr(entity.dxf, 'text', '').strip()
                
                if text_content:
                    all_text_entities.append({
                        'content': text_content,
                        'layer': entity.dxf.layer,
                        'color': getattr(entity.dxf, 'color', 7),
                        'position': (entity.dxf.insert.x, entity.dxf.insert.y)
                    })
                    
                    # Check if this could be a plot number
                    if self._is_plot_number(text_content) or self._is_simple_number(text_content):
                        potential_plot_numbers.append({
                            'content': text_content,
                            'layer': entity.dxf.layer,
                            'color': getattr(entity.dxf, 'color', 7),
                            'position': (entity.dxf.insert.x, entity.dxf.insert.y),
                            'cleaned': self._clean_plot_number(text_content)
                        })
        
        result = {
            'total_text_entities': len(all_text_entities),
            'potential_plot_numbers': potential_plot_numbers,
            'all_text_entities': all_text_entities
        }
        
        print(f"   📝 Total text entities: {len(all_text_entities)}")
        print(f"   🏷️  Potential plot numbers found: {len(potential_plot_numbers)}")
        
        # Show some potential plot numbers
        if potential_plot_numbers:
            print(f"   📋 Sample plot numbers: {[p['cleaned'] for p in potential_plot_numbers[:10]]}")
            print(f"   📋 All potential plot numbers: {[p['cleaned'] for p in potential_plot_numbers]}")
        else:
            print(f"   ❌ No plot numbers found! Showing all text entities:")
            for i, text in enumerate(all_text_entities[:20]):  # Show first 20
                print(f"      {i+1}. '{text['content']}' on layer '{text['layer']}'")
        
        return result
    
    def _calculate_polygon_area_perimeter(self, entity) -> Tuple[float, float]:
        """Calculate area and perimeter of a polygon entity."""
        try:
            points = []
            
            if hasattr(entity, 'get_points'):
                points = list(entity.get_points())
            elif hasattr(entity, 'vertices'):
                points = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
            
            if len(points) < 3:
                return 0.0, 0.0
            
            # Calculate area using shoelace formula
            area = 0.0
            perimeter = 0.0
            
            for i in range(len(points)):
                j = (i + 1) % len(points)
                area += points[i][0] * points[j][1]
                area -= points[j][0] * points[i][1]
                
                # Calculate perimeter
                dx = points[j][0] - points[i][0]
                dy = points[j][1] - points[i][1]
                perimeter += np.sqrt(dx*dx + dy*dy)
            
            area = abs(area) / 2.0
            
            return area, perimeter
            
        except Exception as e:
            print(f"Warning: Could not calculate polygon area/perimeter: {e}")
            return 0.0, 0.0
    
    def _get_entity_center(self, entity) -> Tuple[float, float]:
        """Get the center point of an entity."""
        try:
            if entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
                points = []
                if hasattr(entity, 'get_points'):
                    points = list(entity.get_points())
                elif hasattr(entity, 'vertices'):
                    points = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
                
                if points:
                    x_coords = [p[0] for p in points]
                    y_coords = [p[1] for p in points]
                    return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))
                    
            elif entity.dxftype() == 'CIRCLE':
                return (entity.dxf.center.x, entity.dxf.center.y)
                
            elif entity.dxftype() == 'INSERT':
                return (entity.dxf.insert.x, entity.dxf.insert.y)
                
        except Exception:
            pass
        
        return (0.0, 0.0)
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate distance between two points."""
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return np.sqrt(dx*dx + dy*dy)
    
    def display_detailed_area_report(self, original_result: Dict, final_result: Dict) -> None:
        """
        Display a detailed area report for all plots in square meters.
        """
        print("\n" + "="*80)
        print("📋 DETAILED AREA REPORT (SQUARE METERS)")
        print("="*80)
        
        # Original plots table
        if original_result['entities']:
            print(f"\n🏷️  ORIGINAL PLOTS ({len(original_result['entities'])} plots):")
            print("-" * 120)
            print(f"{'Index':<6} {'Plot No.':<12} {'Area (sq m)':<15} {'Perimeter (m)':<15} {'Type':<12} {'Layer':<20}")
            print("-" * 120)
            
            for i, plot in enumerate(original_result['entities']):
                # Use actual plot number if available, otherwise use index
                plot_num = plot.get('plot_number', f"Plot_{i+1}")
                print(f"{i+1:<6} {plot_num:<12} {plot['area'] * (self.scale_factor ** 2):<15.2f} "
                      f"{plot['perimeter'] * self.scale_factor:<15.2f} {plot['type']:<12} {plot['layer']:<20}")
            
            print("-" * 120)
            print(f"TOTAL: {original_result['total_area_sq_meters']:.2f} sq meters")
        
        # Final plots table
        if final_result['entities']:
            print(f"\n🏷️  FINAL PLOTS ({len(final_result['entities'])} plots):")
            print("-" * 120)
            print(f"{'Index':<6} {'Plot No.':<12} {'Area (sq m)':<15} {'Perimeter (m)':<15} {'Type':<12} {'Layer':<20}")
            print("-" * 120)
            
            for i, plot in enumerate(final_result['entities']):
                # Use actual plot number if available, otherwise use index
                plot_num = plot.get('plot_number', f"Plot_{i+1}")
                print(f"{i+1:<6} {plot_num:<12} {plot['area'] * (self.scale_factor ** 2):<15.2f} "
                      f"{plot['perimeter'] * self.scale_factor:<15.2f} {plot['type']:<12} {plot['layer']:<20}")
            
            print("-" * 120)
            print(f"TOTAL: {final_result['total_area_sq_meters']:.2f} sq meters")
        
        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"   Original plots: {original_result['total_entities']} (Total area: {original_result['total_area_sq_meters']:.2f} sq meters)")
        print(f"   Final plots: {final_result['total_entities']} (Total area: {final_result['total_area_sq_meters']:.2f} sq meters)")
        print(f"   Total plots: {original_result['total_entities'] + final_result['total_entities']}")
        
        if original_result['total_area_sq_meters'] > 0 and final_result['total_area_sq_meters'] > 0:
            area_diff = abs(original_result['total_area_sq_meters'] - final_result['total_area_sq_meters'])
            print(f"   Area difference: {area_diff:.2f} sq meters")
        
        print(f"\n📏 Scale Factor: 1CM = {self.scale_factor}M (1:2000)")

def main():
    """
    Main function to load DXF file and call all analysis functions.
    """
    print("="*70)
    print("PLOT ANALYZER - DXF FILE ANALYSIS")
    print("="*70)
    
    # Initialize analyzer
    dxf_file = "CTP01(LALDARWAJA)FINAL.dxf"
    
    try:
        analyzer = PlotAnalyzer(dxf_file)
        
        print("\n🚀 Starting comprehensive plot analysis...")
        
        # 0. Analyze text entities to understand plot number detection
        print("\n" + "="*50)
        print("0. TEXT ENTITY ANALYSIS FOR PLOT NUMBERS")
        print("="*50)
        text_analysis = analyzer.analyze_text_entities()
        
        # 1. Analyze original plots
        print("\n" + "="*50)
        print("1. ORIGINAL PLOTS ANALYSIS")
        print("="*50)
        original_result = analyzer.original_plots()
        
        # 2. Analyze final plots
        print("\n" + "="*50)
        print("2. FINAL PLOTS ANALYSIS")
        print("="*50)
        final_result = analyzer.final_plots()
        
        # 3. Check unassigned plots with survey numbers
        print("\n" + "="*50)
        print("3. UNASSIGNED PLOTS WITH SURVEY NUMBERS")
        print("="*50)
        unassigned_result = analyzer.check_unassigned_plots_with_survey()
        
        # 4. Check area pending
        print("\n" + "="*50)
        print("4. AREA PENDING ANALYSIS")
        print("="*50)
        pending_result = analyzer.check_area_pending(original_result, final_result)
        
        # 5. Display detailed area report
        print("\n" + "="*50)
        print("5. DETAILED AREA REPORT")
        print("="*50)
        analyzer.display_detailed_area_report(original_result, final_result)
        
        # 6. Summary report
        print("\n" + "="*70)
        print("📋 COMPREHENSIVE SUMMARY REPORT")
        print("="*70)
        
        print(f"\n📊 Original Plots:")
        print(f"   • Total entities: {original_result['total_entities']}")
        print(f"   • Total area: {original_result['total_area_sq_meters']:.2f} sq meters")
        print(f"   • Plot numbers: {original_result['plot_numbers']}")
        
        print(f"\n📊 Final Plots:")
        print(f"   • Total entities: {final_result['total_entities']}")
        print(f"   • Total area: {final_result['total_area_sq_meters']:.2f} sq meters")
        print(f"   • Plot numbers: {final_result['plot_numbers']}")
        
        print(f"\n📊 Unassigned Plots with Survey Numbers:")
        print(f"   • Count: {unassigned_result['total_unassigned_with_survey']}")
        print(f"   • Survey numbers found: {unassigned_result['total_survey_numbers_found']}")
        
        print(f"\n📊 Area Pending:")
        print(f"   • Has pending area: {'Yes' if pending_result['has_pending_area'] else 'No'}")
        print(f"   • Area difference: {pending_result['area_difference_sq_meters']:.2f} sq meters")
        print(f"   • Percentage difference: {pending_result['percentage_difference']:.2f}%")
        
        print("\n" + "="*70)
        print("✅ ANALYSIS COMPLETE")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Please check if the DXF file exists and is valid.")

if __name__ == "__main__":
    main() 