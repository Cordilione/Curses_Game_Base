def repeatedLog(log, times):
    if times > 1:
        return f"{log}\tRepeated {times} times\n"
    else:
        return f"{log}\t------Once------\n"


def cleanUpLog(file):
    with open(file, 'r') as log_file:
        with open("logs/logOut.txt", 'a') as logOut_file:
            logOut_file.write("*-----------------NEW CLEANING-----------------*\n")
            curLine = log_file.readline()
            nextLine = log_file.readline()
            dupCount = 1
            oneMore = iter([True, False])
            while nextLine or next(oneMore):
                if curLine == nextLine:
                    dupCount += 1
                    nextLine = log_file.readline()
                else:
                    if dupCount > 1:
                        print(repeatedLog(curLine, dupCount))
                        logOut_file.write(repeatedLog(curLine, dupCount))
                        dupCount = 1
                        curLine = nextLine
                        nextLine = log_file.readline()
                    else:
                        print(repeatedLog(curLine, dupCount))
                        logOut_file.write(repeatedLog(curLine, dupCount))
                        curLine = nextLine
                        nextLine = log_file.readline()
        logOut_file.close()
    log_file.close()
    open(file, 'w').close()

