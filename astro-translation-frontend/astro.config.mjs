import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  integrations: [
    react(),
    tailwind()
  ],
  output: 'hybrid',
  adapter: cloudflare({
    mode: 'directory',
    functionPerRoute: false
  }),
  vite: {
    define: {
      'process.env.PUBLIC_SUPABASE_URL': JSON.stringify(process.env.PUBLIC_SUPABASE_URL),
      'process.env.PUBLIC_SUPABASE_ANON_KEY': JSON.stringify(process.env.PUBLIC_SUPABASE_ANON_KEY),
      'process.env.PUBLIC_TRANSLATION_API_URL': JSON.stringify(process.env.PUBLIC_TRANSLATION_API_URL)
    }
  }
});