import csv

def read_url_info(fp):
    url_and_time = dict()

    with open(fp) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cnt = 0
        for row in csv_reader:
            if cnt > 0:
                url_and_time[row[0]] = (float(row[1]), float(row[2]))
            cnt += 1
    print(url_and_time)
    return url_and_time