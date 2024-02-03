# ShareHub ULB
The source code of ShareHub, have fun reading my code and highlighting my mistakes 
## Overview
ShareHub is originally an initiative aiming to explore a new economic model, focused on a more equitable redistribution and diverging from the prevalent competitive patterns on most second-hand platforms. This platform is part of a thesis project, merging the fields of computer science and economics, drawing on the work of various former students and professors at ULB. By using ShareHub, you contribute to advancing research and improving the understanding of second-hand platforms, while enabling ULB students to easily resell their syllabi.
## Requirements
Is really easy, you just need python3 and pip. 
Install python `sudo apt install python3`
Install pip `sudo apt install python3-pip`
Install the dependencies `pip install -r requirements.txt`

There's a good chance there are dependency issues and if there are good luck, just read what the error says and install the package or reinstall the package. 

## How to run
Now that the dependencies are installed, you can clone the project. I advise you to create a virtual environment to run the project.

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
The MIT License (MIT)

Copyright (c) 2024 Edgardo Cuellar Sanchez