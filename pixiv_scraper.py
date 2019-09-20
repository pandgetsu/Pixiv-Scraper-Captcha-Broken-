import re


def scrape(link, pgnum, extension):
    """

    :param link: link to the image
    :param pgnum: holds the page number
    :return: the completed link
    """
    parts = re.split(r'[\\/_]', link)
    download = parts[0] + "//" + parts[4] + "/" + "img-original" + "/" + parts[13] + "/"
    for num in parts[15:26:2]:
        download += num + "/"
    download += parts[27] + "_p" + str(pgnum)
    download += extension
    return download

