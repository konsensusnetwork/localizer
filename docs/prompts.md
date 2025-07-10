# Prompt Customization Guide

This guide explains how to create and use custom translation prompts to achieve specific translation styles and requirements.

## Overview

The Bilingual Book Maker supports custom prompts in multiple formats:
- Simple text templates
- JSON configuration files
- PromptDown markdown files
- Environment variables

## Basic Prompt Structure

### Simple Text Template

```bash
--prompt "Translate {text} to {language} in a formal academic style"
```

**Placeholders:**
- `{text}` - The content to translate
- `{language}` - Target language
- `{crlf}` - Line break (optional)

### JSON Configuration

```json
{
  "system": "You are a professional translator specializing in academic texts.",
  "user": "Translate {text} to {language} maintaining formal academic style."
}
```

### PromptDown Format

```markdown
# Academic Translation Prompt

## Developer Message
You are a professional translator specializing in academic texts.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate {text} to {language} maintaining formal academic style. |
```

## Language-Specific Prompts

### Chinese Translation

#### Simplified Chinese (zh-hans)
```bash
--prompt "将以下文本翻译成简体中文，保持原文的学术风格和准确性：{text}"
```

#### Traditional Chinese (zh-hant)
```bash
--prompt "將以下文本翻譯成繁體中文，保持原文的學術風格和準確性：{text}"
```

### Japanese Translation

```bash
--prompt "以下のテキストを日本語に翻訳し、原文の学術的スタイルと正確性を保持してください：{text}"
```

### Korean Translation

```bash
--prompt "다음 텍스트를 한국어로 번역하고 원문의 학술적 스타일과 정확성을 유지하세요：{text}"
```

### European Languages

#### French
```bash
--prompt "Traduisez le texte suivant en français en conservant le style académique et la précision du texte original : {text}"
```

#### German
```bash
--prompt "Übersetzen Sie den folgenden Text ins Deutsche und bewahren Sie dabei den akademischen Stil und die Genauigkeit des Originals : {text}"
```

#### Spanish
```bash
--prompt "Traduzca el siguiente texto al español manteniendo el estilo académico y la precisión del texto original : {text}"
```

#### Italian
```bash
--prompt "Traduca il seguente testo in italiano mantenendo lo stile accademico e la precisione del testo originale : {text}"
```

## Style-Specific Prompts

### Academic Translation

```json
{
  "system": "You are a professional academic translator with expertise in scholarly texts. Maintain formal academic style, preserve technical terminology, and ensure accuracy.",
  "user": "Translate the following academic text to {language}, maintaining formal academic style and preserving all technical terminology: {text}"
}
```

### Creative Writing Translation

```json
{
  "system": "You are a literary translator specializing in creative works. Preserve the emotional tone, cultural nuances, and artistic style of the original text.",
  "user": "Translate this creative text to {language}, preserving the poetic and emotional tone while adapting cultural references appropriately: {text}"
}
```

### Technical Documentation

```json
{
  "system": "You are a technical translator specializing in documentation and manuals. Maintain precise technical terminology and clear instructional style.",
  "user": "Translate this technical documentation to {language}, maintaining precise technical terminology and clear step-by-step instructions: {text}"
}
```

### Legal Translation

```json
{
  "system": "You are a legal translator with expertise in legal documents. Maintain formal legal language and preserve exact meaning of legal terms.",
  "user": "Translate this legal document to {language}, maintaining formal legal language and preserving the exact meaning of all legal terms: {text}"
}
```

### Medical Translation

```json
{
  "system": "You are a medical translator with expertise in healthcare documentation. Maintain precise medical terminology and ensure accuracy for patient safety.",
  "user": "Translate this medical text to {language}, maintaining precise medical terminology and ensuring accuracy for patient safety: {text}"
}
```

## File-Based Prompts

### Text File Prompts

Create a text file with your prompt:

```bash
# academic_prompt.txt
Translate the following academic text to {language}, maintaining formal academic style and preserving all technical terminology: {text}
```

Use it:
```bash
--prompt academic_prompt.txt
```

### JSON File Prompts

Create a JSON file with system and user messages:

```json
# creative_prompt.json
{
  "system": "You are a literary translator specializing in creative works.",
  "user": "Translate this creative text to {language}, preserving the poetic and emotional tone: {text}"
}
```

Use it:
```bash
--prompt creative_prompt.json
```

### PromptDown File Prompts

Create a markdown file with PromptDown format:

```markdown
# Technical Translation Prompt

## Developer Message
You are a technical translator specializing in documentation and manuals.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate this technical documentation to {language}, maintaining precise technical terminology: {text} |
```

Use it:
```bash
--prompt technical_prompt.md
```

## Environment Variable Prompts

Set prompts using environment variables:

```bash
# Set user message template
export BBM_CHATGPTAPI_USER_MSG_TEMPLATE="Translate {text} to {language} in a formal style"

# Set system message
export BBM_CHATGPTAPI_SYS_MSG="You are a professional translator"

# Run without --prompt argument
python3 make_book.py --book_name book.epub --model openai --language fr
```

## Advanced Prompt Techniques

### Context-Aware Prompts

