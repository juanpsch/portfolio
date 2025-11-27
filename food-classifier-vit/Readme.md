# Fine-Tuning Vision Transformer (ViT) for Food Classification

This project demonstrates the implementation of Deep Learning techniques for image recognition by fine-tuning a pre-trained Vision Transformer (ViT) model on the Food-101 dataset. The goal is to classify images into specific food categories with high accuracy, showcasing expertise in modern Computer Vision architectures and PyTorch.

## 🎯 Project Goal

To develop a high-performance image classification model capable of distinguishing between 101 distinct food categories, reaching a classification accuracy above 87% on the validation set through efficient fine-tuning strategies.

## ⚙️ Technical Stack & Technologies

The project leverages a modern Deep Learning stack optimized for performance and scalability.

| **Component** | **Technology** | **Role in Project** | 
| ----- | ----- | ----- | 
| **Framework** | PyTorch (with PyTorch Lightning) | Core Deep Learning library for model training and management. | 
| **Model Architecture** | Vision Transformer (ViT) | Utilizing the powerful attention-based architecture for superior feature extraction. | 
| **Pre-trained Models** | `timm` Library | Used for seamless access to pre-trained ViT models (e.g., `vit_base_patch16_224`). | 
| **Data Handling** | NumPy, Pillow | Efficient loading, transformation, and augmentation of image data. | 
| **Environment** | Jupyter Notebook | Documentation and execution of the end-to-end ML workflow. | 

## 🚀 Key Achievements & Results

* **High Accuracy:** Achieved a validation accuracy of 87.57%, confirming the efficacy of the ViT fine-tuning approach.

* **Transfer Learning:** Successfully implemented transfer learning from a model pre-trained on ImageNet, significantly reducing training time and computational cost compared to training from scratch.

* **Performance Optimization:** Implemented custom data loaders and leveraged GPU acceleration for efficient training cycles.

## 🛠️ Implementation Details

The core workflow is documented in `TPFinal.ipynb` and includes the following steps:

1. **Data Preparation:** Loading the Food-101 dataset, splitting it into training, validation, and test sets.

2. **Data Augmentation:** Applying essential transformations (resizing, normalization, random cropping) to improve model generalization.

3. **Model Loading:** Instantiating the pre-trained ViT model and preparing the final classification layer for the 101 classes.

4. **Training & Fine-Tuning:** Training the model using the Adam optimizer with a learning rate scheduler and an early stopping mechanism.

5. **Evaluation:** Calculating key performance metrics (accuracy, loss, confusion matrix) on the held-out test set.

## 📂 Project Structure

* **TPFinal File:** Contains the analysis, training code, and some tests.

* **TPFinal2 File:** Contains the metrics code, loading the pre-trained model.

* **trained-model Folder:** Contains the final model with fine-tuning.

* **Final Model Link:** The final fine-tuned model is also available at the following [link](https://drive.google.com/drive/folders/12-z3U-goiskTPY2wMMqcPB07o7GaNiG-).
