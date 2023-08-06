from unittest import TestCase
from pytest import raises

from dphon.lib import Comparator, Match


class TestNgrams(TestCase):

    def test_number_of_ngrams(self):
        a = '天下皆知美之為美，斯惡已。'
        # ignore punctuation, we should get 8 4-grams here
        ngrams = Comparator.get_text_ngrams(a, n=4)
        assert len(ngrams) == 8
        # if we push n up to 11, there is only one "gram"
        ngrams = Comparator.get_text_ngrams(a, n=11)
        assert len(ngrams) == 1
        # if n is longer than the number of possible ngrams, output is empty
        ngrams = Comparator.get_text_ngrams(a, n=100)
        assert len(ngrams) == 0
        # if n is negative, we should get a ValueError
        with raises(ValueError):
            ngrams = Comparator.get_text_ngrams(a, n=-4)

    def test_ngram_start_end(self):
        a = '天下皆知美之為美，斯惡已。'
        ngrams = Comparator.get_text_ngrams(a, n=4)
        # check an ngram with no punctuation
        assert ngrams[0]['start'] == 0
        assert ngrams[0]['end'] == 3
        # check one that has punctuation inside it
        assert ngrams[-1]['start'] == 7
        assert ngrams[-1]['end'] == 11

    def test_ngram_text_punctuation(self):
        a = '天下皆知美之為美，斯惡已。'
        ngrams = Comparator.get_text_ngrams(a, n=4)
        # check an ngram text to make sure no punctuation
        assert '。' not in ngrams[-1]['text']
        assert '，' not in ngrams[-1]['text']

    def test_ngram_tokenizes_known_char(self):
        a = '天下皆知美之為美，斯惡已。'
        ngrams = Comparator.get_text_ngrams(a, n=4)
        # in our dictionary, 皆 becomes 示
        assert '皆' not in ngrams[0]['text']
        assert '示' in ngrams[0]['text']

    def test_ngram_text_unknown_char(self):
        a = '驫'
        ngrams = Comparator.get_text_ngrams(a, n=1)
        # as 驫 not in dictionary, it should remain unchanged
        assert '驫' in ngrams[0]['text']


class TestInitialMatches(TestCase):

    def test_matches_trigrams(self):
        a = '孔於鄉黨孔孔孔孔孔孔孔孔孔孔孔孔孔孔'
        b = '其其其其其其其其其其鴉羕上其其其其其'
        comp = Comparator(a, b, 'a', 'b')
        matches = comp.get_initial_matches()
        # in these fake texts there is exactly one match
        assert len(matches) == 1
        assert matches[0].a_start == 1
        assert matches[0].a_end == 3
        assert matches[0].b_start == 10
        assert matches[0].b_end == 12

    def test_matches_quadgrams(self):
        a = '孔於鄉黨於孔孔孔孔孔孔孔孔孔'
        b = '其其鴉羕上鴉其其其其其'
        comp = Comparator(a, b, 'a', 'b')
        matches = comp.get_initial_matches(n=4)
        # exactly one quad-gram match
        assert len(matches) == 1
        assert matches[0].a_start == 1
        assert matches[0].a_end == 4
        assert matches[0].b_start == 2
        assert matches[0].b_end == 5

    def test_overlapping_matches(self):
        a = '孔於鄉黨於孔孔孔孔孔孔孔孔孔'
        b = '其其鴉羕上鴉其其其其其'
        comp = Comparator(a, b, 'a', 'b')
        matches = comp.get_initial_matches()
        # two overlapping trigram matches
        assert len(matches) == 2
        assert matches[0].a_start == 1
        assert matches[0].a_end == 3
        assert matches[0].b_start == 2
        assert matches[0].b_end == 4
        assert matches[1].a_start == 2
        assert matches[1].a_end == 4
        assert matches[1].b_start == 3
        assert matches[1].b_end == 5

    def test_partial_overlap(self):
        a = '孔於鄉黨於孔孔孔孔孔孔孔'
        b = '其鴉羕上其其其羕上鴉其其'
        comp = Comparator(a, b, 'a', 'b')
        matches = comp.get_initial_matches()
        # a sequence in A partially matches two different places in B
        assert len(matches) == 2
        assert matches[0].a_start == 1
        assert matches[0].a_end == 3
        assert matches[0].b_start == 1
        assert matches[0].b_end == 3
        assert matches[1].a_start == 2
        assert matches[1].a_end == 4
        assert matches[1].b_start == 7
        assert matches[1].b_end == 9

    def test_no_matches(self):
        a = '孔孔孔孔孔孔孔孔孔孔'
        b = '其其鴉羕上鴉其其其其其'
        comp = Comparator(a, b, 'a', 'b')
        matches = comp.get_initial_matches()
        assert len(matches) == 0


