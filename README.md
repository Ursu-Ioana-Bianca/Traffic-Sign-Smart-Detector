# Traffic-Sign-Smart-Detector

## Table of Contents

- [Project Description](#project-description)
- [Technologies and Libraries Used](#technologies-and-libraries-used)
- [External APIs](#external-apis)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)

## Project description

This project develops a web-based system designed to improve urban mobility. It detects and classifies traffic signs from video recordings captured via webcams or user uploads. Using a microservice architecture, the system employs public APIs, among other technologies, to identify traffic signs along urban routes commonly traveled by vehicles, bicycles, or pedestrians.

The base functionality allows users to upload video and image content, access real-time webcam feeds, and view detected traffic signs within these media. An OWL-based conceptual model supports the system, facilitating the classification of traffic signs. This model supports a SPARQL endpoint that provides information about each sign, including its legal implications, related signs, and practical usage recommendations.

Additional features of the system include a user profile management, traffic sign database access, and incident reporting. Users can also receive notifications about traffic signs and conditions near them, improving awareness and promoting safer driving practices.

This system extends beyond basic detection by integrating user-generated content and external data sources to improve accuracy and relevancy, taking care of the changing needs of urban environments.

### Technologies and libraries used

<ul>
  <li>:stop_sign:	Frontend: HTML, CSS, JavaScript</li>
  <li>:stop_sign:	Backend: Python, Flask framework for web development</li>
  <li>:stop_sign:	RDF: Used for representing and linking data about traffic signs in a structured format</li>
  <li>:stop_sign:	SPARQL: Query language for RDF</li>
  <li>:stop_sign:	Swagger: Used for describing and documenting RESTful APIs</li>
</ul>

### External APIs
<ul>
  <li>:police_car:	SpeechSynthesis: Converts text into spoken voice output</li>
  <li>:police_car:	Overpass: Used for retrieving the locations of the nearest traffic signs based on user's location</li>
</ul>

## Installation

To use the project, it is first necessary to configure Darknet on your personal computer. For this purpose, we recommend following the steps provided [here](https://pjreddie.com/darknet/install/). These instructions suggest installing the OpenCV and FFmpeg libraries first, then cloning the repository where [Darknet](https://github.com/alexeyab) is located. Optionally, you can download CUDA and cuDNN for running Darknet on GPU. Traffic sign detection in images, videos, or via webcam can also be done from the terminal. For example, the command for a video would look like this:

```bash
DARKNET_EXECUTABLE,
"detector", "demo",
DATA_FILE,
CFG_FILE,
WEIGHTS_FILE,
file_path,
"-out_filename", OUTPUT_VIDEO,
"-json_file_output", OUTPUT_LABEL_VIDEO,
"-dont_show"
```

To run the application, clone the repository from GitHub:

```bash
git clone https://github.com/Ursu-Ioana-Bianca/Traffic-Sign-Smart-Detector.git
```

In the project, the path to the Darknet executable must be modified in the *config.py* file. Optionally, you can choose between the model with 4 classes and the one with 30. Then, the dataset we used needs to be downloaded from the address: https://www.kaggle.com/datasets/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign. You can choose another dataset and train it if you like, and all scripts which need to be executed in order to make the dataset compatible with YOLO are in **data_preparation** folder. No matter which option you choose, the files *change_path_txt.py*, and *change_slashes.py* must be executed in order to modify the paths where the training and test data files are saved.

Finally, run **dbConnection.py** to launch an instance of the application.

## Usage

### Before authentication 
Users can upload images or videos of their routes without needing to authenticate. Upon uploading, the system automatically detects traffic signs and provides results, including the accuracy of the detection, and details about each traffic sign such as its name, description, and category.

### After authentication
Upon creating an account or logging in:
- :vertical_traffic_light:	Access to database: Users gain full access to an extensive database of traffic signs. They can explore properties of each sign or have the information read aloud for accessibility.
- :vertical_traffic_light:	Location-based services: Users can opt to share their location or allow the system to detect it, enabling them to view nearby traffic signs on a map along with their meanings.
- :vertical_traffic_light:	Community interaction: Authenticated users receive real-time notifications about events reported by other users in their vicinity. They can also report issues and contribute to the community-driven data.
Profile Management: Users can view and update their profile information, including changing their profile picture.

## Contributors
- Ursu Ioana-Bianca: [@Ursu-Ioana-Bianca](https://github.com/Ursu-Ioana-Bianca/)
- Rebegea Irina: [@irinarebegea](https://github.com/irinarebegea/)
