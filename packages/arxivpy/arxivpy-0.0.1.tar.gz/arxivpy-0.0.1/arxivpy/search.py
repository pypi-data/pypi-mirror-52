from bs4 import BeautifulSoup as bs

from .exceptions.empty_query_exception import EmptyQueryException
from .exceptions.empty_term_exception import EmptyTermException

from arxivpy.request import get

class Search:

    def __init__(self, url):
        self._url = url

    def simple(self, query=None, searchtype='all', abstracts=True, download=False, path=None,
               downloadonly=None, page=1, size=25):
        """
        Searches in the arXiv site using only some fields, like query and searchtype.

        :kwarg query: the term(s) which will be searched
        :kwarg searchtype: 
        :kwarg abstracts: includes abstacts if is set to true, or excludes them. The default option 
          is true
        :kwarg download: if set to true, will download all pdfs found with the given query term
        :kwarg path: downloads all pdfs in the specified folder
        :kwarg downloadonly: downloads only first `downloadonly` paper, or 
                              if not set downloads only `size` number of papers
        :kwarg page: returns papers only from given page, by default is set to `1`
        :kwarg size: number of papers returned per page, can be set to `25`
        """
        if not query:
            raise EmptyQueryException('Query cannot be empty.')

        params = {}
        query = query.replace(' ', '+')

        params['query'] = query
        params['searchtype'] = searchtype
        params['abstracts'] = 'show' if abstracts else 'hide'
        params['start'] = page * size if page > 1 else 0

        response = get(self._url, params=params)

        downloadonly = downloadonly if downloadonly else size
        result = self._format_result(response, download, path, downloadonly)
        return result

    def advanced(self, term=None, terms=None, physics='all', classification=None,
                 fromdate=None, todate=None, past_12=False, year=None, abstracts=True, size=25,
                 include_older_versions=False, cross_listed_papers=True, datetype='submitted_date_first',
                 download=False, path=None, page=1, downloadonly=None):
        """
        Searches in the arxiv site, using more fields.

        :kwarg term: a string object, containing one or more terms, or a dict object, 
                      represented in the following way: 
                      { 'term': 'your-term', 'field': 'searchtypefield' }
        :kwarg terms: list with dict-objects, each of which is represented in the
                     following way:
                      { 'term': 'your-term', 'field': 'searchtypefield', 
                        'operator': '`AND`/`OR`/`NOT` 
                      or `&`/`|`/`~`'}, where the meaning of operator means:

                          AND / &:
                          OR  / |:
                          NOT / ~:
        :kwarg physics:  if `classification` type includes physics, the field can 
                          be set to specific type of `physics`:
                          `all`, `astro-ph`, `cond-mat`, `gr-qc`, `hep-ex`, 
                          `hep-ph`, `hep-lat`, `hep-th`, `math-ph`, `nlin`, 
                          `nicl-ex`, `nucl-th`, `quant-ph`, `physics`
        :kwarg classification: a list or str type, where str
                          can contain one, or more classifications separated with `,`.
                          valid `classifications` are:
                          `computer_science`, `economics`, `mathematics`, 
                          `eess`, `physics`, `q_biology`, `q_finance`, `statistics`
        :kwarg fromdate: results can be filtered by 
          `specific_year` (`year`), `date_range` (`fromdate`, `todate`), 
          `all_dates`(non of `year`, or `from`-`to` date is specified, or `past_12`).
          `fromdate` must be represented as a `python-datetime` object.
        :kwarg todate: results can be filtered by 
          `specific_year` (`year`), `date_range` (`fromdate`, `todate`), 
          `all_dates`(non of `year`, or `from`-`to` date is specified, or `past_12`).
          `todate` must be represented as a `python-datetime` object.
        :kwarg past_12: results can be filtered by 
          `specific_year` (`year`), `date_range` (`fromdate`, `todate`), 
          `all_dates`(non of `year`, or `from`-`to` date is specified, or `past_12`).
          `past_12` can be `True`, or `False`
        :kwarg year: results can be filtered by 
          `specific_year` (`year`), `date_range` (`fromdate`, `todate`), 
          `all_dates`(non of `year`, or `from`-`to` date is specified, or `past_12`).
          `year` can be a valid year, represented as ordinary int, or str.
        :kwarg abstracts: returns abstract papers, if the option is set to `True` /default/
        :kwarg size: number of papers returned per page, can be set to `25`
        :kwarg include_older_version: by default is set to `False`,
                                      if is set to `True`, the returned result 
                                      will contain older versions of papers
        :kwarg cross_listed_paper: 
        :kwarg datetype: returned papers will be sorted by one of the following ways: 
                        `announced_date_first`, `submitted_date_first`/default/, `submitted_date`
        :kwarg download: by default is set to `False`, if is set to `True` 
                          will download all papers returned as result
        :kwarg path: if `download` is set to `True`, all papers will be downloaded in `path`
        :kwarg page: returns papers only from given page, by default is set to `1`
        :kwarg downloadonly: downloads only first `downloadonly` paper, or 
                              if not set downloads only `size` number of papers
        """
        
        if not term and not terms:
            raise EmptyTermException()

        params = {'advanced': ''}

        self._set_terms(params, term, terms)
        self._set_classifications(params, classification, physics)
        self._format_date(params, fromdate, todate, year, past_12, datetype)
        self._additional_response_fields(params, abstracts, include_older_versions,
                                         cross_listed_papers, size)

        params['start'] = page * size if page > 1 else 0
        downloadonly = downloadonly if downloadonly else size

        url = "{}/advanced".format(self._url)
        response = get(url, params=params)
        result = self._format_result(response, download, path, downloadonly)
        return result

    def _format_result(self, response, download=False, path=False, downloadonly=None):
        soup = bs(response.content, 'html.parser')

        journals = soup.find_all('li', {'class': 'arxiv-result'})

        result = []
        successful = None
        for journal in journals:
            title = journal.find('p', {'class': 'title is-5 mathjax'}) \
                           .get_text() \
                           .replace('\n', '') \
                           .replace('  ', '') \
                           .encode('utf-8')

            authors = journal.find('p', {'class': 'authors'}) \
                             .get_text() \
                             .replace('\n', '') \
                             .replace('  ', '') \
                             .replace('Authors:', '') \
                             .encode('utf-8')

            if download and downloadonly:
                download_links = journal.find('p', {'class': 'list-title is-inline-block'})
                pdfs = download_links.find_all(href=True)[1::2]
                url = pdfs[0]['href']

                successful = self._download(url, path)
                downloadonly = downloadonly - 1

            record = type('Journal', (object,),
                          {'title': title, 'authors': authors, 'downloaded': successful})
            result.append(record)

        return result

    def _download(self, url, path):
        try:
            response = get(url)
            name = url.split('/')[-1]
            with open('{}/{}.pdf'.format(path, name), 'wb') as file:
                file.write(response.content)
        except:
            return False

        return True

    def _set_terms(self, params, term, terms):
        if terms:
            for i, term in enumerate(terms):
                if i is 0:
                    params["terms-{}-operator".format(i)] = 'AND'
                else:
                    oparator = term['operator'] if 'operator' in term else 'AND'
                    params["terms-{}-operator".format(i)] = self._set_operator(operator)

                params["terms-{}-term".format(i)] = term['term']
                params["terms-{}-field".format(i)] = term['field']
        else:
            params["terms-0-operator"] = 'AND'
            params["terms-0-term"] = term if type(term) is str else term['term']
            params["terms-0-field"] = 'title' if type(term) is str else term['field']

    def _set_operator(self, operator):
        operators = {'&': 'AND', '|': 'OR', '~': 'NOT'}
        return operators[operator] if operator in operators else operator.upper()

    def _set_classifications(self, params, classification, physics):
        if classification:
            classifications = classification.split(',') if type(classification) is str else classification
            for classification in classifications:
                params['classification-{}'.format(classification)] = 'y'
        params['classification-physics_archives'] = physics if classification is 'physics' else 'all'

    def _format_date(self, params, fromdate, todate, year, past_12, datetype):
        if fromdate:
            params['date-filter_by'] = 'date_range'
            params['date-from_date'] = "{}-{}-{}".format(fromdate.year, fromdate.month, fromdate.day)
            params['date-to_date'] = "{}-{}-{}".format(todate.year, todate.month, todate.day)
        elif year:
            params['date-filter_by'] = 'specific_year'
            params['date-year'] = year
        elif past_12:
            params['date-filter_by'] = 'past_12'
        else:
            params['date-filter_by'] = 'all_dates'

        params['date-date_type'] = datetype

    def _additional_response_fields(self, params, abstracts, include_older_versions, cross_listed_papers, size):
        params['order'] = '-announced_date_first'
        params['abstracts'] = 'show' if abstracts else 'hide'
        params['include_older_versions'] = 'y' if include_older_versions else ''
        params['classification-include_cross_list'] = 'include' if cross_listed_papers else 'exclude'
        params['size'] = size