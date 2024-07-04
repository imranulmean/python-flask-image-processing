import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '172.23.1.28', // Replace with your desired IP address
    port: 5173, // Optional: specify the port
  },  
})
