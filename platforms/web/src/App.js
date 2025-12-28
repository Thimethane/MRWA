// ============================================================================
// FILE: platforms/web/src/App.js
// Complete Web Dashboard Implementation
// ============================================================================

import React, { useState, useEffect } from 'react';
import { Play, Upload, Globe, Youtube, FileText, Code, RefreshCw, CheckCircle, XCircle, AlertCircle, Clock, Zap, Download, Eye, Trash2 } from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const SAMPLE_TASKS = [
  {
    id: 'research_synthesis',
    name: 'Research Paper Synthesis',
    description: 'Analyze multiple research papers and generate comprehensive insights with citations',
    icon: FileText,
    inputs: [
      { type: 'pdf', name: 'attention_is_all_you_need.pdf' },
      { type: 'pdf', name: 'gpt4_technical_report.pdf' },
      { type: 'url', name: 'https://arxiv.org/abs/2303.08774' }
    ]
  },
  {
    id: 'code_analysis',
    name: 'Code Quality Analysis',
    description: 'Analyze code repositories, detect issues, and suggest improvements',
    icon: Code,
    inputs: [
      { type: 'code', name: 'ml_pipeline/' },
      { type: 'code', name: 'api_server/' }
    ]
  },
  {
    id: 'video_research',
    name: 'Video Content Analysis',
    description: 'Extract insights from educational videos and generate study guide',
    icon: Youtube,
    inputs: [
      { type: 'youtube', name: 'https://youtube.com/watch?v=kCc8FmEb1nY' }
    ]
  }
];

