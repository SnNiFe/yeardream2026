# uv pip install datasets
# from os import truncate

from datasets import load_dataset
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')

def token_func(ds):
    # print(ds)
    return tokenizer(ds['text'],truncation=True,max_length=128)

if __name__ == '__main__' : # 모듈명이 메인 이라면 실행 해라
    # 병렬처리를 할때는 이 내용 자체를 메인 스레드가 실행하도록 설정해줘야 한다.
    # 1. HF 에서 데이터셋 불러오기
    dataset = load_dataset('stanfordnlp/imdb', split='train')
    # print(dataset)

    # 2. 데이터 전처리
    encoded_ds = dataset.map(
        token_func, # 해야할 일
        batched=True, # 특정 단위로 작업을 몰아서 처리
        num_proc=4, # 사용할 스레드 수
        remove_columns=['text'], # 불필요한 컬럼 삭제
    )
    print('전처리 완료 : ',encoded_ds)

    # filter : 특정 조건의 샘플만 가져오도록
    # item => item.label == 1
    pos_ds = encoded_ds.filter(
        lambda item : item['label'] == 1,
        num_proc=4
    )
    print(f'filtering : {pos_ds}')

    # map 을 가지고 토큰수를 length 로 추가 한다.
    # item=> {'length' : len(item['input_ids']) }
    pos_ds = pos_ds.map(
        lambda item : {'length' : len(item['input_ids']) },
        num_proc=4
    )
    print(f'pos_ds : {pos_ds}')

    # length 를 기준으로 sort
    sorted_ds = pos_ds.sort("length",reverse=True)

    # select() : 특정개수 n 개만 가져온다.
    top10_df = sorted_ds.select([0,1,2,3,4,5,6,7,8,9]) # range(10)

    for i,item in enumerate(top10_df):
        print(f'[{i}] : 토큰길이 : {item["length"]} / label:{item["label"]}')