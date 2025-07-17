# Real-Time Radar Demonstrator

Welcome to the Real-Time Radar Demonstrator project! This guide will walk you through setting up and running the project on your computer.

## 1. Prerequisites

Before you begin, you will need to install a couple of things:

*   **Git:** A tool for downloading the project from GitHub. You can download it from [git-scm.com](https://git-scm.com/downloads).
*   **Miniconda:** A tool to manage the project's Python environment and dependencies. You can download it from the [Miniconda documentation](https://docs.conda.io/en/latest/miniconda.html). Make sure to download the version for your operating system (Windows, macOS, or Linux).

## 2. Installation

Follow these steps to get the project set up on your computer:

### Step 1: Clone the Repository

First, you need to download the project files from GitHub. Open a terminal (on Windows, you can use the "Anaconda Prompt" that comes with Miniconda) and run the following command:

```bash
git clone https://github.com/aijay3/Live-Radar-Demonstrator-using-Raw-ADC-Data-in-Python.git
```

This will create a new folder named `Live-Radar-Demonstrator-using-Raw-ADC-Data-in-Python`.

### Step 2: Navigate to the Project Directory

Next, move into the newly created project folder by running this command:

```bash
cd Live-Radar-Demonstrator-using-Raw-ADC-Data-in-Python
```

### Step 3: Create the Conda Environment

Now, you will create a dedicated Python environment for this project. This ensures that all the required packages are installed without conflicting with other Python projects on your computer. Run the following command:

```bash
conda env create -f environment.yml
```

This command reads the `environment.yml` file and installs all the necessary packages. This might take a few minutes.

### Step 4: Activate the Environment

Once the environment is created, you need to activate it. Run this command:

```bash
conda activate real-time-radar
```

You will know it's active because you will see `(real-time-radar)` at the beginning of your terminal prompt.

## 3. Running the Application

Now that everything is set up, you can run the radar demonstrator. Make sure your radar hardware is connected to your computer, and then run the following command in your terminal:

```bash
python launcher.py
```

This will start the application, and you should see the radar data visualized on your screen.

Congratulations, you have successfully set up and run the Real-Time Radar Demonstrator!
