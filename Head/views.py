from django.shortcuts import render
from Event.models import Event

def home(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # For logged-in users, show both public and their own private events
        upcoming_events = (Event.objects.filter(is_private=False) | Event.objects.filter(creator=request.user)).order_by('date')[:5]
        interesting_events = Event.objects.filter(is_private=False)[:3]
    else:
        # For non-logged-in users, show only public events
        upcoming_events = Event.objects.filter(is_private=False).order_by('date')[:5]
        interesting_events = Event.objects.filter(is_private=False)[:3]

    # Render the home page with the events
    return render(request, 'pages/home.html', {
        'upcoming_events': upcoming_events,
        'interesting_events': interesting_events,
    })