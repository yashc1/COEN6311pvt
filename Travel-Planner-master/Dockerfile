# Use a base Python image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Set the environment variable
ENV FLASK_APP=app.py

# Start MySQL service
#CMD ["service mysql start"]
#CMD ["mysql -u root -p < team1-schema.sql"]
#CMD ["mysql -u root -p < team1-data.sql"]
# Run the Flask application
#ENTRYPOINT [ "python" ]

#CMD ["run.py" ]
