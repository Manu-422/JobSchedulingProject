# Job Scheduling Using Graph

A browser-based version of the Job Scheduling Using Graph project. It uses topological sorting to find a valid job execution order and displays the dependency graph.

## Files
- `app.py` — Streamlit web interface and graph visualization
- `algorithm.py` — Topological sorting algorithm
- `requirements.txt` — Python dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy online
1. Upload `app.py`, `algorithm.py`, and `requirements.txt` to your GitHub repository.
2. Sign in to Streamlit Community Cloud at https://share.streamlit.io/
3. Create a new app and select your GitHub repository.
4. Choose branch `main` and main file path `app.py`.
5. Deploy the app.

The original Tkinter `main.py` can stay in the repository, but the live browser app starts from `app.py`.
