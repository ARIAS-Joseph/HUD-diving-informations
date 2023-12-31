#
# ARIAS Joseph
#
# Release V2.06
#   - Support Windows (Test on Windows 10) and Linux (Test on Ubuntu & Kali)
#     --------------------------------------
#     - My processor : Intel64 Family 6 Model 85 Stepping 7, GenuineIntel
#     - My OS : Windows
#     - My OS Relase : Windows-10-10.0.19044-SP0
#     - My Python Version :3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)]
#     - My FFMPEG : ffmpeg version 2023-07-19-git-efa6cec759-full_build-www.gyan.dev Copyright (c) 2000-2023 the FFmpeg developers
#     --------------------------------------
# For Windows
#   - Install FFMPEG : https://www.gyan.dev/ffmpeg/builds/ or see https://ffmpeg.org/download.html#build-windows
#   - And also install with PIP :
#       - python -m pip install plotly
#       - python -m pip install kaleido
#       - pip install Pillow
#
# For Windows : Don't put folder in OneDrive ... too many files and too big.
#
#

from PIL import Image, ImageDraw, ImageFont
import csv
import os
import subprocess
from datetime import datetime
import time
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import platform
import sys
import types
import argparse


def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            try:
                yield val.__name__, val.__version__
            except:
                yield val.__name__, 'no version available for built ins'


if platform.system() == "Windows":
    import tkinter as tk

# import gauges

if platform.system() == "Windows":
    window = tk.Tk()
    window.title('HUD Diving information')

    fichier = tk.Label(window, text='Choose a file')
    # fichier.bind(tk.filedialog.askopenfile(mode='rb', title='Choose a file'))

print("-----------------------START-------------------------------")
start_time = int(time.time())

# Init
my_file = 'test.csv'
my_path = os.getcwd()

if platform.system() == "Windows":
    my_tempFolder = './tmpPNG'
else:
    my_tempFolder = 'tmpPNG'

if platform.system() == "Windows":
    # my_path2 = my_path.replace(' ', '\ ')
    # my_path2 = my_path2.replace('-', '\-')
    my_path2 = my_path
    my_videooutput = '"'+my_path2+'\\video.mp4'+'"'
    my_videoinput = '"'+my_path2+'\\Luccut.mp4'+'"'
    my_videooutputmerge = '"'+my_path2+'\\videomerge.mp4'+'"'
    my_videooutputmergecompress = '"'+my_path2+'\\videomergecompress.mp4'+'"'
    my_videooutputcompress = '"'+my_path2+'\\videocompress.mp4'+'"'
    my_videooutput2 = my_path2+'\\video.mp4'
    my_videoinput2 = my_path2+'\\Luccut.mp4'
    my_videooutputmerge2 = my_path2+'\\videomerge.mp4'
    my_videooutputmergecompress2 = my_path2+'\\videomergecompress.mp4'
    my_videooutputcompress2 = my_path2+'\\videocompress.mp4'
    my_time_file = my_path+"\\Time.png"
    my_pression_file = my_path+"\\Pression.png"
    my_depth_file = my_path+"\\Profondeur.png"
    my_temp_file = my_path+"\\Temp.png"
else:
    my_videooutput = 'video.mp4'
    my_videoinput = 'Luccut.mp4'
    my_videooutputmerge = 'videomerge.mp4'
    my_videooutputmergecompress = 'videomergecompress.mp4'
    my_videooutputcompress = 'videocompress.mp4'
    my_videoinput2 = 'TestVideo.mp4'
    my_videooutputmerge2 = 'videomerge.mp4'
    my_videooutputmergecompress2 = 'videomergecompress.mp4'
    my_videooutputcompress2 = 'videocompress.mp4'
    my_time_file = "Time.png"
    my_pression_file = "Pression.png"
    my_depth_file = "Profondeur.png"
    my_temp_file = "Temp.png"

my_font = "./FreeMono.ttf"

if platform.system() == "Windows":
    my_ffmpeg = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
elif platform.system() == "Darwin":
    my_ffmpeg = '/usr/local/bin/ffmpeg'
else:
    my_ffmpeg = '/usr/bin/ffmpeg'

my_num_depth = 0

my_h = 1280
my_w = 720
my_scale = 0.5
my_scale_2 = 0.8
my_frequency = 9
my_font_size = 60
my_font_size_2 = 40
my_font_size_3 = 50
my_color = "white"
my_familly = "Arial"
# Most important parameter !!!
my_start_time = 1


parser = argparse.ArgumentParser(description="HUD Diving information",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-H", "--height", default=1280,
                    action="store_true", help="height")
parser.add_argument("-W", "--witdh", default=720,
                    action="store_true", help="with")
