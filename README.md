# Library Management System Project

## Steps to setup environment for project
1. Download and install **python 3.8.1**
2. Install python virtual env => **pip install virtualenv**
3. Activate virtual env => **rahul\test_django\Scripts\activate.bat**
4. Install the python pip dependency => **pip install -r rahul\requirements.txt**
4. Download and install posgreSQL Database (**version = 10.22**) Link => https://www.enterprisedb.com/postgresql-tutorial-resources-training?uuid=ea5c8104-3940-4ed1-b427-81cf19781581&campaignId=70138000000rYFmAAM
5. Note: Add **password as password** for **postgres user** during installation
6. Create database (**LMSDB**) using following command in cmd => **"c:\Program Files\PostgreSQL\10\bin\createdb.exe" -U postgres LMSDB**
7. Run following python commands =>
    - **python manage.py makemigrations**
    - **python manage.py sqlmigrate LMS 0001**
    - **python manage.py sqlmigrate LMS 0002**
    - **python manage.py sqlmigrate LMS 0003**
    - **python manage.py sqlmigrate LMS 0004**
    - **python manage.py sqlmigrate LMS 0005**
    - **python manage.py sqlmigrate LMS 0006**
    - **python manage.py sqlmigrate LMS 0007**
    - **python manage.py migrate**

## Starting project local server
1. **python rahul\manage.py runserver**
