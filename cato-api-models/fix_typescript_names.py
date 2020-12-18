import os

if __name__ == '__main__':
    folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cato-api-models-typescript','src','catoapimodels')
    names = []
    for ts_file in  os.listdir(folder):
        filename_without_ext = os.path.splitext(ts_file)[0]
        corrent_name = filename_without_ext[0].upper() + filename_without_ext[1:]
        interface_name = "I" + corrent_name

        names.append((interface_name, corrent_name))

    for ts_file in os.listdir(folder):
        with open(os.path.join(folder, ts_file))as f:
            content = f.read()

        for interface_name, corrent_name in names:
            content = content.replace(interface_name, corrent_name)
        with open(os.path.join(folder, ts_file), "w")as f:
            f.write(content)