#!/usr/bin/env python3
"""
Test script for the report generator to ensure it works correctly.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """Test cases for the ReportGenerator class"""
    
    def setUp(self):
        """Set up test environment"""
        self.current_dir = Path.cwd()
        self.generator = ReportGenerator()
    
    def test_initialization(self):
        """Test that the ReportGenerator initializes correctly"""
        self.assertIsInstance(self.generator, ReportGenerator)
        self.assertIsNotNone(self.generator.courses)
        self.assertIsInstance(self.generator.courses, list)
    
    def test_scan_courses(self):
        """Test that courses are scanned correctly"""
        # Should find at least some courses in the Deep Learning Specialization repo
        self.assertGreater(len(self.generator.courses), 0)
        
        # Check that courses have the expected structure
        for course in self.generator.courses:
            self.assertIn('number', course)
            self.assertIn('title', course)
            self.assertIn('weeks', course)
            self.assertIsInstance(course['weeks'], list)
    
    def test_generate_html_report(self):
        """Test that HTML report is generated correctly"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_file = os.path.join(tmp_dir, 'test_report.html')
            result = self.generator.generate_html_report(output_file)
            
            # Check that file was created
            self.assertTrue(os.path.exists(output_file))
            
            # Check that file has content
            with open(output_file, 'r') as f:
                content = f.read()
                self.assertIn('Deep Learning Specialization', content)
                self.assertIn('Course Progress Report', content)
                self.assertIn('print-friendly', content.lower())
    
    def test_count_total_assignments(self):
        """Test assignment counting"""
        total = self.generator._count_total_assignments()
        self.assertIsInstance(total, int)
        self.assertGreaterEqual(total, 0)
    
    def test_notebook_analysis(self):
        """Test that notebook analysis works for existing notebooks"""
        # Find a notebook to test
        notebook_path = None
        for course in self.generator.courses:
            for week in course['weeks']:
                for assignment in week['assignments']:
                    if assignment['notebooks']:
                        notebook_path = assignment['notebooks'][0]['path']
                        break
                if notebook_path:
                    break
            if notebook_path:
                break
        
        if notebook_path:
            result = self.generator.analyze_notebook(notebook_path)
            self.assertIsNotNone(result)
            self.assertIn('filename', result)
            self.assertIn('title', result)
            self.assertIn('cell_count', result)
    
    def test_html_template(self):
        """Test that HTML template is valid"""
        template = self.generator._get_html_template()
        self.assertIn('<!DOCTYPE html>', template)
        self.assertIn('<html', template)
        self.assertIn('</html>', template)
        self.assertIn('print-friendly', template.lower())
        # Check for CSS media queries for print
        self.assertIn('@media print', template)


def main():
    """Run the tests"""
    print("Running tests for Deep Learning Specialization Report Generator...")
    
    # Run the tests
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()