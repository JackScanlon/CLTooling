# CLL scraper 

[Concept Library](https://github.com/SwanseaUniversityMedical/concept-library) tooling

### Usage
1. Modify ```./builder.py``` for CL scraping targets
2. Adjust ```./main.py``` for any pre-processing you need to perform prior to sending requests to the server
3. Follow the terminal's command line interface to create, update or publish your data to CL

### Sample
The current builder targets CRPD@Cam phenotypes, please take a look at ```./builder.py``` - this should serve as an example of how to retarget to your desired URL.