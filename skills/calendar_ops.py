import EventKit
import Foundation
import threading
import datetime

def get_nearest_event(search_term, speak_func):
    speak_func("Checking your calendar, sir...")

    store = EventKit.EKEventStore.alloc().init()
    access_granted = False
    access_event = threading.Event()

    def callback(granted, error):
        nonlocal access_granted
        access_granted = granted
        access_event.set()

    # Request access to calendar
    store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, callback)
    access_event.wait(timeout=5)

    if not access_granted:
        msg = "Sir, I don't have permission to access your calendar. Please allow Terminal in Mac Privacy & Security settings under Calendars."
        speak_func(msg)
        return "Permission denied."

    # Look for events in the next 30 days (since birthdays/meetings might be further out)
    start_date = Foundation.NSDate.date()
    end_date = Foundation.NSDate.dateWithTimeIntervalSinceNow_(30 * 24 * 3600)

    predicate = store.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, None)
    events = store.eventsMatchingPredicate_(predicate)

    if not events:
        msg = "You have no upcoming events in the next 30 days, sir."
        speak_func(msg)
        return msg

    # Sort events by start date
    sorted_events = sorted(events, key=lambda e: e.startDate().timeIntervalSince1970())

    # Filter events if the user asked for something specific (like "birthday" or "meeting")
    filtered_events = []
    search_term = search_term.lower().strip()

    # Ignore generic targets that the LLM might hallucinate
    generic_terms = ['all', 'calendar', 'event', 'next event', 'upcoming', 'my calendar']

    if search_term not in generic_terms:
        for e in sorted_events:
            # Check if the search term is in the event title or the calendar's name (e.g., "Birthdays" calendar)
            if search_term in e.title().lower() or (e.calendar() and search_term in str(e.calendar().title()).lower()):
                filtered_events.append(e)
    else:
        filtered_events = sorted_events

    if not filtered_events:
        msg = f"You have no upcoming events matching '{search_term}' in the next 30 days, sir."
        speak_func(msg)
        return msg

    nearest_event = filtered_events[0]
    title = nearest_event.title()

    # Convert NSDate to Python datetime
    timestamp = nearest_event.startDate().timeIntervalSince1970()
    dt = datetime.datetime.fromtimestamp(timestamp)

    # Format the time nicely for Text-To-Speech (e.g., "April 21 at 11:00 PM")
    formatted_date = dt.strftime("%B %d at %I:%M %p").replace(" 0", " ")

    response_text = f"Your next event is '{title}', scheduled for {formatted_date}."
    print(f"Calendar: {response_text}")
    speak_func(response_text)

    return response_text
