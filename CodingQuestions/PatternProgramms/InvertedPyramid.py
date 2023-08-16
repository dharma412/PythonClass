def pattern(l):
    for row in range(0, l):
        for i in range(0, row):
            print(' ', end=' ')
        for i in range(0, l - row):
            print('*', end=' ')
        print('')

pattern(5)