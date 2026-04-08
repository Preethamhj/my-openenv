import uvicorn

from importlib import import_module

fastapi_app = import_module("app").app


def main():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
