from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event, UserEvent

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
    event = Event.objects.get(pk=id)
    user_joined = False

    if request.user.is_authenticated:
        # Check if the user has joined this event
        user_joined = UserEvent.objects.filter(user=request.user, event=event).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            # If the user clicks "Join", add the user to the event
            if not user_joined:
                UserEvent.objects.create(user=request.user, event=event)
            return redirect('calendar')
        else:
            # If user is not logged in, redirect to login and save the next URL to return back after login
            return redirect(f'/accounts/login/?next=/event/events/{id}/')

    return render(request, 'event/event_detail.html', {
        'event': event,
        'user_joined': user_joined,
    })