import cv2
import multiprocessing
import time
import ToUnicode
import os

FPS = 5
VIDEO_FILE = "countdown.mp4"  # video must be in the main folder
CPU_CORES=True # used to set the batch count on how many frames will be generated every batch (when on it sets it to the unmber of your system cores else it sets it to the fps value times 3) is faster on average

batch=os.cpu_count() if CPU_CORES else FPS*3
if multiprocessing.get_start_method() != "spawn":
    multiprocessing.set_start_method("spawn")
DONE = multiprocessing.Event()  # Event to signal when processing is done
vidiocap = cv2.VideoCapture(VIDEO_FILE)
framecount = int(vidiocap.get(cv2.CAP_PROP_FRAME_COUNT))
vidiocap.release()
approximatedtime = framecount / FPS
morerealistictime=approximatedtime*1.5

def generate_frame(fileframe, vidcap, iteration):
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, fileframe + ((FPS*3)*iteration))
    success, image = vidcap.read()
    cv2.imwrite(f"frame{fileframe}.jpg", image)
    time.sleep(0.1)
    return success

def FrameToUnicode(framenumber, vidcap, iteration):
    success = generate_frame(framenumber, vidcap, iteration)
    if success:
        return ToUnicode.generate_full(invert="False", image=f"frame{1}.jpg")
    else:
        return "Could Not Find Frame"

def thread_function(info):
    framenumber, iter = info
    vidcap = cv2.VideoCapture(VIDEO_FILE)
    global DONE
    result = FrameToUnicode(framenumber=framenumber, vidcap=vidcap, iteration=iter)
    vidcap.release()
    
    if result == "Could Not Find Frame":
        DONE.set()  # Signal that processing is done
        return {str(framenumber): "DONE"}
    else:
        return {str(framenumber): result}

def process_results(results, ITERATION):
    print("Finished Iteration: ", ITERATION)

def main():
    global DONE,batch
    ITERATION = 0

    while not DONE.is_set():  # Change the condition as needed
        starttime = time.time()
        results = {}

        with multiprocessing.Pool(processes=batch) as pool:
            thread_numbers = [(i, ITERATION) for i in range(1, (FPS * 3) + 1)]
            results_list = pool.map(thread_function, thread_numbers)

        for result in results_list:
            results.update(result)

        process_results(results, ITERATION)
        print(time.time() - starttime)

        ITERATION += 1

if __name__ == "__main__":
    starttime = time.time()
    main()