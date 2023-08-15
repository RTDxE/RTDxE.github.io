from trello import TrelloClient
import os
from datetime import datetime

client = TrelloClient(
    api_key=os.environ['TRELLO_API_KEY'],
    token=os.environ['TRELLO_TOKEN']
)

def get_progress(target_list, target_label = ""):
    lists = {}

    all_boards = client.list_boards()
    last_board = all_boards[-1]
    last_board.list_lists()

    for list_info in last_board.all_lists():
        lists[list_info.id] = list_info.name

    done = 0
    undone = 0

    for card in last_board.get_cards():
        if (lists[card.list_id] in ["BACKLOG"]):
            continue

        if target_label.strip() != "":
            if not any(label.name == target_label for label in card.labels):
                continue
            
        if (any(label.name == lists[card.list_id] for label in card.labels) and lists[card.list_id] == target_list):
            done += 1
        else:
            undone += 1
    if (undone + done) == 0:
        return (0, 0, 0, 0)
    return (done / (undone + done), undone, done, undone + done)

(total_percent, _, _, _) = get_progress("Alpha 0.1")
(building_percent, _, _, _) = get_progress("Alpha 0.1", "Building")
(classes_percent, _, _, _) = get_progress("Alpha 0.1", "Class")
(story_percent, _, _, _) = get_progress("Alpha 0.1", "Story")
(gold_hills_percent, _, _, _) = get_progress("Alpha 0.1", "Golden Hills")

update_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

file = open("status.html", "w")
file.write(os.environ['STATUS'].format(total=total_percent*100, building=building_percent*100, classes=classes_percent*100, story=story_percent*100, gold_hills=gold_hills_percent*100, date=update_time))
file.close()
