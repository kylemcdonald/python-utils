import numpy as np
import subprocess as sp
import os
import time
DEVNULL = open(os.devnull, 'w')

# attempts to handle all float/integer conversions with and without normalizing
def convert_bit_depth(y, in_type, out_type, normalize=False):
    in_type = np.dtype(in_type).type
    out_type = np.dtype(out_type).type
    
    if normalize:
        peak = np.abs(y).max()
        if peak == 0:
            normalize = False
            
    if issubclass(in_type, np.floating):
        if normalize:
            y /= peak
        if issubclass(out_type, np.integer):
            y *= np.iinfo(out_type).max
        y = y.astype(out_type)
    elif issubclass(in_type, np.integer):
        if issubclass(out_type, np.floating):
            y = y.astype(out_type)
            if normalize:
                y /= peak
        elif issubclass(out_type, np.integer):
            in_max = peak if normalize else np.iinfo(in_type).max
            out_max = np.iinfo(out_type).max
            if out_max > in_max:
                y = y.astype(out_type)
                y *= (out_max / in_max)
            elif out_max < in_max:
                y /= (in_max / out_max)
                y = y.astype(out_type)
    return y

# load_audio can not detect the input type
# could use a command like this with sr=None or detect=True:
# ffprobe -hide_banner \
#     -loglevel fatal \
#     -show_error \
#     -show_format \
#     -show_streams \
#     -print_format json \
#     -i fn
def auread(filename, sr=44100, mono=False, normalize=True, in_type=np.int16, out_type=np.float32):
    in_type = np.dtype(in_type).type
    out_type = np.dtype(out_type).type
    channels = 1 if mono else 2
    format_strings = {
        np.float64: 'f64le',
        np.float32: 'f32le',
        np.int16: 's16le',
        np.int32: 's32le',
        np.uint32: 'u32le'
    }
    format_string = format_strings[in_type]
    command = [
        'ffmpeg',
        '-i', filename,
        '-f', format_string,
        '-acodec', 'pcm_' + format_string,
        '-ar', str(sr),
        '-ac', str(channels),
        '-']
    p = sp.Popen(command, stdout=sp.PIPE, stderr=DEVNULL)
    raw, err = p.communicate()
    audio = np.frombuffer(raw, dtype=in_type)
    
    if channels > 1:
        audio = audio.reshape((-1, channels)).transpose()

    if audio.size == 0:
        return audio.astype(out_type), sr
    
    audio = convert_bit_depth(audio, in_type, out_type, normalize)

    return audio, sr

def auwrite(fn, audio, sr, channels=1):
    format_strings = {
        'float64': 'f64le',
        'float32': 'f32le',
        'int16': 's16le',
        'int32': 's32le',
        'uint32': 'u32le'
    }
    format_strings = {np.dtype(key): value for key,value in format_strings.items()}
    format_string = format_strings[audio.dtype]
    command = [
        'ffmpeg',
        '-y',
        '-ar', str(sr),
        '-f', format_string,
        '-i', 'pipe:',
        fn]
    p = sp.Popen(command, stdin=sp.PIPE, stdout=None, stderr=None)
    raw, err = p.communicate(audio.tobytes())
    
import ffmpeg

class VideoWriter:
    def __init__(self, fn, vcodec='libx264', fps=60, in_pix_fmt='rgb24', out_pix_fmt='yuv420p'):
        self.fn = fn
        self.vcodec = vcodec
        self.fps = fps
        self.process = None
        self.in_pix_fmt = in_pix_fmt
        self.out_pix_fmt = out_pix_fmt
    
    def add(self, frame):
        if self.process is None:
            h,w = frame.shape[:2]
            self.process = (
                ffmpeg
                    .input('pipe:', format='rawvideo', pix_fmt=self.in_pix_fmt, s='{}x{}'.format(w, h), framerate=self.fps)
                    .output(self.fn, pix_fmt=self.out_pix_fmt, vcodec=self.vcodec)
                    .overwrite_output()
                    .run_async(pipe_stdin=True)
            )
        self.process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )

    def close(self):
        if self.process is None:
            return
        self.process.stdin.close()
        self.process.wait()

def vidwrite(fn, images, **kwargs):
    writer = VideoWriter(fn, **kwargs)
    for image in images:
        writer.add(image)
    writer.close()