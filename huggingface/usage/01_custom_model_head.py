"""
    사전학습모델은 본체(Backbone)와 헤드(Head)로 구분된다.
    Backbone - 문장을 이해하고 임베딩하는 부분을 담당
    Head - 받은 임베딩 내용을 우리가 원하는 최종 결과로 바꿔주는 부분
"""
from torch import nn
from transformers import PreTrainedModel, AutoModel


# 1. 커스텀모델 만들기
class CustomClassifier(PreTrainedModel):

    def __init__(self, config:PreTrainedConfig): # 생성자(클래스가 객체화 될때 가장먼저 실행)
        super().__init__(config) # 부모 초기화를 위해 전달
        # (1) backbone 생성
        # config 가 뭐죠? config.json(모델설계도)
        self.backbone = AutoModel.from_config(config)

        # backbone 이 출력하는 벡터 차원 알아내기
        hidden_size = config.hidden_size # 768 차원

        # (2) 커스텀헤드 만들기 - 받아온 벡터들을 원하는 결과로 추출
        # 영화 리뷰를 가지고 긍정/부정 등을 구분하는 것을 할 예정
        self.custom_head = nn.Sequential(
            nn.Linear(hidden_size,hidden_size//2), # 768 -> 384
            nn.ReLU(), # 활성함수
            nn.Dropout(0.3), # 30% 무작위 끄기(전교1등 재우기)
            nn.Linear(hidden_size//2, 2) # 384 -> 2
        )

        self.post_init() # 가중치 초기화

    # model() 하면 forward() 가 실행 된다.
    def forward(self, input_ids, attention_mask=None):
        # 1. backbone 에 입력을 넣어서 결과를 받는다.
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        print(f'outputs shape : {outputs.last_hidden_state.shape}') # [문장수,토큰수,벡터수]
        # 2. 커스텀헤드에 보내서 최종 결과값을 받아낸다.
        # 3. 결과값 반환