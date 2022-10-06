import csv 
import os
import youtube_dl
import cv2
from moviepy.editor import *
from utils import read_url_info

def download_tmp_vids(video_dir, url_and_time):
    for u, (s_t, e_t) in url_and_time.items():
        fname = u.split("=")[1] + '_tmp.mp4'
        print('Processing {}'.format(fname))
        ydl_opts = {'outtmpl': os.path.join(video_dir, fname), 'format': 'mp4'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([u])

def cut_resize_fps(video_dir, url_and_time, video_height, fps):
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

def save_frames(video_dir, image_dir):
    video_ids = [fp.split('.')[0] for fp in os.listdir(video_dir) if fp[0]!='.']

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
        vidcap.release()
        
if __name__=='__main__':
    video_dir = './vids'
    image_dir = './imgs'
    audio_dir = './audios'

    url_fp = 'url.csv'
    video_height = 720
    url_and_time = dict()
    fps = 30

    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    url_and_time = read_url_info(url_fp)
    download_tmp_vids(video_dir, url_and_time)
    cut_resize_fps(video_dir, url_and_time, video_height, fps)
    save_frames(video_dir, image_dir)