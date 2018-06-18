# Djob
## Download & Launch

Clone this repo with:
  ```bash
  $ git clone https://github.com/matt115/Djob
  ```

Go to Djob directory and pull images from public registry:

  ```bash
    $ cd Djob
    $ docker-compose pull
  ```
Connect to the web service and apply migrations to PostgreSQL:
  ```bash
  $ docker-compose run --rm web sh
  $ ./manage.py migrate
  $ exit
  ```
Launch:
  ```bash
  $ docker-compose up
  ```
Open your browser and go to <http://localhost:8001/signup>.

Enjoy :)

## Load example data

Inside web service you should do:
```bash
$ ./manage loaddata data.json
```
...done.
You can then login as xaustin@gmail.com with password 'password'.

P.S every user have the same password ('password').

## Build images

If you want build directly the images, after you have cloned the repo you have to init git submodules\
(i.e fetch [python-graph](https://github.com/Shoobx/python-graph/tree/master) repo); so you can type:
  ```bash
  $ git submodule update --init --recursive
  ```
**_tip_**: if you want that git downloads external repo automagically you can set this option:
  ```bash
  git config --global submodule.recurse true
  ```
Then you can build images with:
  ```bash
  $ docker-compose build
  ```
After that:
  ```bash
  $ docker-compose up
  ```

## Note

This project is not actually intended for deploy.  
