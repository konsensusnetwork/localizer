# Commands

## Formatting texts to quarto

pdm run bbook_maker --book_name books/formatter/21F2_EN_test.md --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/formatter.prompt.md --batch_size=12 --single_translate --language en

## TSI_FI

# BM_IT

pdm run bbook_maker --book_name books/bm-it/ch01.qmd --model openai --model_list o3-mini --prompt prompts/it-translation.prompt.md --batch_size=5 --single_translate --language it

# BM_NL

pdm run bbook_maker --book_name books/bm-nl/ch09.qmd --model openai --model_list o3-mini --prompt prompts/nl/nl-edit-o3.prompt.md --batch_size=5 --single_translate --language nl --use_context --reasoning_effort=high

pdm run bbook_maker --book_name books/tsi-nl/ch01.qmd --model openai --model_list o3-mini --prompt prompts/nl/nl-edit-o3.prompt.md --batch_size=5 --single_translate --language nl --use_context --reasoning_effort=high

## 21FFF_FR

### Run 1

pdm run dir_process books/21fff/fr --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/fr-translation-2.prompt.md --batch_size=5 --single_translate --language fr

### Run 2

pdm run dir_process books/21fff/fr/to-edit --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/fr-edit-2.prompt.md --batch_size=5 --single_translate --language fr

## 21FFF_ES

pdm run dir_process books/21fff/es --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/es-translation-prompt.md --batch_size=5 --single_translate --language es

pdm run dir_process books/21fff/es/to-edit --model openai --model_list o3-mini --reasoning_effort=high --prompt prompts/es/es-edit.prompt.md --batch_size=5 --single_translate --language es

# Using Gemini to translate

python3 make_book.py --book_name test_books/animal_farm.epub --model gemini --language nl

pdm run bbook_maker --book_name books/tsi-nl/ch02.qmd --model gemini  --prompt prompts/nl/nl-translation-tsi.prompt.md --batch_size=5 --single_translate --language nl --gemini_key AIzaSyA1ZHnMzY6F4vn7JA8QJ6UJXwUvMe2pnfU --model_list gemini-2.5-pro-preview-06-05

pdm run bbook_maker --book_name books/bm-al/ch00.md --model gemini --prompt prompts/al-translation.prompt.md --batch_size=5 --single_translate --language Albanian --gemini_key AIzaSyA1ZHnMzY6F4vn7JA8QJ6UJXwUvMe2pnfU --model_list gemini-2.5-pro-preview-06-05

pdm run dir_process books/bm-it/todo --model gemini --prompt prompts/it-translation-2.prompt.md --batch_size=5 --single_translate --language it --gemini_key AIzaSyA1ZHnMzY6F4vn7JA8QJ6UJXwUvMe2pnfU --model_list gemini-2.5-pro-preview-06-05