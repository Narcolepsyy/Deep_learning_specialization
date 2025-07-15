#!/usr/bin/env python3
"""
Deep Learning Specialization Report Generator
============================================

This script generates print-friendly HTML reports for the Deep Learning Specialization course.
It can create both a comprehensive course overview and individual assignment reports.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import argparse


class ReportGenerator:
    """Main class for generating print-friendly reports"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.courses = []
        self.scan_courses()
    
    def scan_courses(self):
        """Scan the directory structure to identify courses and assignments"""
        course_pattern = re.compile(r'^Course \d+:')
        
        for item in self.base_path.iterdir():
            if item.is_dir() and course_pattern.match(item.name):
                course_info = self.analyze_course(item)
                if course_info:
                    self.courses.append(course_info)
        
        # Sort courses by number
        self.courses.sort(key=lambda x: x['number'])
    
    def analyze_course(self, course_path):
        """Analyze a single course directory to extract information"""
        course_name = course_path.name
        course_match = re.match(r'^Course (\d+):\s*(.+)$', course_name)
        
        if not course_match:
            return None
        
        course_number = int(course_match.group(1))
        course_title = course_match.group(2)
        
        course_info = {
            'number': course_number,
            'title': course_title,
            'path': course_path,
            'weeks': []
        }
        
        # Scan for weeks
        week_pattern = re.compile(r'^Week \d+')
        for item in course_path.iterdir():
            if item.is_dir() and week_pattern.match(item.name):
                week_info = self.analyze_week(item)
                if week_info:
                    course_info['weeks'].append(week_info)
        
        # Sort weeks by number
        course_info['weeks'].sort(key=lambda x: x['number'])
        
        return course_info
    
    def analyze_week(self, week_path):
        """Analyze a week directory to extract assignment information"""
        week_name = week_path.name
        week_match = re.match(r'^Week (\d+)', week_name)
        
        if not week_match:
            return None
        
        week_number = int(week_match.group(1))
        
        week_info = {
            'number': week_number,
            'name': week_name,
            'path': week_path,
            'assignments': []
        }
        
        # Scan for assignments
        for item in week_path.iterdir():
            if item.is_dir():
                assignment_info = self.analyze_assignment(item)
                if assignment_info:
                    week_info['assignments'].append(assignment_info)
        
        # Sort assignments by name
        week_info['assignments'].sort(key=lambda x: x['name'])
        
        return week_info
    
    def analyze_assignment(self, assignment_path):
        """Analyze an assignment directory"""
        assignment_info = {
            'name': assignment_path.name,
            'path': assignment_path,
            'notebooks': [],
            'python_files': [],
            'has_tests': False
        }
        
        for item in assignment_path.iterdir():
            if item.is_file():
                if item.suffix == '.ipynb' and not item.name.startswith('.'):
                    notebook_info = self.analyze_notebook(item)
                    if notebook_info:
                        assignment_info['notebooks'].append(notebook_info)
                elif item.suffix == '.py':
                    if 'test' in item.name.lower():
                        assignment_info['has_tests'] = True
                    assignment_info['python_files'].append(item.name)
        
        return assignment_info if assignment_info['notebooks'] or assignment_info['python_files'] else None
    
    def analyze_notebook(self, notebook_path):
        """Analyze a Jupyter notebook to extract basic information"""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook_data = json.load(f)
            
            title = "Untitled"
            description = ""
            cell_count = len(notebook_data.get('cells', []))
            
            # Try to extract title from first markdown cell
            for cell in notebook_data.get('cells', []):
                if cell.get('cell_type') == 'markdown':
                    source = ''.join(cell.get('source', []))
                    if source.strip():
                        lines = source.strip().split('\n')
                        first_line = lines[0].strip()
                        if first_line.startswith('#'):
                            title = first_line.lstrip('#').strip()
                        if len(lines) > 1:
                            description = '\n'.join(lines[1:3]).strip()
                        break
            
            return {
                'filename': notebook_path.name,
                'title': title,
                'description': description,
                'cell_count': cell_count,
                'path': notebook_path
            }
        except Exception as e:
            print(f"Error analyzing notebook {notebook_path}: {e}")
            return None
    
    def generate_html_report(self, output_path="course_report.html"):
        """Generate a comprehensive HTML report"""
        html_content = self._get_html_template()
        
        # Generate course content
        courses_html = ""
        for course in self.courses:
            courses_html += self._generate_course_html(course)
        
        # Replace placeholders
        html_content = html_content.replace('{{COURSES_CONTENT}}', courses_html)
        html_content = html_content.replace('{{GENERATION_DATE}}', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        html_content = html_content.replace('{{TOTAL_COURSES}}', str(len(self.courses)))
        html_content = html_content.replace('{{TOTAL_ASSIGNMENTS}}', str(self._count_total_assignments()))
        
        # Write to file
        output_file = self.base_path / output_path
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Report generated: {output_file}")
        return output_file
    
    def _generate_course_html(self, course):
        """Generate HTML for a single course"""
        html = f"""
        <div class="course">
            <h2>Course {course['number']}: {course['title']}</h2>
            <div class="course-summary">
                <p><strong>Total Weeks:</strong> {len(course['weeks'])}</p>
                <p><strong>Total Assignments:</strong> {sum(len(week['assignments']) for week in course['weeks'])}</p>
            </div>
        """
        
        for week in course['weeks']:
            html += self._generate_week_html(week)
        
        html += "</div>"
        return html
    
    def _generate_week_html(self, week):
        """Generate HTML for a single week"""
        html = f"""
            <div class="week">
                <h3>{week['name']}</h3>
                <div class="assignments">
        """
        
        for assignment in week['assignments']:
            html += self._generate_assignment_html(assignment)
        
        html += """
                </div>
            </div>
        """
        return html
    
    def _generate_assignment_html(self, assignment):
        """Generate HTML for a single assignment"""
        html = f"""
                    <div class="assignment">
                        <h4>{assignment['name']}</h4>
                        <div class="assignment-details">
        """
        
        if assignment['notebooks']:
            html += "<h5>Notebooks:</h5><ul class='notebooks'>"
            for notebook in assignment['notebooks']:
                html += f"""
                    <li>
                        <strong>{notebook['filename']}</strong> - {notebook['title']}
                        <br><span class="description">{notebook['description'][:100]}{'...' if len(notebook['description']) > 100 else ''}</span>
                        <br><span class="meta">Cells: {notebook['cell_count']}</span>
                    </li>
                """
            html += "</ul>"
        
        if assignment['python_files']:
            html += "<h5>Python Files:</h5><ul class='python-files'>"
            for py_file in assignment['python_files']:
                html += f"<li>{py_file}</li>"
            html += "</ul>"
        
        if assignment['has_tests']:
            html += "<p class='test-indicator'>✓ Contains test files</p>"
        
        html += """
                        </div>
                    </div>
        """
        return html
    
    def _count_total_assignments(self):
        """Count total number of assignments across all courses"""
        total = 0
        for course in self.courses:
            for week in course['weeks']:
                total += len(week['assignments'])
        return total
    
    def _get_html_template(self):
        """Return the HTML template for the report"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Learning Specialization - Course Report</title>
    <style>
        /* Print-friendly CSS styles */
        @media print {
            body { margin: 0; }
            .no-print { display: none; }
            .page-break { page-break-before: always; }
            h1, h2 { page-break-after: avoid; }
            .course { page-break-inside: avoid; }
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            text-align: center;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        
        h3 {
            color: #7f8c8d;
            margin-top: 25px;
        }
        
        h4 {
            color: #95a5a6;
            margin-top: 20px;
        }
        
        h5 {
            color: #bdc3c7;
            margin-top: 15px;
            margin-bottom: 5px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
        }
        
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .summary-item {
            background-color: #f1f2f6;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .summary-item h3 {
            margin: 0 0 10px 0;
            color: #3498db;
        }
        
        .summary-item p {
            margin: 0;
            font-size: 1.2em;
            font-weight: bold;
        }
        
        .course {
            margin-bottom: 40px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background-color: #fafafa;
        }
        
        .course-summary {
            background-color: #e8f4f8;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .course-summary p {
            margin: 5px 0;
        }
        
        .week {
            margin-bottom: 25px;
            padding: 15px;
            border-left: 4px solid #3498db;
            background-color: #fff;
        }
        
        .assignments {
            margin-left: 20px;
        }
        
        .assignment {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background-color: #fefefe;
        }
        
        .assignment-details {
            margin-top: 10px;
        }
        
        .notebooks li, .python-files li {
            margin-bottom: 10px;
            padding: 8px;
            background-color: #f8f9fa;
            border-radius: 3px;
        }
        
        .description {
            font-style: italic;
            color: #666;
            font-size: 0.9em;
        }
        
        .meta {
            font-size: 0.8em;
            color: #888;
        }
        
        .test-indicator {
            color: #27ae60;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
        
        ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        ul li {
            margin-bottom: 8px;
        }
        
        /* Print button styles */
        .print-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            z-index: 1000;
        }
        
        .print-button:hover {
            background-color: #2980b9;
        }
        
        @media print {
            .print-button { display: none; }
        }
    </style>
</head>
<body>
    <button class="print-button no-print" onclick="window.print()">🖨️ Print Report</button>
    
    <div class="header">
        <h1>Deep Learning Specialization</h1>
        <h2>Course Progress Report</h2>
        <p><strong>Generated on:</strong> {{GENERATION_DATE}}</p>
    </div>
    
    <div class="summary">
        <div class="summary-item">
            <h3>Total Courses</h3>
            <p>{{TOTAL_COURSES}}</p>
        </div>
        <div class="summary-item">
            <h3>Total Assignments</h3>
            <p>{{TOTAL_ASSIGNMENTS}}</p>
        </div>
    </div>
    
    <div class="content">
        {{COURSES_CONTENT}}
    </div>
    
    <div class="footer">
        <p>This report was generated automatically from the Deep Learning Specialization repository.</p>
        <p>For best printing results, use landscape orientation and enable background graphics.</p>
    </div>
</body>
</html>
        """


def main():
    parser = argparse.ArgumentParser(description='Generate print-friendly reports for Deep Learning Specialization')
    parser.add_argument('--output', '-o', default='course_report.html', 
                       help='Output HTML file name (default: course_report.html)')
    parser.add_argument('--path', '-p', default=None,
                       help='Base path to scan (default: current directory)')
    
    args = parser.parse_args()
    
    print("Deep Learning Specialization Report Generator")
    print("=" * 50)
    
    generator = ReportGenerator(args.path)
    
    if not generator.courses:
        print("No courses found in the specified directory.")
        return
    
    print(f"Found {len(generator.courses)} courses:")
    for course in generator.courses:
        print(f"  - Course {course['number']}: {course['title']}")
        print(f"    Weeks: {len(course['weeks'])}, Assignments: {sum(len(week['assignments']) for week in course['weeks'])}")
    
    print(f"\nGenerating report...")
    output_file = generator.generate_html_report(args.output)
    print(f"Report saved to: {output_file}")
    print("\nTo view the report, open the HTML file in your web browser.")
    print("Use the print button or Ctrl+P to print the report.")


if __name__ == "__main__":
    main()