parser.add_argument("-S", "--scale", default=0.5,
                    action="store_true", help="scale")
parser.add_argument("-T", "--scale2", default=0.8,
                    action="store_true", help="scale2")
parser.add_argument("-F", "--frequency", default=9,
                    action="store_true", help="ferquency")
parser.add_argument("-A", "--font", default=60,
                    action="store_true", help="font")
parser.add_argument("-B", "--font2", default=40,
                    action="store_true", help="font2")
parser.add_argument("-C", "--font3", default=50,
                    action="store_true", help="font3")
parser.add_argument("-D", "--color", default="white",
                    action="store_true", help="color")
parser.add_argument("-E", "--familly", default="Arial",
                    action="store_true", help="familly")
parser.add_argument("-SC", "--source_csv", default="test.csv",
                    action="store_true", help="Source location")
parser.add_argument("-DV", "--destination_video", default="videomerge.mp4",
                    action="store_true", help="Destination location")
args = parser.parse_args()
# config = vars(args)

List_Depth = []

last_temp = '?'
last_pressure = '?'

if not os.path.exists(my_tempFolder):
    os.makedirs(my_tempFolder)

# Get information for support.

print("---------------------------------------------------------------")
print("-----------------ADD THIS IN CASE OF ISSUE---------------------")
print("My processor : %s " % (platform.processor()))
print("My OS : "+platform.system())
print("My OS Relase : "+platform.platform())
print("My Python Version :"+sys.version)
print("My FFMPEG :")
os.system(my_ffmpeg+" -version ")
print("My access to Time File : "+str(os.access(my_time_file, os.W_OK)))
print("My access to Pression File : "+str(os.access(my_pression_file, os.W_OK)))
if os.access(my_pression_file, os.W_OK) == False:
    print("WARNING : Not possible to write file ... change folder please ")
print("My Lib used :")
print(list(imports()))
print("My Conf :")
# print(config)
print("-------------------------THANK--------------------------")
print("--------------------------------------------------------")
# Step 0 :
# remove previous Video

# os.system('rm -rf ./video.webm');
print("1-Clean")
if platform.system() == "Linux" or platform.system() == "linux" or platform.system() == "linux2":
    os.system('rm -rf ./video.mp4')
    os.system('rm -rf ./videomerge.mp4')
    os.system('rm -rf ./videomergecompress.mp4')
    os.system('rm -rf ./videocompress.mp4')

# Step 1 :
# Find min & max of value

