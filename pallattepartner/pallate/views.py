from django.shortcuts import render


def index(request):
	"""Render a simple home page for the pallate app."""
	context = {
		'title': 'Pallate — Collaboration Finder',
		'message': 'Welcome to the Pallate demo app — find collaborators and share palettes.'
	}
	return render(request, 'pallate/index.html', context)
