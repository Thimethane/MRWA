# ============================================================================
# FILE: core/orchestrator/server.py
# ============================================================================
SERVER_CODE = '''"""
core/orchestrator/server.py
Flask API Server for MRWA
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import asyncio
import os
from .engine import WorkflowEngine

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store active workflows
workflows = {}
engine = WorkflowEngine(gemini_api_key=os.getenv('GEMINI_API_KEY'))


def get_event_loop():
    """Get or create event loop"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'version': '1.0.0'})


@app.route('/api/workflows', methods=['POST'])
def create_workflow():
    """Create and execute workflow"""
    try:
        config = request.json
        if not config or 'name' not in config:
            return jsonify({'error': 'Invalid configuration'}), 400
        
        loop = get_event_loop()
        result = loop.run_until_complete(engine.execute_workflow(config))
        workflows[result.workflow_id] = result
        
        socketio.emit('workflow_update', result.to_dict())
        return jsonify(result.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/workflows/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    if workflow_id not in workflows:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(workflows[workflow_id].to_dict())


@app.route('/api/workflows', methods=['GET'])
def list_workflows():
    return jsonify({
        'workflows': [w.to_dict() for w in workflows.values()],
        'count': len(workflows)
    })


@app.route('/api/samples', methods=['GET'])
def list_samples():
    """List available sample files"""
    return jsonify({
        'research_papers': [
            {'name': 'attention_is_all_you_need.pdf', 'size': '2.1 MB'},
            {'name': 'gpt4_technical_report.pdf', 'size': '1.8 MB'}
        ],
        'code_repositories': [
            {'name': 'ml_pipeline', 'language': 'Python'},
            {'name': 'api_server', 'language': 'JavaScript'}
        ],
        'web_links': [
            'https://arxiv.org/abs/2303.08774',
            'https://paperswithcode.com/sota'
        ],
        'youtube_videos': [
            {'url': 'https://youtube.com/watch?v=kCc8FmEb1nY', 'title': 'Transformers'}
        ]
    })


@socketio.on('connect')
def handle_connect():
    emit('connection_status', {'status': 'connected'})


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting MRWA API Server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
'''
