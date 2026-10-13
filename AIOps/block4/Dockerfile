# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files into container
COPY app.py .
COPY iris_model.pkl .

# Install dependencies
RUN pip install streamlit scikit-learn numpy

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]