def UI(state_vector):
    string_vector=["0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
    for i in range(0,14):
        if(state_vector[i]<10):
            string_vector[i] = " " + str(state_vector[i])
        else:
            string_vector[i] = str(state_vector[i])
    print("\x1b[0;30;41m" + "[ {} ]".format(string_vector[13]) + "\x1b[0;30;47m"+" "+"\x1b[0;30;41m" + "({})\u2085 ({})\u2084 ({})\u2083 ({})\u2082 ({})\u2081 ({})\u2080".format(
        string_vector[12], string_vector[11], string_vector[10], string_vector[9], string_vector[8],
        string_vector[7]) + "\x1b[0;30;47m" + "       "+"\33[0m")
    print("\x1b[0;30;47m"+"                                                 "+"\33[0m")
    print("\x1b[0;30;47m"+"       "+"\x1b[0;30;44m" + "({})\u2080 ({})\u2081 ({})\u2082 ({})\u2083 ({})\u2084 ({})\u2085".format(string_vector[0],
                                                                                                       string_vector[1],
                                                                                                       string_vector[2],
                                                                                                       string_vector[3],
                                                                                                       string_vector[4],
                                                                                                       string_vector[
                                                                                                           5]) + "\x1b[0;30;47m"+" " + "\x1b[0;30;44m" + "[ {} ]".format(
        string_vector[6]) + "\33[0m")
    print()
