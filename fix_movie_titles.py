with open('resources/movie_titles.csv', 'r', encoding = "ISO-8859-1") as f:
    with open('resources/movie_titles_fixed.csv', 'w') as f2:
        for line in f.readlines():
            splitted_line = line.split(',')
            if len(splitted_line)>3:
                line_fixed = ','.join(splitted_line[:2]) + ',' + ''.join(splitted_line[2:])
                f2.write(line_fixed)
            else:
                f2.write(line)
        