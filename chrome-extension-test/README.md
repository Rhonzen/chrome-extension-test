# User Manual
## Backend Information
### System Requirements
All packages in the below table can be installed with `pip install <package name>`

|Package Name|Version|
|---|---|
|beautifulsoup4|4.12.2|
|Flask|3.0.0|
|Flask-Cors|4.0.0|
|news_please|1.5.35|
|pandas|2.1.3|
|Requests|2.31.0|
|scikit_learn|1.3.2|
|spacy|3.7.2|
|torch|2.1.0|
|transformers|4.34.0|
|sentencepiece|0.1.99|

Node is also required, which can be installed with `sudo apt install nodejs`.
The project uses Git-LFS which can be installed with `sudo apt install git-lfs`.
One final library can be installed with `python3 -m spacy download en_core_web_lg`.
### Installation
1. Navigate into the project's root folder
2. Run `npm install`. 
3. Run `npm run build`.
### Usage
Run `python3 src/tweet-processor.py`. Wait until a message comes up saying the program is running before interacting with the frontend. 
## Frontend Information
### System Requirements
- Google Chrome Browser
### Installation
1. Open google chrome and navigate to chrome://extensions/.
2. Select pack extension and enter `<project root>/dist` into the extension root directory box and select ‘Pack extension’.
3. Select load unpacked and enter `<project root>/dist`.
### Usage
When navigating twitter, each tweet will have an analyse button. Pressing this button will send a request, and a few seconds later the information about the tweet will appear. 
Note: Ensure that the backend is running before using the frontend or tweet analysis will not be returned. 
