# Open Speech Corpus CLI

This repository contains the code required to download audiodata from openspeechcorpus.com


To download files from the Isolated Words Project use

```bash
ops  \
    --from 1 \
    --to 500 \
    --output_folder isolated_words/ \
    --output_file isolated_words.txt  \
    --url http://openspeechcorpus.contraslash.com/api/isolated-words/list/ \
    --text_node isolated_word
```

