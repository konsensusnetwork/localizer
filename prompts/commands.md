# Commands

pdm run bbook_maker --book_name  books/tsi-fr/ch09.qmd --model openai --model_list o1 --prompt prompts/fr-translation.prompt.md --batch_size=50 --single_translate --language fr

pdm run bbook_maker --book_name  books/tsi-fi/ch09.qmd --model openai --model_list o3-mini --prompt prompts/fi-translation.prompt.md --batch_size=50 --single_translate --language fi


## TSI_FI


# BM_IT

pdm run bbook_maker --book_name  books/bm-it/ch01.qmd --model openai --model_list o3-mini --prompt prompts/it-translation.prompt.md --batch_size=5 --single_translate --language it