print("2-First parse")
with open(my_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        elif line_count == 1:
            List_Depth.append(-float(row[4]))
            my_num_depth += 1
            min_depth = float(row[4])
            max_depth = float(row[4])
            first_temp = '?'
            min_temp = '?'
            max_temp = '?'
            first_pressure = '?'
            min_pressure = '?'
            max_pressure = '?'
            line_count += 1
        else:
            List_Depth.append(-float(row[4]))
            my_num_depth += 1
            if (float(row[4]) > max_depth):
                max_depth = float(row[4])
            if (float(row[4]) < min_depth):
                min_depth = float(row[4])
            if len(row[5]) > 0:
                last_temp = float(row[5])
            if len(row[6]) > 0:
                last_pressure = float(row[6])
            if (last_temp != '?'):
                if first_temp == '?':
                    first_temp = last_temp
                if min_temp == '?':
                    min_temp = last_temp
                if max_temp == '?':
                    max_temp = last_temp
                if (last_temp > max_temp):
                    max_temp = last_temp
                if (last_temp < min_temp):
                    min_temp = last_temp
            if (last_pressure != '?'):
                if first_pressure == '?':
                    first_pressure = last_pressure
                if min_pressure == '?':
                    min_pressure = last_pressure
                if max_pressure == '?':
                    max_pressure = last_pressure
                if (last_pressure > max_pressure):
                    max_pressure = last_pressure
                if (last_pressure < min_pressure):
                    min_pressure = last_pressure
            line_count += 1

# To debug
# print("Temp Min "+str(min_temp)+" Max "+str(max_temp)+" Depth Min "
# +str(min_depth)+" Max "+str(max_depth)+" Pressure Min "+str(min_pressure)+
# " Max "+str(max_pressure));
# print(List_Depth)

last_temp = first_temp
last_pressure = first_pressure
previous_depth = 0
current_num_depth = 0

print("3-Create picture")
with open(my_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            print('\t Time '+row[3]+' ')
            img = Image.new('RGBA', (my_h, my_w), (255, 0, 0, 0))
            if len(row[5]) > 0:
                last_temp = row[5]
            if len(row[6]) > 0:
                last_pressure = row[6]
            fnt = ImageFont.truetype(my_font, 40)

            # draw1 = ImageDraw.Draw(img)
            # draw1.text((10, 0), "Dive number : "+row[0]+" ", font=fnt,
            # fill=(25, 25, 75, 75), stroke_width=4, stroke_fill="black")
            # draw1 = ImageDraw.Draw(img)
            # draw1.text((10, 60), "Time : "+row[3]+" ", font=fnt,
            # fill=(25, 25, 75, 75), stroke_width=4, stroke_fill="black")
            # draw2 = ImageDraw.Draw(img)
            # draw2.text((10, 120), "Depth : "+row[4]+" m ", font=fnt,
            # fill=(25, 25, 75, 75), stroke_width=4, stroke_fill="black")
            # draw3 = ImageDraw.Draw(img)
            # draw3.text((10, 180), "Temperature : "+last_temp+" C ",
            # font=fnt, fill=(25, 25, 75, 75), stroke_width=4,
            # stroke_fill="black")
            # draw4 = ImageDraw.Draw(img)
            # draw4.text((10, 240), "Pressure : "+last_pressure+" Bar ",
            # font=fnt, fill=(25, 25, 75, 75), stroke_width=4,
            # stroke_fill="black")

            # Pressure
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=int(float(last_pressure)),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Pressure", 'font': {'size': my_font_size}},
                delta={'reference': int(float(max_pressure)), 'increasing': {
                    'color': "RebeccaPurple"}},
                gauge={
                    'axis': {'range': [None, 200], 'tickwidth': 1,
                             'tickcolor': my_color},
                    'bar': {'color': "purple"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': 'red'},
                        {'range': [50, 100], 'color': 'orange'},
                        {'range': [100, 200], 'color': 'green'}],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': int(float(last_pressure))}}))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={
                              'color': my_color, 'family': my_familly})
            fig.write_image(my_pression_file, scale=my_scale)

            # Time
            fig = go.Figure(go.Indicator(
                mode="number",
                value=line_count,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': 'Time '+row[3], 'font': {'size': my_font_size}}
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={
                              'color': my_color, 'family': my_familly})
            fig.write_image(my_time_file, scale=my_scale)

            # Depth
            layout = Layout(plot_bgcolor='rgba(0,0,0,0)')
            fig = go.Figure(layout=layout)
            fig.add_trace(go.Indicator(
                mode="number+delta",
                value=-int(float(row[4])),
                delta={"reference": previous_depth, "valueformat": ".0f"},
                title={"text": "Depth", 'font': {'size': my_font_size_2}},
                domain={'y': [0, 1], 'x': [0.25, 0.75]}))
            fig.add_trace(go.Scatter(
                y=List_Depth, line=dict(color="purple", width=10)))
            fig.add_hline(
                y=-int(float(row[4])), line_width=5, line_dash="dash",
                line_color="green")
            fig.add_vline(x=current_num_depth, line_width=5,
                          line_dash="dash", line_color="green")
            fig.add_vrect(x0=0, x1=current_num_depth,
                          line_width=0, fillcolor="red", opacity=0.3)
            fig.update_layout(xaxis={'range': [0, my_num_depth]})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={
                              'color': my_color, 'family': my_familly})
            fig.write_image(my_depth_file, scale=my_scale_2)

            # Temp
            fig = go.Figure(go.Indicator(
                mode="number+gauge+delta",
                gauge={'shape': "bullet"},
                delta={'reference': max_temp},
                value=int(float(last_temp)),
                domain={'x': [0.1, 1], 'y': [0.2, 0.9]},
                title={'text': "Temp", 'font': {'size': my_font_size_3}}))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={
                              'color': my_color, 'family': my_familly})
            fig.write_image(my_temp_file, scale=my_scale)

            foreground = Image.open(my_pression_file)
            img.paste(foreground, (0, 100), foreground)

            foreground = Image.open(my_time_file)
            img.paste(foreground, (0, -40), foreground)

            foreground = Image.open(my_depth_file)
            img.paste(foreground, (-30, my_w-350), foreground)

            foreground = Image.open(my_temp_file)
            img.paste(foreground, (my_h-350, my_w-150), foreground)

            filename = my_tempFolder+'/pic-%04d.png' % line_count
            img.save(filename, 'PNG')
            line_count += 1
            previous_depth = -int(float(row[4]))
            current_num_depth += 1
            i = 1
            while i <= my_frequency:
                img = Image.new('RGBA', (my_h, my_w), (255, 0, 0, 0))
                my_time = row[3]
                my_time = my_time[:-1] + str(i)

                fig = go.Figure(go.Indicator(
                    mode="number",
                    value=line_count,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': 'Time '+my_time,
                           'font': {'size': my_font_size}}
                ))
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={
                                  'color': my_color, 'family': my_familly})
                fig.write_image(my_time_file, scale=my_scale)

                # draw1 = ImageDraw.Draw(img)
                # draw1.text((10, 0), "Dive number : "+row[0]+" ", font=fnt,
                # fill=(25, 25, 75, 75), stroke_width=4, stroke_fill="black")
                # draw1 = ImageDraw.Draw(img)
                # draw1.text((10, 60), "Time : "+time+" ", font=fnt,
                # fill=(25, 25, 75, 75), stroke_width=4, stroke_fill="black")
                # draw2 = ImageDraw.Draw(img)
                # draw2.text((10, 120), "Depth : "+row[4]+" m ", font=fnt,
                # fill=(25, 25, 75, 75), stroke_width=4, stroke_fill="black")
                # draw3 = ImageDraw.Draw(img)
                # draw3.text((10, 180), "Temperature : "+last_temp+" C ",
                # font=fnt, fill=(25, 25, 75, 75), stroke_width=4,
                # stroke_fill="black")
                # draw4 = ImageDraw.Draw(img)
                # draw4.text((10, 240), "Pressure : "+last_pressure+" Bar ",
                # font=fnt, fill=(25, 25, 75, 75), stroke_width=4,
                # stroke_fill="black")

                foreground = Image.open(my_pression_file)
                img.paste(foreground, (0, 100), foreground)

                foreground = Image.open(my_time_file)
                img.paste(foreground, (0, -40), foreground)

                foreground = Image.open(my_depth_file)
                img.paste(foreground, (-30, my_w-350), foreground)

                foreground = Image.open(my_temp_file)
                img.paste(foreground, (my_h-350, my_w-150), foreground)

                filename = my_tempFolder+'/pic-%04d.png' % line_count
                img.save(filename, 'PNG')
                line_count += 1
                i += 1
    print(f'Processed {line_count} files PNG.')

