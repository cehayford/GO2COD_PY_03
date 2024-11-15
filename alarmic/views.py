from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .models import Alarm
from .forms import AlarmForm
import threading
import time
from datetime import datetime
import pygame
import os
from django.http import JsonResponse

# pygame.mixer.init()

class AlarmSound:
    def __init__(self):
        self.is_playing = False
    
    def play_sound(self, sound_file):
        if not self.is_playing:
            self.is_playing = True
            try:
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play(loops=3)
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print(f"Error playing sound: {e}")
            finally:
                self.is_playing = False

alarm_sound = AlarmSound()

def check_alarms():
    while True:
        current_time = datetime.now().time()
        active_alarms = Alarm.objects.filter(is_active=True)      
        for alarm in active_alarms:
            alarm_time = alarm.time
            if (current_time.hour == alarm_time.hour and 
                current_time.minute == alarm_time.minute):
                sound_file = alarm.sound_path
                if os.path.exists(sound_file):
                    threading.Thread(target=alarm_sound.play_sound, args=(sound_file,), daemon=True).start()
                alarm.is_active = False
                alarm.save()
        time.sleep(30)
        
alarm_thread = threading.Thread(target=check_alarms, daemon=True)
alarm_thread.start()

def alarm_list(request):
    alarms = Alarm.objects.all().order_by('time')
    available_sounds = get_available_sounds()
    context = {
        'alarms': alarms,
        'available_sounds': available_sounds
    }
    return render(request, 'alarmic/alarm_list.html', context)

def get_available_sounds():
    sounds_dir = os.path.join(settings.MEDIA_ROOT, 'alarm_sounds')
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
    sounds = []
    for file in os.listdir(sounds_dir):
        if file.endswith(('.mp3', '.wav')):
            sounds.append(file)
    return sounds

def alarm_create(request):
    if request.method == 'POST':
        form = AlarmForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alarm created successfully!')
            return redirect('alarm-list')
    else:
        form = AlarmForm()
    context = {
        'form': form,
        'title': 'Create Alarm',
        'available_sounds': get_available_sounds()
    }
    return render(request, 'alarmic/alarm_form.html', context)

def alarm_update(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    if request.method == 'POST':
        form = AlarmForm(request.POST, instance=alarm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alarm updated successfully!')
            return redirect('alarm-list')
    else:
        form = AlarmForm(instance=alarm)
    context = {
        'form': form,
        'title': 'Update Alarm',
        'alarm': alarm,
        'available_sounds': get_available_sounds()
    }
    return render(request, 'alarmic/alarm_form.html', context)

def alarm_delete(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    if request.method == 'POST':
        alarm.delete()
        messages.success(request, 'Alarm deleted successfully!')
        return redirect('alarm-list')
    context = {'alarm': alarm}
    return render(request, 'alarmic/alarm_confirm_delete.html', context)

def alarm_toggle(request, pk):
    alarm = get_object_or_404(Alarm, pk=pk)
    if request.method == 'POST':
        alarm.is_active = not alarm.is_active
        alarm.save()
        status = 'activated' if alarm.is_active else 'deactivated'
        messages.success(request, f'Alarm {status} successfully!')
    return redirect('alarm-list')

def test_sound(request, sound_file):
    sound_path = os.path.join(settings.MEDIA_ROOT, 'alarm_sounds', sound_file)
    if os.path.exists(sound_path):
        threading.Thread(
            target=alarm_sound.play_sound,
            args=(sound_path,),
            daemon=True
        ).start()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Sound file not found'})