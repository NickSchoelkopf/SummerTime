import spacy
import pytextrank
from math import sqrt
from operator import itemgetter
from .Model import Model


class text_rank(Model):
    def __init__(self, num_sentences=1):
        self.num_sentences = num_sentences
        # load a spaCy model, depending on language, scale, etc.
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("textrank", last=True)

    def summarize(self, corpus):
        # add PyTextRank to the spaCy pipeline
        doc = self.nlp(corpus)
        sent_bounds = [[s.start, s.end, set([])] for s in doc.sents]

        limit_phrases = self.num_sentences
        phrase_id = 0
        unit_vector = []
        for p in doc._.phrases:
            unit_vector.append(p.rank)
            for chunk in p.chunks:
                for sent_start, sent_end, sent_vector in sent_bounds:
                    if chunk.start >= sent_start and chunk.end <= sent_end:
                        sent_vector.add(phrase_id)
                        break
            phrase_id += 1
            if phrase_id == limit_phrases:
                break

        sum_ranks = sum(unit_vector)

        unit_vector = [rank/sum_ranks for rank in unit_vector]

        sent_rank = {}
        sent_id = 0
        for sent_start, sent_end, sent_vector in sent_bounds:
            sum_sq = 0.0
            for phrase_id in range(len(unit_vector)):
                if phrase_id not in sent_vector:
                    sum_sq += unit_vector[phrase_id]**2.0
            sent_rank[sent_id] = sqrt(sum_sq)
            sent_id += 1

        sorted(sent_rank.items(), key=itemgetter(1))

        sent_text = {}
        sent_id = 0
        limit_sentences = self.num_sentences
        summary_sentences = []
        for sent in doc.sents:
            sent_text[sent_id] = sent.text
            sent_id += 1
        num_sent = 0
        for sent_id, rank in sorted(sent_rank.items(), key=itemgetter(1)):
            summary_sentences.append(sent_text[sent_id])
            num_sent += 1
            if num_sent == limit_sentences:
                break

        return summary_sentences

    def show_capability(self):
        print("A graphbased ranking model for text processing. Extractive sentence summarization. \n Strengths: \n - Fast with low memory usage \n - Allows for control of summary length \n Weaknesses: \n - Not as accurate as neural methods.")