# Other test :
# os.system('/usr/bin/ffmpeg -r 1 -s 1280x720 -i tmpPNG/pic-%04d.png -crf 25
# -pix_fmt yuva420p video.webm');

# os.system('/usr/bin/ffmpeg -r 1 -s 1280x720 -i tmpPNG/pic-%04d.png -c:v png
# -auto-alt-ref 0 -pix_fmt rgba video.mov');

# Good test :
print("4-Create video with picture")
my_command = my_ffmpeg+' -framerate 1 -start_number '+str(my_start_time)+'  -s ' + str(
    my_h) + 'x'+str(my_w)+' -i ' + my_tempFolder + '/pic-%04d.png  -y -c:v png -r 1 ' + my_videooutput
print("The command (1) : "+my_command)
os.system(my_command)

# Clean space
# os.system('rm -rf ./tmpPNG');

print("5-Merge two video")
my_command = my_ffmpeg+'  -y  -i '+my_videoinput+' -i ' + my_videooutput + ' -filter_complex "  [0:v]setpts=PTS-STARTPTS, scale='+str(my_h) + 'x' + str(my_w)+'[top]; [1:v]setpts=PTS-STARTPTS, scale='+str(
    my_h) + 'x'+str(my_w) + ',  format=yuva420p,colorchannelmixer=aa=0.5[bottom];  [top][bottom]overlay=shortest=1"  -c:a aac -vcodec libx264 '+my_videooutputmerge
print("The command (2) : "+my_command)
os.system(my_command)

print("6-(optionnal) Compress video")

os.system(my_ffmpeg+' -y  -i '+my_videooutputmerge +
          ' -vcodec libx265 -crf 28 '+my_videooutputmergecompress)
os.system(my_ffmpeg+' -y  -i '+my_videooutput +
          ' -vcodec libx265 -crf 28 '+my_videooutputcompress)

end_time = int(time.time())

print("--------------------------------------------------------")
print('Resolution : ' + str(my_h) + ' x '+str(my_w))
file_stats = os.stat(my_videooutputmerge2)
print('File Size '+my_videooutputmerge2+' in MegaBytes is %d ' %
      (file_stats.st_size / (1024 * 1024)))
file_stats = os.stat(my_videooutputmergecompress2)
print('File Size '+my_videooutputmergecompress2+' in MegaBytes is %d ' %
      (file_stats.st_size / (1024 * 1024)))
file_stats = os.stat(my_videooutput2)
print('File Size '+my_videooutput2+' in MegaBytes is %d ' %
      (file_stats.st_size / (1024 * 1024)))
file_stats = os.stat(my_videooutputcompress2)
print('File Size '+my_videooutputcompress2+' in MegaBytes is %d ' %
      (file_stats.st_size / (1024 * 1024)))
print("End (%d sec)" % (end_time-start_time))
print("--------------------------------------------------------")

if platform.system() == "Windows":
    window.mainloop()
