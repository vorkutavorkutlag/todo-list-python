import tkinter
import tkinter.font


def main():
    root = tkinter.Tk()
    last_font = tkinter.font.families()[-1]
    print(tkinter.font.families())

    MyLabel = tkinter.Label(root, text="AUTOMATIC LOVE", font=(last_font, 25))

    MyLabel.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
