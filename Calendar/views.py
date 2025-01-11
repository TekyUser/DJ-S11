from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Event.models import Event, UserEvent
from django.core.paginator import Paginator

@login_required
def calendar(request):
    user_events = UserEvent.objects.filter(user=request.user).select_related('event')
    
    # Paginate the events, showing 5 events per page
    paginator = Paginator(user_events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if not user_events:
        message = "You haven't joined any events yet."
    else:
        message = None

    return render(request, 'calendar/calendar_view.html', {
        'page_obj': page_obj,
        'message': message,
    })
