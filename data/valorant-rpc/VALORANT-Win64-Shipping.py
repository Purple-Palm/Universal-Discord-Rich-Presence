import time
import os
import win32gui
import win32process
import psutil
from pypresence import Presence
import asyncio

def main():
    print("RPC connected, displaying custom RPC./n1 Minute delay before swapping RP for optimization.")
    os.system("python presets/valorant/main.py")


if __name__ == "__main__":
    main()