# Name: Jeff Yostanto
# Microservice
# CS 361

from mutagen.mp3 import MP3
import os
import time

# Citation: https://www.geeksforgeeks.org/how-to-get-the-duration-of-audio-in-python/
def audio_duration(length):
    """
    Function to return total length of a mp3 file in the format of
    hours, minutes and seconds.
    """
    hours = length // 3600
    length %= 3600
    mins = length // 60
    length %= 60
    seconds = length

    return hours, mins, seconds


# Citation: https://www.programcreek.com/python/?CodeExample=wait+for+file
def wait_for_file(source_dir, filename, timeout=100):
        """Wait for the creation of the specific file.

        This method checks if the specified file exists and waits for it to
        appear during the specified amount of time (by default 10 seconds).

        source_dir[in]  Source directory where the file is located.
        filename[in]    Name of the file to wait for.
        timeout[in]     Time to wait in seconds (by default 10 seconds).
        """
        file_path = os.path.normpath(os.path.join(source_dir, filename))
        attempts = 0
        while attempts < timeout:
            # Check if the file exists.
            if os.path.isfile(file_path):
                return True
            # Wait 1 second before trying again.
            time.sleep(1)
            attempts += 1


# Citation: https://www.geeksforgeeks.org/how-to-get-the-duration-of-audio-in-python/
def percent_played(filepath, seconds_played):
    """
    Function to get the percentage played of a mp3 file. It will create and write
    the percentage of the file to a txt file (or create one in the root directory)
    and also a message.
    """
    # Grab metadata from the mp3 file
    audio = MP3(filepath)
    audio_info = audio.info
    length = int(audio_info.length)
    hours, mins, seconds = audio_duration(length)
    tot_duration = ('Total Duration: {}:{}'.format(mins, seconds))
    print(tot_duration)

    # Find percentage of song played and print.
    raw_pct = (seconds_played/length)
    played_percent = ((seconds_played/length) * 100)
    percentage = "{:.1f}".format(played_percent) + "%"
    perc_msg = "\nYou have played " + "{:.1f}".format(played_percent) + "% of the song!"
    print(perc_msg)
    with open('percentage-played.txt', 'w+') as wf:
        wf.write(str(raw_pct))
        # You can comment this out if not necessary for txt file.
        wf.write(str(perc_msg))
        wf.close()


# Citation: https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
def read_mp3_from_txt():
    """
    Function that waits for the params.txt file to be created in the same directory and then
    calls the other functions to return a txt file.
    """
    #curr_dir = os.getcwd()
    #while wait_for_file(curr_dir, 'params.txt') is not True:
    #    wait_for_file(curr_dir, 'params.txt')
    try:
        f = open('params.txt')
    except:
        pass
    else:
        lines = [line.rstrip() for line in f]
        f.close()
        filepath = lines[0]
        seconds_played = int(lines[1])

        if filepath == "Stop":
            exit(0)
        percent_played(filepath, seconds_played)


# Comment this out if you don't need the prompts
if __name__ == '__main__':
    while True:
        read_mp3_from_txt()
        time.sleep(0.5)
