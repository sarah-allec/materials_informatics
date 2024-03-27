from menu import unauthenticated_menu
import streamlit as st

st.set_page_config(
    page_title="Physics-Informed Learning",
    page_icon="⚛️",
    layout="wide",
)

st.write("# Physics-Informed Learning ⚛️")
st.write("## Background")
st.write(r"Physics-informed learning is an ML approach where physical knowledge is embedded into the learning processes, usually via a differential equation. Most often, this is achieved by incorporating an additional loss into the training of a neural network, where the loss is defined by the differential equation. Here, I have adapted <a href='https://medium.com/@theo.wolf/physics-informed-neural-networks-a-simple-tutorial-with-pytorch-f28a890b874a' target='_blank'>this example on cooling</a> to solve the time-dependency of Newton's law of cooling at various environmental temperatures $T_{env}$:", unsafe_allow_html=True)

col1 = st.columns(3)
with col1[1]:
    st.write(r"$$\frac{dT(t)}{dt}=r(T_{env}-T(t)),$$")

st.write(r" where $T(t)$ is the temperature at time $t$, $T_{env}$ is the environmental or surrounding temperature, and $r$ is the cooling rate. In this example, $r$ is a parameter that the network will learn from the data, $T_{env}$ is provided by the user, and $T(t)$ is the output of the network.")
 
st.write(r"To incorporate a physics-based loss into the network, we simply move all terms to one side of the equation:")

col2 = st.columns(3)
with col2[1]:
    st.write(r"$$g=\frac{dT(t)}{dt}-r(T_{env}-T(t)) = 0$$.")

st.write(r"Now we can take the physics-based loss to simply be the difference between the predicted $g$ and $0$. The derivative term, $\frac{dT(t)}{dt}$ is easily obtained via the gradients computed during backpropagation.")
unauthenticated_menu()
