# Create your views here.
from ebserv.lib.dictionaries import EpwingDictionary
from django.views.decorators.http import require_POST, require_GET
from forms import SearchForm
from django.shortcuts import render_to_response
import dictionary_formatter

DICTIONARY_DIRECTORY = '/home/alex/dictionaries/'
EpwingDictionary.books_directory = DICTIONARY_DIRECTORY

EpwingDictionary.uri_templates = {
  'entry': 'book/{book_id}/subbook/{subbook_id}/entry/{entry_id}/',
  'subbook': 'book/{book_id}/subbook/{subbook_id}/',
  'book': 'book/{book_id}/',
  'audio': 'book/{book_id}/subbook/{subbook_id}/audio/{audio_id}/'
}
EpwingDictionary.uri_base = '' #'/dict/'


@require_GET
def books(request):
  EpwingDictionary.uri_base = '/dict/'
  EpwingDictionary.initialize()
  
  books = { 'books': EpwingDictionary.books() }

  EpwingDictionary.finalize()

  if request.is_ajax():
    return HttpResponse(simplejson.dumps(ret))
  else:
    return render_to_response('restful_dictionary/book_list.html', books)
  

@require_GET
def book(request, book_id):
  EpwingDictionary.uri_base = '/dict/'
  EpwingDictionary.initialize()
  book = EpwingDictionary(book_id)
  
  ret = { 'book': { 'name': book.name,
                    'subbooks': book.subbooks() } }
  #import pdb;pdb.set_trace()
  EpwingDictionary.finalize()
  
  if request.is_ajax():
    return HttpResponse(simplejson.dumps(ret))
  else:
    return render_to_response('restful_dictionary/book.html', ret)


@require_GET
def entry(request, book_id, subbook_id, entry_id):
  #TODO error handling for invalid ids
  EpwingDictionary.uri_base = ''
  EpwingDictionary.initialize()
  book = EpwingDictionary(book_id)
  heading, content = book.entry(entry_id, subbook_id)
  
  EpwingDictionary.finalize()
  
  
  ret = { 'heading': heading,
          'text': content,
          'word_search_uri_base': '/dict/search?book={0}&search_method=prefix&query='.format(book_id) }
  
  if request.is_ajax():
    return HttpResponse(simplejson.dumps(ret))
  else:
    #HTML
    EpwingDictionary.initialize()
    ret['text'] = dictionary_formatter.clean_links(book, content, '/dict/')
    #ret['text'] = dictionary_formatter.prefetch_references(book, ret['text'])      
    EpwingDictionary.finalize()
    return render_to_response('restful_dictionary/entry.html', ret)

@require_GET
def search(request): #default should be 'all'
  #book_name='chujiten'
  #todo:book_name validation, search_method validation etc
  #TODO only get headings
  #TODO use bookname IDs
  EpwingDictionary.uri_base = '/dict/'
  
  #TODO json view of fields available for search (for REST!)
  if request.GET:
    EpwingDictionary.initialize()
    
    search_dict = EpwingDictionary(request.GET['book'])
    results = []
    search_results = search_dict.search(request.GET['query'], search_method=request.GET['search_method'])
    for heading, content, subbook_id, entry_id, uri in search_results:
      results.append({ 'uri': uri,
                       'heading': heading })
    
    EpwingDictionary.finalize()
    
    ret = { 'results': results }
            
    if request.is_ajax():
      return HttpResponse(simplejson.dumps(ret))
    else:
      return render_to_response('restful_dictionary/search_results.html', ret)
  else:
    books = EpwingDictionary.books()
    form = SearchForm(books)
    return render_to_response('restful_dictionary/search_form.html', { 'form': form })
    

