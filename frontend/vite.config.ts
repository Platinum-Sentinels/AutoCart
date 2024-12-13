import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import process from 'process'; // Import the process polyfill

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      process: 'process/browser', // Polyfill for 'process' in the browser
    },
  },
  define: {
    'process.env': process.env, // Ensures process.env is available in your code
  },
});
