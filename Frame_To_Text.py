# Import required packages 
import cv2 
import pytesseract 
import os
import sys
  
# Mention the installed location of Tesseract-OCR in your system 
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
video_path = 'Sample3.mp4'
frames_dir = 'data'
video_path = os.path.normpath(video_path)  # make the paths OS (Windows) compatible
frames_dir = os.path.normpath(frames_dir)  # make the paths OS (Windows) compatible
video_dir, video_filename = os.path.split(video_path)  # get the video path and filename from the path
assert os.path.exists(video_path)  # assert the video file exists
os.makedirs(os.path.join(frames_dir, video_filename,"Output"), exist_ok=True)
capture = cv2.VideoCapture(video_path)  # load the video
total = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))  # get its total frame count
frame_count = total - 1
for frame in range(frame_count):
    # Read image from which text needs to be extracted 
    
    curr_path_to_img = os.path.join(frames_dir,video_filename,"frame{:d}.jpg".format(frame))
    img = cv2.imread(curr_path_to_img)
    print(img)
  
    # Preprocessing the image starts 
    # Convert the image to gray scale 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
    # Performing OTSU threshold 
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
  
    # Specify structure shape and kernel size.  
    # Kernel size increases or decreases the area  
    # of the rectangle to be detected. 
    # A smaller value like (10, 10) will detect  
    # each word instead of a sentence. 
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 
  
    # Appplying dilation on the threshold image 
    dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 
  
    # Finding contours 
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,  
                                                 cv2.CHAIN_APPROX_NONE) 
  
    # Creating a copy of image 
    im2 = img.copy() 
  
    # A text file is created and flushed 
    save_path = os.path.join(frames_dir, video_filename,"Output", "frame{:d}.txt".format(frame)) 
    file = open(save_path, "w+") 
    file.write("") 
    file.close() 
  
    # Looping through the identified contours 
    # Then rectangular part is cropped and passed on 
    # to pytesseract for extracting text from it 
    # Extracted text is then written into the text file 
    for cnt in contours: 
        x, y, w, h = cv2.boundingRect(cnt) 
      
        # Drawing a rectangle on copied image 
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
      
        # Cropping the text block for giving input to OCR 
        cropped = im2[y:y + h, x:x + w] 
      
        # Open the file in append mode 
        file = open(save_path, "a") 
      
        # Apply OCR on the cropped image 
        text = pytesseract.image_to_string(cropped) 
      
        # Appending the text into file 
        file.write(text) 
        file.write("\n") 
      
        # Close the file 
        file.close 