import re
import math
import random
import sys

def load_file(filename):

    with open(filename) as file:
        lowercase_file = [line.lower() for line in file]
        sentences = [re.split(r'\s+', line.strip('\n"')) for line in lowercase_file]

        for sentence in sentences:
            if sentence[0] != '<s>':
                sentence.insert(0, '<s>')
            if sentence[-1] != '</s>':
                sentence.append('</s>')
        return sentences


def calculate_counts(text_data):

    unigrams = []
    bigrams = []
    unigram_counts = {}
    bigram_counts = {}
    word_count = 0

    for sentence in text_data:
        for i in range(len(sentence) - 1):

            unigrams.append(sentence[i])
            bigrams.append((sentence[i], sentence[i + 1]))

            if (sentence[i], sentence[i + 1]) in bigram_counts:
                bigram_counts[(sentence[i], sentence[i + 1])] += 1
            else:
                bigram_counts[(sentence[i], sentence[i + 1])] = 1

        unigrams.append(sentence[i + 1])

        for i in range(len(sentence)):
            if sentence[i] in unigram_counts:
                unigram_counts[sentence[i]] += 1
            else:
                unigram_counts[sentence[i]] = 1

            word_count += 1

    return unigrams, bigrams, bigram_counts, unigram_counts, word_count


def calculate_unigram_probabilities(unigrams, unigram_counts, word_count):

    probabilities = {}
    for unigram in unigrams:
        probabilities[unigram] = float(unigram_counts[unigram] / word_count)

    return probabilities


def calculate_bigram_probabilities(bigrams, bigram_counts, unigram_counts, unigram_probabilities, smooth):

    probabilities = {}
    for bigram in bigrams:
        word_1 = bigram[0]

        if bigram in bigram_counts and word_1 in unigram_counts:
            probabilities[bigram] = float(bigram_counts[bigram] / unigram_counts[word_1])
        else:
            probabilities[bigram] = 0

        if smooth:
            if word_1 in unigram_counts:
                probabilities[bigram] = (0.5 * probabilities[bigram]) + (0.5 * unigram_probabilities[word_1])
            else:
                probabilities[bigram] = 0.5 * probabilities[bigram]

    return probabilities


def calculate_sentence_probability(sentence, unigram_counts, bigram_counts, unigram_probabilities, word_count, smooth, use_log):

    sentence_probability = 1
    if use_log:
        sentence_probability = 0

    for i in range(len(sentence) - 1):

        bigram_probability = calculate_bigram_probabilities([(sentence[i], sentence[i + 1])], bigram_counts, unigram_counts, unigram_probabilities, smooth)
        bigram_probability = bigram_probability[(sentence[i], sentence[i + 1])]

        if use_log:
            sentence_probability += math.log(bigram_probability, 2)
        else:
            sentence_probability *= bigram_probability

    if use_log:
        return math.pow(2, sentence_probability)
    else:
        return sentence_probability


def augment_sentence(bigram_counts, unigram_counts, unigram_probabilities, smooth, word_count):

    sentence = '<s>'
    previous_word = '<s>'
    while previous_word != '</s>':
        potential_successors = {}
        for bigram in list(bigram_counts.keys()):
            if previous_word == bigram[0]:
                successor = bigram[1]

                bigram_probability = calculate_bigram_probabilities([(previous_word, successor)], bigram_counts, unigram_counts, unigram_probabilities, smooth=True)
                bigram_probability = bigram_probability[(previous_word, successor)]
                potential_successors[successor] = bigram_probability

        divisor = sum(potential_successors.values())
        for successor in potential_successors:
            potential_successors[successor] = potential_successors[successor] / divisor

        next_word = random.choices(list(potential_successors.keys()), weights = potential_successors.values(), k = 1)[0]
        sentence = sentence + ' ' + next_word
        previous_word = next_word

    if previous_word != '</s>':
        sentence = sentence + ' </s>'

    return sentence


