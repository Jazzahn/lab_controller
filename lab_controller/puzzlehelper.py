# lab_controller/puzzlehelper.py

def return_status_text(puzzle, status):
    if puzzle == "retina":
        if status == 0:
            text = "Puzzle Offline"
        elif status == 1:
            text = "retina reset"
        elif status == 2:
            text = "latch locked :: door locked"
        elif status == 3:
            text = "gen 2 done, sending latch"
        elif status == 4:
            text = "latch open :: door locked"
        elif status == 5:
            text = "latch open :: door open"
    return text