import React from 'react';

export default function ValidationReport({ validation }) {
  if (!validation) {
    return (
      <div className="card p-6">
        <p className="text-text_secondary">No validation report available</p>
      </div>
    );
  }

  const errors = validation.errors || [];
  const warnings = validation.warnings || [];
  const isValid = validation.is_valid;

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-6 font-mono">
        <span className={isValid ? 'text-success' : 'text-error'}>
          {isValid ? '✓' : '✕'}
        </span>
        {' '}Validation Report
      </h2>

      {/* Status Summary */}
      <div className={`p-4 rounded-lg border mb-6 ${
        isValid
          ? 'bg-success bg-opacity-10 border-success'
          : 'bg-error bg-opacity-10 border-error'
      }`}>
        <p className={`font-mono font-bold ${isValid ? 'text-success' : 'text-error'}`}>
          {isValid ? 'Configuration is valid ✓' : 'Configuration has errors ✕'}
        </p>
        <p className="text-xs text-text_secondary mt-1 font-mono">
          {errors.length} errors, {warnings.length} warnings
        </p>
      </div>

      {/* Errors */}
      {errors.length > 0 && (
        <div className="mb-6">
          <h3 className="font-mono font-bold text-sm mb-3 text-error">Errors</h3>
          <div className="space-y-2">
            {errors.map((error, i) => (
              <div
                key={i}
                className="bg-background border border-error border-opacity-30 p-3 rounded-lg"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-mono text-sm text-error font-bold">{error.field}</p>
                    <p className="text-xs text-text_secondary mt-1">{error.error}</p>
                  </div>
                  <span className={`stage-badge ${
                    error.severity === 'critical' ? 'error' : 'warning'
                  }`}>
                    {error.severity}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Warnings */}
      {warnings.length > 0 && (
        <div className="mb-6">
          <h3 className="font-mono font-bold text-sm mb-3 text-warning">Warnings</h3>
          <div className="space-y-2">
            {warnings.map((warning, i) => (
              <div
                key={i}
                className="bg-background border border-warning border-opacity-30 p-3 rounded-lg"
              >
                <p className="text-xs text-text_secondary">{warning}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Issues */}
      {errors.length === 0 && warnings.length === 0 && (
        <div className="text-center py-6">
          <p className="text-success text-xl font-mono mb-2">✓</p>
          <p className="text-text_secondary">No validation issues found</p>
        </div>
      )}
    </div>
  );
}
