# app.py
from main import main
import cProfile

if __name__ == "__main__":
    with open("profile_output.txt", "w") as f:
        cProfile.run('main()', filename=f)