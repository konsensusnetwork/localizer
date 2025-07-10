#!/usr/bin/env python3
"""
Environment Setup Script for Bilingual Book Maker Tests
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check the current environment setup"""
    print("🔍 Checking environment setup...")
    
    # Check API keys
    openai_key = os.getenv("BBM_OPENAI_API_KEY")
    gemini_key = os.getenv("BBM_GOOGLE_GEMINI_KEY")
    
    print(f"API Keys:")
    print(f"  BBM_OPENAI_API_KEY: {'✅ Set' if openai_key else '❌ Not set'}")
    print(f"  BBM_GOOGLE_GEMINI_KEY: {'✅ Set' if gemini_key else '❌ Not set'}")
    
    # Check .env file
    env_file = Path('.env')
    if env_file.exists():
        print(f"  .env file: ✅ Found")
    else:
        print(f"  .env file: ❌ Not found")
    
    # Check test books
    print(f"\nTest Books:")
    test_books = {
        "epub": "test_books/animal_farm.epub",
        "txt": "test_books/the_little_prince.txt",
        "srt": "test_books/Lex_Fridman_episode_322.srt"
    }
    
    for book_type, book_path in test_books.items():
        if Path(book_path).exists():
            print(f"  {book_type}: ✅ Found")
        else:
            print(f"  {book_type}: ❌ Missing")
    
    # Check test prompts
    print(f"\nTest Prompts:")
    test_prompts = {
        "en": "prompts/en/en-translation.prompt.md",
        "fr": "prompts/fr/fr-translation-1.prompt.md",
        "it": "prompts/it/it-translation.prompt.md"
    }
    
    for prompt_type, prompt_path in test_prompts.items():
        if Path(prompt_path).exists():
            print(f"  {prompt_type}: ✅ Found")
        else:
            print(f"  {prompt_type}: ❌ Missing")
    
    # Summary
    print(f"\n📊 Summary:")
    if openai_key or gemini_key:
        print(f"  ✅ API keys available - tests can run")
    else:
        print(f"  ❌ No API keys found - tests will be skipped")
    
    if all(Path(book_path).exists() for book_path in test_books.values()):
        print(f"  ✅ All test books available")
    else:
        print(f"  ⚠️  Some test books missing")
    
    if all(Path(prompt_path).exists() for prompt_path in test_prompts.values()):
        print(f"  ✅ All test prompts available")
    else:
        print(f"  ⚠️  Some test prompts missing")

def create_env_template():
    """Create a template .env file"""
    env_content = """# Bilingual Book Maker API Keys
# Get your OpenAI API key from: https://platform.openai.com/account/api-keys
BBM_OPENAI_API_KEY=sk-your-openai-key-here

# Get your Gemini API key from: https://makersuite.google.com/app/apikey
BBM_GOOGLE_GEMINI_KEY=your-gemini-key-here

# Optional: Custom API base URL (for Azure, etc.)
# BBM_OPENAI_API_BASE=https://your-endpoint.openai.azure.com/

# Optional: Deployment ID (for Azure)
# BBM_OPENAI_DEPLOYMENT_ID=your-deployment-name
"""
    
    env_file = Path('.env')
    if env_file.exists():
        print(f"⚠️  .env file already exists. Backing up to .env.backup")
        env_file.rename('.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"✅ Created .env template file")
    print(f"📝 Please edit .env and add your actual API keys")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--create-env":
        create_env_template()
        return
    
    check_environment()
    
    print(f"\n🚀 Next steps:")
    print(f"  1. If no API keys are set, run: python tests/setup_env.py --create-env")
    print(f"  2. Edit .env file with your actual API keys")
    print(f"  3. Run tests: pdm run test-examples")
    print(f"  4. Or run specific tests: pdm run test-examples-basic")

if __name__ == "__main__":
    main() 