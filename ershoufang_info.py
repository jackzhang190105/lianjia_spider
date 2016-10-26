import urllib.request
import re
import random
from bs4 import BeautifulSoup

hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]
 


regions=[u"pudongxinqu", u"minhang", u"baoshan", u"xuhui", u"putuo", u"yangpu", u"changning", u"songjiang", u"jiading", u"huangpu", u"jingan"]

ershou_url = 'http://sh.lianjia.com/ershoufang/'


def xiaoqu_ershoufang_one_page(xiaoqu_key,i):
    xiaoqu_ershoufang_page_url = 'http://sh.lianjia.com/ershoufang/d%d%s' % (i+1,xiaoqu_key)

    try:
        resp=urllib.request.urlopen(xiaoqu_ershoufang_page_url)
        html=resp.read()
        soup = BeautifulSoup(html, "html.parser")
    except (urllib2.HTTPError, urllib2.URLError) as e:
        print("xiaoqu_ershoufang_one_page err")
        print(e)
        return
    except Exception as e:
        print("xiaoqu_ershoufang_one_page Exception") 
        print(e)
        return

    ershoufang_list = soup.find_all('div',{'class':'info-panel'})
    for ershoufang_info in ershoufang_list:
        col_1 = ershoufang_info.find('div', {'class':'col-1'})
        col_1_laisuzhou = col_1.find('a', {'class':'laisuzhou'})
        ershoufang_info_dict['xiaoqu'] = col_1_laisuzhou.find('span', {'class':'nameEllipsis'}).string
        os_system("pause")


        ershoufang_info_dict['chanquan'] = ershoufang_info.find('span', {'class':'taxfree-ex'}).string
        ershoufang_info_dict['price'] = ershoufang_info.find('div', {'class':'price'}).find('span',{'class':'num'}).string
        ershoufang_info_dict['price_per_metre'] = ershoufang_info.find('div', {'class':'price-pre'}).string
        ershoufang_info_dict['look_people'] = ershoufang_info.find('div', {'class':'col-2'}).find('span',{'class':'num'}).string
        print("%s %s万 %s万/平 %s人看过此房" % (chanquan_info, price, price_per_metre, look_people))



    os_system("pause")


    return


"""
list the xiaoqu in one page

output:  xiaoqu_property_count[],  xiaoqu_average_price, xiaoqu_look_number 
"""
def xiaoqu_ershoufang_info(xiaoqu_key, xiaoqu_sales_num):
    property_right_count = {'5_only':0, '2_5_only':0, '2_only':0, '5_notonly':0, '2_5_notonly':0, '2_notonly':0}



    #find the total pages
    total_pages = int(xiaoqu_sales_num)//20
    if int(xiaoqu_sales_num) > total_pages*20:
        total_pages += 1

    for i in range(total_pages):
        xiaoqu_ershoufang_one_page(xiaoqu_key,i)


    return




"""
list the xiaoqu in one page
"""
def xiaoqu_spider(sub_page_url):
    print(sub_page_url)
    try:
        resp=urllib.request.urlopen(sub_page_url)
        html=resp.read()
        soup = BeautifulSoup(html, "html.parser")
    except (urllib2.HTTPError, urllib2.URLError) as e:
        print("xiaoqu_spider err")
        print(e)
        return
    except Exception as e:
        print("xiaoqu_spider Exception") 
        print(e)
        return

    xiaoqu_list=soup.find_all('div',{'class':'info-panel'})
    for xiaoqu_info in xiaoqu_list:

        xiaoqu_name = xiaoqu_info.find('a',{'name':'selectDetail'}).string
        xiaoqu_key = xiaoqu_info.find('a',{'name':'selectDetail'}).get('key')
        

        col_1 = xiaoqu_info.find('div',{'class':'col-1'})
        col_1_con = col_1.find('div',{'class':'other'}).find('div',{'class','con'})
        #xiaoqu_sub_region = col_1_con.contents[3].string
        xiaoqu_col_1_info = col_1_con.get_text("|", strip=True)

        range_index = xiaoqu_col_1_info.find('|',0) 
        xiaoqu_range = xiaoqu_col_1_info[0:range_index]

        sub_range_index = xiaoqu_col_1_info.find('|',range_index+1) 
        xiaoqu_sub_range = xiaoqu_col_1_info[range_index+1:sub_range_index]

        year_index = xiaoqu_col_1_info.find('|',sub_range_index+2) 
        xiaoqu_year = xiaoqu_col_1_info[year_index+1:]



        col_3 = xiaoqu_info.find('div',{'class':'col-3'})
        col_3_price = col_3.find('div', {'class':'price'})
        col_3_price_num = col_3_price.find('span',{'class':'num'})

        xiaoqu_board_price = col_3_price_num.get_text("|", strip=True)


        print("%-20s:  %s %s %s, %s元/平" % (xiaoqu_name, xiaoqu_range, xiaoqu_sub_range, xiaoqu_year, xiaoqu_board_price))
        

        col_2 = xiaoqu_info.find('div',{'class':'col-2'})
        col_2_sales_num = col_2.find('span', {'class':'num'})
        xiaoqu_sales_num = col_2_sales_num.string
        print("%s 套" % xiaoqu_sales_num)


        xiaoqu_ershoufang_info(xiaoqu_key, xiaoqu_sales_num)


def do_xiaoqu_spider(region=u"pudongxinqu"):
    url=u"http://sh.lianjia.com/xiaoqu/"+region+"/"
    print(url)
    try:
        resp=urllib.request.urlopen(url)
        html=resp.read()
        soup = BeautifulSoup(html, "html.parser")
    except (urllib2.HTTPError, urllib2.URLError) as e:
        print("do_xiaoqu_spider err1")
        print(e)
        return
    except Exception as e:
        print("do_xiaoqu_spider err2") 
        print(e)
        return

    xiaoqu_number = soup.find('div',{'class':'con-box'}).find('h2').find('span').string
    print("find total %d xiaoqus" % int(xiaoqu_number))

    results_totalpage = soup.find('a', {'gahref':'results_totalpage'})
    print(results_totalpage.string)
    
    total_pages = int(results_totalpage.string)

    print("total pages: %d" % total_pages)
    
    #for i in range(total_pages):
    for i in range(1):
        page_url_page=u"http://sh.lianjia.com/xiaoqu/%s/d%d" % (region, i+1)
        xiaoqu_spider(page_url_page)
    print("spder regon %s 's info" % region)


"""
list all the sub regions in this region, for example:  zhangjiang is a sub region in pudongxinqu
"""
do_xiaoqu_spider("pudongxinqu")



