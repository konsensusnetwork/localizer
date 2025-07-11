# BookTranslator Frontend

A modern web application for AI-powered book translation, built with Astro, React, and Tailwind CSS. This frontend connects to your translation API backend and provides a user-friendly interface for uploading books, configuring translations, and managing translation jobs.

## Features

- 🔐 **Supabase Authentication** - Secure user sign-up and sign-in
- 📁 **File Upload** - Support for TXT, MD, EPUB, and PDF files
- ⚙️ **Translation Configuration** - Choose AI models, languages, and advanced options
- 📊 **Job Management** - Real-time status tracking and progress monitoring
- 💾 **Secure Downloads** - Direct download of translated files
- 📱 **Responsive Design** - Works on desktop and mobile devices
- ⚡ **Fast Performance** - Optimized with Astro and deployed on Cloudflare

## Tech Stack

- **Framework**: Astro 4.x
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **Authentication**: Supabase Auth
- **Deployment**: Cloudflare Pages
- **Language**: TypeScript

## Prerequisites

- Node.js 18+ 
- npm or yarn
- Supabase project (for authentication)
- Translation API backend (running)

## Setup

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd astro-translation-frontend
npm install
```

### 2. Environment Configuration

Copy the environment template:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Supabase Configuration
PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key

# Translation API Configuration
PUBLIC_TRANSLATION_API_URL=http://localhost:8000
```

### 3. Supabase Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Get your project URL and anon key from Settings > API
3. Enable Email authentication in Authentication > Settings
4. (Optional) Configure email templates in Authentication > Email Templates

### 4. Translation API Backend

Ensure your translation API backend is running and accessible. The frontend expects these endpoints:

- `POST /translate/start` - Start translation job
- `GET /translate/jobs/{job_id}` - Get job status
- `GET /translate/user/{user_id}/translations` - Get user's translations
- `GET /translate/download/{job_id}` - Download translated file
- `DELETE /translate/jobs/{job_id}` - Delete translation job

## Development

Start the development server:

```bash
npm run dev
```

Visit `http://localhost:4321` to see the application.

## Build and Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Cloudflare Pages

#### Option 1: Automatic Git Deployment

1. Push your code to GitHub/GitLab
2. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
3. Connect your repository
4. Use these build settings:
   - **Framework preset**: Astro
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Node.js version**: 18

#### Option 2: Wrangler CLI Deployment

```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Deploy
wrangler pages deploy dist
```

### Environment Variables for Production

Set these environment variables in your Cloudflare Pages dashboard:

```env
PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
PUBLIC_TRANSLATION_API_URL=https://your-api-domain.com
```

## Project Structure

```
src/
├── components/          # React components
│   ├── App.tsx         # Main app component
│   ├── AuthComponent.tsx    # Authentication UI
│   ├── FileUpload.tsx      # File upload and translation config
│   └── TranslationRuns.tsx # Translation history and status
├── layouts/            # Astro layouts
│   └── Layout.astro    # Main page layout
├── lib/               # Utility libraries
│   └── supabase.ts    # Supabase client configuration
├── pages/             # Astro pages
│   └── index.astro    # Homepage
├── client.tsx         # React client-side hydration
└── env.d.ts          # TypeScript environment declarations
```

## API Integration

The frontend communicates with your translation API backend through these main flows:

### Authentication Flow
1. User signs up/signs in with Supabase
2. User ID is used for all API calls
3. JWT tokens handle authentication

### Translation Flow
1. User uploads file and configures parameters
2. Frontend calls `POST /translate/start` with user ID
3. Backend starts translation job and returns job ID
4. Frontend polls job status and displays progress
5. When complete, user can download the translated file

### Data Flow
- **User Management**: Handled by Supabase Auth
- **Job Data**: Stored in your backend's Supabase database
- **File Storage**: Handled by your backend's Supabase Storage
- **Real-time Updates**: Polling-based status updates

## Features in Detail

### Authentication
- Email/password authentication via Supabase
- Persistent sessions with automatic refresh
- Secure sign-out functionality

### File Upload
- Drag & drop interface
- File type validation (TXT, MD, EPUB, PDF)
- Size limit validation
- Progress indicators

### Translation Configuration
- AI model selection (GPT-4, Claude, Gemini, etc.)
- Target language selection
- Advanced options (temperature, context, test mode)
- Parameter validation

### Job Management
- Real-time status polling
- Progress visualization
- Error handling and display
- Job history with timestamps

### File Downloads
- Secure signed URL downloads
- Automatic file naming
- Download progress indication

## Customization

### Styling
- Modify `tailwind.config.mjs` for custom colors and themes
- Edit component styles in individual `.tsx` files
- Add global styles in `Layout.astro`

### Components
- Extend existing components in `src/components/`
- Add new pages in `src/pages/`
- Configure API endpoints in `src/lib/supabase.ts`

### Features
- Add new AI models in `FileUpload.tsx`
- Add new languages in the language selector
- Extend job status polling logic
- Add file preview functionality

## Troubleshooting

### Common Issues

1. **Authentication not working**
   - Check Supabase URL and keys
   - Verify email authentication is enabled
   - Check browser console for errors

2. **API calls failing**
   - Verify translation API is running
   - Check CORS settings on backend
   - Verify API endpoint URLs

3. **File upload issues**
   - Check file size limits
   - Verify file types are supported
   - Check backend file handling

4. **Build errors**
   - Ensure Node.js version is 18+
   - Clear node_modules and reinstall
   - Check TypeScript configuration

### Debug Mode

Enable debug logging by setting:

```env
DEBUG=true
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues related to:
- **Frontend**: Check GitHub issues or create a new one
- **Backend API**: Refer to your translation API documentation
- **Supabase**: Check [Supabase documentation](https://supabase.com/docs)
- **Cloudflare Pages**: Check [Cloudflare Pages documentation](https://developers.cloudflare.com/pages/)