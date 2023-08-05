from polarishub_flask import server
import os, sys
from multiprocessing import Process

# if sys.platform != "win32":
#     os.chdir("polarishub_flask")
    
app = server.create_app()
def open_browser():
    # if os.name == 'nt':
        # os.system("start http://localhost:5000/")
    # else:
    os.system("python -m webbrowser \"http://localhost:5000/\"")

def start_app():
    app.run(host="0.0.0.0", port=5000)

def main():
    open_browser()
    start_app()

if __name__ == "__main__":
    main()