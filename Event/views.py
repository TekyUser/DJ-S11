from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user  # Gắn người tạo là người dùng đăng nhập
            event.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'event/create_event.html', {'form': form})
def event_list_view(request):
    if request.user.is_authenticated:
        # Show all public events and private events that the logged-in user created
        events = Event.objects.filter(is_private=False) | Event.objects.filter(creator=request.user)
    else:
        # Only show public events for non-authenticated users
        events = Event.objects.filter(is_private=False)
    
    return render(request, 'event/event_list.html', {'events': events})

# View to display the details of a single event
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)  # Fetch event by ID or show 404 if not found
    return render(request, 'event/event_detail.html', {'event': event})
# def my_events(request):
#     if request.user.is_authenticated:
#         # Fetch only events created by the logged-in user (including private ones)
#         events = Event.objects.filter(creator=request.user)  # Shows all events the user created
#     else:
#         # If the user is not authenticated, redirect them to login or show an error
#         return redirect('login')  # Adjust this based on your login URL name

#     return render(request, 'event/my_event_list.html', {'events': events})