###### Clone the GitHub repository



git clone https://github.com/Sahelisau/EstateWise-AI.git

cd EstateWise-AI



###### Create the Python environment and install packages



py -3 -m venv .venv

.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip

.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt



###### **Source: .\\archive.zip in the repository root**

###### **Destination: .\\data\\raw\\india\_property\_listings\_81\_cities.zip**

###### **Use archive.zip, not archive (1).zip**



New-Item -ItemType Directory -Force .\\data\\raw | Out-Null

Copy-Item .\\archive.zip .\\data\\raw\\india\_property\_listings\_81\_cities.zip

Test-Path .\\data\\raw\\india\_property\_listings\_81\_cities.zip



###### Run each command separately. Wait for success before running the next one.



.\\.venv\\Scripts\\python.exe -m src.eda

.\\.venv\\Scripts\\python.exe -m src.train

.\\.venv\\Scripts\\python.exe -m streamlit run app.py



(" the 1st archive contains the most data to train the model archive(1) doesn't needed to be trained this archive is kept for future use")
