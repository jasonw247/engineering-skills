"""Shell tool with foreground and background execution."""

import subprocess
import time

FOREGROUND_LIMIT_SECONDS = 900
TASKS = {}


def run(command, timeout=3600):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        out, _ = proc.communicate(timeout=FOREGROUND_LIMIT_SECONDS)
        return {"status": "done", "output": out.decode()}
    except subprocess.TimeoutExpired:
        proc.kill()
        return start_background(command, timeout)


def start_background(command, timeout):
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    TASKS[proc.pid] = {"proc": proc, "deadline": time.time() + timeout}
    return {"status": "background", "task_id": proc.pid}


def read_task(task_id):
    task = TASKS[task_id]
    task["deadline"] = time.time() + 3600
    if task["proc"].poll() is None:
        return {"status": "running"}
    return {"status": "done", "output": task["proc"].stdout.read().decode()}
