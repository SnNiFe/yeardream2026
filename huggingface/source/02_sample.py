from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Classify a new sentence
sentence = "공간을 많이 차지하지 않고 냉방 능력이 확실하며, 1등급 인버터 제품은 하루 종일 틀어도 전기요금 부담이 적습니다." 
# "I love this product! It's amazing and works perfectly."
result = pipe(sentence)

# Print the result
print(result)
