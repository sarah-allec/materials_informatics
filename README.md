<h1 align="center">✨ Materials Informatics ✨</h1>

<h4 align="center">A collection of toy examples of various materials informatics techniques.</h4>

<p align="center">
  <a href="#key-features">About</a> •
  <a href="#key-features">Background</a> •
  <a href="#how-to-use">Techniques</a> •
  <a href="#how-to-use">Usage</a>
</p>

<p align="center">
    <a href="https://materials-informatics.streamlit.app/">
    <img src="https://github.com/sarah-allec/materials_informatics/blob/main/img/streamlit.png?raw=true" alt="portfolio"/>
    </a>
</p>

## About
This repository contains both <a href="notebooks">Jupyter notebooks</a> for each materials informatics technique and the <a href="streamlit">source code</a> for my <a href="https://materials-informatics.streamlit.app/">personal portfolio</a>. 

## Background
*Materials informatics* is the application of data science and informatics techniques, including artificial intelligence and machine learning, to better understand and design materials. There are many aspects of materials science and engineering that make the application of these techniques unique and in many cases different than mainstream data science. Much of this uniqueness is due to the nature of materials-related datasets, which tend to be some combination of small, sparse, biased, clustered, and low quality.

## Techniques
### Transfer learning
Transfer learning is a machine learning (ML) approach where knowledge gained from a pre-trained model is used in the training of another model. Usually the pre-trained model is trained on a higher quality or more general dataset, and the target model is trained on a lower quality or more specific dataset. The goal is usually to *speed up and/or improve learning on the target task*. There are many transfer learning methods; two examples are: i) a latent variable (LV) approach, where the output of the pre-trained model is used as an input feature to the target model, and ii) a fine-tuning (FT) approach, where some optimized parameters of the pre-trained model are used to initialize the parameters of the target model. 

I currently only have code up for the LV approach - see <a href="notebooks/latent_variable.ipynb">here</a>  for the corresponding Jupyter notebook and <a href="https://materials-informatics.streamlit.app/Transfer_Learning">here</a> for an overview on my portfolio page.

### Active learning
Active learning is a machine learning (ML) approach where the ML model predictions and uncertainties are used to decide what data point to evaluate next in a search space. In the context of materials and chemicals, active learning is often used to guide design and optimization. To decide what material or experiment to run next, we utilize :violet[acquisition functions] to either *explore* or *exploit* the search space. For example, if we seek to optimize a particular chemical property, we would utilize an *exploitive* :violet[acquisition function] that prioritizes compounds predicted to have property values close to our target value. On the other hand, if we want to *explore* the search space and diversify our training data, we would utilize an *explorative* :violet[acquisition function] that prioritizes compounds for which the model is most uncertain. For more information on :violet[acquisition functions], see <a href='https://tune.tidymodels.org/articles/acquisition_functions.html' target='_blank'>`here`</a> and <a href='https://ekamperi.github.io/machine%20learning/2021/06/11/acquisition-functions.html' target='_blank'>`here`</a>. 

See <a href="notebooks/active_learning.ipynb">here</a>  for the corresponding Jupyter notebook and <a href="https://materials-informatics.streamlit.app/Active_Learning">here</a> for an overview on my portfolio page.

## Usage

```sh
pip install -r requirements.txt
```
