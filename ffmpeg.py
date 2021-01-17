import numpy as np
import subprocess as sp
import os
import time
import ffmpeg
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

def aureadmeta(fn):
    if not os.path.exists(fn):
        raise FileNotFoundError
    probe = ffmpeg.probe(fn)
    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            meta = {
                'channels': stream['channels'],
                'sample_rate': int(stream['sample_rate']),
                'duration': float(probe['format']['duration'])
            }
            return meta
    return None

# auread should be combined with aureadmeta to not force the samplerate or input type if they are None
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
    
import json
def vidreadmeta(fn):
    if not os.path.exists(fn):
        raise FileNotFoundError
    probe = ffmpeg.probe(fn)
    for stream in probe['streams']:
        if stream['codec_type'] == 'video':
            meta = {
                'width': int(stream['width']),
                'height': int(stream['height']),
                'duration': float(probe['format']['duration'])
            }
            return meta
    return None

def vidread(fn, samples=None, rate=None, hwaccel=None):
    if not os.path.exists(fn):
        raise FileNotFoundError
    probe = ffmpeg.probe(fn)
    out_params = {}
    for stream in probe['streams']:
        if stream['codec_type'] == 'video':
            width, height = stream['width'], stream['height']
            try:
                if stream['tags']['rotate'] in ['90','270','-90']: # not sure if -90 ever happens
                    width, height = height, width
            except KeyError:
                pass
            if samples is not None:
                duration = float(stream['duration'])
                interval = duration / samples
                out_params['r'] = 1 / interval
                out_params['ss'] = interval / 2
            elif rate is not None:
                out_params['r'] = rate
                out_params['ss'] = 1 / (2 * rate)
    in_params = {}
    if hwaccel is not None:
        in_params['hwaccel'] = hwaccel
    proc = (
        ffmpeg
        .input(fn, **in_params)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', **out_params)
        .run_async(pipe_stdout=True)
    )
    channels = 3
    frame_number = -1
    while True:
        in_bytes = proc.stdout.read(width*height*channels)
        frame_number += 1
        if not in_bytes:
            break
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([height, width, channels])
        )
        yield in_frame
    proc.wait()

class VideoWriter:
    def __init__(self, fn, vcodec='libx264', fps=60, in_pix_fmt='rgb24', out_pix_fmt='yuv420p', input_args=None, output_args=None):
        self.fn = fn
        self.process = None
        self.input_args = {} if input_args is None else input_args
        self.output_args = {} if output_args is None else output_args
        self.input_args['framerate'] = fps
        self.input_args['pix_fmt'] = in_pix_fmt
        self.output_args['pix_fmt'] = out_pix_fmt
        self.output_args['vcodec'] = vcodec
    
    def add(self, frame):
        if self.process is None:
            h,w = frame.shape[:2]
            self.process = (
                ffmpeg
                    .input('pipe:', format='rawvideo', s='{}x{}'.format(w, h), **self.input_args)
                    .output(self.fn, **self.output_args)
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
