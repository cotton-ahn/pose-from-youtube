import csv 
import os
import youtube_dl
import cv2
from moviepy.editor import *

video_dir = './vids'
image_dir = './imgs'
video_height = 720
url_and_time = dict()
fps = 30

with open('url.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    cnt = 0
    for row in csv_reader:
        if cnt > 0:
            url_and_time[row[0]] = (float(row[1]), float(row[2]))
        cnt += 1
print(url_and_time)

os.makedirs(video_dir, exist_ok=True)

for u, (s_t, e_t) in url_and_time.items():
    fname = u.split("=")[1] + '_tmp.mp4'
    print('Processing {}'.format(fname))
    ydl_opts = {'outtmpl': os.path.join(video_dir, fname), 'format': 'mp4'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([u])
video_files = [os.path.join(video_dir, fp) for fp in os.listdir(video_dir) if fp[0]!='.']
for fp in video_files:
    (s_t, e_t) = url_and_time['https://www.youtube.com/watch?v='+fp.split('/')[-1].split('_tmp')[0]]
    clip = VideoFileClip(fp).subclip(s_t, e_t)
    clip = clip.resize(height=video_height)
    print('FPS: ', clip.fps, '-------------->', fps)
    clip.write_videofile(fp.replace('_tmp', ''), fps=fps)
    
    clip.reader.close()
    if '_tmp.mp4' in fp:
        os.remove(fp)

video_ids = [fp.split('.')[0] for fp in os.listdir(video_dir) if fp[0]!='.']

os.makedirs(os.path.join(image_dir), exist_ok=True)
for v_id in video_ids:
    os.makedirs(os.path.join(image_dir, v_id), exist_ok=True)
    vid_fp = os.path.join(video_dir, v_id+'.mp4')
    
    print('Reading {}'.format(vid_fp))
    
    vidcap = cv2.VideoCapture(vid_fp)
    success, image = vidcap.read()
    cnt = 0
    while success:
        cv2.imwrite(os.path.join(image_dir, v_id, "scene_{0:08}.jpg".format(cnt)), image)
        success, image = vidcap.read()
        cnt += 1