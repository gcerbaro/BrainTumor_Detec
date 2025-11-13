from cv2.typing import MatLike
import matplotlib.pyplot as plt

def log_warn(message: str):
  print(f"⚠️ \033[1;33mALERTA: \033[33m{message}\033[0m")

def log_error(message: str):
  print(f"❌ \033[1;31mERRO: \033[31m{message}\033[0m")

def log_success(message: str):
  print(f"✅ \033[32m{message}\033[0m")

def log_info(message: str):
  print(f"ℹ️ \033[34m{message}\033[0m")

def plot_img_samples(images: list[MatLike], title, cmap='gray', nrows=3, ncols=10, figsize=(15, 5)):
    '''
    Exibe uma amostra das imagens fornecidas.
    '''
    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = axes.ravel()

    fig.suptitle(title, fontsize=14, weight='bold')

    for i in range(nrows * ncols):
        axes[i].imshow(images[i], cmap=cmap)
        axes[i].axis('off')

    plt.tight_layout(pad=0.25)
    plt.show()