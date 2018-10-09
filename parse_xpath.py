from lxml import etree

def parse_xpath(html,rule):
    selector = etree.HTML(html)
    return selector.xpath(rule)

if __name__ == '__main__':
    print(parse_xpath('<html><a herf = "www.baidu.com"></a></html>', '//a/@herf'))
