import React, { useState } from 'react';

export default function PromptInput({ onCompile, loading }) {
  const [prompt, setPrompt] = useState('');
  const [context, setContext] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onCompile(prompt, context);
    }
  };

  return (
    <div className="card p-6">
      <h2 className="text-2xl font-bold mb-4 font-mono">
        <span className="text-primary">$</span> Enter Product Prompt
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-mono text-text_secondary mb-2">
            Product Description
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your application idea. Example: Build an e-commerce platform where customers can browse products, add to cart, and checkout..."
            className="input-field min-h-32 font-mono text-sm"
            disabled={loading}
          />
          <p className="text-xs text-text_secondary mt-1">
            Minimum 10 characters. Be specific about features and requirements.
          </p>
        </div>

        <div>
          <label className="block text-sm font-mono text-text_secondary mb-2">
            Additional Context (Optional)
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Any additional context like target users, use cases, or constraints..."
            className="input-field min-h-20 font-mono text-sm"
            disabled={loading}
          />
        </div>

        <div className="flex gap-4">
          <button
            type="submit"
            disabled={loading || prompt.trim().length < 10}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed font-mono"
          >
            {loading ? 'Compiling...' : 'Generate Configuration'}
          </button>
        </div>
      </form>

      {/* Example Prompts */}
      <div className="mt-8 pt-6 border-t border-gray-700">
        <h3 className="text-sm font-mono font-bold text-text_secondary mb-3">
          Example Prompts
        </h3>
        <div className="space-y-2">
          {[
            'Build an e-commerce platform with product catalog, shopping cart, and payment processing',
            'Create a project management tool for teams with task tracking and collaboration',
            'Develop a social networking app with user profiles, posts, and messaging',
          ].map((example, i) => (
            <button
              key={i}
              onClick={() => setPrompt(example)}
              className="block text-xs text-primary hover:text-secondary transition-colors text-left py-1"
            >
              → {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
