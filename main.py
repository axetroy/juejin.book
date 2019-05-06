# -*- coding: utf-8 -*-
import requests
import json


# 获取所有的小册信息
def get_all_books():
    page_num = 1

    url = 'https://xiaoce-timeline-api-ms.juejin.im/v1/getListByLastTime'

    books = []

    print('正在检索掘金小册...')

    while page_num > 0:

        params = {"src": 'web', "pageNum": page_num}

        r = requests.get(url, params=params).json()

        response_books = r["d"]

        books = books + response_books

        if len(response_books) == 20:
            page_num = page_num + 1
        else:
            page_num = 0

    books.sort(key=lambda x: int(x["buyCount"]), reverse=True)
    print('总共发现有 %s 本小册' % len(books))

    print('-'*10 + '销量 TOP 10' + '-'*10)

    # 销量 TOP 10 的书
    top10_sell_books = books[:10]

    # 最长的书名字
    max_name_len = max(list(map(lambda x: len(x["title"]), top10_sell_books)))

    for book in top10_sell_books:
        title = book["title"]
        book_name = ("《%s》" % title).ljust(max_name_len + 10, ' ')
        out = '%s 销量: %s 本' % (book_name, book["buyCount"])
        print(out)

    print('-'*10 + '最赚钱 TOP 10' + '-'*10)

    def add_value(x):
        x["value"] = int(x["buyCount"]) * float(x['price'])
        return x

    books = list(
        map(
            lambda x: add_value(x),
            books
        )
    )

    # 按收益最多的排序
    books.sort(
        key=lambda x: float(x["value"]),
        reverse=True
    )

    # 赚钱最多的书
    top10_value_books = list(books)[:10]

    max_name_len = max(list(map(lambda x: len(x["title"]), top10_value_books)))

    for book in top10_value_books:
        book_name = ("《%s》" % book["title"]).ljust(max_name_len + 10, ' ')
        out = '%s 销量: %s 本, 单价 %s  收益: ¥%.2f' % (
            book_name,
            book["buyCount"],
            book["price"],
            book["value"]
        )
        print(out)

    # 筛选出免费的书
    free_books = list(
        filter(lambda x: float(x['price'] <= 0), books)
    )
    free_percent = len(free_books)/len(books) * 100
    print('其中有 %s 本免费书籍, 占总数的 %.2f%%' % (len(free_books), free_percent))


def main():
    get_all_books()


if __name__ == "__main__":
    main()
