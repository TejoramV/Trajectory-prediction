!pip install urllib
!pip install m3u8
!pip install streamlink
import urllib
import m3u8
import streamlink
import subprocess
import os


def get_stream(url):
    """
    Get upload chunk URL
    """
    streams = streamlink.streams(url)
    stream_url = streams["best"]

    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]


def dl_stream(url, filename, chunks):
    """
    Download and save video frames as PNG files
    """
    pre_time_stamp = 0
    for i in range(chunks+1):
        stream_segment = get_stream(url)
        cur_time_stamp = stream_segment.program_date_time.strftime("%Y%m%d-%H%M%S")

        if pre_time_stamp == cur_time_stamp:
            pass
        else:
            print(cur_time_stamp)

            # Download the segment
            with urllib.request.urlopen(stream_segment.uri) as response:
                data = response.read()

            # Save the segment as a temporary video file
            temp_filename = filename + '_temp.ts'
            with open(temp_filename, 'wb') as file:
                file.write(data)

            # Extract video frames using ffmpeg
            output_filename = filename + '_' + str(cur_time_stamp) + '.png'
            subprocess.run(['ffmpeg', '-i', temp_filename, '-vf', 'fps=1', output_filename])

            # Delete the temporary video file
            os.remove(temp_filename)

            pre_time_stamp = cur_time_stamp


url = "https://www.youtube.com/watch?v=NQEOfN-HU2o"
dl_stream(url, "live", 15)
