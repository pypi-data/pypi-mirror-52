# -*- coding: utf-8 -*-
from flashtext import KeywordProcessor

class ThemesMatcher():


    def __init__(self,filename):
        """
        Init keyword processor
        @param filename to flashtext
        """
        self.keyword_processor = KeywordProcessor()
        self.keyword_processor.add_keyword_from_file(filename)
        self.keyword_processor.non_word_boundaries = self.keyword_processor.non_word_boundaries.union(list("@&ÇçÉÈÀÊÁüéáÍíôÔÎîâÂÛûóÓÚúÜüñÑàéèëêù"))


    def _get_matches(self,tagged_verbatim):
        """
        Get tagged themes from verbatim
        @tagged_verbatim : string
        @return list of lists : [[keyword, theme, polarity],[kw2, th2, p2],...,[kwn, thn, pn]]
        """
        matches = []
        add_char = False
        curr_vble = ''

        for i in range(len(tagged_verbatim)):
            if add_char and tagged_verbatim[i] == '<':
                matches.append(curr_vble.split(';'))
                add_char = False
                curr_vble = ''
            elif add_char:
                curr_vble += tagged_verbatim[i]
            elif tagged_verbatim[i] == '<':
                add_char = True
            else:
                pass

        return matches


    def match(self,verbatims):
        """
        Match themes in verbatims via flashtext
        @param verbatims : list of strings
        @return list of list of matches : [[[keyword, theme, polarity],[kw2, th2, p2],...,[kwn, thn, pn]],...] 
        """
        matches = []

        for verbatim in verbatims:
            try:
                tagged_verbatim = self.keyword_processor.replace_keywords(verbatim.replace('<',' ').replace("'","' "))
                matches.append(self._get_matches(tagged_verbatim))
            except:
                matches.append([])
        
        return matches

