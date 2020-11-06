# GoOutSafe

![Travis (.org)](https://img.shields.io/travis/GreyTeam2020/GoOutSafe_Primer2020?style=for-the-badge)
![Coveralls github](https://img.shields.io/coveralls/github/GreyTeam2020/GoOutSafe_Primer2020?style=for-the-badge)

## Table of Content

- [How Build the project]()
- [How run the project]()
- [Developing]()

## How Build and run with Docker

>To enable celery you need to change the value inside the `monolith/utils/dispaccer_events.py` at line 4 
the propriety `_CELERY` from `False` to `True`.

Clone the repository and run in the root folder the command
`docker-compose up`
This will make docker downloads all the file needed and start building the containers. 
After that, you can browse to http://localhost:5000/ to use the app.

## Developing

Each programmer has a personal style on write code and we accept this, but to make readability the
code from all component of the team, we used a good tool to format the code in automatically.

It is [black](https://github.com/psf/black), and it is installed with the requirements.txt

To format the code you can run the command below after `pip3 install -r requirements.txt --user`

`black monolith`

When you see the following line, you are done to push your PR

All done! ✨ 🍰 ✨


## Additional information

- Deadline - November 6th, 2020 at 08:59 am
  - (Sub) Deadline for the priority one - October 28th, 2020 at 06:00pm.
