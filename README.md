<div align="center">
<h1> HAILUO API </h1>


HAILUO - AI Videos Generation. It is developed based on FastAPI technologies

Official website: [https://suno.com/](https://suno.com/)

Github: [https://github.com/djp82645/hailuo-api](https://github.com/djp82645)

</div>

## Features

1. Support latest minimax-t2v model
2. fetch .env token from https://surl.id/1uKeEiP5CG
3. if you set callback true .env callback_url set own callback url
5. You can visit API documentation through http://localhost:8000/docs

## Install

1. From https://surl.id/1uKeEiP5CG fetch HAILUO Application TOKEN and edit the `.env.example` file, rename to `.env` and fill in cookie.
2. if you set callback true .env callback_url set own callback url
3. Start the service
    ```
    docker-compose up --build -d
    ```
4. Now you can access the service through http://localhost:8000


## License

[MIT licensed](./LICENSE)

