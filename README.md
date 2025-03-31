# Implementation Details:

1. Clone the Repository:
    - `git clone https://github.com/mallow-self/blog.git`

2. Change directory into blog:
    - `cd blog`

3. Set up a conda virtual environment:
    - Current directory:
        - ~/blog/
    1. Create a virtual conda environment:
        - `conda create -n blog python=3.12`
        - Note: You need to have conda installed globally - [Refer](https://docs.conda.io/projects/conda/en/stable/user-guide/getting-started.html)
    2. Activate the environment:
        - `conda activate blog`

4. Set up poetry:
    - Current directory:
        - ~/blog/
    1. Add packages using poetry:
        - `poetry install`
        - Note: You need to have poetry installed globally - [Refer](https://python-poetry.org/docs/basic-usage/)

5. Change Directory:
    - Current directory:
        - ~/blog/
    1. Change into blog directory(Django Project) from blog directory(root):
        - `cd blog`

6. Run app/server:
    - Current directory:
        - ~/blog/blog
    
    - Run this command to run the server:
        - ubuntu/linux: `python3 manage.py runserver`
        - windows: `python manage.py runserver`