class TestReduceMatches(TestCase):

    def test_reduce_trigram_to_quad(self):
        matches = [
            Match(0, 2, 1, 3),
            Match(1, 3, 2, 4)
        ]
        # combines two trigrams into a single quad-gram match
        reduced = Comparator.reduce_matches(matches)
        assert len(reduced) == 1
        assert reduced[0].a_start == 0
        assert reduced[0].a_end == 3
        assert reduced[0].b_start == 1
        assert reduced[0].b_end == 4

    def test_different_match_lengths(self):
        matches = [
            Match(3, 7, 1, 4),
            Match(4, 8, 2, 5)
        ]
        # matches of different lengths, e.g. with punctuation
        reduced = Comparator.reduce_matches(matches)
        assert len(reduced) == 1
        assert reduced[0].a_start == 3
        assert reduced[0].a_end == 8
        assert reduced[0].b_start == 1
        assert reduced[0].b_end == 5

    def test_many_overlapping_matches(self):
        matches = [
            Match(0, 2, 10, 12),
            Match(1, 3, 11, 13),
            Match(2, 4, 12, 14),
            Match(3, 5, 13, 15),
            Match(4, 6, 14, 16),
        ]
        # many trigrams combined into a single match
        reduced = Comparator.reduce_matches(matches)
        assert len(reduced) == 1
        assert reduced[0].a_start == 0
        assert reduced[0].a_end == 6
        assert reduced[0].b_start == 10
        assert reduced[0].b_end == 16


class TestGroupMatches(TestCase):

    def test_no_groups(self):
        matches = [
            Match(1, 5, 4, 9),
            Match(1, 8, 12, 14),
            Match(1, 4, 356, 350),
            Match(1, 2, 342, 2342)
        ]
        grouped = Comparator.group_matches(matches)
        assert len(grouped) == 4
        for k, v in grouped.items():
            assert len(v) == 1  # every "group" is just one match in b

    def test_small_group(self):
        matches = [
            Match(1, 5, 4, 9),
            Match(1, 5, 12, 14),
            Match(1, 4, 356, 350),
            Match(1, 2, 342, 2342)
        ]
        # a single line in a matches two places in b
        grouped = Comparator.group_matches(matches)
        assert len(grouped) == 3
        # two matches in b for the first entry in a
        assert len(grouped[range(1, 5)]) == 2
        assert grouped[range(1, 5)] == [range(4, 9), range(12, 14)]

    def test_multiple_groups(self):
        matches = [
            Match(1, 5, 4, 9),
            Match(1, 5, 12, 14),
            Match(1, 4, 356, 350),
            Match(1, 2, 342, 2342),
            Match(1, 2, 25, 26),
            Match(4, 9, 356, 350),
        ]
        # two groupings
        grouped = Comparator.group_matches(matches)
        assert len(grouped) == 4
        assert len(grouped[range(1, 5)]) == 2  # two matches in b
        assert len(grouped[range(1, 2)]) == 2  # also two matches
        assert grouped[range(1, 5)] == [range(4, 9), range(12, 14)]
        assert grouped[range(1, 2)] == [range(342, 2342), range(25, 26)]
