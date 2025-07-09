#!/usr/bin/env python3
"""
FastAPI Translation Service Startup Script

This script helps you start the translation service with proper configuration.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        ('fastapi', 'fastapi'),
        ('uvicorn', 'uvicorn'),
        ('python-multipart', 'multipart')
    ]
    
    missing = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print(f"❌ Missing required packages: {', '.join(missing)}")
        print("📦 Install them with: pip install -r fastapi_requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True


def check_environment():
    """Check environment configuration"""
    required_env = [
        'BBM_OPENAI_API_KEY',  # At least one translation model key should be set
    ]
    
    optional_env = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_KEY',
        'REDIS_URL'
    ]
    
    warnings = []
    
    # Check if at least one translation API key is set
    translation_keys = [
        'BBM_OPENAI_API_KEY',
        'BBM_CLAUDE_API_KEY',
        'BBM_GOOGLE_GEMINI_KEY',
        'BBM_GROQ_API_KEY',
        'BBM_XAI_API_KEY',
        'BBM_CAIYUN_API_KEY',
        'BBM_DEEPL_API_KEY'
    ]
    
    has_translation_key = any(os.getenv(key) for key in translation_keys)
    
    if not has_translation_key:
        warnings.append("⚠️  No translation API keys found. Set at least one in your .env file")
    else:
        print("✅ Translation API key(s) configured")
    
    # Check optional environment variables
    for key in optional_env:
        if not os.getenv(key):
            if key.startswith('SUPABASE'):
                warnings.append(f"⚠️  {key} not set - Supabase features will be disabled")
            elif key == 'REDIS_URL':
                warnings.append(f"⚠️  {key} not set - Celery workers will not be available")
    
    if warnings:
        print("\nEnvironment warnings:")
        for warning in warnings:
            print(warning)
        print("\n💡 The service will run in development mode with limited features")
        print("💡 See .env.example for configuration options")
    else:
        print("✅ Environment fully configured")
    
    return True


def create_directories():
    """Create required directories"""
    dirs = [
        'uploads',
        'logs',
        'tmp'
    ]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 Created directory: {dir_name}")


def start_fastapi(host='0.0.0.0', port=8000, workers=1, reload=False):
    """Start the FastAPI server"""
    print(f"🚀 Starting FastAPI server on {host}:{port}")
    
    # Check if frontend exists
    frontend_path = Path("frontend/index.html")
    if frontend_path.exists():
        print("📱 Frontend dashboard will be available at:")
        print(f"   🌐 http://{host}:{port}/")
        print(f"   📊 http://{host}:{port}/dashboard")
    else:
        print("⚠️  Frontend not found - API only mode")
    
    print(f"📚 API documentation: http://{host}:{port}/docs")
    
    cmd = [
        'uvicorn',
        'my_app.main:app',
        '--host', host,
        '--port', str(port)
    ]
    
    if workers > 1:
        cmd.extend(['--workers', str(workers)])
    
    if reload:
        cmd.append('--reload')
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


def start_celery():
    """Start Celery worker"""
    print("🔄 Starting Celery worker")
    
    if not os.getenv('REDIS_URL'):
        print("❌ REDIS_URL not configured. Cannot start Celery worker.")
        return False
    
    cmd = [
        'celery',
        '-A', 'my_app.workers.tasks',
        'worker',
        '--loglevel=info'
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Celery worker stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Celery worker: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(description='Start the FastAPI Translation Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to')
    parser.add_argument('--workers', type=int, default=1, help='Number of worker processes')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    parser.add_argument('--celery', action='store_true', help='Start Celery worker instead of FastAPI')
    parser.add_argument('--check-only', action='store_true', help='Only check configuration, don\'t start service')
    
    args = parser.parse_args()
    
    print("🔍 FastAPI Translation Service Startup")
    print("=" * 50)
    
    # Load environment variables from .env file if it exists
    env_file = Path('.env')
    if env_file.exists():
        print("📄 Loading environment from .env file")
        from dotenv import load_dotenv
        load_dotenv()
    else:
        print("⚠️  No .env file found - using system environment variables")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    check_environment()
    
    # Create directories
    create_directories()
    
    if args.check_only:
        print("\n✅ Configuration check complete")
        return
    
    print("\n" + "=" * 50)
    
    if args.celery:
        start_celery()
    else:
        start_fastapi(args.host, args.port, args.workers, args.reload)


if __name__ == '__main__':
    main()