import EventKit
import Foundation
import time
import threading

store = EventKit.EKEventStore.alloc().init()
access_granted = False
access_event = threading.Event()

def callback(granted, error):
    global access_granted
    access_granted = granted
    access_event.set()

store.requestAccessToEntityType_completion_(EventKit.EKEntityTypeEvent, callback)
access_event.wait(timeout=10)

if not access_granted:
    print("Access Denied or Timeout")
else:
    start_date = Foundation.NSDate.date()
    end_date = Foundation.NSDate.dateWithTimeIntervalSinceNow_(7 * 24 * 3600)
    predicate = store.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, None)
    events = store.eventsMatchingPredicate_(predicate)
    
    if not events:
        print("No events found")
    else:
        sorted_events = sorted(events, key=lambda e: e.startDate())
        for e in sorted_events[:3]:
            print(f"Event: {e.title()} at {e.startDate()}")
