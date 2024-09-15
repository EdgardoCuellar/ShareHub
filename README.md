# ShareHub ULB

Welcome to the source code of ShareHub! Enjoy browsing through the code, and feel free to point out any mistakes or improvements. 

## Overview

ShareHub is an initiative aimed at testing a **new economic model**, one that focuses on **fairer redistribution**, contrasting with the competitive nature of most second-hand platforms. This platform was developed as part of a **thesis project**, blending **computer science** and **economics**, drawing from the work of various former students and professors at ULB. By using ShareHub, you contribute to **academic research** and help us better understand the dynamics of second-hand platforms, while providing a simple way for ULB students to **buy and sell their syllabi**.

## Requirements
It's quite straightforward! All you need is **Python 3** and **pip**.

- Install Python:   `sudo apt install python3`
- Install pip: `sudo apt install python3-pip`
- Install the dependencies: `pip install -r requirements.txt`

There's a chance you might run into dependency issues. If so, good luck! Just follow what the error message says—install or reinstall the required package(s).

## How to run
After installing the dependencies, follow these steps to get the project running. I recommend creating a virtual environment to keep things organized.

1. **Activate the Virtual Environment**: If you're using a virtual environment, activate it:
```bash
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate     # for Windows
```
2. **Navigate to the Project Directory**: Use the cd command to navigate to the ShareHub directory.
3. **Modify settings.py**: As ShareHub is a public project, it requires a minimum of security with private keys kept secret. To run ShareHub, you need to delete settings.py from the ShareHub subfolder and replace it with settings_local.py. If you're lucky, it should work.
4. **Apply Migrations:* Django uses migrations to propagate changes you make to your models (adding a field, deleting a model, etc.) into the database schema. Run the following command to apply migrations:
```bash
python manage.py migrate
```
5. **Run the Server**: Now you can run ShareHub locally:
```bash
python manage.py runserver
```
Now, you can access your ShareHub by navigating to http://127.0.0.1:8000/ in your web browser. Is cool isn't it !

## Usage
Now that you're running ShareHub, you can do whatever you want locally, and if you find a bug, a flaw, or simply want to improve the platform, don't hesitate to create an issue, and create a new branch.

## Contributing
1. **Open an Issue**: If you find a bug or have a suggestion, please open an issue to discuss it.
2. **Create a Branch**: Make your changes in a new branch.
3. **Submit a Pull Request**: Once you're done with your changes, submit a pull request. 

Please note, only administrators can merge pull requests. Thanks for your contributions!


## License
ShareHub is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike (CC BY-NC-SA) license. This means:

- Attribution: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- NonCommercial: You may not use the material for commercial purposes.
- ShareAlike: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

For more information, visit the [Creative Commons website](https://creativecommons.org/).