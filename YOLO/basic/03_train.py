from torchvision import datasets


clss_name = [
    "T-shirt", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle-boot"
]
# 1. fashion-mnist 를 받는다.
def download_image(split='train'):
    is_train = True if split == 'train' else False
    datasets.FashionMNIST()