from eb import *
import sys
import string

def initialize():
  eb_initialize_library()

def finalize():
  eb_finalize_library()

class BaseDictionary(object):
  SEARCH_METHODS = ['exact', 'prefix', 'suffix', 'substring']
  SEARCH_OPTIONS = ['icase']
  
  def search(self, query='', search_method=SEARCH_METHODS[0], search_options=None):
    pass
  def goto(self, entry_id=0):
    pass

class EpwingDictionary(BaseDictionary):
  SEARCH_METHODS = ['exact']
  SEARCH_OPTIONS = []
  
  def __init__(self, dictionary_directory):
    self.book, self.appendix, self.hookset = EB_Book(), EB_Appendix(), EB_Hookset()
    try:
        eb_bind(self.book, dictionary_directory)
        eb_set_subbook(self.book, 0)
        self.subbook = eb_subbook(self.book)
    except EBError, (error, message):
        code = eb_error_string(error)
        sys.stderr.write("Error: %s: %s\n" % (code, message))
        sys.exit(1)
        
  def search(self, query='', search_method=SEARCH_METHODS[0], search_options=None, container=None):
    query_encoded = unicode(query, 'utf-8').encode('euc-jp')
    
    if search_method == 'exact':
      eb_search_exactword(self.book, query_encoded)
    elif search_method == 'prefix':
      eb_search_word(self.book, query_encoded)
    
    while True:
      hits = eb_hit_list(self.book)
      if not hits:
          break
      #found = 1
      for heading_location, text_location in hits:
        heading = self._get_content(self.subbook, heading_location, container, eb_read_heading)
        content = self._get_content(self.subbook, text_location, container, eb_read_text)
        if string.strip(content):
          yield (unicode(heading, 'euc-jp', errors='ignore'), unicode(content, 'euc-jp', errors='ignore'), )

  def _get_content(self, subbook, position, container, content_method):
    current_subbook = eb_subbook(self.book)
    if current_subbook != subbook:
      eb_set_subbook(self.book, subbook)
    else:
      current_subbook = None
    eb_seek_text(self.book, position)
    buffer = []
    while True:
      data = content_method(self.book, self.appendix, self.hookset, container)
      if not data:
        break
      buffer.append(data)
    #restore current subbook
    if current_subbook:
      eb_set_subbook(self.book, current_subbook)
    return string.join(buffer, '')

def main():
  eb_initialize_library()
  
  my_dict = EpwingDictionary('/home/alex/dictionaries/chujiten/')
  
  for h, c in my_dict.search('horse'):
    print(u"{0}:\n{1}".format(h, c))
  
  eb_finalize_library()
  
  
if __name__ == "__main__":
    main()
