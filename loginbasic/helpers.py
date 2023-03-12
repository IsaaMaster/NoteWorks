def format3(items):
    PERROW = 3
    items2d = []
    for i in range(len(items)):
        if(i%PERROW == 0):
            items2d.append([])
        items2d[-1].append(items[i])
    return items2d

def searchEngine(notes, text):
    found = []
    for note in notes:
        if text in note["title"] or text in note["text"]:
            found.append(note)
    return found