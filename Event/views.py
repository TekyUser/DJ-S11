from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, UserEvent  # Add UserEvent import here


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
    event = get_object_or_404(Event, id=id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        user_event = UserEvent.objects.create(user=request.user, event=event)
        messages.success(request, "You have successfully joined the event!")
        return redirect('calendar')  # Ensure you're using the correct namespace
    
    return render(request, 'event/event_detail.html', {'event': event})
