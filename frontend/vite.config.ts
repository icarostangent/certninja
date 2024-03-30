import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import viteTsconfigPaths from 'vite-tsconfig-paths'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), viteTsconfigPaths()],
  server: {
    host: '0.0.0.0',
    port: 8080,
    strictPort: true,
    hmr: {
      protocol: 'https',
      host: 'odinscall.com',
      clientPort: 443,
      path: '/hmr/',
    },
  }

})
