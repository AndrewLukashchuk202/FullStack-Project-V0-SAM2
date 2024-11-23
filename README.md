# FullStack-Project-V0-SAM2

Object-Backend is a project designed to utilize SAM2 for object detection and other functionalities. It provides support for both GPU (CUDA-enabled) and CPU processing. Follow the instructions below to set up and run the project.

---


## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installing CUDA (Optional for GPU)](#installing-cuda)
3. [Installing SAM2](#installing-sam2)
4. [Setting Up Dependencies](#setting-up-dependencies)
5. [Checkpoints Directory (Model Files)](#checkpoints-directory-model-files)
6. [Running the Servers](#running-the-servers)
    - [Django Server](#django-server)
    - [Next.js Frontend](#nextjs-frontend)
7. [Folder Structure](#folder-structure)
8. [License](#license)

---

## Prerequisites
Ensure you have the following installed:
- Python 3.10 or later
- Node.js (for the Next.js frontend)
- pip (Python package installer)
- Git

For GPU support:
- A CUDA-compatible NVIDIA GPU
- CUDA Toolkit (see instructions below)

---

## Installing CUDA
CUDA is required if you plan to use GPU acceleration. If you want to run the project on CPU, you can skip this step.

1. **Check Your GPU Compatibility**  
   Verify your GPU supports CUDA by visiting the [CUDA-Enabled GPU List](https://developer.nvidia.com/cuda-gpus).

2. **Download and Install CUDA**  
   - Visit the [CUDA Toolkit Downloads](https://developer.nvidia.com/cuda-downloads).
   - Select your operating system and download the **Local Installer** for your version.

3. **Add CUDA to PATH**  
   Ensure that CUDA binaries are in your PATH. Add the following (adjust paths as necessary):
   - **Windows**:
     ```
     C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\<version>\bin
     ```
   - **Linux/macOS** (add to `.bashrc` or `.zshrc`):
     ```bash
     export PATH=/usr/local/cuda/bin:$PATH
     export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
     ```

4. **Verify Installation**  
   Run the following command to verify your installation:
   ```bash
   nvcc --version

## Installing SAM2
SAM2 is required for running object detection models.

Follow the installation instructions in the SAM2 GitHub repository. Make sure the necessary SAM2 models are downloaded.
[SAM2 GitHub](https://github.com/facebookresearch/sam2)

## Setting Up Dependencies
1. **Clone this repository:**
```bash
git clone https://github.com/AndrewLukashchuk202/FullStack-Project-V0-SAM2.git
```
2. **Set up a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv/Scripts/activate
```
3. **Install the dependencies:**
```bash
pip install -r requirements.txt
```
## Checkpoints Directory (Model Files)
The **checkpoints** folder (SAM2 model files) must be placed in the **Django root directory of the project(object-backend)**. The directory structure should look like this:
```bash
object-backend/
├── checkpoints/       # SAM2 model files here
├── media/
├── configs/
├── imagifier/
├── manage.py
├── requirements.txt
...
```

## Running the Servers ##
**Django Server**
1. Navigate to the Django project directory (**object-backend**)
2. Apply migrations:
```bash
python manage.py migrate
```
3. Start the Django development server:
```bash
python manage.py runserver
```
4. The backend will be available at **http://127.0.0.1:8000**

**Next.js Frontend**
1. Navigate to the Next.js frontend folder **object-frontend**:
```bash
cd object-frontend
```
2. Install Node.js dependencies:
```bash
npm install
```
**Set up shadcn:**
1. Install the shadcn CLI globally:
```bash
npm install -g shadcn
```
2. Initialize shadcn in the project:
```bash
npx shadcn init
```
3. Add components:
```bash
npx shadcn add button card input table
```

4. Start the Next.js development server:
```bash
npm run dev
```
5. The frontend will be available at **http://localhost:3000**

## Folder Structure
The project should be organized as follows:
```bash
object-backend/
├── checkpoints/       # Place SAM2 models here
├── configs/
├── imagifier/
├── media/
├── requirements.txt
├── setup.py
├── manage.py          # Django entry point
├── frontend/          # Next.js frontend folder
│   ├── package.json
│   ├── pages/
│   ├── public/
│   └── ...
|── sam2/              # SAM2 dependencies
|── venv               # Virtual environment with installed dependencies
```

## License
This project is licensed under the MIT License.
```bash
MIT License

Copyright (c) 2024 North Metropolitan TAFE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
