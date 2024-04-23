# HASS Pathways
[![Netlify Status](https://api.netlify.com/api/v1/badges/5f319796-9a6d-4747-9269-c2bd33bbdf72/deploy-status)](https://app.netlify.com/sites/kind-jepsen-8817be/deploys)
[![deployment](https://github.com/Bram-Hub/HASSPathways/actions/workflows/deployment.yml/badge.svg)](https://github.com/Bram-Hub/HASSPathways/actions/workflows/deployment.yml)
#### Project Details
This project was developed to help students navigate through Rensselaer Polytechnic Institute's newly designed HASS (humanities, arts, and social sciences) curriculum--effective for the class of 2023 and beyond--which requires students to take part in an integrated pathway. The HASS Integrative Pathways were created to enhance students' HASS Core curriculum by bringing intentionality and depth to the requirements. The themes of the pathways vary in their intentionality; some are interdisciplinary, while others focus on a single discipline, providing students with significant options for their coursework. In addition to providing a more in-depth focus to the HASS Core, many Integrative Pathways can be transformed into minors with relative ease.
#### Information in regards to the **[goals of the pathways](https://hass.rpi.edu/advising/hass-integrative-pathways "source")** include:
- Improve student curriculum and academic development.
- Simplify the lives of students in terms of satisfying HASS requirements.
- Lead to minor, or even major.

# Administrator Information
#### Admin Portal
(NOT LIVE AS OF 8/14)
1. Go to www.hasspathways.com
2. Navigate to the Admin portal from home page.
3. Log in using RPI RCS login through shibboleth.
4. Any changes you make will be sent to the backend and later deployed.

<s>
    
#### Data Sheet
https://docs.google.com/spreadsheets/d/1w6BNcxYCE54pvCJJWHiEoE9CiMjRrVNKeUArV97qN8w/edit?usp=sharing

#### Automation
1. Head to https://hasspathways.herokuapp.com/admin
2. Login
3. Head to https://hasspathways.herokuapp.com/upload-csv and upload the CSV file
4. Go to this repository's GitHub Actions page
5. Run the automation (it'll run automatically every Sunday @ 12 AM)
</s>

# Developer Information
#### Frontend Setup
- Clone the repository to your computer
- Install Nodejs - https://nodejs.org/en/download/ (Note some developers may have issues using npm commands, you can use nvm to rollback your node version to work for this project)
- Use the terminal navigate to the `/frontend` directory within the repo.
- Type `npm install` into the terminal to install all packages for the repository.
- Once everything is installed (ignore warnings), type `npm run serve`.
- Visit the specified website the console spits out.
- Note you can use `npm run lint` to fix some warnings that are present.
- Note If using Windows we recommend you use Powershell over WSL


#### Backend Setup
- Clone the Repository to your computer
- Navigate to \backend
- Install Python3.7 or above (either directly or through a distribution like Anaconda)
- Install pip - (`curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py`, then run the script with `python3 get-pip.py`)
- Run `pip install -r requirements.txt`
- Run `python3 admin.py`
- Visit the specified Developer Server's address using any browser. This shouldn't show anything, but a connection should be established. Try connecting to `/guard`. If you see `{"auth": "0"}` the server is working properly.

-- NOTE: In order to run the backend properly, you must edit the endpoints which are being called by Axios in the Front End. Feel free to use ours, as it is already hosted on AWS, however, do note that you will not be able to access our hosted database without a proper key. Alternatively, you will need to edit the backend python code to connect to your own database.

-- To access our hosted AWS resources, please contact a Contributor. The code reflected here is what we are hosting currently, just without our Security Keys.

