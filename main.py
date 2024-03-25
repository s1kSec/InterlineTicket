# -*- coding: utf-8 -*-

import json
import datetime

# 定义间隔的时间
__SpaceTime__ = 3
result_tickets = []


def read_config():
    with open(r"air.json", encoding="utf-8") as json_file:
        config = json.load(json_file)
    return config


# 清洗重复的航班数据
def remove_json(tickets):
    i = 0
    while i < len(tickets) - 1:
        j = i + 1
        while j < len(tickets):
            if tickets[i]['arrAirportName'] == tickets[j]['arrAirportName'] and \
                    tickets[i]['depAirportName'] == tickets[j]['depAirportName'] and \
                    tickets[i]['arrTime'] == tickets[j]['arrTime']:
                del tickets[j]
            else:
                j += 1
        i += 1
    return tickets


# 排序航班树递归结果
def sort_links_tickets(link_tickets):
    i = 0
    while i < len(link_tickets) - 1:
        j = i + 1
        while j < len(link_tickets):
            if len(link_tickets[i]) < len(link_tickets[j]):
                exchange = link_tickets[i]
                link_tickets[i] = link_tickets[j]
                link_tickets[j] = exchange
            else:
                j += 1
        i += 1
    return link_tickets


# 递归航班树
def mix_tickets(dep, tickets, link_tickets):
    flag = False
    # 存储子树的分支
    result = []
    for ticket in tickets:
        depDateTime = datetime.datetime.strptime(dep["depTime"], "%Y-%m-%d %H:%M:%S")
        arrDateTime = datetime.datetime.strptime(ticket["arrTime"], "%Y-%m-%d %H:%M:%S")
        # 如果目的地=出发地 and 上一程的出发时间 < 下一程的出发时间
        if ticket["arrCityName"] == dep["depCityName"] and \
                depDateTime > arrDateTime and (depDateTime - arrDateTime).days <= __SpaceTime__:
            result.append(ticket)
    if result:
        for r in result:
            # 在这里不能直接写link_tickets.append()传递给形参，因为他的返回值为null，所以会报不能将null.append，这里用一个副本来传递
            link_tickets_copy = list(link_tickets)  # 创建link_tickets的副本
            link_tickets_copy.append(r)  # 将r添加到副本中
            mix_tickets(r, tickets, link_tickets_copy)
    elif len(link_tickets) > 1:
        result_tickets.append(link_tickets)


if __name__ == '__main__':
    tickets = read_config()
    for i in tickets:
        del i['score']
    print("数据总数：" + str(len(tickets)))
    tickets = remove_json(tickets)
    print("清洗之后的总数：" + str(len(tickets)))
    for i, ticket in enumerate(tickets):
        mix_tickets(ticket, tickets, [ticket])
    for link_tickets in sort_links_tickets(result_tickets):
        print("\n----------------------------出发-----------------------------"
              "\n首票出发地为：%s    联程次数为%s次" % (link_tickets[len(link_tickets) - 1]["depCityName"],len(link_tickets)))
        # 因为是递归的，所以append会从最后一个递归过去，所以说是逆序的，这里重置输出
        for cycleticket in range(len(link_tickets) - 1, -1, -1):
            cycleticket = link_tickets[cycleticket]
            print("**  %s--->%s  **  %s-->%s" \
                  % (cycleticket['depCityName'], cycleticket['arrCityName'], cycleticket['depTime'], cycleticket['arrTime']))
        print("----------------------------结束-----------------------------")
