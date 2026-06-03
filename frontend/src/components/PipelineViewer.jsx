import React, { useState } from 'react';

const STAGES = [
  {
    name: 'intent_extraction',
    label: 'Intent Extraction',
    icon: '🎯',
    description: 'Extract user intent from prompt',
  },
  {
    name: 'system_design',
    label: 'System Design',
    icon: '🏗️',
    description: 'Design system architecture',
  },
  {
    name: 'schema_generation',
    label: 'Schema Generation',
    icon: '📋',
    description: 'Generate UI, API, and DB schemas',
  },
  {
    name: 'validation_layer',
    label: 'Validation',
    icon: '✓',
    description: 'Validate configuration',
  },
  {
    name: 'repair_engine',
    label: 'Repair Engine',
    icon: '🔧',
    description: 'Fix validation errors',
  },
  {
    name: 'execution_simulator',
    label: 'Execution Simulator',
    icon: '⚡',
    description: 'Simulate execution flow',
  },
  {
    name: 'evaluation_framework',
    label: 'Evaluation',
    icon: '📊',
    description: 'Evaluate quality metrics',
  },
];

export default function PipelineViewer({ stages }) {
  const [expandedStage, setExpandedStage] = useState(0);

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-6 font-mono">
        <span className="text-primary">→</span> Pipeline Execution
      </h2>

      <div className="space-y-3">
        {stages.map((stage, index) => {
          const stageInfo = STAGES.find((s) => s.name === stage.name);
          const isExpanded = expandedStage === index;

          return (
            <div
              key={index}
              className="border border-gray-700 rounded-lg overflow-hidden hover:border-primary transition-colors"
            >
              <button
                onClick={() => setExpandedStage(isExpanded ? -1 : index)}
                className="w-full p-4 bg-surface hover:bg-opacity-70 transition-colors text-left flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{stageInfo?.icon}</span>
                  <div>
                    <h3 className="font-mono font-bold">{stageInfo?.label}</h3>
                    <p className="text-xs text-text_secondary">{stageInfo?.description}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-text_secondary">
                    {stage.output.time?.toFixed(2)}s
                  </span>
                  <span
                    className={`stage-badge ${
                      stage.output.success ? 'success' : 'error'
                    }`}
                  >
                    {stage.output.success ? '✓' : '✕'}
                  </span>
                  <span className="text-text_secondary">{isExpanded ? '▼' : '▶'}</span>
                </div>
              </button>

              {isExpanded && (
                <div className="p-4 bg-background border-t border-gray-700">
                  <div className="code-block text-xs">
                    <pre>{JSON.stringify(stage.output, null, 2)}</pre>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Timeline Summary */}
      <div className="mt-6 pt-6 border-t border-gray-700">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-surface p-3 rounded-lg">
            <p className="text-xs text-text_secondary font-mono">Total Time</p>
            <p className="text-xl font-mono font-bold text-primary">
              {(stages.reduce((sum, s) => sum + (s.output.time || 0), 0)).toFixed(2)}s
            </p>
          </div>
          <div className="bg-surface p-3 rounded-lg">
            <p className="text-xs text-text_secondary font-mono">Stages</p>
            <p className="text-xl font-mono font-bold text-secondary">{stages.length}</p>
          </div>
          <div className="bg-surface p-3 rounded-lg">
            <p className="text-xs text-text_secondary font-mono">Successful</p>
            <p className="text-xl font-mono font-bold text-success">
              {stages.filter((s) => s.output.success).length}
            </p>
          </div>
          <div className="bg-surface p-3 rounded-lg">
            <p className="text-xs text-text_secondary font-mono">Failed</p>
            <p className="text-xl font-mono font-bold text-error">
              {stages.filter((s) => !s.output.success).length}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
