import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
  ],
  // server: {
  //   host: '127.0.0.1',
  //   port: 5173,
  //   // optional: proxy your API to avoid CORS
  //   proxy: {
  //     '/api': { target: 'http://localhost:8000', changeOrigin: true },
  //   },
  // },
})
