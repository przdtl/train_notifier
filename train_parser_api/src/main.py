import uvicorn

from fastapi import FastAPI


application = FastAPI(
    title='TranParserAPI',
    description='An application for obtaining data on trains and available tickets'
)


def main() -> None:
    uvicorn.run("main:application", host="127.0.0.1", port=8000, reload=True)


if __name__ == '__main__':
    main()
