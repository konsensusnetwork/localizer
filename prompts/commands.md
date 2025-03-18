# Commands

pdm run bbook_maker --book_name  books/tsi-fr/ch09.qmd --model openai --model_list o1 --prompt prompts/fr-translation.prompt.md --batch_size=50 --single_translate --language fr

pdm run bbook_maker --book_name  books/tsi-fi/ch09.qmd --model openai --model_list o3-mini --prompt prompts/fi-translation.prompt.md --batch_size=50 --single_translate --language fi

## TSI_FI
pdm run bbook_maker --book_name  books/tsi-fi/ch05.qmd --model openai --model_list o3-mini --prompt prompts/fi-translation-2.prompt.md --batch_size=5 --single_translate --language fi

# BM_IT

pdm run bbook_maker --book_name  books/bm-it/ch01.qmd --model openai --model_list o3-mini --prompt prompts/it-translation.prompt.md --batch_size=5 --single_translate --language it

# BM_NL

pdm run bbook_maker --book_name  books/bm-nl/todo/ch20.qmd --model openai --model_list o3-mini --prompt prompts/nl-edit-o3.prompt.md --batch_size=5 --single_translate --language nl --use_context
