# Pre-Requisites:
1. Install docker locally
2. Run `docker run -d -p 6379:6379 redis`

3. Run `crontab -e`
    - Add the below two line in the file
    ```
    # for daily message to users
    # 0 8 * * * /bin/bash -c 'source /home/rishicollinz/miniconda3/etc/profile.d/conda.sh && conda activate blog && python /home/rishicollinz/Documents/mallow/project/blog/blog/manage.py shell -c "from blog_app.tasks import daily_mail_users; daily_mail_users.delay()"' >> /home/rishicollinz/cron_logs/daily_blog_email.log 2>&1

    # for publishing every 5 minutes
    # */5 * * * * /bin/bash -c 'source /home/rishicollinz/miniconda3/etc/profile.d/conda.sh && conda activate blog && python /home/rishicollinz/Documents/mallow/project/blog/blog/manage.py shell -c "from blog_app.tasks import publish_scheduled_blogs; publish_scheduled_blogs.delay()"' >> /home/rishicollinz/cron_logs/publish.log 2>&1
    ```

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

7. Run celery worker:
    - Open a new terminal

    - Current directory:
        - ~/blog/blog
    
    - Run this command to run the celery worker: 
        - `celery -A blog worker --loglevel=info`
