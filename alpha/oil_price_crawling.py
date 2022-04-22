from datetime import datetime
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import re

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)

def get_data(url_name):
    url = url_name
    driver.get(url)

    driver.switch_to.frame(0)

    table = driver.find_element(by=By.XPATH,value="//*[@id='objBody']/table/tbody")
    tr = table.find_elements(by=By.TAG_NAME,value="tr")
    year = driver.find_element(by=By.XPATH,value="//*[@id='print_body']/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]")
    year = year.text.split()
    year = re.findall("\d+", year[0])
    
    np_date = np.zeros(len(tr)-1,dtype=datetime)
    np_dubai = np.zeros(len(tr)-1,dtype=float)
    control = 0
    
    for tr in table.find_elements(by=By.TAG_NAME,value="tr"):
        if not control == 0:
            td = tr.find_elements(by=By.TAG_NAME,value="td")
            s = td[0].text.split()
            month = re.findall("\d+", s[0])
            day = re.findall("\d+", s[1])
            np_date[control-1] = datetime(int(year[0]),int(month[0]),int(day[0]))
            if td[3].text == "N.A":
                np_dubai[control-1] = 0    
            else:
                np_dubai[control-1] = re.findall("\d+.\d+",td[3].text)[0]
        control += 1
    df_dubai = pd.DataFrame({'date':np_date[:],'price':np_dubai[:]},index=np.arange(control-1))
    return df_dubai

