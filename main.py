from enum import Enum
from pytubefix import YouTube, Stream
from pytubefix.exceptions import RegexMatchError

# link for testing
# https://youtu.be/3c-176VE_qQ?si=v0sCwEcDTJlvGim7

# workaround age restricted
from pytubefix.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


class OutputType(Enum):
    VIDEO = "video"
    AUDIO = "audio"


file_endings = {
    OutputType.VIDEO: ".mp4",
    OutputType.AUDIO: ".mp3"
}


def get_data_with_url(url, output_type) -> (Stream | None):
    try:
        if output_type == OutputType.VIDEO:
            return YouTube(url).streams.first()
        else:
            return YouTube(url).streams.filter(only_audio=True).first()
    except RegexMatchError:
        return None


def output_type_from_str(output_type: str) -> OutputType:
    lowered_wo_whitespace = output_type.lower().replace(" ", "")
    if lowered_wo_whitespace in OutputType.VIDEO.value:
        return OutputType.VIDEO
    else:
        return OutputType.AUDIO


def convert_video(url_input, output_type):
    data: (Stream | None) = get_data_with_url(url_input, output_type)
    if data is None:
        print("Conversion of url >{}< didn't work".format(url_input))
        return False
    filename: str = "{}{}".format(data.default_filename.split(".")[0], file_endings[output_type])
    filename = filename.replace(" ", "_")
    data.download(output_path="results/", filename=filename)
    print("SUCCESS")


if __name__ == '__main__':
    url_input: str = input("Enter the urls separated by comma (url1, url2, ...): ")
    urls: list[str] = url_input.split(",")
    output_type_str: str = input("Choose between the output types {}, {} (substrings are enough): ".format(OutputType.VIDEO.value, OutputType.AUDIO.value))
    output_type: OutputType = output_type_from_str(output_type_str)
    print("{} selected".format(output_type.value))
    for url in urls:
        url_wo_whitespace: str = url.replace(" ", "")
        convert_video(url_wo_whitespace, output_type)