```json
{
  "system": "You are a translator working on a novel. Maintain consistency with previous translations and character names.",
  "user": "Translate this passage to {language}, maintaining consistency with the story context and character names: {text}"
}
```

### Style-Specific Instructions

```json
{
  "system": "You are a translator specializing in formal business documents.",
  "user": "Translate this business document to {language} using formal business language and maintaining professional tone: {text}"
}
```

### Cultural Adaptation Prompts

```json
{
  "system": "You are a cultural translator who adapts content appropriately for the target culture while preserving the original meaning.",
  "user": "Translate this text to {language}, adapting cultural references appropriately while preserving the original meaning: {text}"
}
```

### Quality Control Prompts

```json
{
  "system": "You are a professional translator and editor. Translate accurately, then review and improve the translation.",
  "user": "Translate {text} to {language}, then review and improve the translation for accuracy and fluency."
}
```

## Prompt Examples by Use Case

### 1. Academic Papers

```markdown
# Academic Translation Prompt

## Developer Message
You are a professional academic translator with expertise in scholarly texts. Your translations must maintain formal academic style, preserve technical terminology, and ensure accuracy.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate the following academic text to {language}, maintaining formal academic style and preserving all technical terminology, citations, and references: {text} |
```

### 2. Fiction and Literature

```markdown
# Literary Translation Prompt

## Developer Message
You are a literary translator specializing in creative works. Preserve the emotional tone, cultural nuances, and artistic style of the original text.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate this creative text to {language}, preserving the poetic and emotional tone while adapting cultural references appropriately: {text} |
```

### 3. Technical Manuals

```markdown
# Technical Translation Prompt

## Developer Message
You are a technical translator specializing in documentation and manuals. Maintain precise technical terminology and clear instructional style.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate this technical documentation to {language}, maintaining precise technical terminology and clear step-by-step instructions: {text} |
```

### 4. Business Documents

```markdown
# Business Translation Prompt

## Developer Message
You are a business translator specializing in formal business documents. Use appropriate business terminology and maintain professional tone.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate this business document to {language} using formal business language and maintaining professional tone: {text} |
```

### 5. Medical Documents

```markdown
# Medical Translation Prompt

## Developer Message
You are a medical translator with expertise in healthcare documentation. Maintain precise medical terminology and ensure accuracy for patient safety.

## Conversation

| Role  | Content                                           |
|-------|---------------------------------------------------|
| User  | Translate this medical text to {language}, maintaining precise medical terminology and ensuring accuracy for patient safety: {text} |
```

## Best Practices

### 1. Be Specific
```bash
# Good
--prompt "Translate to {language} maintaining formal academic style and preserving technical terminology: {text}"

# Better
--prompt "Translate this academic paper to {language}, maintaining formal academic style, preserving all technical terminology, citations, and mathematical notation: {text}"
```

### 2. Include Context
```bash
--prompt "You are translating a novel. Maintain consistency with character names and story context. Translate to {language}: {text}"
```

### 3. Specify Style Requirements
```bash
--prompt "Translate to {language} using formal business language, avoiding colloquialisms, and maintaining professional tone: {text}"
```

### 4. Consider Cultural Adaptation
```bash
--prompt "Translate to {language}, adapting cultural references appropriately while preserving the original meaning and intent: {text}"
```

### 5. Quality Control
```bash
--prompt "Translate {text} to {language}, then review and improve the translation for accuracy, fluency, and naturalness."
```

## Testing Prompts

### 1. Test with Small Sample
```bash
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_KEY \
  --prompt "your_custom_prompt.md" \
  --test \
  --test_num 3 \
  --language zh-hans
```

### 2. Compare Different Prompts
```bash
# Test academic prompt
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_KEY \
  --prompt "prompts/academic_prompt.md" \
  --test \
  --language fr

# Test creative prompt
python3 make_book.py \
  --book_name test_books/animal_farm.epub \
  --model openai \
  --openai_key YOUR_KEY \
  --prompt "prompts/creative_prompt.md" \
  --test \
  --language fr
```

## Prompt Validation

The system validates prompts to ensure they contain required placeholders:

### Required Placeholders
- `{text}` - The content to translate
- `{language}` - Target language

### Optional Placeholders
- `{crlf}` - Line break

### Validation Errors
```
ValueError: prompt must contain `{text}` placeholder
ValueError: Invalid placeholders found in user message
```

## Troubleshooting Prompts

### Issue: "Invalid placeholders"
**Solution:**
- Only use `{text}`, `{language}`, and `{crlf}` placeholders
- Check for typos in placeholder names

### Issue: "Prompt file not found"
**Solution:**
- Check file path is correct
- Ensure file has proper extension (.txt, .json, .md)

### Issue: "JSON parsing error"
**Solution:**
- Validate JSON syntax
- Check for missing quotes or commas
- Use a JSON validator

### Issue: "PromptDown parsing error"
**Solution:**
- Check markdown syntax
- Ensure proper table format
- Verify developer message format

## Next Steps

- **[Command Reference](./cmd.md)** - Complete CLI documentation
- **[Examples](./commands_examples.md)** - Real-world usage scenarios
- **[Troubleshooting](./troubleshooting.md)** - Common issues and solutions 