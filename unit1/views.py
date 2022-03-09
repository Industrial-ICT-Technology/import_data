from django.shortcuts import render
from .models import Review
from django.contrib import messages
import pandas as pd
from django.core.files.storage import FileSystemStorage


# Create your views here.

def cleansing(csv_file):
    '''전처리 시작'''
    raw_data = pd.read_csv("." + csv_file, encoding='utf-8')
    print(raw_data)
    data = raw_data.filter(['Original Comment'])

    '''중복 제거(1)'''
    data = data.drop_duplicates(['Original Comment'])

    '''불필요한 문자열 제거'''
    # html태그 제거
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'<[^>]*>', repl=r'', regex=True)

    # email 주소 제거
    data['Original Comment'] = data['Original Comment'].str.replace(
        pat=r'(\[a-zA-Z0-9\_.+-\]+@\[a-zA-Z0-9-\]+.\[a-zA-Z0-9-.\]+)',
        repl=r'', regex=True)
    # _제거
    data['Original Comment'] = data['Original Comment'].str.replace('_', '')

    # \r, \n 제거
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'[\r|\n]', repl=r'', regex=True)

    # url 제거
    data['Original Comment'] = data['Original Comment'].str.replace(
        pat=r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
        repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(
        pat=r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*',
        repl=r'', regex=True)

    # 자음, 모음 제거
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'([ㄱ-ㅎㅏ-ㅣ]+)', repl=r'', regex=True)

    # 특수 기호 제거
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'[^\w\s]', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace('1n', '')
    data['Original Comment'] = data['Original Comment'].str.replace('_', '')

    # 모두 영어인 행 공백으로 대체
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'^[a-zA-Z\s]+$', repl=r'', regex=True)

    # 모두 숫자인 행 공백으로 대체
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'^[0-9\s]+$', repl=r'', regex=True)

    # 좌우 공백 제거
    data['Original Comment'] = data['Original Comment'].str.strip()

    # 아이디 관련 단어 제거
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'ID\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'아이디\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'id\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'ID[a-zA-Z0-9]+', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'아이디[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'id[a-zA-Z0-9]+', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'ID\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'아이디\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'id\s', repl=r'', regex=True)

    # 주문번호 관련 단어 제거
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'주문번호\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'결제번호\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'구매번호\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'주문\s번호\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'결제\s번호\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'구매\s번호\s[a-zA-Z0-9]+', repl=r'',
                                                                    regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'주문번호\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'결제번호\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'구매번호\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'주문\s번호\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'결제\s번호\s', repl=r'', regex=True)
    data['Original Comment'] = data['Original Comment'].str.replace(pat=r'구매\s번호\s', repl=r'', regex=True)

    '''중복 제거(2)'''
    data['temp'] = data['Original Comment']
    data['temp'] = data['temp'].str.replace(' ', '')
    data = data.drop_duplicates(['temp'], ignore_index=True)
    data = data.drop(['temp'], axis=1)
    print(data)
    return data


def Import_csv(request):
    try:
        if request.method == 'POST' and request.FILES['myfile']:

            myfile = request.FILES['myfile']
            if not myfile.name.endswith('csv'):
                messages.info(request, '엑셀 형식으로 업로드 해주세요')
                return render(request, 'unit1/upload2.html')

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            csv_file = uploaded_file_url

            dbframe = cleansing(csv_file)

            for index, row in dbframe.iterrows():
                print(int(int(index) / int(dbframe.shape[0]) * 100), end='%\n')
                obj = Review.objects.create(review_content=row['Original Comment'])
                obj.save()
            return render(request, 'unit1/upload.html', {'uploaded_file_url': uploaded_file_url})

    except Exception as identifier:
        print(identifier)

    return render(request, 'unit1/upload.html', {})


