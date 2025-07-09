# Translation UI Updates

## Summary of Changes

I've successfully updated the translation service frontend and backend according to your requirements. Here are the implemented changes:

## Frontend Changes (frontend/index.html)

### 1. Translation Models
- **Removed**: Claude option
- **Kept**: Only OpenAI and Gemini as translation model options
- **Note**: Optional model list functionality is preserved

### 2. Target Languages
- **Updated** language dropdown to include:
  - Dutch (nl)
  - French (fr) 
  - Finnish (fi)
  - Italian (it)
  - Spanish (es)
  - English (en)
  - **Other (Custom)** - allows users to input any custom language code

### 3. Prompt File Selection
- **Added**: Language-conditional prompt file dropdown
- **Feature**: Automatically loads available prompt files when a language is selected
- **Location**: Looks in both `prompts/{language}/` subdirectories and root `prompts/` directory
- **Display**: Shows user-friendly names (removes language prefix and .prompt.md extension)

### 4. Prompt Preview
- **Added**: Live preview functionality in the custom prompt textarea
- **Behavior**: When a prompt file is selected, its content is loaded and displayed
- **Fallback**: Users can still enter custom prompts manually
- **Smart**: Preserves custom text if user has manually entered content

### 5. UI Improvements
- **Removed**: Temperature control field
- **Expanded**: Custom prompt textarea from 3 to 8 rows for better prompt viewing
- **Updated**: Placeholder text to guide users about prompt file selection
- **Added**: Custom language input field with conditional display and validation

### 6. Custom Language Support
- **Dynamic Input**: When "Other (Custom)" is selected, a text input field appears
- **Validation**: Ensures custom language code is provided when custom option is selected
- **Prompt Compatibility**: Custom languages can still load prompt files if they exist
- **Graceful Fallback**: Shows "no prompts found" message for unsupported custom languages
- **Smart Detection**: Uses `getCurrentLanguage()` function throughout the app

### 7. Form Submission
- **Removed**: Temperature parameter from form data (backend uses default value of 1.0)
- **Enhanced**: Language validation ensures either predefined or custom language is selected
- **Maintained**: All other functionality intact

## Backend Changes (my_app/routers/translate.py)

### 1. New API Endpoints

#### GET /translate/prompts/{language}
- Lists available prompt files for a specific language
- Searches both language-specific directories and root prompts directory
- Returns JSON with array of prompt filenames

#### GET /translate/prompts/{language}/{prompt_file}
- Returns the content of a specific prompt file
- Tries language directory first, falls back to root directory
- Returns plain text content of the prompt file

### 2. Updated Translation Endpoints
- **Removed**: Temperature parameter from `/start` and `/upload-and-translate` endpoints
- **Default**: Backend now uses temperature=1.0 as default value
- **Maintained**: All other parameters and functionality

### 3. Updated Data Models
- **Modified**: TranslationRequest class to use default temperature value
- **Maintained**: All other configuration options

## File Structure Requirements

The prompt file system expects this structure:
```
prompts/
├── nl/                          # Dutch prompts
│   ├── nl-translation.prompt.md
│   └── nl-edit.prompt.md
├── fr/                          # French prompts
│   ├── fr-translation.prompt.md
│   └── fr-edit.prompt.md
├── fi/                          # Finnish prompts
├── it/                          # Italian prompts
├── es/                          # Spanish prompts
├── en/                          # English prompts
└── {language}-*.prompt.md       # Root level language-specific files
```

## Key Features

1. **Simplified Model Selection**: Only OpenAI and Gemini options
2. **Targeted Language Support**: Focused on the 6 specified languages
3. **Smart Prompt Loading**: Automatic discovery and loading of language-specific prompts
4. **Live Preview**: See prompt content before starting translation
5. **Backward Compatibility**: Existing translation functionality preserved
6. **Error Handling**: Graceful fallbacks when prompt files aren't found

## JavaScript Functions Added

- `handleLanguageChange()` - Manages language dropdown changes and custom input visibility
- `getCurrentLanguage()` - Returns the current language (predefined or custom)
- Updated `loadPromptFiles()` - Uses current language for prompt file discovery  
- Updated `loadPromptPreview()` - Uses current language for prompt content loading

## Testing

- ✅ Backend syntax validation passed
- ✅ Frontend JavaScript functions implemented and validated
- ✅ Custom language functionality tested
- ✅ API endpoints structured correctly
- ✅ Form submission updated appropriately

## User Experience Improvements

1. **Streamlined Workflow**: Fewer model options reduce decision complexity
2. **Language-Specific Prompts**: Automatically shows relevant prompts for selected language
3. **Visual Feedback**: Large textarea provides better prompt preview experience
4. **Progressive Enhancement**: Prompt files are optional - users can still enter custom prompts
5. **Clean Interface**: Removed temperature reduces interface complexity
6. **Flexible Language Support**: Users can choose from predefined languages or enter custom ones
7. **Smart UI**: Custom language input appears only when needed, with helpful placeholder text
8. **Robust Validation**: Clear error messages guide users to complete required fields

The implementation maintains all existing functionality while adding the requested features in a user-friendly way. 