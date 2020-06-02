from concurrent.futures import ProcessPoolExecutor, as_completed
import cv2
import multiprocessing
import os
import sys
import pytesseract


def extract_frame_progress(iteration, total, prefix='', suffix='', decimals=3, bar_length=100):
    """
    This loop is basically used to print the process of our operation

    :parameter iteration: current iteration
    :parameter total: total iterations
    :parameter prefix: prefix string
    :parameter suffix: suffix string
    :parameter decimals: positive number of decimals in percent complete
    :param bar_length: character length of bar
    :return: None

    """

    format_str = "{0:." + str(decimals) + "f}"  # format the % done number string
    percents = format_str.format(100 * (iteration / float(total)))  # calculate the % done
    filled_length = int(round(bar_length * iteration / float(total)))  # calculate the filled bar length
    bar = '#' * filled_length + '-' * (bar_length - filled_length)  # generate the bar string
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),  # write out the bar
    sys.stdout.flush()  # flush to stdout


def extract_frames(video_path, frames_dir, overwrite=False, start=-1, end=-1, every=1):
    """
    Extract frames from a video using OpenCVs VideoCapture

    :parameter video_path: path of the video
    :parameter frames_dir: the directory to save the frames
    :parameter overwrite: to overwrite frames that already exist?
    Yes = True, No = False, default is No = False.
    :parameter start: start frame
    :parameter end: end frame
    :parameter every: frame spacing
    :return: count of images saved
    """

    video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible
    video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path
    assert os.path.exists(video_path)  # assert the video file exists

    capture = cv2.VideoCapture(video_path)  # open the video using OpenCV

    if start < 0:  # if start isn't specified lets assume 0
        start = 0
    if end < 0:  # if end isn't specified assume the end of the video
        end = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    capture.set(1, start)  # set the starting frame of the capture
    frame = start  # keep track of which frame we are up to, starting from start
    while_safety = 0  # a safety counter to ensure we don't enter an infinite while loop (hopefully we won't need it)
    saved_count = 0  # a count of how many frames we have saved
    failure_limit = 500
    """
    :parameter - failure_limt is used to limit the maximum failed read of frames from the video
    """
    while frame < end:  # lets loop through the frames until the end

        _, image = capture.read()  # read an image from the capture

        if while_safety > failure_limit:  # break the while if our safety maxs out at 500
            break

        # sometimes OpenCV reads None's during a video, in which case we want to just skip
        if image is None:  # if we get a bad return flag or the image we read is None, lets not save
            while_safety += 1  # add 1 to our while safety, since we skip before incrementing our frame variable
            continue  # skip

        if frame % every == 0:  # if this is a frame we want to write out based on the 'every' argument
            while_safety = 0  # reset the safety count
            save_path = os.path.join(frames_dir, video_filename, "frame{:d}.jpg".format(frame))  # create the save path
            if not os.path.exists(save_path) or overwrite:  # if it doesn't exist or we want to overwrite anyways
                cv2.imwrite(save_path, image)  # save the extracted image
                saved_count += 1  # increment our counter by one

        frame += 1  # increment our frame count

    capture.release()  # after the while has finished close the capture

    return saved_count  # and return the count of the images we saved


def video_to_frames(video_path, frames_dir, overwrite=False, every=1, chunk_size=1000):
    """
    Extracts the frames from a video using multiprocessing

    :parameter video_path: path to the video
    :parameter frames_dir: directory to save the frames
    :parameter overwrite: overwrite frames if they exist?
    :parameter every: extract every this many frames
    :parameter chunk_size: how many frames to split into chunks (one chunk per cpu core process)
    :return: path to the directory where the frames were saved, or None if fails
    """

    video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
    frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible

    video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path

    # make directory to save frames, its a sub dir in the frames_dir with the video name
    os.makedirs(os.path.join(frames_dir, video_filename), exist_ok=True)
    capture = cv2.VideoCapture(video_path)  # load the video
    total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # get its total frame count
    print(total)
    capture.release()  # release the capture straight away

    if total < 1:  # if video has no frames, might be error to read video
        print("Video has no frames")
        return None  # return None

    frame_chunks = [[i, i + chunk_size] for i in range(0, total, chunk_size)]  # split the frames into chunk lists
    frame_chunks[-1][-1] = min(frame_chunks[-1][-1], total - 1)  # make sure last chunk has correct end frame

    prefix_str = "Extracting frames from {}".format(video_filename)  # a prefix string to be printed in progress bar

    # execute across multiple cpu cores to speed up processing, get the count automatically
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:

        futures = [executor.submit(extract_frames, video_path, frames_dir, overwrite, f[0], f[1], every)
                   for f in frame_chunks]  # submit the processes: extract_frames(...)

        for i, f in enumerate(as_completed(futures)):  # as each process completes
            extract_frame_progress(i, len(frame_chunks) - 1, prefix=prefix_str,
                                   suffix='Complete')  # print it's progress

    return os.path.join(frames_dir, video_filename)  # when done return the directory containing the frames


if __name__ == '__main__':
    # Running the video_to_frame function to convert video to frames

    video_to_frames(video_path='Sample1.mp4', frames_dir='data', overwrite=True, every=1, chunk_size=10)
    """
    To delete the folder 'data', execute following command in terminal(without quotes)
    "rm -r data" 
    or use suitable commands to delete the folder data
    """