def main():
    smooth = True
    use_log = True
    generate_sentences = True
    to_be_generated = 100

    corpus = load_file(f'input/{sys.argv[1]}')


    if len(sys.argv) == 3:
        given_sentences = load_file(f'input/{sys.argv[2]}')
    else:
        given_sentences = False

    unigrams, bigrams, bigram_counts, unigram_counts, word_count = calculate_counts(corpus)

    unigram_probabilities = calculate_unigram_probabilities(unigrams, unigram_counts, word_count)
    bigram_probabilities = calculate_bigram_probabilities(bigrams, bigram_counts, unigram_counts, unigram_probabilities, smooth)

    if given_sentences:
        given_sentence_probabilities = {}
        for sentence in given_sentences:
            probability = calculate_sentence_probability(sentence, unigram_counts, bigram_counts, unigram_probabilities, word_count, smooth, use_log)
            full_sentence = ' '.join(sentence)
            given_sentence_probabilities[full_sentence] = probability

    if generate_sentences:
        generated_sentences = []
        i = 0
        while i < to_be_generated:
            augmented_sentence = augment_sentence(bigram_counts, unigram_counts, unigram_probabilities, smooth, word_count)
            generated_sentences.append(augmented_sentence)
            i += 1

    # Below is the code to handle output.
    main_file_output = []
    main_file_output.append('Bigram Language Model\n')
    main_file_output.append('Smoothing: ' + str(smooth))
    main_file_output.append('Use Log Probabilities: ' + str(use_log))
    main_file_output.append(f'Unigrams by decreasing probability can be found in unigram_probabilities.txt')
    main_file_output.append(f'Bigrams by decreasing probability can be found in bigram_probabilities.txt')
    if generate_sentences:
        main_file_output.append(f'Generated {to_be_generated} sentences')
        main_file_output.append(f'These can be found in generated_sentences.txt')
    else:
        main_file_output.append('Sentence Generation Off\n')
    if given_sentences:
        main_file_output.append('-' * 45)
        main_file_output.append('Given sentences and their probabilities:')
        main_file_output.append('-' * 45 + '\n')
        for given_sentence in given_sentence_probabilities:
            main_file_output.append(given_sentence + ' has probability ' + str(given_sentence_probabilities[given_sentence]) + ' of occuring')

    unigram_file_output = []
    unigram_file_output.append('-' * 35)
    unigram_file_output.append('Unigrams and their probabilities:')
    unigram_file_output.append('-' * 35 + '\n')
    unigram_probabilities = dict(sorted(unigram_probabilities.items(), key=lambda item: item[1], reverse=True))
    for unigram in unigram_probabilities:
        unigram_file_output.append(unigram + ' has probability ' + str(unigram_probabilities[unigram]))

    bigram_file_output = []
    bigram_file_output.append('-' * 35)
    bigram_file_output.append('Bigrams and their probabilities:')
    bigram_file_output.append('-' * 35 + '\n')
    bigram_probabilities = dict(sorted(bigram_probabilities.items(), key=lambda item: item[1], reverse=True))
    for bigram in bigram_probabilities:
        bigram_file_output.append(str(bigram) + ' has probability ' + str(bigram_probabilities[bigram]))

    if generate_sentences:
        generate_file_output = []
        generate_file_output.append('-' * 20)
        generate_file_output.append('Generated Sentences')
        generate_file_output.append('-' * 20 + '\n')
        for sentence in generated_sentences:
            generate_file_output.append(sentence)

    with open('output/language_model_output.txt', 'w') as txt_file:
        for line in main_file_output:
            txt_file.write(line + '\n')

    with open('output/bigram_probabilities.txt', 'w') as txt_file:
        for line in bigram_file_output:
            txt_file.write(line + '\n')

    with open('output/unigram_probabilities.txt', 'w') as txt_file:
        for line in unigram_file_output:
            txt_file.write(line + '\n')

    if generate_sentences:
        with open('output/generated_sentences.txt', 'w') as txt_file:
            for line in generate_file_output:
                txt_file.write(line + '\n')


if __name__ == '__main__':
    main()
