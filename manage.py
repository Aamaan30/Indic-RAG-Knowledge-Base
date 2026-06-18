import typer
import uvicorn

cmd = typer.Typer(no_args_is_help=True)

@cmd.command(name="run")
def run():
    """run application"""
    print("App is Starting...")
    uvicorn.run(
        app="main:app", reload=True, port=8000, host="0.0.0.0"
    )

if __name__ == "__main__":
    cmd()
