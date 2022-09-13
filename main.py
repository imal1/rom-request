import os
import sys

import requests
from bs4 import BeautifulSoup

origin_host = 'https://xiaomirom.com'
file_path = '/Users/imali/Downloads'

list_page_url = origin_host + "/rom/redmi-k50-rubens-china-fastboot-recovery-rom/#%E4%B8%8B%E8%BD%BD-%E7%BA%A2%E7%B1" \
                              "%B3-k50-%E5%BC%80%E5%8F%91%E7%89%88%E5%86%85%E6%B5%8B%E7%89%88-recovery-%E5%8D%A1%E5" \
                              "%88%B7%E5%8C%85 "

requests.packages.urllib3.disable_warnings()


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/104.0.0.0 Safari/537.36',
    }
    res = requests.get(url, headers=headers, allow_redirects=False)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        return res.text
    else:
        sys.stdout.write('------%s，爬取失败------' % res.status_code)
        return ''


def get_download_page_url(html):
    soup = BeautifulSoup(html, 'html5lib')
    anchor = soup.find(id='下载-红米-k50-开发版内测版-recovery-卡刷包')
    href = anchor.find_next('a')['href']
    return origin_host + href


def get_target_download_url(url):
    download_page_html = get_html(url)
    soup = BeautifulSoup(download_page_html, 'html5lib')
    btn_group = soup.select('.btn.btn-warning')

    for btn in btn_group:
        click_event_str = btn['onclick']
        click_event_str = click_event_str.removeprefix("window.open('")
        click_event_str = click_event_str.removesuffix("','_blank');")
        if click_event_str.endswith('.zip'):
            return click_event_str


def decrypt_file(path):
    sys.stdout.write('------解压开始------')
    dir_path = path.removesuffix('.zip')
    os.system('unzip -n ' + path + ' -d ' + dir_path)
    payload_path = dir_path + '/payload.bin'
    if os.path.exists(payload_path):
        sys.stdout.write('------解包开始------')
        os.system('./payload-dumper-go ' + payload_path)
        sys.stdout.write('------解包结束------')


def chunk_download(url, path):
    r1 = requests.get(url, stream=True, verify=False)
    total_size = int(r1.headers['Content-Length'])

    if os.path.exists(path):
        if total_size > os.path.getsize(path):
            sys.stdout.write('------下载任务继续------')
            temp_size = os.path.getsize(path)
        else:
            sys.stdout.write('------下载任务已完成------')
            sys.stdout.flush()
            return decrypt_file(path)
    else:
        sys.stdout.write('------下载任务开始------')
        temp_size = 0

    headers = {'Range': 'bytes=%d-' % temp_size}
    r = requests.get(url, stream=True, verify=False, headers=headers)

    with open(path, "ab") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()

                # done = int(50 * temp_size / total_size)
                # sys.stdout.write("\r[%s%s] %d%%" % ('█' * done, ' ' * (50 - done), 100 * temp_size / total_size))
                # sys.stdout.flush()
                if temp_size == total_size:
                    sys.stdout.write('------下载任务完成------')
                    sys.stdout.flush()
                    decrypt_file(path)


def download_rom():
    list_page_html = get_html(list_page_url)
    if len(list_page_html) > 0:
        download_page_url = get_download_page_url(list_page_html)
        download_url = get_target_download_url(download_page_url)
        # 测试其他网址
        # download_url = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png'
        chunk_download(download_url, file_path + '/' +
                       download_url.split('/')[-1])


# 临时测试
download_rom()

# schedule.every().saturday.at('00:00').do(download_rom)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