export default function MRWADashboard() {
  const [workflows, setWorkflows] = useState([]);
  const [currentWorkflow, setCurrentWorkflow] = useState(null);
  const [selectedTask, setSelectedTask] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [customLinks, setCustomLinks] = useState('');
  const [viewingArtifact, setViewingArtifact] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    checkAPIStatus();
  }, []);

  const checkAPIStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setApiStatus('connected');
      } else {
        setApiStatus('error');
      }
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  const executeWorkflow = async () => {
    if (!selectedTask && uploadedFiles.length === 0 && !customLinks) {
      alert('Please select a task template or add custom inputs');
      return;
    }

    if (apiStatus !== 'connected') {
      alert('API server is not running. Please start the server first.');
      return;
    }

    setIsExecuting(true);

    const config = {
      name: selectedTask?.name || 'Custom Workflow',
      inputs: selectedTask?.inputs || [
        ...uploadedFiles.map(f => ({ type: f.type, name: f.name })),
        ...customLinks.split('\n').filter(l => l.trim()).map(url => ({ type: 'url', name: url }))
      ]
    };

    try {
      const response = await fetch(`${API_BASE_URL}/workflows`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });

      if (!response.ok) throw new Error('Failed to create workflow');

      const result = await response.json();
      setCurrentWorkflow(result);
      setWorkflows(prev => [result, ...prev]);

    } catch (error) {
      console.error('Workflow execution failed:', error);
      alert(`Failed to execute workflow: ${error.message}\n\nMake sure the API server is running on port 8000.`);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files);
    const fileData = files.map(f => ({
      name: f.name,
      type: f.type.includes('pdf') ? 'pdf' : f.type.includes('text') ? 'text' : 'file',
      size: `${(f.size / 1024).toFixed(1)} KB`
    }));
    setUploadedFiles(prev => [...prev, ...fileData]);
  };

  const removeFile = (index) => {
    setUploadedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const resetWorkflow = () => {
    setCurrentWorkflow(null);
    setSelectedTask(null);
    setUploadedFiles([]);
    setCustomLinks('');
  };

  const getStageColor = (stage) => {
    const colors = {
      idle: 'bg-gray-500',
      ingesting: 'bg-blue-500',
      planning: 'bg-purple-500',
      executing: 'bg-yellow-500',
      validating: 'bg-orange-500',
      correcting: 'bg-red-500',
      completed: 'bg-green-500',
      failed: 'bg-red-700'
    };
    return colors[stage] || colors.idle;
  };

  const getLogIcon = (level) => {
    switch(level) {
      case 'success': return <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />;
      case 'error': return <XCircle className="w-4 h-4 text-red-400 flex-shrink-0" />;
      case 'warning': return <AlertCircle className="w-4 h-4 text-orange-400 flex-shrink-0" />;
      default: return <Clock className="w-4 h-4 text-blue-400 flex-shrink-0" />;
    }
  };

  const getInputIcon = (type) => {
    switch(type) {
      case 'pdf': return <FileText className="w-3 h-3" />;
      case 'code': return <Code className="w-3 h-3" />;
      case 'url': return <Globe className="w-3 h-3" />;
      case 'youtube': return <Youtube className="w-3 h-3" />;
      default: return <FileText className="w-3 h-3" />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 mb-6 border border-white/20 shadow-2xl">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-4xl font-bold text-white mb-2 flex items-center gap-3">
                <Zap className="w-10 h-10 text-yellow-400" />
                MRWA
              </h1>
              <p className="text-gray-300 text-lg">Marathon Research & Workflow Agent</p>
              <p className="text-sm text-gray-400 mt-1">
                Autonomous AI • Multi-Step Planning • Self-Correcting • Powered by Gemini 3
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className={`px-4 py-2 rounded-lg text-sm font-semibold ${
                apiStatus === 'connected' ? 'bg-green-600 text-white' :
                apiStatus === 'disconnected' ? 'bg-red-600 text-white' :
                'bg-yellow-600 text-white'
              }`}>
                API: {apiStatus}
              </div>
              {currentWorkflow && (
                <div className={`px-6 py-3 rounded-xl font-semibold ${getStageColor(currentWorkflow.stage)} text-white shadow-lg`}>
                  {currentWorkflow.stage.toUpperCase()}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar */}
          <div className="space-y-6">
            {/* Task Templates */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-400" />
                Workflow Templates
              </h2>
              <div className="space-y-3">
                {SAMPLE_TASKS.map(task => {
                  const Icon = task.icon;
                  return (
                    <button
                      key={task.id}
                      onClick={() => setSelectedTask(task)}
                      className={`w-full text-left p-4 rounded-xl transition-all ${
                        selectedTask?.id === task.id
                          ? 'bg-purple-600 shadow-lg shadow-purple-500/50 scale-105'
                          : 'bg-white/5 hover:bg-white/10'
                      }`}
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <Icon className="w-5 h-5 text-white" />
                        <span className="font-semibold text-white">{task.name}</span>
                      </div>
                      <div className="text-sm text-gray-300 mb-2">{task.description}</div>
                      <div className="flex flex-wrap gap-2 text-xs">
                        {task.inputs.map((inp, idx) => (
                          <span key={idx} className="flex items-center gap-1 bg-white/20 px-2 py-1 rounded text-white">
                            {getInputIcon(inp.type)}
                            {inp.name.length > 25 ? inp.name.substring(0, 25) + '...' : inp.name}
                          </span>
                        ))}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Custom Upload */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
              <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-blue-400" />
                Custom Upload
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-300 mb-2">
                    Files (PDF, TXT, Code)
                  </label>
                  <input
                    type="file"
                    multiple
                    onChange={handleFileUpload}
                    className="w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-purple-600 file:text-white hover:file:bg-purple-700 file:cursor-pointer"
                  />
                </div>

                {uploadedFiles.length > 0 && (
                  <div>
                    <p className="text-sm font-semibold text-gray-300 mb-2">Uploaded:</p>
                    <div className="space-y-1">
                      {uploadedFiles.map((file, idx) => (
                        <div key={idx} className="flex items-center justify-between text-xs text-gray-400 bg-white/5 p-2 rounded">
                          <div className="flex items-center gap-2">
                            {getInputIcon(file.type)}
                            {file.name} ({file.size})
                          </div>
                          <button onClick={() => removeFile(idx)} className="text-red-400 hover:text-red-300">
                            <Trash2 className="w-3 h-3" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-semibold text-gray-300 mb-2">
                    Web/YouTube Links (one per line)
                  </label>
                  <textarea
                    value={customLinks}
                    onChange={(e) => setCustomLinks(e.target.value)}
                    placeholder="https://arxiv.org/abs/...&#10;https://youtube.com/watch?v=..."
                    rows={3}
                    className="w-full bg-black/30 text-white rounded-lg p-3 text-sm border border-white/20 focus:border-purple-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            {/* Controls */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
              <button
                onClick={executeWorkflow}
                disabled={isExecuting || apiStatus !== 'connected'}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white font-bold py-4 px-6 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-green-500/50 disabled:shadow-none mb-3"
              >
                {isExecuting ? (
                  <>
                    <RefreshCw className="w-5 h-5 animate-spin" />
                    Executing Autonomously...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5" />
                    Start Autonomous Execution
                  </>
                )}
              </button>

              {!isExecuting && currentWorkflow && (
                <button
                  onClick={resetWorkflow}
                  className="w-full bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-4 rounded-xl flex items-center justify-center gap-2 transition-all"
                >
                  <RefreshCw className="w-5 h-5" />
                  Reset & Start New
                </button>
              )}
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {!currentWorkflow ? (
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-12 border border-white/20 shadow-xl text-center">
                <Zap className="w-16 h-16 text-purple-400 mx-auto mb-4 animate-pulse" />
                <h3 className="text-2xl font-bold text-white mb-2">Ready to Execute</h3>
                <p className="text-gray-300 mb-4">
                  Select a workflow template or upload custom files to begin autonomous execution
                </p>
                <div className="text-sm text-gray-400">
                  <p>✓ Multi-step planning with Gemini 3</p>
                  <p>✓ Automatic validation & self-correction</p>
                  <p>✓ Verified artifact generation</p>
                </div>
              </div>
            ) : (
              <>
                {/* Progress */}
                <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-white">Workflow Progress</h2>
                    <span className="text-white font-semibold text-lg">{Math.round(currentWorkflow.progress * 100)}%</span>
                  </div>
                  <div className="w-full bg-black/30 rounded-full h-4 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-purple-500 transition-all duration-500 shadow-lg animate-pulse"
                      style={{ width: `${currentWorkflow.progress * 100}%` }}
                    />
                  </div>
                </div>

                {/* Workflow Plan */}
                {currentWorkflow.tasks.length > 0 && (
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
                    <h2 className="text-xl font-bold text-white mb-4">Multi-Step Plan (Gemini 3)</h2>
                    <div className="space-y-2">
                      {currentWorkflow.tasks.map((task) => (
                        <div
                          key={task.id}
                          className={`p-4 rounded-xl border-2 transition-all ${
                            task.status === 'completed' || task.status === 'corrected'
                              ? 'bg-green-900/30 border-green-500/50'
                              : task.status === 'running'
                              ? 'bg-yellow-900/30 border-yellow-500/50 animate-pulse'
                              : task.status === 'failed'
                              ? 'bg-red-900/30 border-red-500/50'
                              : 'bg-white/5 border-white/20'
                          }`}
                        >
                          <div className="flex items-center gap-3">
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${
                              task.status === 'completed' || task.status === 'corrected' ? 'bg-green-500' :
                              task.status === 'running' ? 'bg-yellow-500' :
                              task.status === 'failed' ? 'bg-red-500' :
                              'bg-gray-600'
                            }`}>
                              {task.step_number}
                            </div>
                            <span className="text-white font-medium flex-1">{task.description}</span>
                            {task.status === 'completed' && <CheckCircle className="w-5 h-5 text-green-400" />}
                            {task.status === 'corrected' && <CheckCircle className="w-5 h-5 text-orange-400" />}
                            {task.status === 'running' && <RefreshCw className="w-5 h-5 text-yellow-400 animate-spin" />}
                            {task.status === 'failed' && <XCircle className="w-5 h-5 text-red-400" />}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Validation Failure */}
                {currentWorkflow.validation_failure && (
                  <div className="bg-red-900/40 backdrop-blur-md rounded-2xl p-6 border-2 border-red-500/50 shadow-xl animate-pulse">
                    <h3 className="text-lg font-bold text-red-300 mb-2 flex items-center gap-2">
                      <XCircle className="w-5 h-5" />
                      Validation Failure Detected
                    </h3>
                    <div className="space-y-2 text-gray-200">
                      <p><strong>Issues Found:</strong></p>
                      {currentWorkflow.validation_failure.issues.map((issue, idx) => (
                        <p key={idx} className="ml-4">• {issue}</p>
                      ))}
                      <p className="text-sm text-gray-400 mt-2">
                        Severity: {currentWorkflow.validation_failure.severity}
                      </p>
                    </div>
                  </div>
                )}

                {/* Self-Correction */}
                {currentWorkflow.correction && (
                  <div className="bg-orange-900/40 backdrop-blur-md rounded-2xl p-6 border-2 border-orange-500/50 shadow-xl">
                    <h3 className="text-lg font-bold text-orange-300 mb-3 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5" />
                      Autonomous Self-Correction Applied ✓
                    </h3>
                    <div className="space-y-2 text-gray-200">
                      <p><strong>Action:</strong> {currentWorkflow.correction.action}</p>
                      <p><strong>Strategy:</strong> {currentWorkflow.correction.strategy}</p>
                      <p><strong>Confidence:</strong> {(currentWorkflow.correction.confidence * 100).toFixed(0)}%</p>
                    </div>
                  </div>
                )}

                {/* Execution Logs */}
                <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
                  <h2 className="text-xl font-bold text-white mb-4">Real-Time Execution Log</h2>
                  <div className="bg-black/40 rounded-xl p-4 h-72 overflow-y-auto font-mono text-sm space-y-1">
                    {currentWorkflow.logs.map((log, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-gray-300 hover:bg-white/5 px-2 py-1 rounded">
                        {getLogIcon(log.level)}
                        <span className="text-gray-500 text-xs">[{log.timestamp}]</span>
                        <span className={
                          log.level === 'error' ? 'text-red-400' :
                          log.level === 'success' ? 'text-green-400' :
                          log.level === 'warning' ? 'text-orange-400' :
                          'text-gray-300'
                        }>{log.message}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Verified Artifacts */}
                {currentWorkflow.artifacts.length > 0 && (
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl">
                    <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-400" />
                      Verified Artifacts
                    </h2>
                    <div className="space-y-3">
                      {currentWorkflow.artifacts.map((artifact, idx) => (
                        <div key={idx} className="flex items-center justify-between p-4 bg-gradient-to-r from-green-900/20 to-emerald-900/20 rounded-xl border border-green-500/30">
                          <div className="flex items-center gap-3">
                            <FileText className="w-6 h-6 text-green-400" />
                            <div>
                              <div className="text-white font-semibold">{artifact.name}</div>
                              <div className="text-sm text-gray-400">{artifact.type} • {artifact.size}</div>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            {artifact.verified && (
                              <span className="flex items-center gap-1 text-green-400 text-sm font-semibold">
                                <CheckCircle className="w-4 h-4" />
                                Verified
                              </span>
                            )}
                            <button
                              onClick={() => setViewingArtifact(artifact)}
                              className="px-3 py-1 bg-purple-600 hover:bg-purple-700 text-white rounded-lg text-sm flex items-center gap-1"
                            >
                              <Eye className="w-4 h-4" />
                              View
                            </button>
                            <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm flex items-center gap-1">
                              <Download className="w-4 h-4" />
                              Download
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>

        {/* Artifact Viewer Modal */}
        {viewingArtifact && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-slate-900 rounded-2xl p-6 max-w-2xl w-full max-h-[80vh] overflow-auto border border-white/20">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-white">{viewingArtifact.name}</h3>
                <button
                  onClick={() => setViewingArtifact(null)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>
              <div className="bg-black/40 rounded-xl p-4 text-gray-300 font-mono text-sm whitespace-pre-wrap">
                {viewingArtifact.content_preview || 'Content preview not available'}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
