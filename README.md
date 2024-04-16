# MetroAPI

MetroAPI is an API that interacts with the api mosmetro. For information on the Zamoskvoretskaya (green) line of the Moscow metro. The program is designed to collect data on trains, as well as to receive new trains "Moscow 2024"

## Install (Linux)

1. Clone repository and moving to a directory

```git clone https://github.com/Mishazx/MetroAPI && cd MetroAPI```

<details><summary>Run in a local computer</summary> 

- Creating and activating a virtual environment

    ```python3 -m venv venv```

    ```source venv/bin/activate```

- Installing dependencies and setting up the environment file

    ```pip3 install -r requirements.txt```

    ```mv .template.env .env```

- Run in a local computer

    ```python3 run.py```
</details>

<details><summary>Run in a Docker container</summary> 

- Setting up the environment file 

    ```mv .template.env .env```

- Run Docker container

    ```docker-compose up -d```

</details>

## Plans
- Add more features
- Add docs
- Add unit tests

## Support
Write here or in telegram in my profile, I will consider any questions and suggestions
