import React from 'react';

export default function EvaluationDashboard({ evaluation }) {
  if (!evaluation) {
    return (
      <div className="card p-6">
        <p className="text-text_secondary">No evaluation data available</p>
      </div>
    );
  }

  const metrics = evaluation.metrics || [];
  const overallScore = evaluation.overall_score || 0;
  const recommendations = evaluation.recommendations || [];

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-success';
    if (score >= 60) return 'text-warning';
    return 'text-error';
  };

  const getScoreBackground = (score) => {
    if (score >= 80) return 'bg-success bg-opacity-10 border-success';
    if (score >= 60) return 'bg-warning bg-opacity-10 border-warning';
    return 'bg-error bg-opacity-10 border-error';
  };

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-6 font-mono">
        <span className="text-secondary">📊</span> Quality Evaluation
      </h2>

      {/* Overall Score */}
      <div className={`p-6 rounded-lg border mb-6 ${getScoreBackground(overallScore)}`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-text_secondary font-mono text-sm mb-1">Overall Score</p>
            <p className={`text-4xl font-bold font-mono ${getScoreColor(overallScore)}`}>
              {overallScore.toFixed(1)}
            </p>
          </div>
          <div className="w-24 h-24 rounded-lg bg-background border border-gray-700 flex items-center justify-center">
            <svg className="w-full h-full" viewBox="0 0 100 100">
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="text-gray-700"
              />
              <circle
                cx="50"
                cy="50"
                r="40"
                fill="none"
                stroke="currentColor"
                strokeWidth="3"
                strokeDasharray={`${(overallScore / 100) * 251} 251`}
                className={getScoreColor(overallScore)}
                strokeLinecap="round"
                transform="rotate(-90 50 50)"
              />
              <text
                x="50"
                y="55"
                textAnchor="middle"
                className="text-xs font-bold fill-text"
              >
                {Math.round(overallScore)}%
              </text>
            </svg>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        {metrics.map((metric, i) => (
          <div key={i} className="metric-card">
            <div className="flex items-center justify-between mb-2">
              <p className="font-mono font-bold text-sm">{metric.name}</p>
              <span className={`font-mono font-bold text-lg ${getScoreColor(metric.score)}`}>
                {metric.score.toFixed(1)}
              </span>
            </div>
            <p className="text-xs text-text_secondary mb-3">{metric.description}</p>

            {/* Score Bar */}
            <div className="w-full h-2 bg-background rounded-full overflow-hidden border border-gray-700">
              <div
                className={`h-full transition-all ${
                  metric.score >= 80
                    ? 'bg-success'
                    : metric.score >= 60
                    ? 'bg-warning'
                    : 'bg-error'
                }`}
                style={{ width: `${metric.score}%` }}
              />
            </div>

            {/* Recommendations */}
            {metric.recommendations && metric.recommendations.length > 0 && (
              <ul className="mt-3 space-y-1">
                {metric.recommendations.map((rec, j) => (
                  <li key={j} className="text-xs text-text_secondary flex gap-2">
                    <span className="text-text_secondary">→</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div className="bg-surface p-4 rounded-lg border border-gray-700">
          <h3 className="font-mono font-bold text-sm mb-3">Recommendations</h3>
          <ul className="space-y-2">
            {recommendations.map((rec, i) => (
              <li key={i} className="text-sm text-text_secondary flex gap-2">
                <span className="text-secondary">→</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
