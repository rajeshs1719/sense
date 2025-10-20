from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def video_call(request, room_name):
    # Pass room_name to template if needed
    return render(request, "home.html", {"room_name": room_name})


def jitsi_meeting(request):
    return render(request, 'meet/index.html')
