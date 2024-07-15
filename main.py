from enum import Enum
from pytube import YouTube
from pytube.exceptions import RegexMatchError

# remove patch below if pytube fixed the bug
from pytube import cipher
from patch import get_throttling_function_name as patched_func
cipher.get_throttling_function_name = patched_func

# link for testing
# https://youtu.be/3c-176VE_qQ?si=v0sCwEcDTJlvGim7

# workaround age restricted
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


class OutputType(Enum):
    VIDEO = "video"
    AUDIO = "audio"


file_endings = {
    OutputType.VIDEO: ".mp4",
    OutputType.AUDIO: ".mp3"
}


def get_data_by_url(url, output_type):
    try:
        if output_type == OutputType.VIDEO:
            return YouTube(url).streams.first()
        else:
            return YouTube(url).streams.filter(only_audio=True).first()
    except RegexMatchError as e:
        return None


def parse_output_type_input(output_type):
    lowered_wo_whitespace = output_type.lower().replace(" ", "")
    if lowered_wo_whitespace in OutputType.VIDEO.value:
        return OutputType.VIDEO
    else:
        return OutputType.AUDIO


def convert_video(url_input, output_type):
    data = get_data_by_url(url_input, output_type)
    if data is None:
        print("Conversion of url >{}< didn't work".format(url_input))
        return
    filename = "{}{}".format(data.default_filename.split(".")[0], file_endings[output_type])
    data.download(output_path="results/", filename=filename)
    print("SUCCESS")


if __name__ == '__main__':
    url_input = input("Enter the urls separated by comma (url1, url2, ...): ")
    urls = url_input.split(",")
    output_type_input = input("Choose between the output types {}, {} (substrings are enough): ".format(OutputType.VIDEO.value, OutputType.AUDIO.value))
    output_type = parse_output_type_input(output_type_input)
    print("{} selected".format(output_type.value))
    for url in urls:
        url_wo_whitespace = url.replace(" ", "")
        convert_video(url_wo_whitespace, output_type)

