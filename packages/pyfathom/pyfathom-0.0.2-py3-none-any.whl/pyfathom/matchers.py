import re

# matches parts of the input string
class matcher:
	def __init__(self, is_type):
		self.is_type = is_type

# matches single token with a regex pattern
class pattern_matcher(matcher):
	
	_fmt_pat = '(?:\\\\\\\\|\\\\\\/|[^\\/])+'
	_fmt_qtf = '(?:\\+\\??|\\*\\??|\\?)?'
	_fmt_caps = '\\/(' + _fmt_pat + ')\\/(' + _fmt_qtf + ')'
	
	fmt = '\\/' + _fmt_pat + '\\/' + _fmt_qtf
	
	def __init__(self, pattern, is_type):
		super(pattern_matcher, self).__init__(is_type)
		m = re.match(pattern_matcher._fmt_caps, pattern)
		self.pattern = '^(?:' + m.group(1) + ')$'
		self.quantifier = m.group(2) or '/'
	
	def match(self, token, idx, types):
		return re.match(self.pattern, token) is not None
		
	def __repr__(self):
		return '/' + self.pattern + '/'
	
# matches a single token with a type
class type_matcher(matcher):
	
	fmt = '[\w\|-]+\??'
	
	def __init__(self, types, is_type):
		super(type_matcher, self).__init__(is_type)
		self.types = types.rstrip('?').split('|')
		self.quantifier = '*' if types[-1] == '?' else '+'
	
	def match(self, token, idx, types):
		for t in types:
			if t.start_token <= idx and t.end_token >= idx and t.type in self.types:
				return True
		return False
		
	def __repr__(self):
		return '|'.join(self.types)

