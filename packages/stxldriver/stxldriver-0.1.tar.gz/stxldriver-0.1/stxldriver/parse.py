import collections
import html.parser


class IndexParser(html.parser.HTMLParser):
    
    def __init__(self):
        super(IndexParser, self).__init__()
        self.stack = ['ROOT']
        self.properties = collections.OrderedDict()
    
    def handle_starttag(self, tag, attrs):
        if tag in ('meta', 'link', 'img', 'li'):
            # Ignore start tags that have no matching end tag.
            # <li> should not be in this list, but this is what the camera outputs.
            return
        self.stack.append(tag)
        self.attrs = collections.defaultdict(str, attrs)

    def handle_endtag(self, tag):
        assert self.stack.pop() == tag
        
    def handle_data(self, data):
        if self.stack[-1] == 'td':
            if self.attrs['class'] == 'valuename':
                # Remember the name for a subsequent value.
                self.key = data
            elif self.attrs['class'] == 'value':
                # Save this (name, value) pair.
                self.properties[self.key] = data


class FormParser(html.parser.HTMLParser):
    
    def __init__(self):
        super(FormParser, self).__init__()
        self.forms = collections.OrderedDict()
        self.form = None
        self.form_name = None
    
    def handle_starttag(self, tag, attrs):
        attrs = collections.defaultdict(str, attrs)
        if tag == 'form':
            # Start parsing a new form.
            name = attrs['name']
            if name in self.forms:
                raise RuntimeError('Found duplicate form with name "{0}".'.format(name))
            self.form = self.forms[name] = collections.OrderedDict()
            self.form_name = name
            return
        if tag != 'input':
            return
        # Update the current form.
        if self.form is None:
            raise RuntimeError('Found orphan form input with attrs: {0}.'.format(attrs))
        itype = attrs['type']
        if itype not in ('radio', 'text', 'hidden', 'submit', 'button'):
            raise RuntimeError(
                'Found bad input type in "{0}" with attrs {1}.'.format(self.form_name, attrs))
        name, value = attrs['name'], attrs['value']
        if itype in ('submit', 'button'):
            pass
        elif itype in ('text', 'hidden'):
            if name in self.form:
                raise RuntimeError(
                    'Found duplicate input "{0}" in "{1}".'.format(name, self.form_name))
            self.form[name] = value
        elif itype == 'radio':            
            # Record all allowed values.
            values_key = '_{0}_values'.format(name)
            if values_key not in self.form:
                self.form[values_key] = [value]
            else:
                self.form[values_key].append(value)
            # Record the one checked value.
            if 'checked' in attrs:
                if name in self.form:
                    raise RuntimeError(
                        'Found duplicate checked value for "{0}" in "{1}".'
                        .format(input, self.form_name))
                self.form[name] = value
        
    def handle_endtag(self, tag):
        if tag == 'form':
            self.form = None
            self.form_name = None


class FilterParser(html.parser.HTMLParser):
    """Parse the response from /filtersetup.html to extract the current filter number.
    """
    def __init__(self):
        super(FilterParser, self).__init__()
        self.current_filter_number = None

    def handle_starttag(self, tag, attrs):
        if tag == 'option':
            name, value = attrs.pop(0)
            assert name == 'value'
            filter_number = int(value)
            if len(attrs) > 0:
                name, value = attrs.pop(0)
                assert name == 'selected' and value is None
                self.current_filter_number = filter_number
