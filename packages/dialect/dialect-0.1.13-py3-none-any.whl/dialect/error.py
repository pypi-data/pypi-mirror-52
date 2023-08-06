def syntax_error(path, lineno, lexpos):
    print('SYNTAX ERROR\n{}:'.format(path))
    with open(path, 'r') as f:
        lines = f.readlines()
        lines = [line.replace('\n', '') for line in lines]
        for i in range(len(lines)):
            lexpos -= len(lines[i]) + 1
            if lexpos >= 0 and lexpos <= len(lines[i]):
                print('FOUND LEX POS', lexpos, i)
            if i == lineno:
                print('->', i, '|', lines[i])
            elif i >= lineno - 2 and i <= lineno + 2:
                print('  ', i, '|', lines[i])
