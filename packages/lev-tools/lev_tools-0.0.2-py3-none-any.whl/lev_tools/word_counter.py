import re

KEYWORDS_MAP = {
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
}


def get_words_from_line(line):
    return re.findall(r'\w+', line.lower())


def safe_list_get(list_, index, default_value=None):
    try:
        return list_[index]
    except IndexError:
        return default_value


def get_word_value(word, default_value=1):
    return KEYWORDS_MAP.get(word, default_value)


def do_relative_update_for_token(tokens, token, value, init_value=0):
    if token not in tokens:
        # Init a value for this token
        tokens[token] = init_value
    tokens[token] += value


def tokeniser(words):
    token_words = {}

    token_index = 0
    value_index = 1
    consecutive_keyword_penalty = 0

    while token_index < len(words):
        token_word = safe_list_get(words, token_index)
        token_word_value = get_word_value(token_word)

        value_word = safe_list_get(words, value_index)
        value_word_value = get_word_value(value_word)

        if token_word_value != 1:
            # Token word is keyword; move both indexes forward
            token_index += 1
            value_index += 1
        else:
            # Token word is word; update count, adjust indexes
            do_relative_update_for_token(
                tokens=token_words,
                token=token_word,
                value=value_word_value - consecutive_keyword_penalty
            )

            if value_word_value != 1:
                # Value word is keyword; look at future
                future_word = safe_list_get(words, value_index + 1)
                future_word_value = get_word_value(future_word)
                if future_word_value != 1:
                    # Future word is keyword; move the value index forward but enable the penalty
                    value_index += 1
                    consecutive_keyword_penalty = 1
                else:
                    # Future word is word; move the value index forward by two, token index just behind, disable penalty
                    value_index += 2
                    token_index = value_index - 1
                    consecutive_keyword_penalty = 0
            else:
                # Value word is word; move both indexes forward
                token_index += 1
                value_index += 1
    return token_words


def run(file_path):
    with open(file_path, 'r') as f:
        all_words = []
        for line in f.readlines():
            words = get_words_from_line(line)
            all_words += words
        tokenised = tokeniser(all_words)

    # Print top 5 from output sorted in reverse by value and then key
    for word, count in sorted(tokenised.items(), key=lambda item: (item[1], item[0]), reverse=True)[:5]:
        print(count, word)
