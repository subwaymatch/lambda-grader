import glob
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
import re
import textwrap

def extract_test_case_metadata(source: str) -> str:
    tc_result = re.search(
        r'^\s*_test_case\s*=\s*[\'"](.*)[\'"]',
        source,
        flags=re.MULTILINE
    )
    
    if not tc_result or len(tc_result.groups()) == 0:
        return None
    
    metadata = {
        'test_case': tc_result.groups()[0],
        'points': 0,
        'grader_only': False
    }
    
    points_result = re.search(
        r'^\s*_points\s*=\s*(.*)[\s#]*.*[\r\n]',
        source,
        flags=re.MULTILINE
    )
    
    if points_result and len(tc_result.groups()) > 0:
        metadata['points'] = float(points_result.groups()[0])
        
    grader_only_result = re.search(
        r'^\s*_grader_only\s*=\s*(True|False)',
        source,
        flags=re.MULTILINE
    )
    
    if grader_only_result and len(grader_only_result.groups()) > 0:
        metadata['grader_only'] = bool(grader_only_result.groups()[0])
    
    return metadata


def convert_to_grader_code(source: str) -> str:
    indented_source = textwrap.indent(source, '    ')
    
    with open('jupyter-cell-scripts/grader-template.py') as f:
        grader_template_code = f.read()
        
    converted_source = grader_template_code.replace('# TEST_CASE_REPLACE_HERE', indented_source)
    
    return converted_source