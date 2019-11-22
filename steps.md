# Setting up a Python development environment

1 - Configure python on [vscode](https://code.visualstudio.com/docs/python/python-tutorial).

2 - Install Python3 and pip3 (python 2.x was also included in the tutorial but it is not recommend the use since it is deprecated). Most Linux distributions include recent versions of Python.

  2.1 To install Python in a Linux environment, install the appropriate packages for your distribution. For Debian and Ubuntu, these packages are python3, and python3-dev, and python3-venv. Install these packages using the following commands:

  ```bash
  sudo apt update
  sudo apt install python3 python3-dev python3-venv
  ``` 
  You also need to install pip. While Debian and most other distributions include a python-pip package, we recommend that you install pip yourself to get the latest version:

  **PIP for python 2.x:**

  ```bash
  wget https://bootstrap.pypa.io/get-pip.py
  sudo python get-pip.py
  ```
  After the installations are complete, verify that you have pip installed:

  ```bash
  pip --version 
  ```

  The output shows the version from /usr/local/lib/python2.7/dist-packages. 

  **PIP For python 3**:

  ```bash
  curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
  python3 get-pip.py --user
  ```
  After the installations are complete, verify that you have pip installed:

  ```bash
  pip3 --version 
  ```

  The output shows the version from /usr/local/lib/python3/dist-packages. 
  
  You can learn about the latest version of pip in the pip Release Notes.

## Using venv to isolate dependencies

[venv](https://docs.python.org/3/library/venv.html) is a tool that creates isolated Python environments. These isolated environments can have separate versions of Python packages, which allows you to isolate one project's dependencies from the dependencies of other projects. We recommend that you always use a per-project virtual environment when developing locally with Python.

1 - Create the project workspace. Then navigate to the project root directory:

  ```bash
  mkdir project-name
  cd project-name
  ```

2 - Use the venv command to create a virtual copy of the entire Python installation. This tutorial creates a virtual copy in a folder named venv, but you can specify any name for the folder:

  ```bash
  python3 -m venv venv
  ```
  
  or
  
  ```bash
  virtualenv -p python3 venv
  ```

3 - Set your shell to use the venv paths for Python by activating the virtual environment:

  ```bash
  source venv/bin/activate
  ```

4 - Now you can install packages without affecting other projects or your global Python installation. For example lets install the mqtt-paho python lib:

  ```bash
  pip3 install paho-mqtt
  ```
  
  If you want to stop using the virtual environment and go back to your global Python, you can deactivate it:

  ```bash
  deactivate
  ```

5 - Generating the requirements.txt file
  
  We can use the command "pip3 freeze" to check the project dependecies. The requirements.txt file contains all the libraries necessary to run the application. To generate the requirements.txt file run the following command:

  ```bash
  pip3 freeze > requirements.txt
  ```

6 - Install project dependencies in a different machine

  To install the project dependencies on another machine it is necessary have the requirements.txt file and run the following command:

  ```bash
  pip3 install -r requirements.txt
  ```
You can read more about venv in the [venv docs](https://docs.python.org/3/library/venv.html).

## Links: 
- [Setting up a Python development environment](https://cloud.google.com/python/setup?hl=en-us#installing_and_using_virtualenv)
- [Guia definitivo para organizar meu ambiente Python](https://medium.com/welcome-to-the-django/guia-definitivo-para-organizar-meu-ambiente-python-a16e2479b753)
- [Ambientes Virtuais no Python >= 3.6 (venv)
](https://medium.com/capivarapython/ambientes-virtuais-no-python-3-6-venv-791b44e0fb0b)

####  Por que criar ambiente virtual?
Existem muitas vantagens em utilizar um ambiente de desenvolvimento isolado, algumas são:
- Não alterar a instalação padrão do python utilizada pela sua distribuição Linux, o que pode quebrar várias aplicações no seu SO.
- Não poluir o SO com bibliotecas desnecessárias para seu funcionamento.
- Cada projeto pode precisar de versões diferentes da mesma biblioteca, ou framework.
- Facilita replicar o ambiente de desenvolvimento em outra máquina, ou no servidor(através do arquivo requirements.txt.