# Image Analyzer with detection of emotions for persons

## Installation

```bash
pip install -r requirements.txt
```

## Run

Open file in `VS Code` application and press <kbd>F5</kbd> key, to run the program.

## Usage

### 1) You can choose your file (_.jpg,_.jpeg,_.png,_.gif) to analyze it with `tk` package.

### 2) If your image does not contain `person` find the object with percentage of confidence.

### 3) If your image contains `person` next step is detecting emotions.

### 4) For `*.gif` files, convert to `*.jpg` file with `PIL` package and the find the object like items 2 and 3.

### 5) If `*.gif` files in stpet 4 contain `person` object, separate it to multiple frames and analyze each frame for detecting emothons.

### 6) Finaly `output` folder, contains `emotion.jpg` and `detect.jpg` files for reaching the result after runing the project.

### 7) For `*.gif` files, all data writes in `data.csv` in root folder.

## Note

**_1._** Some configuration files like `object's name, interface graph and etc.` impelemet for detecting object in image.<br>
**_2._** To check the code, you can use files in data folder. `it contains GIF and JPG files with many subjects.`
