from flask import Flask, render_template, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector
import ast
import subprocess
import json
from datetime import datetime

app = Flask(__name__)

def get_pylint_score(file_path):
    """Get pylint score for a Python file"""
    try:
        result_text = subprocess.run(
            ['pylint', file_path, '--exit-zero'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        import re
        match = re.search(r'rated at ([\d.]+)/10', result_text.stdout)
        score = float(match.group(1)) if match else 0.0
        
        return score, None
    except FileNotFoundError:
        return None, "pylint not installed"
    except subprocess.TimeoutExpired:
        return None, "pylint analysis timed out"
    except Exception as e:
        return None, str(e)

def analyze_code(file_path):
    """Perform static code analysis on a Python file"""
    analysis = {
        'file': file_path,
        'timestamp': datetime.now().isoformat(),
        'metrics': {},
        'functions': [],
        'imports': [],
        'errors': [],
        'warnings': [],
        'code_quality': {},
        'pylint_score': None,
        'pylint_status': None
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        lines = code.split('\n')
        
        analysis['metrics']['total_lines'] = len(lines)
        analysis['metrics']['code_lines'] = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        analysis['metrics']['comment_lines'] = len([l for l in lines if l.strip().startswith('#')])
        analysis['metrics']['blank_lines'] = len([l for l in lines if not l.strip()])
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'args': len(node.args.args),
                    'docstring': ast.get_docstring(node) is not None,
                    'complexity': 1 + sum(1 for child in ast.walk(node) if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)))
                }
                analysis['functions'].append(func_info)
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analysis['imports'].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    analysis['imports'].append(f"{module}.{alias.name}")
        
        analysis['code_quality'] = {
            'has_type_hints': False,
            'has_docstrings': False,
            'avg_line_length': round(sum(len(l) for l in lines) / len(lines), 2) if lines else 0,
            'max_line_length': max(len(l) for l in lines) if lines else 0,
            'indentation_style': 'tabs' if any(l.startswith('\t') for l in lines) else 'spaces'
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.returns or any(arg.annotation for arg in node.args.args):
                    analysis['code_quality']['has_type_hints'] = True
                if ast.get_docstring(node):
                    analysis['code_quality']['has_docstrings'] = True
        
        pylint_score, pylint_error = get_pylint_score(file_path)
        analysis['pylint_score'] = pylint_score
        
        print("\n" + "="*60)
        print(f"CODE ANALYSIS REPORT: {file_path}")
        print("="*60)
        print(f"Timestamp: {analysis['timestamp']}")
        print(f"\nMETRICS:")
        print(f"  Total Lines: {analysis['metrics'].get('total_lines', 0)}")
        print(f"  Code Lines: {analysis['metrics'].get('code_lines', 0)}")
        print(f"  Comment Lines: {analysis['metrics'].get('comment_lines', 0)}")
        print(f"  Blank Lines: {analysis['metrics'].get('blank_lines', 0)}")
        print(f"  Functions: {len(analysis['functions'])}")
        print(f"  Imports: {len(set(analysis['imports']))}")
        
        print(f"\nPYLINT SCORE:")
        if pylint_score is not None:
            print(f"  Score: {pylint_score:.2f}/10")
        else:
            print(f"  {pylint_error}")
        
        print("="*60 + "\n")
        
        analysis['status'] = 'success'
    
    except Exception as e:
        analysis['status'] = 'error'
        analysis['errors'].append(str(e))
    
    return analysis

@app.errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors"""
    return jsonify({
        'success': False,
        'error': 'Bad Request',
        'message': 'The request was malformed or invalid. Please check your input.',
        'status_code': 400
    }), 400

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 Not Found errors"""
    return jsonify({
        'success': False,
        'error': 'Not Found',
        'message': 'The requested endpoint does not exist.',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    return jsonify({
        'success': False,
        'error': 'Internal Server Error',
        'message': 'An error occurred on the server. Please try again later.',
        'status_code': 500
    }), 500

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/emotionDetector')
def emotion_detector_function():
    """Emotion detection endpoint - handles blank input with 400 error"""
    text_to_analyze = request.args.get('textToAnalyze', '')
    
    # Check for blank input - return 400 error
    if not text_to_analyze or text_to_analyze.strip() == '':
        return jsonify({
            'error': 'Blank input provided',
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }), 400
    
    # Get emotion analysis
    result = emotion_detector(text_to_analyze)
    
    # Build response string showing all emotions and dominant
    response_string = (
        f"Anger: {result['anger']}, "
        f"Disgust: {result['disgust']}, "
        f"Fear: {result['fear']}, "
        f"Joy: {result['joy']}, "
        f"Sadness: {result['sadness']}, "
        f"Dominant Emotion: {result['dominant_emotion']}"
    )
    
    return response_string

@app.route('/analysis')
def code_analysis():
    """Static code analysis page"""
    print("\n🔍 Analysis request received - Running analysis...")
    analysis = analyze_code('EmotionDetection/emotion_detection.py')
    
    html_response = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Static Code Analysis</title>
        <style>
            body {{ font-family: Arial; background: #f5f5f5; margin: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            h1 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
            .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #667eea; }}
            .metric-label {{ font-size: 12px; color: #666; }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background: #667eea; color: white; }}
            .success {{ background: #d4edda; border-left: 4px solid #28a745; padding: 10px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Static Code Analysis</h1>
            <div class="metric">
                <div class="metric-label">Pylint Score</div>
                <div class="metric-value">{analysis['pylint_score']:.2f if analysis['pylint_score'] else 'N/A'}/10</div>
            </div>
            <div class="success"><strong>✅ Analysis Complete!</strong></div>
            <p><a href="/">← Back Home</a></p>
        </div>
    </body>
    </html>
    """
    
    return html_response

if __name__ == '__main__':
    print("Starting Emotion Detection Server...")
    print("Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
