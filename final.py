# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 10:51:25 2021

@author: Charan
"""

import webbrowser
import regex as re
import PySimpleGUI as sg
from pytube import YouTube
from threading import Thread
from PySimpleGUI import FolderBrowse



yt     = ""
count1 = 1
count2 = 1
count3 = 1
close  = True
no_url = True

video_id  = None
itag_dict = {}
file_path = ""

drop_down_list = []
stop_progress_bar_flag = False
stopAudioGeneratorTTS  = False


def regexpression_for_filtering_audio_quality_and_itag(filter):
    itag_bit_rate_dict = {}

    global drop_down_list
    itag_patterns     = 'itag="\d*"'
    bit_rate_patterns = 'abr="\d*kbps"'
    txt = ''.join(str(e) for e in filter)

    itag_pattern     = re.findall(itag_patterns, txt)
    bit_rate_pattern = re.findall(bit_rate_patterns, txt)


    itag_pattern_list     = []
    bit_rate_pattern_list = []

    for itag in itag_pattern:
        itag_pattern_list.append(itag.replace('itag=', '').replace('"',''))

    for bit_rate in bit_rate_pattern:
        bit_rate_pattern_list.append(bit_rate.replace('abr=', '').replace('"',''))

    itag_bit_rate_dict = {key_b_rate:value_itag for key_b_rate, value_itag in zip(bit_rate_pattern_list, itag_pattern_list)}
    drop_down_list = list(set(bit_rate_pattern_list[:]))
    print(itag_bit_rate_dict)
    return itag_bit_rate_dict

def regexpression_for_filtering_res_and_itag(filter):
    itag_res_dict = {}
    
    global drop_down_list
    
    itag_patterns = 'itag="\d*"'
    res_patterns  = 'res="\d*p"'
    txt = ''.join(str(e) for e in filter)

    itag_pattern = re.findall(itag_patterns, txt)
    res_pattern  = re.findall(res_patterns, txt)

    itag_pattern_list = []
    res_pattern_list = []

    for itag in itag_pattern:
        itag_pattern_list.append(itag.replace('itag=', '').replace('"',''))

    for res in res_pattern:
        res_pattern_list.append(res.replace('res=', '').replace('"',''))

    itag_res_dict = {k:v for k,v in zip(res_pattern_list, itag_pattern_list)}
    drop_down_list = list(set(res_pattern_list[:]))

    return itag_res_dict


def stop_progress_bar_thread():
    global stop_progress_bar_flag
    stop_progress_bar_flag = True

    
def progress():
    while True:
        window['DOWNLOAD_PROGRESS'].update("Downloading... Please Wait...!")
        window.FindElement("PROGRESS_BAR").UpdateAnimation(r'C:\Users\hp\Downloads\378.gif', time_between_frames=10)

        global stop_progress_bar_flag
        if stop_progress_bar_flag == True: 
            window['DOWNLOAD_PROGRESS'].update("Download completed")
            break

    
def yt_download(video_id, file_path):
    try:
        global stop_progress_bar_flag
        
        stream = yt.streams.get_by_itag(itag_dict[video_id])

        pgr_thread = Thread(target = progress)
        pgr_thread.setDaemon(True)
        pgr_thread.start()

        stream.download(file_path)
        global stop_progress_bar_flag
        stop_progress_bar_flag = True
        print('Completed')
        stop_progress_bar_thread()
        reset_all()
    except Exception:       
        print("Failed to establish a new connection")
        stop_progress_bar_thread()
        stop_progress_bar_flag = True


def reset_all():
    global no_url
    no_url = True
    window['O_VIDEO'].update(False)
    window['O_AUDIO'].update(False)
    window['BOTH_A_V'].update(False)
    window['DROP_DOWN'].update(value="", values=[])
    window['FOLDER'].update("")


# Define the window's contents
layout = [[sg.Text("YouTube URL", text_color='white')],

          [sg.Input(key='INPUT', enable_events='True',text_color='white', size=(74,1)),
           sg.Button("Search...", enable_events=True, change_submits=True,key = 'SEARCH', button_color=('white', 'springgreen4'), size=(74,1))],

          [sg.Text(size=(40,1), key='OUTPUT')],

          [sg.Radio('Only Audio   ', "RADIO1", text_color='white', default=False, key="O_AUDIO", enable_events=True,change_submits=True) ,
           sg.Radio('Only Video   ', "RADIO1", text_color='white', default=False, key="O_VIDEO", enable_events=True,change_submits=True),
           sg.Radio('Both (AV)   ', "RADIO1", text_color='white', default=False, key="BOTH_A_V", enable_events=True, change_submits=True),
           sg.Text('Bitrate/Resolution', text_color='white'),
           sg.Combo(drop_down_list, key ='DROP_DOWN', enable_events=True,size=(8,1), bind_return_key=True, text_color='white')],

          [sg.Text()],
          [sg.Text('Download Folder',size=(15,1), text_color='white')],
          [sg.InputText(key='FOLDER', size=(55,1), enable_events=True, text_color='white'),FolderBrowse(button_text="Browse", size=(15,1), button_color=('white', 'springgreen4'), enable_events=True),
           sg.Button('Submit', button_color=('white', 'springgreen4'), key='SUBMIT', enable_events=True, size=(50,1))],

          [sg.Text()],
          [sg.Text(size=(40,1),key="DOWNLOAD_PROGRESS")],
          [sg.Image(r'',  key='PROGRESS_BAR', size=(700, 10))],
          
          [sg.Text()],
          [sg.Text()],
          [sg.Text('Thanks for trying YouTube Video Downloader', justification='center', size=(100,1), text_color='#ECCA1C')],
          [sg.Text('@Charan',  tooltip='https://www.linkedin.com/in/charan-c/', enable_events=True, key='Charan', justification='right',size=(100,1), text_color='#EAE70F')]
         ]

# Create the window
sg.theme("DarkBlue")
window = sg.Window('YouTube Video Downloader', layout, size = (700, 400))

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=100)
    
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    
    if event == 'SEARCH':
        try:
            url = values['INPUT']
            yt = YouTube(url)
            
            # Output a message to the window
            window['OUTPUT'].update(yt.title)
            
            window['DOWNLOAD_PROGRESS'].update("")
            window.FindElement("PROGRESS_BAR").UpdateAnimation(r'',time_between_frames=10)

            no_url = False
        except:
            reset_all() 
            sg.popup_error("Please enter a YouTube URL") 

    if event == 'DROP_DOWN':
        video_id = values["DROP_DOWN"]
        print(video_id)

    if values['O_AUDIO'] == True  and count1 == 1:
        try:
            itag_dict = {}
            filter = yt.streams.filter(only_audio=True)
            itag_dict = regexpression_for_filtering_audio_quality_and_itag(filter)

            window['DROP_DOWN'].update(value="", values=sorted(drop_down_list) )
            print(drop_down_list)
            count1 = 2
            count2 = count3 = 1
        except:
            reset_all()
            sg.popup_error("Please enter a YouTube URL")

    if values['O_VIDEO'] == True  and count2 == 1:
        try:
            itag_dict = {}

            filter = yt.streams.filter(file_extension='mp4')
            itag_dict = regexpression_for_filtering_res_and_itag(filter)

            window['DROP_DOWN'].update(value="", values=sorted(drop_down_list))
            print(drop_down_list)
            count2 = 2
            count1 = count3 = 1
        except:
            reset_all()
            sg.popup_error("Please enter a YouTube URL")

    if values['BOTH_A_V'] == True and count3 == 1:
        try:
            itag_dict = {}
            filter = yt.streams.filter(progressive=True, file_extension='mp4')
            itag_dict = regexpression_for_filtering_res_and_itag(filter)

            window['DROP_DOWN'].update(value="", values=sorted(drop_down_list))
            print(drop_down_list)
            count3 = 2
            count1 = count2 = 1
        except:
             reset_all()
             sg.popup_error("Please enter a YouTube URL")

    if event == 'FOLDER':
        try:
            file_path = values['FOLDER']
        except:
            sg.popup_error("Please enter a proper folder")

    if event == 'SUBMIT':
        try:
            if no_url:
                raise NameError

            if video_id == None or file_path == None:
                raise KeyError
            
            dwnld_thread = Thread(target = yt_download, args = (video_id, file_path), daemon = True)
            dwnld_thread.setDaemon(True)
            dwnld_thread.start()  
        except NameError:
            sg.popup_error("Please enter a YouTube URL")
        except KeyError:
            sg.popup_error("Please select Bitrate/Resolution options")
        except Exception:
            sg.popup_error("Something went wrong")

    if event == 'Charan':
        webbrowser.open('https://www.linkedin.com/in/charan-c/')
            
# Finish up by removing from the screen
window.close()


