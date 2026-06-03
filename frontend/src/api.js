import axios from 'axios';

const API_BASE = 'https://ai-assignment-65v2.onrender.com';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const compilePrompt = async (prompt, context) => {
  const response = await api.post('/compile', {
    prompt,
    context: context || null,
  });
  return response.data;
};

export const getCompilation = async (compilationId) => {
  const response = await api.get(`/compilation/${compilationId}`);
  return response.data;
};

export const getHistory = async (limit = 50) => {
  const response = await api.get('/history', { params: { limit } });
  return response.data;
};

export const getConfigSchema = async () => {
  const response = await api.get('/docs-config');
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};
