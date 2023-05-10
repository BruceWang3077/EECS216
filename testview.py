import View
def main():
    view=View.FinderView()
    path=[(1,1),(1,2),(1,3),(2,3),(3,3),(3,2),(3,1)]
    worker=(1,1)
    view.printMap((40,20),[(3,5),(12,2)],(1,1))
    view.printDirection(path)

main()