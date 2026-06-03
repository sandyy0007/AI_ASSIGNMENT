import React, { useState } from 'react';
import PromptInput from './components/PromptInput';
import PipelineViewer from './components/PipelineViewer';
import ConfigViewer from './components/ConfigViewer';
import ValidationReport from './components/ValidationReport';
import EvaluationDashboard from './components/EvaluationDashboard';
import History from './components/History';
import { compilePrompt } from './api';

export default function App() {
  const [compilation, setCompilation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('prompt');
  const [history, setHistory] = useState([]);

  const handleCompile = async (prompt, context) => {
    setLoading(true);
    setError(null);
    try {
      const result = await compilePrompt(prompt, context);
      if (result.success) {
        setCompilation(result);
        setActiveTab('pipeline');
        // Add to history
        setHistory([
          {
            id: result.compilation_id,
            name: result.config.app_name,
            timestamp: new Date().toISOString(),
          },
          ...history.slice(0, 9),
        ]);
      } else {
        setError(result.error || 'Compilation failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadHistory = (item) => {
    if (compilation && compilation.compilation_id === item.id) return;
    setActiveTab('pipeline');
    // In a real app, would load from backend
  };

  return (
    <div className="min-h-screen bg-background text-text">
      {/* Header */}
      <div className="bg-surface border-b border-gray-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold font-mono">
            <span className="text-primary">{'<'}</span>
            AI App Config Compiler
            <span className="text-primary">{' />'}</span>
          </h1>
          <p className="text-text_secondary text-sm mt-1">
            Convert product prompts into strict valid JSON app configurations
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-2 mb-6 flex-wrap">
          {[
            { id: 'prompt', label: 'Prompt Input' },
            { id: 'pipeline', label: 'Pipeline', disabled: !compilation },
            { id: 'config', label: 'Configuration', disabled: !compilation },
            { id: 'validation', label: 'Validation', disabled: !compilation },
            { id: 'evaluation', label: 'Evaluation', disabled: !compilation },
            { id: 'history', label: 'History' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => !tab.disabled && setActiveTab(tab.id)}
              disabled={tab.disabled}
              className={`px-4 py-2 rounded-lg font-mono text-sm transition-colors ${
                activeTab === tab.id
                  ? 'bg-primary text-white'
                  : 'bg-surface border border-gray-700 hover:border-primary ' +
                    (tab.disabled ? 'opacity-50 cursor-not-allowed' : 'hover:text-primary')
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-error bg-opacity-10 border border-error rounded-lg">
            <p className="text-error font-mono text-sm">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="card p-8 text-center">
              <div className="animate-spin mb-4">
                <div className="w-12 h-12 border-4 border-gray-700 border-t-primary rounded-full mx-auto"></div>
              </div>
              <p className="text-text_secondary font-mono">Compiling configuration...</p>
            </div>
          </div>
        )}

        {/* Tab Content */}
        <div className="space-y-6">
          {activeTab === 'prompt' && (
            <PromptInput onCompile={handleCompile} loading={loading} />
          )}

          {activeTab === 'pipeline' && compilation && (
            <PipelineViewer stages={compilation.pipeline_stages} />
          )}

          {activeTab === 'config' && compilation && (
            <ConfigViewer config={compilation.config} />
          )}

          {activeTab === 'validation' && compilation && (
            <ValidationReport validation={compilation.config.validation_report} />
          )}

          {activeTab === 'evaluation' && compilation && (
            <EvaluationDashboard evaluation={compilation.config.evaluation_framework} />
          )}

          {activeTab === 'history' && (
            <History items={history} onSelect={handleLoadHistory} />
          )}
        </div>
      </div>
    </div>
  );
}
