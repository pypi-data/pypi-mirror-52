from setuptools import setup, find_packages

long_description = "cadCAD is a differential games based simulation software package for research, validation, and \
    Computer Aided Design of economic systems. An economic system is treated as a state based model and defined through \
    a set of endogenous and exogenous state variables which are updated through mechanisms and environmental processes, \
    respectively. Behavioral models, which may be deterministic or stochastic, provide the evolution of the system \
    within the action space of the mechanisms. Mathematical formulations of these economic games treat agent utility as \
    derived from state rather than direct from action, creating a rich dynamic modeling framework. Simulations may be \
    run with a range of initial conditions and parameters for states, behaviors, mechanisms, and environmental \
    processes to understand and visualize network behavior under various conditions. Support for A/B testing policies, \
    monte carlo analysis and other common numerical methods is provided."

setup(name='cadCAD',
      version='0.3.0',
      description="cadCAD: a differential games based simulation software package for research, validation, and \
        Computer Aided Design of economic systems",
      long_description=long_description,
      url='https://github.com/BlockScience/cadCAD',
      author='Joshua E. Jodesty',
      author_email='joshua@block.science, joshua.jodesty@gmail.com',
      license='LICENSE.txt',
      packages=find_packages()
)