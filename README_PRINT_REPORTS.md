# Print-Friendly Report Generator

This feature provides a comprehensive print-friendly report generation system for the Deep Learning Specialization course repository.

## Overview

The print-friendly report generator creates HTML reports that summarize the entire course content, including:
- Course structure and organization
- Assignment details and progress
- Notebook analysis and metadata
- Print-optimized formatting and styling

## Features

### 📊 Comprehensive Course Analysis
- Automatically scans all courses, weeks, and assignments
- Extracts notebook titles and descriptions
- Counts cells and identifies test files
- Provides detailed progress overview

### 🖨️ Print-Friendly Design
- Optimized CSS for both screen and print viewing
- Print-specific media queries for clean output
- Page break controls for better formatting
- Professional typography and layout

### 📋 Detailed Reports
- Course-by-course breakdown
- Assignment-level details
- Notebook metadata and descriptions
- Test file indicators
- Progress statistics

## Usage

### Basic Usage

Generate a complete course report:

```bash
python report_generator.py
```

This creates a `course_report.html` file in the current directory.

### Advanced Usage

Specify custom output file:

```bash
python report_generator.py -o my_report.html
```

Specify custom path to scan:

```bash
python report_generator.py -p /path/to/course/directory
```

### Command Line Options

- `-o, --output`: Output HTML file name (default: course_report.html)
- `-p, --path`: Base path to scan (default: current directory)
- `-h, --help`: Show help message

## Generated Report Structure

The generated HTML report includes:

1. **Header Section**
   - Course title and generation timestamp
   - Summary statistics (total courses, assignments)

2. **Course Sections**
   - Course number and title
   - Week-by-week breakdown
   - Assignment details

3. **Assignment Details**
   - Notebook information (title, description, cell count)
   - Python file listings
   - Test file indicators

4. **Print Features**
   - Print button for easy printing
   - Print-optimized styling
   - Professional layout

## Print Instructions

1. Open the generated HTML file in a web browser
2. Click the "🖨️ Print Report" button or use Ctrl+P (Cmd+P on Mac)
3. For best results:
   - Use landscape orientation
   - Enable background graphics
   - Select appropriate paper size

## File Structure

```
Deep_learning_specialization/
├── report_generator.py          # Main report generation script
├── test_report_generator.py     # Test suite
├── course_report.html          # Generated report (created on run)
└── README_PRINT_REPORTS.md     # This documentation
```

## Technical Details

### Dependencies
- Python 3.6+
- Standard library modules: `os`, `json`, `re`, `datetime`, `pathlib`, `argparse`

### Architecture
- **ReportGenerator Class**: Main class handling course analysis and report generation
- **Course Analysis**: Recursive directory scanning and notebook parsing
- **HTML Generation**: Template-based report creation with embedded CSS
- **Print Optimization**: CSS media queries and layout controls

### Key Methods
- `scan_courses()`: Discovers and analyzes course structure
- `analyze_notebook()`: Extracts notebook metadata and content
- `generate_html_report()`: Creates the final HTML report
- `_get_html_template()`: Provides the HTML template with print-friendly CSS

## Testing

Run the test suite to verify functionality:

```bash
python test_report_generator.py
```

The test suite includes:
- Initialization tests
- Course scanning validation
- HTML generation verification
- Notebook analysis testing
- Template validation

## Customization

### CSS Styling
The HTML template includes comprehensive CSS that can be customized:
- Print-specific styles in `@media print` blocks
- Color schemes and typography
- Layout and spacing controls
- Page break management

### Report Content
Modify the `ReportGenerator` class to:
- Add additional metadata extraction
- Include custom analysis features
- Extend the HTML template
- Add new report formats

## Examples

### Sample Output
The generated report includes sections like:

```
Course 1: Neural Networks and Deep Learning
├── Week 2
│   ├── W2A1 - Python Basics with Numpy
│   └── W2A2 - Logistic Regression
├── Week 3
│   └── Planar Data Classification
└── Week 4
    ├── W4A1 - Building Deep Neural Networks
    └── W4A2 - Deep Neural Network Application
```

### Generated Statistics
- Total Courses: 4
- Total Assignments: 17
- Total Notebooks: ~25
- Test Coverage: Most assignments include test files

## Troubleshooting

### Common Issues

1. **No courses found**: Ensure you're in the correct directory or specify the path with `-p`
2. **Empty report**: Check that course directories follow the expected naming pattern
3. **Notebook parsing errors**: Some notebooks may have formatting issues (errors are logged)
4. **Print issues**: Ensure background graphics are enabled in browser print settings

### Getting Help

For issues with the report generator:
1. Check the command line help: `python report_generator.py --help`
2. Run the test suite: `python test_report_generator.py`
3. Review the generated HTML file for content issues

## Contributing

To extend the report generator:

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Ensure print-friendly formatting is maintained

## License

This report generator is part of the Deep Learning Specialization repository and follows the same licensing terms.