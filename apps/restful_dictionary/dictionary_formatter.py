from lxml import html
import re

def clean_links(book, content, uri_base):
  '''
  If a reference links to a position within the entries already loaded,
  then its link will be rewritten to point to the named anchor.
  
  Other links will have uri_base prepended.
  '''
  doc = html.fromstring(content)
  anchor_names = [anchor.attrib['name'] for anchor in doc.cssselect('a[name]')]
  for reference in doc.cssselect('a[href]'):
    if reference.attrib['href'] in anchor_names:
      reference.attrib['href'] = '#' + reference.attrib['href']
    else:
      reference.attrib['href'] = uri_base + reference.attrib['href']
  return html.tostring(doc)

def prefetch_references(book, content, counter=0):
  #TODO maximum recursion depth
  doc = html.fromstring(content)
  for reference in doc.cssselect('a[href][rel=\"subsection\"]'): #TODO select on 'a' with rel="subsection"
    if '#' not in reference.attrib['href']: #no relative links
      m = re.match('.*book/(.+)/subbook/(.+)/entry/(.+)/$', reference.attrib['href'])
      inline_subbook_id = m.group(2)
      inline_entry_id = m.group(3)
      heading, inline_content = book.entry(inline_entry_id, inline_subbook_id)
      
      inline_content = prefetch_references(book, inline_content, counter=counter)
      
      inline_div = html.Element('div')
      inline_div.attrib['class'] = 'dict_inline_content'
      inline_div.attrib['id'] = 'dict_{0}_{1}_{2}'.format(inline_subbook_id, inline_entry_id, counter)
      reference.attrib['id'] = 'dict_{0}_{1}_{2}_link'.format(inline_subbook_id, inline_entry_id, counter)
      reference.attrib['class'] = 'dict_inline_content_link'
      inline_div.append(html.fromstring(inline_content))
      reference.addnext(inline_div)
      counter += 1
  return html.tostring(doc)
