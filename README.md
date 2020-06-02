# Address Plate Recognition and Delivery System using Drone <br><br>

This is a project that we made as our final college project on **Video Text Extraction & Image Processing**. The objective is to successfully extract text from address plates of people's houses from a drone's camera which would help in correct delivery of goods. The software implementation, i.e. the video text extraction part of the project is included here. <br>
We basically divide the project into 2 parts: <br>
1. Extraction of individual frames from the video.<br>
2. Text extraction from the frames<br><br>

## Steps to run the project<br>

1. Download all the files of this repository to your computer.<br>
2. Use any code editor or IDE that supports Python.<br>
3. Create a folder(say: ABC) and inside it paste the two python files "**Extract_Frames.py**" and "**Frame_to_text.py**".<br>
4. Copy all the videos: **Sample.mp4, Sample1.mp4, Sample2.mp4, Sample3.mp4** to the folder ABC that you created. You can also use your own video. Make sure to keep your video in this directory.<br>
5. Inside the folder ABC, create a directory named "**data**". All output will be generated and stored in this directory.<br>
6. Run the program "**Extract_Frames.py**" first. Be sure to change the name of the video to the appropriate name and the path where the output is to be stored appropriately. The code is properly documented and can be easily understood.<br>
7. Next run the program "**Frame_to_text.py**" to generate the text from the frames.

__"Our outputs for the respective videos are stored in the zip files. Unzip them to see the output that was generated."__<br>

### Other Requirements<br>

If you see an error like: "**module cv2 not found**", then we need to install __cv2__ in the system.<br>
Generally it can be installed by running the command "**pip install opencv-python**" in the terminal. However it may vary from IDE to IDE. Make sure that your IDE supports Python and OpenCV.<br>
Next we also need to have "**pytesseract**" installed in our system. Also make sure that all the packages used the programs are installed. The easiest and best way to obtain tesseract for Windows is [here.](https://github.com/UB-Mannheim/tesseract/wiki)<br>

Click **download->tesseract-ocr-w64-setup-v5.0.0-alpha.20200328.exe** (for 64 bit system)<br>
After installation, you need to set the environment variable for Tesseract OCR. For that go to "**settings-> search for edit environment variables -> open environment variables-> go to user variables -> go to path -> create a new entry and set it to “Path to Tesseract OCR**”<br><br>

This is just the software part. For the actual project, we had even constructed a working drone. For more details about the complete project, you can read the __Basic Idea & Motivation__ as follows:<br>
1. Reduce delivery time using drones<br>
2. Can be used for <br>
    speedy delivery of temperature & time-sensitive commodities like blood, organs <br>
    perishable goods like flowers/milk<br>
    delivery to remote areas<br>
3. Fully autonomous to reduce/eliminate human control<br>
4. Feed real-time video to controlling station<br><br>

Our aim is to reduce delivery time for time-sensitive, perishable goods and increase the ease of delivery in remote zones. In times of the pandemic caused by Covid-19, an autonomous drone delivery system is very useful to maintain **contactless delivery** and to reach red zones where humans are not allowed.<br><br>

For more details about our project you can view the presentation "**drone_ppt**" prepared by us. This is actually our final year college project. **The link to my project partner's profile is [meet2mky.](https://github.com/meet2mky)**<br>
