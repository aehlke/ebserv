from django import forms

class SearchForm(forms.Form):
  def __init__(self, books, *args, **kwargs):
    super(SearchForm, self).__init__(*args, **kwargs)
    self.fields['book'].choices = [('', 'All')] + [(book['id'], book['name']) for book in books]

  book = forms.ChoiceField()
  query = forms.CharField(max_length=100)
  search_method = forms.ChoiceField([('exact', 'Exact',),
                                     ('prefix', 'Starts with',),
                                     ('suffix', 'Ends with',),
                                     ('substring', 'Substring',)])
  
