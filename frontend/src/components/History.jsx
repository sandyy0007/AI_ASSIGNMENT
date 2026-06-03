import React from 'react';

export default function History({ items, onSelect }) {
  if (!items || items.length === 0) {
    return (
      <div className="card p-6 text-center">
        <p className="text-text_secondary font-mono">
          No compilation history yet. Generate your first configuration above.
        </p>
      </div>
    );
  }

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-6 font-mono">
        <span className="text-secondary">⏱️</span> Recent Compilations
      </h2>

      <div className="space-y-2">
        {items.map((item) => (
          <button
            key={item.id}
            onClick={() => onSelect(item)}
            className="w-full p-4 bg-surface border border-gray-700 hover:border-primary rounded-lg text-left transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <h3 className="font-mono font-bold text-primary">{item.name}</h3>
                <p className="text-xs text-text_secondary mt-1">
                  {new Date(item.timestamp).toLocaleString()}
                </p>
              </div>
              <span className="text-text_secondary">→</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
