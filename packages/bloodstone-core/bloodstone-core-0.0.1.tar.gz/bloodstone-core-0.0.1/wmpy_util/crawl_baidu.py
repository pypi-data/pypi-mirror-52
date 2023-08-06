# -*- coding:utf-8 -*-

"""
@author: Yan Liu
@file: crawl.py
@time: 2018/3/27 11:43
@desc: 爬取百度图片
"""

import requests
import os

def crawl_img(keyword_list, page_num, img_dir):
    """
    爬虫入口函数
    :param keyword_list: 需要搜索的管检测列表
    :param page_num: 搜索几页
    :param img_dir: 保存图片的路径
    :return:
    """
    for name in keyword_list:
        dataList = getPages(name, page_num)
        download_img(name, dataList, img_dir)


def getPages(keyword, pages):
    params = []
    for i in range(30, 30 * pages + 30, 30):
        params.append({
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'ct': 201326592,
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': 2,
            'lm': -1,
            'ie': 'utf-8',
            'oe': 'utf-8',
            'adpicid': '',
            'st': '',
            'z': '',
            'ic': '',
            'word': keyword,
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '',
            'istype': '',
            'qc': '',
            'nc': 1,
            'fr': '',
            'pn': i,
            'rn': 30,
            'gsm': '1e',
            '1488942260214': ''
        })

    url = 'https://image.baidu.com/search/acjson'
    urls = []
    fail_url_count = 0
    for i in params:
        response = requests.get(url, params=i)
        try:
            jsonObj = response.json()
            urls.append(jsonObj.get('data'))
        except Exception as e:
            print("json数据格式错误 " + str(e))
            fail_url_count += 1
    print("提取图片url成功：%d 失败：%d" % (len(urls), fail_url_count))
    return urls


x = 0


def download_img(keyword, dataList, localPath):
    global x
    if not os.path.exists(localPath):
        os.mkdir(localPath)

    for list in dataList:
        for i in list:
            if i.get('hoverURL') != None:
                try:
                    print('正在下载：%s' % i.get('hoverURL'))
                    ir = requests.get(i.get('hoverURL'))
                    image_path = os.path.join(localPath, '%s_%d.jpg' % (keyword, x))
                    open(image_path, 'wb').write(ir.content)
                    x += 1
                except Exception as e:
                    print("图片下载失败" + i.get('hoverURL') + str(e))

    print('%s图片下载完成' % keyword)





if __name__ == '__main__':

    # terror_list = ['isis', '暴恐', '东突', '伊斯兰国', '本拉登', '恐怖主义', '藏独', '疆独', '邪教']
    # terror_list = ['恐怖袭击','极端穆斯林','打砸抢烧']
    # terror_list = ['枪','炮','恐袭']

    # politics_list = [ '团旗','团徽','少先队队旗','少先队队徽','军旗','八一','国民党党徽','国民党党旗','法西斯','人民币','彭丽媛']
    # '邓小平', '周恩来', '薄熙来', '孙中山', '金正恩', '朴槿惠','普京','朱镕基','温家宝','奥巴马','特朗普','政治人物','中国国旗','国徽','党旗','党徽']
    # politics_list = ['日本国旗','美国国旗','韩国国旗','朝鲜国旗','纳粹标志','法西斯标志']

    # normal_list = ['风景', '证件照', '老照片', '人物照', '人们', '农民', '工人', '白领', '动物', '花', '树', '动漫', '幸福生活', '玩具', '小宝贝', '新疆', '西藏', '北京', '上海']
    # normal_list = [ '抬头','低头','亚洲人','中国男人']
    # normal_list = [ '徽章', '球队logo','标志','欧洲国旗','非洲国旗','南美洲国旗','大洋洲国旗']
    # normal_list = ['背景','广告背景','背景素材','底纹','简单背景','年货','春联','红黄','西红柿鸡蛋','红金','红底','喜事']
    # normal_list = ['黑纱','黑布','头巾','黑人']
    # normal_list = ['宝贝','小宝贝','皮鞋','黑皮鞋','高跟鞋']
    # normal_list = ['吃冰棍','吃热狗','吃香蕉','自拍','拥抱','爱情','恋爱','喜欢']
    # normal_list = ['炼钢','篝火','老城','破败','旧城','徽章','标识','标志','旗','红布','文字','报纸','书','排版','漫画']
    # normal_list = ['长腿','女装','可爱','大头贴','汽车','动漫人物','人脸','正装','黑裤子','大海','沙滩','灯笼','吃鸡','绝地求生','荒野行动','刺激战场']

    # normal_list = ['人物','头像','正脸','证件照','人脸','云海','炊烟']
    # sexy_list = ['性感','性感美女','性感帅哥','美女身材','肌肉帅哥','比基尼','泳装','sexy','翘臀','胸','露脐装','sexy']
    # sexy_list = ['内衣','内裤男','内裤女','大胸妹','事业线','维密']
    # sexy_list = ['沙滩美女','沙滩帅哥','泳池美女','泳池帅哥','胸肌','腹肌','马甲线']

    # advertisement_list = ['广告', '二维码广告', '广告联系方式', '广告推销']

    # logo_list = ['logo','商标','品牌','球队队徽']
    # weapon_list = ['军队','98k','反恐精英','csgo','m15','ak47']
    # emoji_list = ['表情包']
    # human_list = ['握手','牵手','十指相扣','大腿','腿','胳膊','小臂','大臂','肚皮','肚子','膝盖','脚']
    human_list = ['脖子','颈']

    # get_img(normal_list, 10, './train_data_terror/normal/')
    # get_img(advertisement_list, 100, 'D:\\DevWorks\\antispam\\codes\\antispam\\trainer.asimg.wanmei.com\\dataset\\advertisement\\')
    # get_img(politics_list, 15, 'D:/Dataset/asimg/train/political_symbols/')
    # get_img(terror_list, 20, 'D:/Dataset/asimg/train/v2/terror/terror_20181227/')
    crawl_img(human_list, 30, 'D:/Dataset/asimg/download/human/')

    '''
    # 并行抓取
    threads = []

    t1 = threading.Thread(target=get_img, args=(terror_list, 500, './terror/'))
    threads.append(t1)

    t2 = threading.Thread(target=get_img, args=(politics_list, 500, './politics/'))
    threads.append(t2)

    t3 = threading.Thread(target=get_img, args=(normal_list, 100, './normal/'))
    threads.append(t3)

    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()
    '''

    print("一共下载%d张图片" % x)