# Stolen wholesale, then adapted from https://djangosnippets.org/snippets/535/

# The function assumes the object has a get_absolute_url() method that returns the URL. 
# In your template, write {{ obj_list|hyperlink_list:"slug" }} where obj_list is your object list 
# and "slug" is the object's attribute that returns the link text.

from django.template import Library

register = Library()

@register.filter
def hyperlink_list(obj_list, arg):
	"""Converts an object list into a comma-separated list of hyperlinks.
	Assumes obj.get_absolute_url() returns the link URL.
	arg is the name of the object's attribute (as a string) that returns
	the link text.
	Template usage: {{ obj_list|hyperlink_list:"slug" }}"""
	
	links = [] # start with an empty list of links
	for obj in obj_list:
		# initialize url and text to None
		url = None
		text = None
		try:
			url = obj.get_absolute_url() # get the URL
		except:
			pass # if any exceptions occur, do nothing to leave url == None
		try:
			text = obj.title # get the link text
		except:
			pass # if any exceptions occur, do nothing to leave text == None
		
		# if both URL and text are present, return the HTML for the hyperlink
		if url and text:
			links.append('<a href="%s">%s</a>' % (url, text))
		# if no URL but text is present, return unlinked text
		elif not url and text:
			links.append(text)
		
	# if the list has anything in it, return the list items joined
	# by a comma and a non-breaking space (in HTML)
	if len(links) > 0:
		return '&nbsp|&nbsp;'.join(links)
	# else return an empty string
	else:
		return ''