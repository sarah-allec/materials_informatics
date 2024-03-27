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

I currently only have code up for the LV approach - see <a href="notebooks/latent_variable.ipynb">here</a>  for the corresponding Jupyter notebook and <a href="https://materials-informatics.streamlit.app/Transfer_Learning">here</a> for an overview on my portfolio page. All models were built with <a href="https://scikit-learn.org/stable/">`scikit-learn`</a>'s <a href="https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html">`RandomForestRegressor`</a>.

### Active learning
Active learning is a machine learning (ML) approach where the ML model predictions and uncertainties are used to decide what data point to evaluate next in a search space. In the context of materials and chemicals, active learning is often used to guide design and optimization. To decide what material or experiment to run next, we utilize acquisition functions to either *explore* or *exploit* the search space. For example, if we seek to optimize a particular chemical property, we would utilize an *exploitive* acquisition function that prioritizes compounds predicted to have property values close to our target value. On the other hand, if we want to *explore* the search space and diversify our training data, we would utilize an *explorative* acquisition function that prioritizes compounds for which the model is most uncertain. For more information on acquisition functions, see <a href="https://tune.tidymodels.org/articles/acquisition_functions.html" target='_blank'>here</a> and <a href="https://ekamperi.github.io/machine%20learning/2021/06/11/acquisition-functions.html" target='_blank'>here</a>. 

See <a href="notebooks/active_learning.ipynb">here</a>  for the corresponding Jupyter notebook and <a href="https://materials-informatics.streamlit.app/Active_Learning">here</a> for an overview on my portfolio page. All models were built with <a href="https://www.gpflow.org/">`GPflow`</a>'s <a href="https://gpflow.github.io/GPflow/develop/api/gpflow/models/index.html#gpflow.models.GPR">`GPR`</a>.

### Physics-informed learning
Physics-informed learning is an ML approach where physical knowledge is embedded into the learning processes, usually via a differential equation. Most often, this is achieved by incorporating an additional loss into the training of a neural network, where the loss is defined by the differential equation. Here, I have adapted <a href="https://medium.com/@theo.wolf/physics-informed-neural-networks-a-simple-tutorial-with-pytorch-f28a890b874a" target='_blank'>this example on cooling</a> to solve the time-dependency of Newton's law of cooling at various environmental temperatures $T_{env}$: $$\frac{dT(t)}{dt}=r(T_{env}-T(t)),$$ where $T(t)$ is the temperature at time $t$, $T_{env}$ is the environmental or surrounding temperature, and $r$ is the cooling rate. In this example, $r$ is a parameter that the network will learn from the data, and $T_{env}$ is provided by the user. 

To incorporate a physics-based loss into the network, we simply move all terms to one side of the equation: $$g=\frac{dT(t)}{dt}-r(T_{env}-T(t)) = 0$$. Now we can take the physics-based loss to simply be the difference between the predicted $g$ and $0$. The derivative term, $\frac{dT(t)}{dt}$ is easily obtained via the gradients computed during backpropagation.

See <a href="notebooks/pinn.ipynb">here</a>  for the corresponding Jupyter notebook and <a href="https://materials-informatics.streamlit.app/Physics_Informed_Learning">here</a> for an overview on my portfolio page. All models were built with <a href="https://pytorch.org/">`pytorch`</a>.

## Usage
### Running the notebooks
To install the necessary packages for running the <a href="notebooks">Jupyter notebooks</a>, use `pip` to install the packages listed in <a href="requirements_notebooks.txt">`requirements_notebooks.txt`</a> :

```sh
pip install -r requirements_notebooks.txt
```

Note that the notebooks often import data from <a href="data">data</a>, as well as modules from `python` scripts located in <a href="notebooks">notebooks</a>.

### Running the `streamlit` app
To install the necessary packages for running the <a href="streamlit">`streamlit` app</a>, use `pip` to install the packages listed in <a href="requirements_streamlit.txt">`requirements_streamlit.txt`</a> :

```sh
pip install -r requirements_streamlit.txt
```

Note that the app connects to a <a href="https://cloud.google.com/?hl=en">Google cloud</a> bucket to access data - the src code will need to be significantly modified in order to run the app locally, with or without <a href="https://cloud.google.com/?hl=en">Google cloud bucket</a>.