#2022 04    
result_data = get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/9EC1AED6A0160C844925881900836CD6?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/41CD01828EAAA4FC492587F900004C04?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/3712D67AE49761F2492587DE00018716?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/9CCEE2A522D5AD02492587C00002D2EB?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2021
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/81DA904C5CC4FCB94925879F0001DD7B?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FD29A5C98F610E604925878100021A95?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/06A41B16E05F990B49258764008316AD?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/337F1027054512AB492587440005CF2E?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/18ADB52C65F31E864925872700029E48?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B560844676417B9C4925870900015439?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/863C840A00875490492586E8000163A8?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/EF744057B620C804492586CB000088DA?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/D32FF615EBB403D3492586AB0001255D?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/6021F50E72AB892B4925868C000E8B26?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B27270795AA0BF0A492586700000B45F?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/7296EA9A4AC60A244925865300837B67?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2020
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/208AD7EE3D71CD8C492586320007EAEA?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/076C78013D08E2E14925861400827C4C?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DD8E9450C4E2844A492585F7008289AE?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/36540C28329B70C9492585D60081E6AD?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/82D8F3F676BBCE6C492585B900824EBC?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/434D6367A4AF5B1B492585980082BAB9?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BAF86121AF9DAF494925857A0082026B?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/3FF907A06ACB41BC4925856000067BE0?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/127BA5ED8FAEA38F4925853E0000B612?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BFDCE3AC71878DED4925851F00821F6E?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/8065C3F5208A7610492585030083B696?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/377A986A3E5D4A76492584E30083C118?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2019
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/773FC0B5FB05962B492584C40082E600?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/452745788DD5951F492584A700831A65?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/25782CDDE8395C1F4925848600834053?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/A0B4A0544A6CEF7A4925846A00000A3A?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/4DC86912FF7C542E4925844A00039C3E?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/F58CB251E618E0384925842A008388E0?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FF11B9ECA8E510104925840E008336D5?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/E86A2FAB8BFA4F14492583ED0082242A?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/4738F4FDB55A1568492583CF008133DB?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2F0E16C0FBDB631A492583B20081C6AB?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/A121CAFEEDE8DB0A4925839900822380?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/164F05ED3E4B7C56492583760081DA14?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2018
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/843016C63D1CFA424925835800829803?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/F3DD49D13C117593492583380081A2F3?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/4DD5471574D67C69492583190082A404?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/87CDAE8ABFE84C74492582FD0081DC92?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B64E6499779142AA492582DC0082C7DC?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/AE400F3C0A3B047F492582BF00007157?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/ED862CE0AB8A1070492582A0002621B3?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/6D38785BECB3E3CD4925828000824D97?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/773FA961E1EDC1E84925828000823789?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2F9494090EC15470492582430081AC18?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/D7608E221EA1ED5A4925822800002617?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BE7475030382E1D84925820900835A51?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2017
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BB270109BEFB894A492581EB001183BB?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/5883D15D336F4F64492581CB0081A8C4?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/27E89A9E32E31612492581CB0081D16C?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/55D1FAEAC2334C604925818F004050C9?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/98AE519CB73857F24925816F0083CEB6?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/19EB4B6E217D010D4925815300006AED?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2A7B832C4DBAE6AE4925813300833B6A?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B34BAA4316D5A0B14925811400001408?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/487CE693CF1E6EEE492580F8000113A6?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/886B9552CACF4EE3492580D700012B75?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2869CB955592E108492580BB00014FE8?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BDFDEFA4457307194925809E00026C21?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2016
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/593047361DBBE2EF4925807D0000DE83?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/D5F6D53112A333F14925805F000439EE?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/9C91843E724F666749258059000340BD?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/11B4B040F609D28B49258024001FFDDB?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DD13DE5A4234DA77492580030016688F?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/11855623E2D2FEFA49257FE500047946?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/5A6B3DC6773E9D1D49257FC600003DE9?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DBC0A04313FE9EF349257FA80000822C?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DE8F0CBF1AA9A8D449257F8900517647?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FEADF08947FC1F9A49257F6B00059383?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/863AD72A24789C6249257F4D00092301?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/EA278FDDFD11C64149257F31000F9F09?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2015
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/08F76629416AD28E49257F0F000C7800?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FA0E22E2B3E47FC049257EF20007E276?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/526818C4F3E97D8C49257ED2000276CC?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/F2371BEB8C380DAB49257EB40002B842?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/D52724C0B865EE6A49257E970002443C?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/41C64AC3130DFCFF49257E7600023C98?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/1569B8FDC8FB23AD49257E58000C44ED?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/14E950FF23601FF049257E3E00066A26?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2A91453401ED8F4749257E1B0003635A?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/A4DE1B81003FE4A349257DFD001C62FD?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/AA12F2DFACF2A27A49257DE1000612E1?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/F7EA7732FDF76F3A49257DC3002E953D?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2014
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2EFDB5C1822824D149257DA200058332?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/E2D2BDE9EF24B51C49257D860005580F?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/247FF993265D7DF149257D6500041192?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/1696508A7008E1A849257D4600826AD2?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/123CB956C77BD15A49257D2B00042A23?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/EBD101618845530549257D090004BB26?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/CACA78699C335B2449257CEC000109A9?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/E6C310E73833E99149257CCC001D6112?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/78DF5FA7D49F93A649257CAE00029B95?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/8A337C0D4DC5FF2949257C9100007D1B?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B9725C7FDA42673349257C7500066C62?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/5F4B8BDACCBEB92749257C550000E9C8?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2013
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/638229CE9B638ADB49257C360000BB85?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B5ED5D2CBC588F5A49257C19000017D0?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/42D488E9EACBFFDB49257BFA00182D9D?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/845B7136E85E137249257BDB000EF50C?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/126769399E1FEB3349257BBB000117ED?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/E8697F41B3C37B5449257B9C000383A2?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/2AEFA3C7CB6AC23C49257B800001DD73?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FF797A2A0B93E94F49257B5F0001997E?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/432DF3A9B497319649257B4300025FB8?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/352EBD40118E77BD49257B2500025A07?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/8EAAC4030723CC7049257B09000B7F4E?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DE0679BA0CA8B3DE49257AE8000C3948?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2012
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/791888978B707FE649257ACA0002FCED?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/395801AF5576ECA849257AAA000AB8B6?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/1B0CEB2B6C0C73E949257A8D000230C8?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/62176F0B86CAD79B49257A6F0000F127?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/D435E105EA399F2749257A4E00027E9A?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/93DE3A05545A281C49257A30000297AC?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/3FF50C909F4582B149257A1300006E49?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/5C26612C25DDCD46492579FF00080B37?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/89C4650BAB92B4F4492579FF00073813?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/92742717281CBB69492579B70083BB27?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/9F6BBDEF656D66FA4925799800057002?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/9177AFC8E0788AA34925797B0002B61E?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2011
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/D8A5FE21B833624E4925795A00003D9D?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/B2B9F9F194770CE64925793C00015B1D?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BA73B03E98BEC47A4925791F00070F21?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/5FE88C396839F17F4925790200006DE7?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DE221AEA2D979DB9492578DF0083B007?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/E6FD540D032D653D492578C30001018B?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FE17BE4B53D5CAEC492578A30002E1E7?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/6EE3F0045AFB9C1F4925788500026788?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/39BC17EA92A3F7EA4925786700839E51?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/516CDC3ABA91EAAC49257846008385F7?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/37112D85D9918A15492578300000E3B4?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/49FB2A0647B870F24925780E0000E325?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
#2010
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/A72AE214D43267CB492577ED000088E2?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DC5B2A455CB682CE492577CF0000AEB3?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/3FB665EAD1F8D023492577B200029454?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/030E04EDD63DCCA04925779200039103?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/FEC958DABF41E37449257774000016C4?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/C775204B2EEA8B734925775300834EF4?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/1502359B58D40DC649257736008378C3?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/DCCC1D74BA4C82244925771900001566?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/3690E8DC0C0914AB492576F800834E98?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/4E6FA6EF0D977274492576A200007B40?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])
result_data = pd.concat([result_data,get_data('https://www.keei.re.kr/web_keei/d_results.nsf/0/BB3F1BBE1260C9E4492576DB0000D7A2?opendocument&menucode=SS89&category=%B1%B9%C1%A6%BF%F8%C0%AF%B0%A1%B0%DD&rescategory=%EC%A0%84%EC%B2%B4&viewname=main_periodicals_01')])

result_data.sort_values('date')
print(result_data)

result_data.to_csv("dubai_oil.csv", mode='w')

# print(val)
# table의 수 x를 받아오기
# #objBody > table > tbody > tr:nth-child(x) > td:nth-child(4) 를 생성 후 date,dubai를 가져오기
# date를 월,일로 나눔
# 숫자만 추출해서 date에 timestamp로 생성
# npary에 합성