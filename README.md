# CA4023 | Assignment 1 | Bigram Language Model

This is a bigram language model, which can:
- train a model on a given corpus of sentences
- determine the probability of given sentences occurring
- generate sentences

## Using the model

To run the model:

> git clone https://gitlab.computing.dcu.ie/fitzpai3/ca4023-assignment-1
> cd ca4023-assignment-1
> python3 bigram_language_model.py wikiOscars.txt wikiOscars_test.txt

- Providing the second file is optional
- All input files should be stored in the input folder

## Adjusting the parameters of the model

The settings of the model can be adjusted in the *main()* function of bigram_language_model.py

If *smooth* is set to False, the model will use **p(w2|w1)** to calculate probabilities.  
If *smooth* is set to True, the model will use **(0.5 * p(w2|w1)) + (0.5 * p(w1))**

If *use_log* is set to True, the model will calculate probabilities in log space.

If *generate_sentences* is set to True, the model will generate sentences, the number of which can be adjusted with the *to_be_generated* variable.

## Model Output

The model will output:
- language_model_output.txt
A file logging the settings used and files created.
- unigram_probabilities.txt
A file containing all unigrams and their probabilities in decreasing order.
- bigram_probabilities.txt
A file containing all bigrams and their probabilities in decreasing order.
- generated_sentences.txt
A file containing all generated sentences.

# Training corpus and appraisal of generated sentences.

I chose the [INQUISITIVE](https://github.com/wjko2/INQUISITIVE) corpus to train my model. This is a corpus of ~20,000 questions from readers as they read through 1,500 different articles. The total number of words in the corpus is 130,000.

Given that there are longer n-grams in longer sentences, my thinking in selecting this corpus was that as this was a bigram language model, it would perform better having been trained on smaller sentences, all of which were questions. However, the model still struggled to generate coherent sentences. I tried a diverse selection of other corpora, and looking at the generated sentences it seems likely to me that this level of performance is to be expected when using a bigram language model.

Many of the sentences generated are questions of similar length or slightly shorter to those in the corpus, but don't make any or much sense when read. You can see traces of the bigram model in the generated sentences, as quite often there are two words which make sense together, but the words surrounding that bigram are relatively unrelated. It would be interesting to see what questions would be generated if I had split the corpus into sections relating to individual articles. This way, the model would have the benefit of being trained on small questions about the same topic/article. 
