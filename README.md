# Youtube Channel Automater
Social Media Links:
- Youtube: [ShortSpotlightUSA](https://www.youtube.com/channel/UCQ35LdHqYwFMxnfjHbjF0TQ)
- TikTok: [ShortSpotlightUSA](https://www.tiktok.com/@shortspotlightusa)
- Instagram: [ShortSpotlightUSA](https://www.instagram.com/shortspotlightusa/)

This repository is used to automate my youtube channel. This automation is performed in a few different steps. It starts with auto-downloading the tiktok video of my choice using web-scraping, then the commentary I write for the video is generated into an AI voice using ElevenLabs API. 

After generating the AI voice, I create the captions with timestamps for when the words will be said. I use something called a forced alignment technique for this. The final part is generating the actual video, which I use the MoviePy package for.

This script also has the capability to auto-upload the videos to youtube and tiktok, although creating the API app for these respective platforms is difficult as a beginner and may not be worth the time.

I'll break down the process of cloning this repository and all the dependecies that are needed to successfully run the script.

## Required Dependencies

There are multiple dependencies required to run the scripts in this repository that are not commited to the repository due to file size limits. The dependencies are as follows:
- All scripts are run using python which is the first thing that needs to be installed to run anything in this repository. I created a virtual environment to contain all packages needed for these scripts. All scripts were written and tested using python version 3.11.1.
    - The virtual environment can be created using the bash commands below. Ensure that these bash commands are executed after installing python onto your computer and also that you are in the directory of the repository.
    - After creating a virtual environment, install the required python packages with the requirements.txt file. The bash commands are also below.
``` bash
python -m venv name-of-environment
pip install -r requirements.txt
``` 
- "chromedriver.exe" is needed for webscraping to download the TikTok videos from the website: [Veed](https://www.veed.io/tools/tiktok-downloader)
    - The website to download "chromedriver.exe" can be found at [ChromeDriver](https://chromedriver.chromium.org/downloads)
- "ffmpeg.exe" is another executable required. The download can be found at [ffmpeg](https://ffmpeg.org/download.html). 
    - The correct file to download are the already compiled executables, do not download the ".tar.xz" file as it will not work for our purposes.
    - Hover over the operating system that you are using in the "Get packages & executable files" and download the most recent build.
- Need to download [ImageMagick](https://imagemagick.org/script/download.php#macosx) as well.

## Required Files

There is a templates folder that contains the structure of the sensitive information files used in the python scripts. For these scripts to run properly they must be filled out. The main file to fill out is the "api_keys.json" file. 

The other two files are required if you plan on using automatic uploads to youtube. The automatic uploads will only work if you have already created a google API application that is in production. Here you can find more information about the [YouTube API.](https://developers.google.com/youtube/v3/docs)


