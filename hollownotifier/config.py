import csv
from requests import request
from hashlib import md5

def read_ch():
    channels = {}
    with open('hollownotifier/config/subs.csv') as csv_file:
        csv_r = csv.reader(csv_file, delimiter=',')
        for row in csv_r:
            if len(row) > 1:
                channels[row[0]] = row[1:len(row)]
    return channels


def add_ch(group, member):
    res = request('GET',f'{host}:3000/list')
    if res.ok:
        data = res.json()
        write_default_channels(data,'hollownotifier/config/def_ch.csv');
    channels = read_ch()
    if group not in channels:
        channels[group] = [member]
    else:
        channels[group].append(member)
    write_ch(channels)

def remove_ch(group, member):
    channels = read_ch()
    if group in channels:
        if member in channels[group]:
            channels.remove(member)
            write_ch(channels)
            print('success')
        else:
            print(f'{member} cannot be found in {group}')
    else:
        print(f'{group} cannot be found')

def write_ch(channels):
    with open('hollownotifier/config/subs.csv', 'w') as csv_file:
        csv_w = csv.writer(csv_file)
        for group in channels.keys():
            csv_w.writerow([group]+channels[group])

def write_default_channels(channels, filename):
    with open(filename, 'w') as csv_file:
        csv_w = csv.writer(csv_file)
        for group in channels.keys():
            csv_w.writerow([group]+channels[group])
        
def fetch_default_channels(host):
    res = request('GET',f'{host}:3000/list')
    if res.ok:
        return res.json()
    else:
        print('Failed to fetch subscription list')

def update_default_channels(host):
    verification = verify_default_channels()
    if verification == "mismatch":
        print("reloading def_ch.csv from server")
        data = fetch_default_channels(host)
        write_default_channels(data,'hollownotifier/config/def_ch.csv')
    elif verification == "ok":
        print("def_ch.csv is up to date")
    else:
        print("Cannot fetch data from server")

def verify_default_channels():
    try:
        with open('hollownotifier/config/def_ch.csv','rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5sum.update(chunk)
            res = request('HEAD',f'{host}:3000/list')
            if res.ok:
                digest = res.headers['Digest']
                write_default_channels(data,'hollownotifier/config/def_ch.csv');
                md5sum = md5()
                return "ok" if digest[4:] == md5sum.hexdigest() else "mismatch"
            else:
                return "mismatch"
    except IOError:
        return "mismatch"

