import React, { useState } from 'react';

export default function ConfigViewer({ config }) {
  const [activeSection, setActiveSection] = useState('overview');
  const [copied, setCopied] = useState(false);

  const sections = [
    { id: 'overview', label: 'Overview', icon: '📄' },
    { id: 'schema', label: 'Schemas', icon: '📋' },
    { id: 'entities', label: 'Entities', icon: '🗂️' },
    { id: 'roles', label: 'Roles', icon: '👥' },
    { id: 'api', label: 'API', icon: '🔗' },
    { id: 'database', label: 'Database', icon: '🗄️' },
    { id: 'raw', label: 'Raw JSON', icon: '{}' },
  ];

  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(config, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold font-mono">
          <span className="text-primary">{'{'}</span> Configuration
          <span className="text-primary">{'}'}</span>
        </h2>
        <button
          onClick={handleCopy}
          className="btn-secondary text-xs font-mono"
        >
          {copied ? '✓ Copied' : 'Copy JSON'}
        </button>
      </div>

      {/* Section Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {sections.map((section) => (
          <button
            key={section.id}
            onClick={() => setActiveSection(section.id)}
            className={`px-3 py-2 rounded-lg text-xs font-mono whitespace-nowrap transition-colors ${
              activeSection === section.id
                ? 'bg-primary text-white'
                : 'bg-surface border border-gray-700 hover:border-primary text-text_secondary hover:text-text'
            }`}
          >
            {section.icon} {section.label}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="space-y-4">
        {activeSection === 'overview' && (
          <div className="space-y-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-surface p-4 rounded-lg border border-gray-700">
                <p className="text-xs text-text_secondary font-mono mb-1">App Name</p>
                <p className="text-lg font-bold">{config.app_name}</p>
              </div>
              <div className="bg-surface p-4 rounded-lg border border-gray-700">
                <p className="text-xs text-text_secondary font-mono mb-1">Timestamp</p>
                <p className="text-sm font-mono">
                  {new Date(config.timestamp).toLocaleString()}
                </p>
              </div>
            </div>

            <div>
              <h3 className="font-mono font-bold text-sm mb-2">Assumptions</h3>
              <ul className="space-y-1">
                {config.assumptions.map((assumption, i) => (
                  <li key={i} className="text-sm text-text_secondary flex gap-2">
                    <span className="text-text">•</span>
                    <span>{assumption}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {activeSection === 'schema' && (
          <div className="code-block">
            <pre className="text-xs">
              {JSON.stringify(
                {
                  ui_schema: config.ui_schema,
                  api_schema: config.api_schema,
                  database_schema: config.database_schema,
                },
                null,
                2
              )}
            </pre>
          </div>
        )}

        {activeSection === 'entities' && (
          <div className="space-y-2">
            {config.entities?.map((entity, i) => (
              <div key={i} className="bg-surface p-3 rounded-lg border border-gray-700">
                <h4 className="font-mono font-bold text-sm text-primary mb-2">
                  {entity.name}
                </h4>
                <p className="text-xs text-text_secondary mb-2">Attributes:</p>
                <div className="code-block text-xs mb-2">
                  <pre>{JSON.stringify(entity.attributes, null, 2)}</pre>
                </div>
                <p className="text-xs text-text_secondary">Relationships:</p>
                <ul className="text-xs space-y-1">
                  {entity.relationships?.map((rel, j) => (
                    <li key={j} className="text-text_secondary">
                      • {rel}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}

        {activeSection === 'roles' && (
          <div className="space-y-2">
            {config.roles?.map((role, i) => (
              <div key={i} className="bg-surface p-3 rounded-lg border border-gray-700">
                <h4 className="font-mono font-bold text-sm text-secondary mb-1">
                  {role.name}
                </h4>
                <p className="text-xs text-text_secondary mb-2">{role.description}</p>
                <div className="flex flex-wrap gap-1">
                  {role.permissions?.map((perm, j) => (
                    <span key={j} className="stage-badge bg-gray-700 text-text_secondary">
                      {perm}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {activeSection === 'api' && (
          <div className="code-block">
            <pre className="text-xs">
              {JSON.stringify(config.api_schema, null, 2)}
            </pre>
          </div>
        )}

        {activeSection === 'database' && (
          <div className="code-block">
            <pre className="text-xs">
              {JSON.stringify(config.database_schema, null, 2)}
            </pre>
          </div>
        )}

        {activeSection === 'raw' && (
          <div className="code-block overflow-auto max-h-96">
            <pre className="text-xs">
              {JSON.stringify(config, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
